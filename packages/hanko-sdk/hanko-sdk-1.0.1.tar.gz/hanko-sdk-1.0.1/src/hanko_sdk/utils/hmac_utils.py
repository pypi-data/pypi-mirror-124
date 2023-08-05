import time
import uuid
from typing import Optional
import hashlib
import hmac
import json

from . import base64_utils


def hash_body(request_body: str) -> str:
    hashed_body = hashlib.sha256(request_body.encode())
    return hashed_body.hexdigest()


def hash_message_hmac(key: str, message: str) -> str:
    hashed_message = hmac.new(key=key.encode(), msg=message.encode(), digestmod=hashlib.sha256).hexdigest()
    return hashed_message


def calculate_hmac(api_key_id: str, api_secret: str, request_method: str, request_path: str, request_body: Optional[str]) -> str:
    """ Calculates HMAC, given the parameters of a Hanko request.

        :param api_key_id: The Hanko API key ID.
        :param api_secret: The Hanko API secret.
        :param request_method: The request method.
        :param request_path: The request path that follows the base URL.
        :param request_body: The request body.
        :return: The calculated HMAC value, encoded as a hex string. """

    seconds_since_epoch = int(time.time())
    nonce = str(uuid.uuid4())

    message = "{}:{}:{}:{}:{}".format(api_key_id, seconds_since_epoch, request_method, request_path, nonce)

    if request_body is not None and len(request_body) > 0:
        hashed_body = hash_body(request_body)
        message = "{}:{}".format(message, hashed_body)

    signature_hex = hash_message_hmac(api_secret, message)

    hmac_data = {
        "apiKeyId": api_key_id,
        "time": str(seconds_since_epoch),
        "nonce": nonce,
        "signature": signature_hex
    }

    hmac_json = json.dumps(hmac_data)
    return base64_utils.b64encode_without_padding(hmac_json)
