import os
import sys
import glob
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import openai
from langchain_openai import OpenAIEmbeddings  # Updated import
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory

load_dotenv()  # Load variables from .env
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    exit(1)

def main():

    
    # Initialize memory
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)


    # Step 1: Load and process writing samples
    folder_path = './writing_samples'
    documents = []
    for filepath in glob.glob(os.path.join(folder_path, '**/*.*'), recursive=True):
        if os.path.isfile(filepath):
            ext = os.path.splitext(filepath)[1].lower()
            try:
                if ext == '.txt':
                    loader = TextLoader(filepath, encoding='utf-8')
                    documents.extend(loader.load())
                elif ext == '.pdf':
                    loader = PyPDFLoader(filepath)
                    documents.extend(loader.load())
                else:
                    print(f"Unsupported file format: {filepath}")
            except Exception as e:
                print(f"Error reading '{filepath}': {e}")

    if not documents:
        print("No documents found in the folder.")
        exit(1)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Step 2: Create embeddings and vector store
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)  # Pass API key directly
    vector_store = Chroma.from_documents(texts, embeddings, persist_directory="./persona_vectorstore")
    vector_store.persist()

    # Step 3: Set up the retriever and agent
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)


    persona_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an AI assistant imitating the writing style of a specific persona based on provided writing samples.

Context:
{context}

Question:
{question}

Answer in the persona's writing style.
"""
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        memory=memory,
        return_source_documents=False,
        chain_type_kwargs={"prompt": persona_prompt}
    )

    def save_to_markdown(conversation, filename="conversation.md"): 
        with open(filename, "a", encoding="utf-8") as f:
            f.write(conversation + "\n\n---\n\n")


    # Step 4: Interact with the user and save to markdown
    print("You can now interact with the persona. Type 'exit' to quit.\n")
    conversation_history = ""
    while True:
        user_input = input("You: ")
        if user_input.lower() in ('exit', 'quit'):
            break

        # Generate response
        response = qa_chain.run(user_input)

        # Display and save the conversation
        print(f"Persona: {response}\n")
        conversation = f"### You:\n{user_input}\n\n### Persona:\n{response}"
        save_to_markdown(conversation)


if __name__ == "__main__":
    main()
