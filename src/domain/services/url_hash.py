import hashlib
def create_url_hash(url: str) -> str:
    """
    Create a hash for the given URL using SHA-256.

    Returns:
        str: The SHA-256 hash of the URL.
    """
    return hashlib.sha256(url.encode()).hexdigest()