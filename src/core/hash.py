import hashlib

def hash_sum_of_file(filename: str):
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def compare_hashs(filename_a: str, filename_b: str):
    return hash_sum_of_file(filename_a) == hash_sum_of_file(filename_b)