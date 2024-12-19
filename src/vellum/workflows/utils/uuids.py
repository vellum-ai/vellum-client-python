import hashlib
from uuid import UUID


def uuid4_from_hash(input_str: str) -> UUID:
    # Create a SHA-256 hash of the input string
    hash_bytes = hashlib.sha256(input_str.encode()).digest()

    # Modify the hash to follow UUID4 structure
    # UUID4 has 8-4-4-4-12 hexadecimal characters
    # Version bits (4 bits) should be set to 4 (for UUID4),
    # and variant bits (2 bits) should start with 0b10

    # Convert first 16 bytes into UUID
    hash_list = list(hash_bytes[:16])

    # Set the version to 4 (UUID4)
    hash_list[6] = (hash_list[6] & 0x0F) | 0x40

    # Set the variant to 0b10xxxxxx
    hash_list[8] = (hash_list[8] & 0x3F) | 0x80

    # Create a UUID from the modified bytes
    return UUID(bytes=bytes(hash_list))
