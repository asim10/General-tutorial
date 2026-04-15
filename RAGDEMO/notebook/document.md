---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.1
  kernelspec:
    display_name: RAGDEMO (3.9.25)
    language: python
    name: python3
---

### Data Ingestion

```python
###Document Structure
from langchain_core.documents import Document
```

```python
doc = Document(
    page_content = "this is the main test content I am using to create RAG",
    metadata = {
        "source": "example.txt",
        "pages": 1,
        "author": "Asim Dinda",
        "date_created": "2026-01-01"
    }
)
```

```python
## Create a simple txt file
import os
os.makedirs("../data/text_files", exist_ok=True)
```

```python
sample_texts = {
    "../data/text_files/python_intro.txt":"""Python Programming Introduction

Python is a high-level, interpreted programming language known for its simplicity and readability. 
Created by Guido van Rossum and first released in 1991, Python has become one of the most popular 
programming languages in the world.

Key Features:
- Easy to learn and use
- Extensive standard library
- Cross-platform compatibility
- Strong community support

Python is widely used in web development, data science, artificial intelligence, and automation.""",

    "../data/text_files/machine_learning.txt": """Machine Learning Basics

Machine learning is a subset of artificial intelligence that enables systems to learn and improve 
from experience without being explicitly programmed. It focuses on developing computer programs 
that can access data and use it to learn for themselves.

Types of Machine Learning:
1. Supervised Learning: Learning with labeled data
2. Unsupervised Learning: Finding patterns in unlabeled data
3. Reinforcement Learning: Learning through rewards and penalties

Applications include image recognition, speech processing, and recommendation systems
    
    """
}

for filepath, content in sample_texts.items():
    with open(filepath, 'w', encoding="utf-8") as f:
        f.write(content)

print("✅ Sample text files created!")
```

```python
### TextLoader
from langchain.document_loaders import TextLoader

from langchain_community.document_loaders import TextLoader

loader = TextLoader("../data/text_files/python_intro.txt", encoding="utf-8")
document = loader.load()

print(document)
```

```python
### Directory Loader

from langchain_community.document_loaders import DirectoryLoader

## Load all the text files from the directory
dir_loader = DirectoryLoader(
    "../data/text_files",
    glob="**/*.txt", ## Pattern to match files
    loader_cls=TextLoader, ##loader class to use
    loader_kwargs={'encoding': 'utf-8'},
    show_progress=True
)

documents = dir_loader.load()
documents
```

```python
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader

## Load all the text files from the directory
dir_loader = DirectoryLoader(
    "../data/pdf",
    glob="**/*.pdf", ## Pattern to match files
    loader_cls=PyMuPDFLoader, ##loader class to use
    show_progress=True
)

pdf_documents = dir_loader.load()
pdf_documents
```

```python
## Create Sample DB file
import requests
import os

url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
if not os.path.exists("../data/db_files/Chinook.db"):
    response = requests.get(url)
    with open("../data/db_files/Chinook.db", "wb") as f:
        f.write(response.content)
    print("✅ Chinook.db downloaded successfully!")

```

```python
## Load sql db files
from langchain_community.utilities import SQLDatabase
from langchain_community.document_loaders import SQLDatabaseLoader

# 1. Define the connection string (pointing to your downloaded file)
db_uri = "sqlite:///../data/db_files/homelab_inventory.db"
db_engine = SQLDatabase.from_uri(db_uri)

# 2. Write a query to fetch the data you want to 'ingest'
# For example: Let's get all Tracks and their associated Album names
query = """
SELECT 
    * from
    servers where
    status='Online';
"""

# 3. Initialize the loader
loader = SQLDatabaseLoader(
    query=query,
    db=db_engine,
    # You can specify which column becomes the 'page_content'
    source_columns=["TrackName"] 
)

# 4. Load the data into Document objects
db_documents = loader.load()
db_documents
# Check the first document
# print(f"Content: {documents[0].page_content}")
# print(f"Metadata: {documents[0].metadata}")
```

```python
### Create a sample db file
import sqlite3

def create_sample_db():
    conn = sqlite3.connect('../data/db_files/homelab_inventory.db')
    cursor = conn.cursor()

    # Create a sample table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            os TEXT,
            ram_gb INTEGER,
            status TEXT
        )
    ''')

    # Insert sample data
    servers = [
        (1, 'Proxmox-Node-01', 'Debian', 64, 'Online'),
        (2, 'Backup-NAS', 'TrueNAS', 32, 'Online'),
        (3, 'Dev-Worker', 'Ubuntu 22.04', 16, 'Offline')
    ]
    
    cursor.executemany('INSERT INTO servers VALUES (?,?,?,?,?)', servers)
    conn.commit()
    conn.close()
    print("✅ homelab_inventory.db created!")

create_sample_db()
```

```python

```
