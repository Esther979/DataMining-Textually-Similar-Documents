# Locality-Sensitive Hashing: banding + bucketing 生成候选文档对

from collections import defaultdict
from typing import List, Tuple, Set

class LSH:
    def __init__(self, num_perm: int = 128, num_bands: int = 32):
        assert num_perm % num_bands == 0, "num_perm must be divisible by num_bands"
        self.num_perm = num_perm
        self.num_bands = num_bands
        self.rows_per_band = num_perm // num_bands

    def candidate_pairs(self, signatures: List[List[int]]) -> Set[Tuple[int, int]]:
        
        if not signatures:
            return set()

        # 基本一致性检查
        sig_len = len(signatures[0])
        assert all(len(s) == sig_len for s in signatures), "All signatures must have equal length"
        assert sig_len == self.num_perm, "Signature length must equal num_perm given to LSH"

        buckets = [defaultdict(list) for _ in range(self.num_bands)]

        
        for doc_id, sig in enumerate(signatures):
            for b in range(self.num_bands):
                start = b * self.rows_per_band
                end = start + self.rows_per_band
                key = tuple(sig[start:end])      
                buckets[b][key].append(doc_id)

       
        candidates: Set[Tuple[int, int]] = set()
        for b in range(self.num_bands):
            for _, ids in buckets[b].items():
                if len(ids) < 2:
                    continue
                ids.sort()
                for i in range(len(ids)):
                    for j in range(i + 1, len(ids)):
                        candidates.add((ids[i], ids[j]))
        return candidates
