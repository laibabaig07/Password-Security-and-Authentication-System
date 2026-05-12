import hashlib


def generate_hashes(password):

    encoded = password.encode()

    return {
        "MD5": hashlib.md5(encoded).hexdigest(),

        "SHA-1": hashlib.sha1(encoded).hexdigest(),

        "SHA-256": hashlib.sha256(encoded).hexdigest(),

        "SHA-512": hashlib.sha512(encoded).hexdigest(),

        "BLAKE2b": hashlib.blake2b(encoded).hexdigest()
    }