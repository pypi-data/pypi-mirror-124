import hmac
import base64
import hashlib
import logging


logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def hash_function(secret_key, message):
    digest = hmac.new(secret_key, message, hashlib.sha1).digest()
    base64_bytes = base64.b64encode(digest)
    base64_string = base64_bytes.decode("ascii")
    return base64_string
