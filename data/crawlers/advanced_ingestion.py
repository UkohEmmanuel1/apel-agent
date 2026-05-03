import os
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

class AdvancedMarketCrawler:
    def __init__(self):
        print(" Initializing Apex Advanced Crawler...")
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.db_path = os.path.join(base_dir, "ai_engine", "ml_core", "vector_store")
        
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.vector_db = Chroma(persist_directory=self.db_path, embedding_function=self.embeddings)

    def _process_and_store(self, documents, source_name):
        if not documents:
            return
        chunks = self.text_splitter.split_documents(documents)
        self.vector_db.add_documents(chunks)
        self.vector_db.persist()
        print(f" Ingested {len(chunks)} knowledge chunks from: {source_name}")

    def bulk_youtube_extractor(self, video_urls: list):
        """Processes a master list of top business strategy videos."""
        print(f"\n Starting Bulk YouTube Extraction ({len(video_urls)} videos)...")
        for url in video_urls:
            try:
                loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
                docs = loader.load()
                title = docs[0].metadata.get('title', 'Unknown Video')
                self._process_and_store(docs, f"YouTube: {title}")
            except Exception as e:
                print(f" Failed on {url}: {str(e)[:50]}...")

    def dynamic_blog_scraper(self, blog_index_url: str, article_selector: str):
        """Finds the latest articles on a blog and scrapes them all."""
        print(f"\n Scanning for latest market trends on: {blog_index_url}")
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            # 1. Fetch the main blog page
            response = requests.get(blog_index_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 2. Find all article links based on the provided CSS selector
            links = soup.select(article_selector)
            article_urls = [link['href'] for link in links][:5] # Grab the top 5 latest
            
            # Ensure URLs are absolute
            article_urls = [url if url.startswith('http') else f"https://{url.lstrip('/')}" for url in article_urls]
            
            # 3. Scrape each individual article
            for url in article_urls:
                try:
                    art_res = requests.get(url, headers=headers)
                    art_soup = BeautifulSoup(art_res.text, 'html.parser')
                    paragraphs = art_soup.find_all('p')
                    text_content = "\n".join([p.get_text() for p in paragraphs if len(p.get_text()) > 60])
                    
                    if text_content:
                        doc = Document(page_content=text_content, metadata={"source": url})
                        self._process_and_store([doc], url)
                except Exception as inner_e:
                    print(f" Skipped article {url}: {inner_e}")
                    
        except Exception as e:
            print(f" Failed to scan blog index: {e}")

# ==========================================
# EXECUTION SPRINT
# ==========================================
if __name__ == "__main__":
    crawler = AdvancedMarketCrawler()
    
    # --- 1. THE Y-COMBINATOR & HBR PLAYLIST ---
    # Top tier business theories for the AI's brain
    strategy_videos = [
        "https://www.youtube.com/watch?v=DOtCl5PU8F0", # YC: How to Price Your Product
        "https://www.youtube.com/watch?v=yGjqKJoK1y8", # YC: B2B Sales
        "https://www.youtube.com/watch?v=W-Lz0A03V_g", # Pricing Psychology
    ]
    crawler.bulk_youtube_extractor(strategy_videos)

    # --- 2. DYNAMIC BUSINESS BLOG SCRAPER ---
    # Example: Scraping a generic marketing blog structure
    # (Update 'blog_index_url' and 'article_selector' for your specific targets)
    crawler.dynamic_blog_scraper(
        blog_index_url="https://medium.com/tag/marketing-strategy",
        article_selector="a.af.ag.ah.ai.aj.ak.al.am.an.ao.ap.aq.ar.as.at" # Adjust based on target site's HTML
    )
    
    print("\n Advanced knowledge extraction complete. Apex is fully armed.")