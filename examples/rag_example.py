#!/usr/bin/env python3
# Example: RAG Usage

from someone.rag import RAG

rag = RAG()

# Add document
rag.add_document("about_me.txt", "My name is John, I like programming.")

# Search
result = rag.search("programming")
print(result)
