import os
import sys
import argparse
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss 
import pickle

def list_files(path, exts=(".py",".js",".ts")):
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(exts):
                yield os.path.join(root, f)

def chunk_text(text, chunk_size=800):
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--out", default="../data/faiss_index")
    args = parser.parse_args()

    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = []
    metas = []
    for fp in list_files(args.path):
        with open(fp, "r" , encoding="utf-8", errors="ignore") as f:
            content = f.read()
        for i, chunk in enumerate(chunk_text(content)):
            texts.append(chunk)
            metas.append({"path": fp, "chunk_id": i})

    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, os.path.join(args.out, "faiss.index"))
    with open(os.path.join(args.out, "meta.pkl"), "wb") as f:
        pickle.dump({"texts": texts, "metas":metas}, f)
    print(f"Index saved to", args.out)