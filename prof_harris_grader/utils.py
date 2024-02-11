import hashlib

def make_primary_key(session_id: str, homework: str, problem: str) -> str:
    concatenated_string = '|'.join([session_id, homework, problem])
    encoded_string = concatenated_string.encode()

    # use md5 for less storage and no need for extreme cryptographic security
    hash_object = hashlib.md5(encoded_string)

    hex_dig = hash_object.hexdigest()
    return hex_dig