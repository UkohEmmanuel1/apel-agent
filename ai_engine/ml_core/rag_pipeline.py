import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

class MarketIntelligenceRAG:
    def __init__(self, data_dir="data/raw_knowledge"):
        self.data_dir = data_dir
        self.persist_directory = "ai_engine/ml_core/vector_store"
        
        # Using a fast, lightweight embedding model perfect for CPU/Edge or quick GPU inference
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db = self._initialize_db()

    def _initialize_db(self):
        """Loads data and creates the vector database if it doesn't exist."""
        if os.path.exists(self.persist_directory):
            return Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        
        # Fallback if DB doesn't exist yet
        print("Vector DB not found. Initializing empty DB...")
        return Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)

    def retrieve_strategy(self, query: str, top_k: int = 3) -> str:
        """Searches the vector database for relevant market theories."""
        if not self.vector_db:
            return "Knowledge base is currently empty. Please ingest market data."

        docs = self.vector_db.similarity_search(query, k=top_k)
        context = "\n".join([doc.page_content for doc in docs])
        
        # Format the prompt with our retrieved Y-Combinator chunks
        llm_prompt = f"""
        Based on the following market intelligence:
        {context}
        
        Provide an actionable business strategy for: {query}
        """
        
        # Initialize the Gemini Brain
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Pass the formatted prompt to Gemini to generate the final strategy
        response = llm.invoke(llm_prompt)
        
        # Return the final synthesized text
        return response.content

# Singleton instance to be imported by Django views
rag_system = MarketIntelligenceRAG()