<<<<<<< HEAD
from langchain_text_splitters import RecursiveCharacterTextSplitter # Text splitter for chunking documents based on character count
=======
from langchain.text_splitter import RecursiveCharacterTextSplitter # Text splitter for chunking documents based on character count
>>>>>>> b3d9bc4f97dd981af8e3cd08bd43c509d34ce52f
from typing import List, Dict 

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

def chunk_documents(documents: List[Dict], chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[Dict]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = []
    for doc in documents:
        texts = splitter.split_text(doc["text"])
        for i, chunk in enumerate(texts):
            chunks.append({
                "title": doc.get("title", ""),
                "sections": doc.get("sections", []),
                "text": chunk,
                "source": doc["source"],
                "page": doc["page"],
                "chunk_id": i
            })
    return chunks