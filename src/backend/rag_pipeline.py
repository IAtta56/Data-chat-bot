from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from .agent_factory import get_llm
import os

# Persistent directory for vector DB
VECTOR_DB_DIR = "vector_store"
os.makedirs(VECTOR_DB_DIR, exist_ok=True)

class RagPipeline:
    def __init__(self, filepath: str, file_id: str):
        self.filepath = filepath
        self.collection_name = f"collection_{file_id}"
        
        # Use Hugging Face embeddings (free)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
            
        self.persist_directory = os.path.join(VECTOR_DB_DIR, self.collection_name)
        
    def ingest(self):
        """Loads data, splits it, and saves to Vector DB"""
        if self.filepath.endswith(".pdf"):
            loader = PyPDFLoader(self.filepath)
        else:
            loader = TextLoader(self.filepath)
            
        documents = loader.load()
        
        # Split text while keeping page metadata
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True
        )
        texts = text_splitter.split_documents(documents)
        
        # Store in Chroma
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        return vectorstore

    def get_chain(self):
        """Returns a RetrievalQA chain"""
         # Check if vectorstore exists, if not ingest
        if not os.path.exists(self.persist_directory):
             vectorstore = self.ingest()
        else:
            vectorstore = Chroma(
                persist_directory=self.persist_directory, 
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )

        llm = get_llm()
        
        # Custom prompt to force citation
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        return chain
