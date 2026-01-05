# DocTalker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

DocTalker is a Retrieval-Augmented Generation (RAG) system designed to enable natural language querying of PDF documents. It ingests PDFs, processes them into chunks, generates embeddings, and uses FAISS for efficient similarity search to provide context-aware answers.

## Features

- **PDF Ingestion**: Load and extract text from PDF files.
- **Text Chunking**: Split documents into manageable chunks for better retrieval.
- **Embedding Generation**: Convert text chunks into vector embeddings using advanced models.
- **Efficient Retrieval**: Use FAISS indexing for fast similarity search.
- **Question Answering**: Generate answers based on retrieved context.

## Project Structure

```
DocTalker/
├── data/
│   ├── raw/            # Original PDFs (never modified)
│   ├── processed/      # Cleaned text/chunks (optional cache)
├── embeddings/
│   └── faiss_index/    # Persisted FAISS index files
├── ingestion/
│   ├── pdf_loader.py   # PDF → text extraction
│   ├── chunker.py      # Text → chunks
│   └── embedder.py     # Chunks → vectors
├── retrieval/
│   ├── retriever.py    # Query → similar chunks
│   └── qa.py           # Context → answer generation
├── config/
│   └── settings.py     # Paths, model names, constants
├── main.py             # Orchestration entry point
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Jinish2170/DocTalker.git
   cd DocTalker
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare your PDFs**: Place your PDF files in the `data/raw/` directory.

2. **Run the ingestion pipeline**:

   ```python
   from main import ingest_pdfs
   ingest_pdfs()
   ```

3. **Query the system**:
   ```python
   from main import query
   answer = query("What is the main topic of the document?")
   print(answer)
   ```

For a full example, see `main.py`.

## Configuration

Edit `config/settings.py` to customize:

- Model names (e.g., embedding models)
- Paths to data directories
- FAISS index parameters

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FAISS](https://github.com/facebookresearch/faiss) for vector search.
- Uses [PyPDF2](https://pypi.org/project/PyPDF2/) for PDF processing.
- Inspired by modern RAG architectures.
