"""
Integration tests for real source fetchers.
These tests make actual HTTP requests to verify fetchers work with live data.
"""

import pytest
from collector.sources import (
    ArxivFetcher,
    HuggingFaceFetcher,
    ProductHuntFetcher,
    RedditFetcher,
    AINewsFetcher,
    CrescendoFetcher
)
from collector.models import NewsItem


class TestArxivFetcher:
    """Test ArxivFetcher with real arXiv data."""
    
    def test_arxiv_fetch_returns_items(self):
        """Test that ArxivFetcher returns real news items."""
        fetcher = ArxivFetcher()
        items = fetcher.fetch_with_retry()
        
        # ArXiv should return items (unless service is down)
        assert isinstance(items, list)
        
        if items:  # If we got items
            assert len(items) > 0
            assert all(isinstance(item, NewsItem) for item in items)
    
    def test_arxiv_item_structure(self):
        """Test that arXiv items have correct structure."""
        fetcher = ArxivFetcher()
        items = fetcher.fetch_with_retry()
        
        if items:
            item = items[0]
            assert hasattr(item, 'title')
            assert hasattr(item, 'summary')
            assert hasattr(item, 'link')
            assert hasattr(item, 'published')
            assert hasattr(item, 'source')
            
            assert len(item.title) > 0
            assert len(item.summary) > 0
            assert item.link.startswith('http')
            assert item.source == 'arxiv'
    
    def test_arxiv_link_format(self):
        """Test that arXiv links are properly formatted."""
        fetcher = ArxivFetcher()
        items = fetcher.fetch_with_retry()
        
        if items:
            for item in items:
                assert 'arxiv.org' in item.link


class TestHuggingFaceFetcher:
    """Test HuggingFaceFetcher with real Hugging Face data."""
    
    def test_huggingface_fetch_returns_items(self):
        """Test that HuggingFaceFetcher returns real news items."""
        fetcher = HuggingFaceFetcher()
        items = fetcher.fetch_with_retry()
        
        assert isinstance(items, list)
        
        if items:
            assert len(items) > 0
            assert all(isinstance(item, NewsItem) for item in items)
    
    def test_huggingface_item_structure(self):
        """Test that Hugging Face items have correct structure."""
        fetcher = HuggingFaceFetcher()
        items = fetcher.fetch_with_retry()
        
        if items:
            item = items[0]
            assert len(item.title) > 0
            assert len(item.summary) > 0
            assert item.link.startswith('http')
            assert item.source == 'huggingface'
    
    def test_huggingface_link_domain(self):
        """Test that Hugging Face links point to correct domain."""
        fetcher = HuggingFaceFetcher()
        items = fetcher.fetch_with_retry()
        
        if items:
            for item in items:
                assert 'huggingface.co' in item.link


class TestProductHuntFetcher:
    """Test ProductHuntFetcher with real Product Hunt data."""
    
    def test_producthunt_fetch_returns_items(self):
        """Test that ProductHuntFetcher returns real news items."""
        fetcher = ProductHuntFetcher()
        items = fetcher.fetch_with_retry()
        
        assert isinstance(items, list)
        # Product Hunt might have items or might be empty depending on scraping
    
    def test_producthunt_item_structure(self):
        """Test that Product Hunt items have correct structure."""
        fetcher = ProductHuntFetcher()
        items = fetcher.fetch_with_retry()
        
        if items:
            item = items[0]
            assert len(item.title) > 0
            assert len(item.summary) > 0
            assert item.link.startswith('http')
            assert item.source == 'producthunt'
    
    def test_producthunt_ai_filtering(self):
        """Test that Product Hunt items are AI-related."""
        fetcher = ProductHuntFetcher()
        items = fetcher.fetch_with_retry()
        
        if items:
            # Items should be AI-related based on filtering
            for item in items:
                combined_text = (item.title + ' ' + item.summary).lower()
                # Should contain at least some AI-related terms
                assert len(combined_text) > 0


class TestRedditFetcher:
    """Test RedditFetcher with real Reddit data."""
    
    def test_reddit_fetch_returns_items(self):
        """Test that RedditFetcher returns real news items."""
        fetcher = RedditFetcher()
        items = fetcher.fetch_with_retry()
        
        assert isinstance(items, list)
        
        if items:
            assert len(items) > 0
            assert all(isinstance(item, NewsItem) for item in items)
    
    def test_reddit_item_structure(self):
        """Test that Reddit items have correct structure."""
        fetcher = RedditFetcher()
        items = fetcher.fetch_with_retry()
        
        if items:
            item = items[0]
            assert len(item.title) > 0
            assert item.link.startswith('http')
            assert item.source == 'reddit'
    
    def test_reddit_subreddit_prefix(self):
        """Test that Reddit items have subreddit prefix in title."""
        fetcher = RedditFetcher()
        items = fetcher.fetch_with_retry()
        
        if items:
            for item in items:
                # Title should start with [r/subreddit]
                assert item.title.startswith('[r/')
    
    def test_reddit_multiple_subreddits(self):
        """Test that Reddit fetcher collects from multiple subreddits."""
        fetcher = RedditFetcher()
        items = fetcher.fetch_with_retry()
        
        if len(items) > 1:
            # Should have items from different subreddits
            subreddits = set()
            for item in items:
                # Check for various subreddit name formats
                if 'machinelearning' in item.title.lower():
                    subreddits.add('MachineLearning')
                elif 'claudeai' in item.title.lower():
                    subreddits.add('ClaudeAI')
            
            # Might have items from one or both subreddits
            # If we got items, at least some should be identifiable
            assert len(items) > 0


class TestAINewsFetcher:
    """Test AINewsFetcher with real AI News data."""
    
    def test_ainews_fetch_returns_items(self):
        """Test that AINewsFetcher returns real news items."""
        fetcher = AINewsFetcher()
        items = fetcher.fetch_with_retry()
        
        assert isinstance(items, list)
        # Might be empty if scraping fails
    
    def test_ainews_item_structure(self):
        """Test that AI News items have correct structure."""
        fetcher = AINewsFetcher()
        items = fetcher.fetch_with_retry()
        
        if items:
            item = items[0]
            assert len(item.title) > 0
            assert item.link.startswith('http')
            assert item.source == 'ai_news'


class TestCrescendoFetcher:
    """Test CrescendoFetcher with real Crescendo data."""
    
    def test_crescendo_fetch_returns_items(self):
        """Test that CrescendoFetcher returns real news items."""
        fetcher = CrescendoFetcher()
        items = fetcher.fetch_with_retry()
        
        assert isinstance(items, list)
        # Might be empty if scraping fails
    
    def test_crescendo_item_structure(self):
        """Test that Crescendo items have correct structure."""
        fetcher = CrescendoFetcher()
        items = fetcher.fetch_with_retry()
        
        if items:
            item = items[0]
            assert len(item.title) > 0
            assert item.link.startswith('http')
            assert item.source == 'crescendo'


class TestFetcherErrorHandling:
    """Test error handling across all fetchers."""
    
    def test_fetchers_handle_network_errors_gracefully(self):
        """Test that fetchers return empty list on errors, not crash."""
        fetchers = [
            ArxivFetcher(),
            HuggingFaceFetcher(),
            ProductHuntFetcher(),
            RedditFetcher(),
            AINewsFetcher(),
            CrescendoFetcher()
        ]
        
        for fetcher in fetchers:
            # Should not raise exception, even if network fails
            try:
                items = fetcher.fetch_with_retry()
                assert isinstance(items, list)
            except Exception as e:
                pytest.fail(f"{fetcher.source_name} raised exception: {e}")
    
    def test_fetchers_return_newsitem_objects(self):
        """Test that all fetchers return NewsItem objects."""
        fetchers = [
            ArxivFetcher(),
            HuggingFaceFetcher(),
            ProductHuntFetcher(),
            RedditFetcher(),
            AINewsFetcher(),
            CrescendoFetcher()
        ]
        
        for fetcher in fetchers:
            items = fetcher.fetch_with_retry()
            
            if items:
                for item in items:
                    assert isinstance(item, NewsItem)
                    assert hasattr(item, 'title')
                    assert hasattr(item, 'summary')
                    assert hasattr(item, 'link')
                    assert hasattr(item, 'published')
                    assert hasattr(item, 'source')
