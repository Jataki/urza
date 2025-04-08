from config import GOOGLE_API_KEY, KNOWLEDGE_BASE_DIR
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class KnowledgeBaseRetriever:
    """Service for retrieving information from the knowledge base."""
    
    def __init__(self, embedding_model="models/text-embedding-004"):
        """Initialize the knowledge base retriever."""
        self.knowledge_dir = KNOWLEDGE_BASE_DIR
        self.embedding_model = embedding_model
        self.vector_store = None
        self.embeddings = None
    
    def initialize(self):
        """Initialize the vector store with documents from the knowledge base."""
        # Initialize embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=self.embedding_model, 
            google_api_key=GOOGLE_API_KEY
        )
        
        # Load documents
        loader = DirectoryLoader(self.knowledge_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
        splits = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = Chroma.from_documents(documents=splits, embedding=self.embeddings)
        
        return self
    
    def get_retriever(self, k=5):
        """Return the retriever with top k results."""
        if not self.vector_store:
            self.initialize()
        return self.vector_store.as_retriever(search_kwargs={"k": k})