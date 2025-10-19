"""
Data models for Eternal AI News Aggregator.
Defines structures for news items and collection results.
"""

from dataclasses import dataclass, field
from typing import Dict, List
import json
from datetime import datetime


@dataclass
class NewsItem:
    """
    Represents a single news item from any source.
    
    Attributes:
        title: The headline or title of the news item
        summary: Brief description or excerpt of the content
        link: URL to the original source
        published: ISO 8601 formatted publication timestamp
        source: Identifier of the source (e.g., 'arxiv', 'huggingface')
    """
    title: str
    summary: str
    link: str
    published: str
    source: str
    
    def to_dict(self) -> dict:
        """
        Convert NewsItem to dictionary format for JSON serialization.
        
        Returns:
            Dictionary with all news item fields
        """
        return {
            'title': self.title,
            'summary': self.summary,
            'link': self.link,
            'published': self.published
        }
    
    def __hash__(self):
        """Make NewsItem hashable for deduplication using title."""
        return hash(self.title.lower().strip())
    
    def __eq__(self, other):
        """Compare NewsItems by normalized title for deduplication."""
        if not isinstance(other, NewsItem):
            return False
        return self.title.lower().strip() == other.title.lower().strip()


@dataclass
class CollectionResult:
    """
    Represents the complete result of a news collection run.
    
    Attributes:
        date: Date of collection in YYYY-MM-DD format
        last_updated: ISO 8601 timestamp of when collection completed
        collection_status: Metadata about the collection process
        sources: Dictionary mapping source names to lists of NewsItems
    """
    date: str
    last_updated: str
    collection_status: Dict[str, any] = field(default_factory=dict)
    sources: Dict[str, List[NewsItem]] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """
        Convert CollectionResult to dictionary format.
        
        Returns:
            Dictionary with all collection data
        """
        return {
            'date': self.date,
            'last_updated': self.last_updated,
            'collection_status': self.collection_status,
            'sources': {
                source: [item.to_dict() for item in items]
                for source, items in self.sources.items()
            }
        }
    
    def to_json(self, indent: int = 2) -> str:
        """
        Convert CollectionResult to JSON string.
        
        Args:
            indent: Number of spaces for JSON indentation
            
        Returns:
            Formatted JSON string
        """
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def add_source_items(self, source_name: str, items: List[NewsItem]) -> None:
        """
        Add news items from a specific source.
        
        Args:
            source_name: Identifier for the source
            items: List of NewsItem objects from that source
        """
        self.sources[source_name] = items
    
    def get_total_items(self) -> int:
        """
        Get total count of news items across all sources.
        
        Returns:
            Total number of news items
        """
        return sum(len(items) for items in self.sources.values())
    
    def get_successful_sources(self) -> List[str]:
        """
        Get list of sources that successfully returned items.
        
        Returns:
            List of source names with items
        """
        return [source for source, items in self.sources.items() if items]
    
    def get_failed_sources(self) -> List[str]:
        """
        Get list of sources that failed or returned no items.
        
        Returns:
            List of source names without items
        """
        return [source for source, items in self.sources.items() if not items]
