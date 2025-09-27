# Medibot – Multimodal Medical AI Assistant

Medibot is a **multimodal RAG-based medical chatbot** that supports both text and voice input/output. Built with Flask, LangChain, Pinecone, and Hugging Face models, it provides context-aware medical responses through flexible interaction modes.

## Features

### Multimodal Interaction
- **Dual Input Modes**: Type or speak your medical questions
- **Dual Output Modes**: Read text responses or listen to spoken answers
- **Seamless Mode Switching**: Switch between text/voice anytime

### AI/ML Capabilities
- **Retrieval-Augmented Generation (RAG)**: Accurate, context-aware medical responses
- **Vector Semantic Search**: Pinecone vectorstore for relevant information retrieval
- **Input Normalization**: Hugging Face BART for query processing
- **Real-time Processing**: Instant text/voice conversion

## Technology Stack

- **Backend Framework**: Flask
- **AI Orchestration**: LangChain
- **Vector Database**: Pinecone
- **NLP Models**: Hugging Face (BART, Sentence Transformers, Qwen/Qwen3-Next-80B-A3B-Instruct)
- **Speech-to-Text**: OpenAI Whisper
- **Text-to-Speech**: Edge TTS
- **Frontend**: HTML, CSS, JavaScript

### API Keys Required:
- `PINECONE_API_KEY` - for vectorstore access
- `HF_API_KEY` - for Hugging Face model access

## Quick Start

### Option 1: Docker Deployment (Recommended)

```bash
# Build the image
docker build -t medibot .

# Run the container
docker run -p 8888:5000 \
  -e PINECONE_API_KEY=<your-pinecone-key> \
  -e HF_API_KEY=<your-hf-key> \
  medibot
```
Access the application at: http://localhost:8888

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/medibot.git
cd medibot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PINECONE_API_KEY=<your-pinecone-key>
export HF_API_KEY=<your-hf-key>

# Run the application
python app.py
```

## Relevance to AI/ML Role

This project demonstrates skills in:

### Multimodal AI Systems
- Dual-modality processing (text + voice)

- Real-time mode switching and synchronization

- End-to-end multimodal pipelines

### Natural Language Processing
- RAG implementation with LangChain

- Vector similarity search and semantic understanding

- Query normalization and processing

### Voice Data Expertise
- Speech-to-Text integration for voice input

- Text-to-Speech synthesis for voice output

- Audio processing and streaming

### Healthcare AI Applications
- Domain-specific RAG for medical information

- Accuracy-focused response generation

- User-friendly healthcare interfaces

## Contributing

Feel free to submit issues and enhancement requests!

## License

AGPL-3.0 License
