# PersonaChat: AI-Powered Persona Interaction

PersonaChat is a Python application that creates an AI assistant capable of imitating the writing style of a specific persona based on user-provided writing samples. The system uses OpenAI's GPT model with retrieval-augmented generation (RAG) to provide contextual responses.

---

## Features

- **Persona Imitation**: Generate AI responses in the style of a specific persona based on writing samples.
- **Retrieval-Augmented Generation**: Use RAG to retrieve relevant content from documents for enhanced responses.
- **Interactive Conversations**: Engage in live chat with the persona.
- **Conversation Logging**: Save all interactions to a markdown file for review.

---

## Requirements

### Dependencies

The required Python libraries are listed below:

- `openai`
- `python-dotenv`
- `langchain`
- `langchain-openai`
- `langchain-chroma`
- `chromadb`
- `sentence-transformers`
- `PyPDF2`

### Python Version

- Python 3.8 or higher

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/kliewerdaniel/PersonaChat.git
cd personachat
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up the OpenAI API Key
Create a `.env` file in the project root directory and add your OpenAI API key:
```plaintext
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Usage

### 1. Prepare Writing Samples
Place `.txt` and `.pdf` files containing writing samples in the `writing_samples` directory.

### 2. Run the Application
Start the chat interface:
```bash
python chat.py
```

### 3. Interact with the Persona
- Type your questions or prompts to chat with the persona.
- Type `exit` or `quit` to end the conversation.

### 4. View Conversation Logs
All interactions are saved in `conversation.md`. Open the file to review your chat history.

---

## How It Works

1. **Load Writing Samples**:
   - Reads `.txt` and `.pdf` files from the `writing_samples` directory.
   - Splits documents into smaller chunks for processing.

2. **Create Embeddings**:
   - Generates embeddings using OpenAI's embedding model.
   - Stores embeddings in a persistent Chroma vector store.

3. **Query and Respond**:
   - Uses a retriever to fetch relevant content from the vector store.
   - Generates persona-style responses with GPT using the retrieved context.

4. **Log Conversations**:
   - Saves user inputs and persona responses to `conversation.md` in markdown format.

---

## Folder Structure

```
PersonaChat/
├── writing_samples/       # Folder for input files (writing samples)
├── persona_vectorstore/   # Folder for storing vectorized document data
├── conversation.md        # File to save conversation logs
├── chat.py                # Main application script
├── requirements.txt       # List of dependencies
├── .env                   # Environment variables (e.g., API keys)
├── README.md              # Documentation
```

---

## Troubleshooting

### Common Issues

1. **Missing API Key**:
   - Ensure your `.env` file contains the `OPENAI_API_KEY`.

2. **No Writing Samples Found**:
   - Verify that `.txt` or `.pdf` files are placed in the `writing_samples` directory.

3. **Error Importing Libraries**:
   - Ensure the virtual environment is activated and dependencies are installed using `pip install -r requirements.txt`.

---

## Example `.env` File

```plaintext
OPENAI_API_KEY=sk-your-api-key
```

