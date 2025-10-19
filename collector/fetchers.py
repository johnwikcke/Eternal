"""
Base fetcher classes and utilities for collecting AI news from various sources.
Includes error handling, retry logic, and timeout management.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import logging
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from collector.models import NewsItem


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SourceFetcher(ABC):
    """
    Abstract base class for all source-specific fetchers.
    Provides error handling, retry logic, and timeout management.
    """
    
    # Default configuration
    TIMEOUT = 30  # seconds
    MAX_RETRIES = 3
    BACKOFF_FACTOR = 2  # exponential backoff: 2, 4, 8 seconds
    
    def __init__(self, source_name: str):
        """
        Initialize the fetcher with source identification.
        
        Args:
            source_name: Unique identifier for this source
        """
        self.source_name = source_name
        self.session = self._create_session()
        logger.info(f"Initialized {source_name} fetcher")
    
    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry logic and timeout.
        
        Returns:
            Configured requests.Session object
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.MAX_RETRIES,
            backoff_factor=self.BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set user agent to identify the bot
        session.headers.update({
            'User-Agent': 'Eternal-AI-News-Bot/1.0 (GitHub Actions; +https://github.com/eternal)'
        })
        
        return session
    
    def fetch_with_retry(self) -> List[NewsItem]:
        """
        Fetch news items with error handling and retry logic.
        
        Returns:
            List of NewsItem objects, empty list on failure
        """
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                logger.info(f"Fetching from {self.source_name} (attempt {attempt}/{self.MAX_RETRIES})")
                items = self.fetch()
                logger.info(f"Successfully fetched {len(items)} items from {self.source_name}")
                return items
                
            except requests.exceptions.Timeout:
                logger.warning(f"{self.source_name}: Request timeout on attempt {attempt}")
                if attempt < self.MAX_RETRIES:
                    time.sleep(self.BACKOFF_FACTOR ** attempt)
                    
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"{self.source_name}: Connection error on attempt {attempt}: {str(e)}")
                if attempt < self.MAX_RETRIES:
                    time.sleep(self.BACKOFF_FACTOR ** attempt)
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"{self.source_name}: Request failed on attempt {attempt}: {str(e)}")
                if attempt < self.MAX_RETRIES:
                    time.sleep(self.BACKOFF_FACTOR ** attempt)
                    
            except Exception as e:
                logger.error(f"{self.source_name}: Unexpected error on attempt {attempt}: {str(e)}")
                if attempt < self.MAX_RETRIES:
                    time.sleep(self.BACKOFF_FACTOR ** attempt)
        
        logger.error(f"{self.source_name}: All retry attempts failed")
        return []
    
    @abstractmethod
    def fetch(self) -> List[NewsItem]:
        """
        Fetch and parse content from the source.
        Must be implemented by subclasses.
        
        Returns:
            List of NewsItem objects
            
        Raises:
            Various exceptions that will be caught by fetch_with_retry
        """
        pass
    
    def parse(self, raw_content) -> List[NewsItem]:
        """
        Parse raw content into NewsItem objects.
        Can be overridden by subclasses if needed.
        
        Args:
            raw_content: Raw data from the source
            
        Returns:
            List of NewsItem objects
        """
        # Default implementation - subclasses should override if needed
        return []
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text string
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        
        return text.strip()
    
    def truncate_summary(self, text: str, max_length: int = 300) -> str:
        """
        Truncate summary text to a maximum length.
        
        Args:
            text: Full text
            max_length: Maximum character length
            
        Returns:
            Truncated text with ellipsis if needed
        """
        text = self.clean_text(text)
        
        if len(text) <= max_length:
            return text
        
        # Truncate at word boundary
        truncated = text[:max_length].rsplit(' ', 1)[0]
        return truncated + '...'
    
    def is_ai_related(self, text: str) -> bool:
        """
        Check if content is AI-related based on keywords.
        
        Args:
            text: Text to check (title + summary)
            
        Returns:
            True if AI-related, False otherwise
        """
        ai_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'ml',
            'deep learning', 'neural network', 'llm', 'gpt', 'transformer',
            'nlp', 'computer vision', 'reinforcement learning',
            'generative', 'diffusion', 'model', 'dataset', 'training',
            'inference', 'embedding', 'attention', 'agent', 'chatbot',
            'claude', 'openai', 'anthropic', 'hugging face', 'pytorch',
            'tensorflow', 'keras', 'scikit', 'langchain', 'prompt'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in ai_keywords)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(source='{self.source_name}')>"
