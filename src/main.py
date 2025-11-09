import os
import time
from shingling import Shingling
from compare_sets import CompareSets
from minhashing import MinHashing
from compare_signatures import CompareSignatures
from lsh import LSH

def load_documents(data_dir):
    docs = {}
    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith(".txt"):
            with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
                docs[filename] = f.read()
    return docs


def main():
    data_dir = os.path.join(os.path.dirname(__file__), "../data")
    k = 10  # shingle length
    sim_threshold = 0.5
    n_perm = 128
    n_bands = 32
    print(f"🔍 Loading dataset from {data_dir}")
    docs = load_documents(data_dir)
    print(f"✅ Loaded {len(docs)} documents\n")

    shingler = Shingling(k=k)
    compare = CompareSets()

    # Step 1: Compute shingles
    shingle_sets = {}
    for name, text in docs.items():
        shingle_sets[name] = shingler.create_shingles(text) # Pass to Minhasing
        print(f"📄 {name}: {len(shingle_sets[name])} unique shingles")

    # Step 2: Compute pairwise Jaccard similarities
    print("\n=== Pairwise Jaccard Similarities ===")
    doc_names = list(docs.keys())
    for i in range(len(doc_names)):
        for j in range(i + 1, len(doc_names)):
            d1, d2 = doc_names[i], doc_names[j]
            sim = compare.jaccard_similarity(shingle_sets[d1], shingle_sets[d2])
            tag = "✅ Similar" if sim >= sim_threshold else "❌ Different"
            print(f"{d1} vs {d2}: Jaccard={sim:.4f}  →  {tag}")
    # 计算全局最大的 shingle ID
    non_empty_sets = [s for s in shingle_sets.values() if len(s) > 0]
    if non_empty_sets:
        max_id = max(x for s in non_empty_sets for x in s)
    else:
        max_id = 1  

    mh = MinHashing(num_perm=n_perm, max_shingle_id=max_id, seed=42)
    signatures = [mh.compute_signature(shingle_sets[name]) for name in doc_names]

    print("\n=== Pairwise MinHash Signature Similarities ===")
    for i in range(len(doc_names)):
        for j in range(i + 1, len(doc_names)):
            d1, d2 = doc_names[i], doc_names[j]
            sim_hat = CompareSignatures.similarity(signatures[i], signatures[j])
            print(f"{d1} vs {d2}: MinHash≈{sim_hat:.4f}")

    # LSH 
    print("\n=== LSH Candidate Pairs (optional) ===")
    lsh = LSH(num_perm=n_perm, num_bands=n_bands)
    cand_pairs = lsh.candidate_pairs(signatures)
    if not cand_pairs:
        print("No candidates found by LSH.")
    else:
        for (i, j) in sorted(cand_pairs):
            d1, d2 = doc_names[i], doc_names[j]
            # 复核：先看MinHash估计，再看Jaccard真值
            sim_hat = CompareSignatures.similarity(signatures[i], signatures[j])
            sim_true = compare.jaccard_similarity(shingle_sets[d1], shingle_sets[d2])
            tag = "✅ Similar" if sim_true >= sim_threshold else "❌ Different"
            print(f"{d1} vs {d2}: MinHash≈{sim_hat:.4f}, Jaccard={sim_true:.4f} → {tag}")

#性能比较
    import itertools

    print("\n=== Performance Summary ===")
    t1 = time.time()
    all_pairs = list(itertools.combinations(doc_names, 2))
    for d1, d2 in all_pairs:
        _ = CompareSignatures.similarity(
            signatures[doc_names.index(d1)],
            signatures[doc_names.index(d2)]
        )
    t2 = time.time()
    all_time = t2 - t1
    all_count = len(all_pairs)

    
    t3 = time.time()
    for (i, j) in cand_pairs:
        _ = CompareSignatures.similarity(signatures[i], signatures[j])
    t4 = time.time()
    lsh_time = t4 - t3
    lsh_count = len(cand_pairs)

    # 输出结果
    if lsh_count == 0:
        print("⚠️ No candidates found by LSH.")
    else:
        print(f"All-pairs comparisons: {all_count} pairs, time = {all_time:.4f}s")
        print(f"LSH comparisons: {lsh_count} pairs, time = {lsh_time:.4f}s")
        if lsh_time > 0:
            print(f"Speedup ≈ {all_time / lsh_time:.1f}×")


    # Optional timing
    t0 = time.time()
    _ = [compare.jaccard_similarity(a, b) for a in shingle_sets.values() for b in shingle_sets.values()]
    print(f"\n⏱️ Total processing time: {time.time() - t0:.3f}s")

 

if __name__ == "__main__":
    main()
