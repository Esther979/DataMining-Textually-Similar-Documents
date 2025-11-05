import hashlib
import re

class Shingling:
    """
    Construct k-shingles (character-based) for a given document.
    Each shingle is hashed into an integer for compact representation.
    """

    """Pre-process"""
    def __init__(self, k=10, lowercase=True, alnum_only=True):
        self.k = k
        self.lowercase = lowercase
        self.alnum_only = alnum_only

    def _normalize(self, text: str) -> str:
        """Normalize text by lowercasing and optionally removing non-alphanumeric."""
        if self.lowercase:
            text = text.lower()
        if self.alnum_only:
            text = re.sub(r'[^a-z0-9]+', ' ', text)
        return text.strip()

    def _hash_shingle(self, shingle: str) -> int:
        """Convert a shingle to a deterministic integer hash value."""
        return int(hashlib.md5(shingle.encode('utf-8')).hexdigest(), 16)

    def create_shingles(self, text: str):
        """
        Create a set of unique hashed k-shingles from the given text.
        Returns: set[int]
        """
        text = self._normalize(text)
        if len(text) < self.k:
            return {self._hash_shingle(text)} if text else set()

        """Sliding window of k-length"""
        shingles = set()
        for i in range(len(text) - self.k + 1): 
            shingle = text[i:i+self.k]
            shingles.add(self._hash_shingle(shingle))
        return shingles
