import importlib.metadata
import io
import os
import re
import csv
import json
import time
import boto3
import logging
import threading
import gzip
import shutil
import tempfile

from anypubsub import create_pubsub


__version__ = importlib.metadata.version("s3-upload-split")
logger = logging.getLogger(__name__)
RE_TZ = re.compile(r'\+00:00$')


def dict_to_str(record):
    memory_file = io.StringIO()
    csv_writer = csv.writer(memory_file)
    csv_writer.writerow(list(record.values()))
    memory_file.seek(0)
    return next(memory_file)


def upload_stream(bucket, stream, key, gzipped=False):
    opts = {}
    fp = None
    resource_bucket = boto3.resource('s3').Bucket(bucket)
    if gzipped:
        if not key.endswith(".gz"):
            print("When using gzip compression key needs to end with .gz")
            exit(1)

        fp = tempfile.TemporaryFile()
        logger.debug("Compress stream received into tempfile")

        with gzip.GzipFile(fileobj=fp, mode='wb') as gz:
            shutil.copyfileobj(stream, gz)
        logger.debug("Done with compressing")
        fp.seek(0)
        opts = dict(ContentEncoding='gzip')

    resource_bucket.upload_fileobj(fp or stream, key, opts)

    key_to_delete = key[:-3] if gzipped else f"{key}.gz"
    resource_bucket.delete_objects(
            Delete={"Objects": [{'Key': key_to_delete}]}
    )


class SplitUploadS3:
    def __init__(self, bucket, key, regex, iterator, gzipped=False, buffer_size=io.DEFAULT_BUFFER_SIZE):
        self.key = key
        self.regex = regex
        self.iterator = iterator
        self._patterns = dict()
        self.bucket = bucket
        self.gzipped = gzipped
        self.buffer_size = buffer_size

    def handle_content(self):
        pubsub, channel = create_pubsub('memory'), "chan1"
        for idx, record in enumerate(self.iterator):
            pattern = self.regex.search(dict_to_str(record)).group(1)
            if pattern not in self._patterns:
                logger.debug("Adding thread for pattern %s", pattern)
                json_output = os.path.join(self.key, f"data-{pattern}.json")
                if self.gzipped:
                    json_output += ".gz"
                uploading_thread = thread(
                    self.bucket, pubsub, channel, pattern,
                    json_output, self.gzipped, self.buffer_size
                )
                self._patterns[pattern] = 1
                uploading_thread.start()
            pubsub.publish(channel, (pattern, record))
        logger.info("Main thread has published all data, %d records, coming from the database", idx+1)
        while any([subscriber.messages.qsize() for subscriber in pubsub.subscribers[channel]]):
            logger.debug(f"Waiting as there are still messages that have not been read by subscribers...")
            time.sleep(10)
        logger.debug("Main thread finished, sending message to all subscribers that there is no more data")
        pubsub.publish(channel, (None, None))


def next_valid_data(iterable, matching_pattern, done=False):
    if done:
        raise StopIteration
    while True:
        pattern, data = next(iterable)
        if (data, pattern) == (None,)*2:
            raise StopIteration
        if pattern == matching_pattern:
            return data


def handle_value(value):
    return value if value is None or type(value) in [str, int, dict] else RE_TZ.sub('', str(value))


def stringify(data):
    return {key:handle_value(value) for key, value in data.items()}


def jsonize(dictionary):
    return json.dumps(stringify(dictionary))


def iterable_to_stream(subscriber, pattern=None, buffer_size=io.DEFAULT_BUFFER_SIZE):
    class IterStream(io.RawIOBase):
        def __init__(self, subscriber=None, pattern=None):
            self.leftover = None
            self.subscriber = subscriber
            self.pattern = pattern
            self.done = False
            self.next = lambda: next_valid_data(
                    self.subscriber, self.pattern, self.done
                ) if self.pattern else next(self.subscriber)

        def readable(self):
            return True

        def next_chunk(self):
            return jsonize(dict(self.next().items())) + "\n"

        def readinto(self, b):
            try:
                l = len(b)  # We're supposed to return at most this much
                chunk = self.leftover or self.next_chunk().encode()
                output, self.leftover = chunk[:l], chunk[l:]
                b[:len(output)] = output
                return len(output)
            except StopIteration:
                self.done = True
                return 0  # indicate EOF

    return io.BufferedReader(IterStream(subscriber, pattern), buffer_size)


class thread(threading.Thread):
    def __init__(self, bucket, pubsub, channel, pattern, filename, gzipped=False, buffer_size=io.DEFAULT_BUFFER_SIZE):
        threading.Thread.__init__(self)
        self.subscriber = pubsub.subscribe(channel)
        self.pattern = pattern
        self.bucket = bucket
        self.filename = filename
        self.gzipped = gzipped
        self.buffer_size = buffer_size

    def run(self):
        upload_stream(self.bucket,
                      iterable_to_stream(self.subscriber, self.pattern, self.buffer_size),
                      self.filename, gzipped=self.gzipped)
