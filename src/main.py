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


# Test Performance
    print("\n=== Scalability Evaluation ===")
    sizes = list(range(5, len(docs) + 1))  # test with 5 up to N documents

    results = []  # (num_docs, jaccard_time, minhash_time)

    for size in sizes:
        subset = doc_names[:size]
        subset_shingles = {d: shingle_sets[d] for d in subset}

        # Measure Jaccard all-pairs time
        t_start = time.time()
        for i in range(len(subset)):
            for j in range(i + 1, len(subset)):
                CompareSets.jaccard_similarity(
                    subset_shingles[subset[i]],
                    subset_shingles[subset[j]]
                )
        t_jacc = time.time() - t_start

        # Measure MinHash + LSH time
        t_start = time.time()
        subset_sigs = [signatures[doc_names.index(d)] for d in subset]
        _ = lsh.candidate_pairs(subset_sigs)   # only generates candidate pairs
        t_minhash = time.time() - t_start

        results.append((size, t_jacc, t_minhash))

    # Print result table
    print("\nDocuments | Jaccard Time (s) | MinHash+LSH Time (s)")
    print("-" * 45)
    for size, t_j, t_m in results:
        print(f"{size:<10} | {t_j:<17.4f} | {t_m:<.4f}")


if __name__ == "__main__":
    main()
