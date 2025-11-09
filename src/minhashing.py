# 生成每个文档的 MinHash 签名向量
import random
from typing import List, Set, Optional

class MinHashing:
   
    def __init__(self, num_perm: int = 128, max_shingle_id: Optional[int] = None, seed: int = 42):
        assert max_shingle_id is not None and max_shingle_id >= 0
        self.num_perm = num_perm
        self.P = 4294967311
        random.seed(seed)
        self.hash_params = [
            (random.randrange(1, self.P - 1), random.randrange(0, self.P - 1))
            for _ in range(num_perm)
        ]

    def compute_signature(self, shingle_set: Set[int]) -> List[int]:
        if not shingle_set:
            return [0] * self.num_perm

        sig: List[int] = []
        for a, b in self.hash_params:
            m = min(((a * x + b) % self.P) for x in shingle_set)
            sig.append(m)
        return sig
