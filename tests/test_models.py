"""
Unit tests for data models (NewsItem and CollectionResult).
"""

import pytest
import json
from datetime import datetime, timezone

from collector.models import NewsItem, CollectionResult


class TestNewsItem:
    """Test cases for NewsItem model."""
    
    def test_newsitem_creation(self):
        """Test creating a NewsItem with all fields."""
        item = NewsItem(
            title="Test AI Paper",
            summary="This is a test summary",
            link="https://example.com/paper",
            published="2025-10-19T10:00:00Z",
            source="test_source"
        )
        
        assert item.title == "Test AI Paper"
        assert item.summary == "This is a test summary"
        assert item.link == "https://example.com/paper"
        assert item.published == "2025-10-19T10:00:00Z"
        assert item.source == "test_source"
    
    def test_newsitem_to_dict(self):
        """Test NewsItem serialization to dictionary."""
        item = NewsItem(
            title="Test Title",
            summary="Test Summary",
            link="https://test.com",
            published="2025-10-19T10:00:00Z",
            source="test"
        )
        
        result = item.to_dict()
        
        assert isinstance(result, dict)
        assert result['title'] == "Test Title"
        assert result['summary'] == "Test Summary"
        assert result['link'] == "https://test.com"
        assert result['published'] == "2025-10-19T10:00:00Z"
        assert 'source' not in result  # Source not included in dict
    
    def test_newsitem_equality(self):
        """Test NewsItem equality based on title."""
        item1 = NewsItem(
            title="Same Title",
            summary="Different summary 1",
            link="https://link1.com",
            published="2025-10-19T10:00:00Z",
            source="source1"
        )
        
        item2 = NewsItem(
            title="Same Title",
            summary="Different summary 2",
            link="https://link2.com",
            published="2025-10-19T11:00:00Z",
            source="source2"
        )
        
        assert item1 == item2
    
    def test_newsitem_inequality(self):
        """Test NewsItem inequality with different titles."""
        item1 = NewsItem(
            title="Title One",
            summary="Summary",
            link="https://link.com",
            published="2025-10-19T10:00:00Z",
            source="source"
        )
        
        item2 = NewsItem(
            title="Title Two",
            summary="Summary",
            link="https://link.com",
            published="2025-10-19T10:00:00Z",
            source="source"
        )
        
        assert item1 != item2
    
    def test_newsitem_hash(self):
        """Test NewsItem hashing for deduplication."""
        item1 = NewsItem(
            title="Test Title",
            summary="Summary 1",
            link="https://link1.com",
            published="2025-10-19T10:00:00Z",
            source="source1"
        )
        
        item2 = NewsItem(
            title="Test Title",
            summary="Summary 2",
            link="https://link2.com",
            published="2025-10-19T11:00:00Z",
            source="source2"
        )
        
        # Same title should produce same hash
        assert hash(item1) == hash(item2)
        
        # Can be used in sets
        items_set = {item1, item2}
        assert len(items_set) == 1  # Only one item due to same title
    
    def test_newsitem_case_insensitive_equality(self):
        """Test that title comparison is case-insensitive."""
        item1 = NewsItem(
            title="Test Title",
            summary="Summary",
            link="https://link.com",
            published="2025-10-19T10:00:00Z",
            source="source"
        )
        
        item2 = NewsItem(
            title="test title",
            summary="Summary",
            link="https://link.com",
            published="2025-10-19T10:00:00Z",
            source="source"
        )
        
        assert item1 == item2


class TestCollectionResult:
    """Test cases for CollectionResult model."""
    
    def test_collectionresult_creation(self):
        """Test creating a CollectionResult."""
        result = CollectionResult(
            date="2025-10-19",
            last_updated="2025-10-19T10:00:00Z"
        )
        
        assert result.date == "2025-10-19"
        assert result.last_updated == "2025-10-19T10:00:00Z"
        assert isinstance(result.collection_status, dict)
        assert isinstance(result.sources, dict)
    
    def test_add_source_items(self):
        """Test adding items from a source."""
        result = CollectionResult(
            date="2025-10-19",
            last_updated="2025-10-19T10:00:00Z"
        )
        
        items = [
            NewsItem("Title 1", "Summary 1", "https://link1.com", "2025-10-19T10:00:00Z", "test"),
            NewsItem("Title 2", "Summary 2", "https://link2.com", "2025-10-19T10:00:00Z", "test")
        ]
        
        result.add_source_items("test_source", items)
        
        assert "test_source" in result.sources
        assert len(result.sources["test_source"]) == 2
    
    def test_get_total_items(self):
        """Test counting total items across all sources."""
        result = CollectionResult(
            date="2025-10-19",
            last_updated="2025-10-19T10:00:00Z"
        )
        
        result.add_source_items("source1", [
            NewsItem("Title 1", "Summary", "https://link.com", "2025-10-19T10:00:00Z", "source1"),
            NewsItem("Title 2", "Summary", "https://link.com", "2025-10-19T10:00:00Z", "source1")
        ])
        
        result.add_source_items("source2", [
            NewsItem("Title 3", "Summary", "https://link.com", "2025-10-19T10:00:00Z", "source2")
        ])
        
        assert result.get_total_items() == 3
    
    def test_get_successful_sources(self):
        """Test identifying sources with items."""
        result = CollectionResult(
            date="2025-10-19",
            last_updated="2025-10-19T10:00:00Z"
        )
        
        result.add_source_items("source1", [
            NewsItem("Title", "Summary", "https://link.com", "2025-10-19T10:00:00Z", "source1")
        ])
        result.add_source_items("source2", [])
        
        successful = result.get_successful_sources()
        
        assert "source1" in successful
        assert "source2" not in successful
    
    def test_get_failed_sources(self):
        """Test identifying sources without items."""
        result = CollectionResult(
            date="2025-10-19",
            last_updated="2025-10-19T10:00:00Z"
        )
        
        result.add_source_items("source1", [
            NewsItem("Title", "Summary", "https://link.com", "2025-10-19T10:00:00Z", "source1")
        ])
        result.add_source_items("source2", [])
        
        failed = result.get_failed_sources()
        
        assert "source2" in failed
        assert "source1" not in failed
    
    def test_to_dict(self):
        """Test CollectionResult serialization to dictionary."""
        result = CollectionResult(
            date="2025-10-19",
            last_updated="2025-10-19T10:00:00Z",
            collection_status={'total': 1}
        )
        
        result.add_source_items("test", [
            NewsItem("Title", "Summary", "https://link.com", "2025-10-19T10:00:00Z", "test")
        ])
        
        data = result.to_dict()
        
        assert isinstance(data, dict)
        assert data['date'] == "2025-10-19"
        assert data['last_updated'] == "2025-10-19T10:00:00Z"
        assert 'collection_status' in data
        assert 'sources' in data
        assert 'test' in data['sources']
        assert len(data['sources']['test']) == 1
    
    def test_to_json(self):
        """Test CollectionResult serialization to JSON string."""
        result = CollectionResult(
            date="2025-10-19",
            last_updated="2025-10-19T10:00:00Z"
        )
        
        result.add_source_items("test", [
            NewsItem("Title", "Summary", "https://link.com", "2025-10-19T10:00:00Z", "test")
        ])
        
        json_str = result.to_json()
        
        assert isinstance(json_str, str)
        
        # Verify it's valid JSON
        parsed = json.loads(json_str)
        assert parsed['date'] == "2025-10-19"
        assert 'sources' in parsed
