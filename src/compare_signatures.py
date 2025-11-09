# 比较两个 MinHash 签名向量的相似度（等位比）

from typing import Sequence

class CompareSignatures:
    @staticmethod
    def similarity(sig1: Sequence[int], sig2: Sequence[int]) -> float:
        assert len(sig1) == len(sig2), "Signatures must have the same length"
        n = len(sig1)
        if n == 0:
            return 1.0
        agree = sum(1 for i in range(n) if sig1[i] == sig2[i])
        return agree / n
