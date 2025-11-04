# DataMining-Textually-Similar-Documents
 Implement the stages of finding textually similar documents based on Jaccard similarity using the shingling, minhashing, and locality-sensitive hashing (LSH) techniques and corresponding algorithms.

# Structure
```
  text_similarity_project/  
  │  
  ├── data/                     
  │   ├── doc1.txt  
  │   ├── doc2.txt  
  │   ├── doc3.txt  
  │   ├── ...
  │  
  ├── src/  
  │   ├── __init__.py  
  │   ├── shingling.py            
  │   ├── compare_sets.py         
  │   ├── main.py      
  │   ├── minhashing.py           
  │   ├── compare_signatures.py   
  │   ├── lsh.py          
  │  
  └── README.md
```

# Text Similarity Project (Stage 1–2)

This project implements **Shingling** and **Jaccard similarity** for document similarity detection.
k = 10  # shingle length
sim_threshold = 0.5 # similarity threshold
