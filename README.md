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
# Dataset
**Source from: BBC/take-away-english**  
BBC1, BBC2, BBC3: https://www.bbc.co.uk/learningenglish/chinese/features/take-away-english/ep-251020  
BBC4, BBC5, BBC6: https://www.bbc.co.uk/learningenglish/chinese/features/take-away-english/ep-250210  
BBC7, BBC10, BBC11: https://www.bbc.co.uk/learningenglish/chinese/features/take-away-english/ep-240805  
BBC8, BBC9, BBC12: https://www.bbc.co.uk/learningenglish/chinese/features/take-away-english/ep-250728  

# Running
`cd src`
`python main.py`

# Text Similarity Project
**Step 1-2:**
This project implements **Shingling** and **Jaccard similarity** for document similarity detection.  
k = 10  # shingle length  
sim_threshold = 0.5 # similarity threshold  
**Step 3-4:**
Implement **Minhash** and **LSH** to approximate Jaccard similarity more efficiently and efficiently identify likely similar document pairs without comparing all pairs.
Similarity threshold t = 0.5
**Evaluation**
Compare the performance between Jaccard similarity and candidate pairs. 
The result shows that: As the number of documents increases, the Jaccard time significantly increases, but the MinHash + LSH time remains stable. This confirms that MinHash + LSH is more suitable for large datasets.
