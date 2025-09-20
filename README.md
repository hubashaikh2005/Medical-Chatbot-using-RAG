# Medibot – AI Medical Chatbot

Medibot is an AI-powered medical chatbot built with Flask, LangChain, Pinecone, and Hugging Face models. It provides conversational answers to medical queries using a vector database for context-aware responses and BART for input normalization.

## Features

- Answer medical questions with context awareness

- Normalize user input using Hugging Face BART

- Use Pinecone vectorstore for fast retrieval

- Convert Markdown responses to HTML for clean display

- Easy to run locally with Docker

## Requirements

Python 3.11

Docker (optional, for containerized deployment)

API Keys:

PINECONE_API_KEY → for vectorstore

HF_API_KEY → for Hugging Face model access

## Quick Start with Docker

Build the Docker image:

`
docker build -t medibot .
`

Run the container with your API keys:

`
docker run -p 8888:5000 -e PINECONE_API_KEY=<your-pinecone-key> -e HF_API_KEY=<your-hf-key> medibot
`

Open in browser at: http://localhost:8888

## License

AG-UI is open source software licensed as MIT.
