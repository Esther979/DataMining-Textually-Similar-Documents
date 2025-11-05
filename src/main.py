import os
import time
from shingling import Shingling
from compare_sets import CompareSets

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

    # Optional timing
    t0 = time.time()
    _ = [compare.jaccard_similarity(a, b) for a in shingle_sets.values() for b in shingle_sets.values()]
    print(f"\n⏱️ Total processing time: {time.time() - t0:.3f}s")


if __name__ == "__main__":
    main()
