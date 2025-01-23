import uuid
import hmac
import hashlib
import base64


def generate_hmac_signature(secret_key, message):
    hmac_obj = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256)
    hmac_signature = hmac_obj.digest()
    signature = base64.b64encode(hmac_signature).decode()

    return signature


def generate_transaction_id():
    return uuid.uuid4().hex.upper()
