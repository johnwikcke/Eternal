"""
Unit tests for JSON generation and file operations.
Tests use real data from actual fetchers.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone

from collector.models import NewsItem, CollectionResult
from collector.collector import NewsCollector
from collector.sources import ArxivFetcher


class TestJSONGeneration:
    """Test cases for JSON file generation and management."""
    
    @pytest.fixture
    def temp_data_dir(self):
        """Create a temporary directory for test data."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def collector(self, temp_data_dir):
        """Create a NewsCollector with temporary data directory."""
        return NewsCollector(data_dir=temp_data_dir)
    
    @pytest.fixture
    def real_result(self, collector):
        """Create a CollectionResult with real data from arXiv."""
        # Use real arXiv fetcher to get actual data
        arxiv_fetcher = ArxivFetcher()
        collector.register_fetcher(arxiv_fetcher)
        
        # Collect real data
        result = collector.collect_all_sources()
        return result
    
    def test_generate_json_creates_file(self, collector, real_result):
        """Test that generate_json creates a file with real data."""
        filename = "2025-10-19.json"
        filepath = collector.generate_json(real_result, filename)
        
        assert Path(filepath).exists()
        assert Path(filepath).is_file()
    
    def test_generate_json_valid_structure(self, collector, real_result):
        """Test that generated JSON has valid structure with real data."""
        filename = "2025-10-19.json"
        filepath = collector.generate_json(real_result, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert 'date' in data
        assert 'last_updated' in data
        assert 'collection_status' in data
        assert 'sources' in data
        
        assert isinstance(data['sources'], dict)
        assert isinstance(data['collection_status'], dict)
    
    def test_generate_json_contains_arxiv_source(self, collector, real_result):
        """Test that JSON contains arXiv source with real data."""
        filename = "2025-10-19.json"
        filepath = collector.generate_json(real_result, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert 'arxiv' in data['sources']
        # ArXiv should have items (unless the feed is down)
        assert isinstance(data['sources']['arxiv'], list)
    
    def test_generate_json_item_structure(self, collector, real_result):
        """Test that items in JSON have correct structure with real data."""
        filename = "2025-10-19.json"
        filepath = collector.generate_json(real_result, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get first item from arxiv if available
        if data['sources']['arxiv']:
            item = data['sources']['arxiv'][0]
            
            assert 'title' in item
            assert 'summary' in item
            assert 'link' in item
            assert 'published' in item
            assert 'source' not in item  # Source not included in item dict
            
            # Verify real data characteristics
            assert len(item['title']) > 0
            assert item['link'].startswith('http')
    
    def test_update_index_creates_file(self, collector):
        """Test that update_index creates index.json."""
        dates = ["2025-10-19", "2025-10-18", "2025-10-17"]
        index_path = collector.update_index(dates)
        
        assert Path(index_path).exists()
        assert Path(index_path).name == "index.json"
    
    def test_update_index_structure(self, collector):
        """Test index.json structure."""
        dates = ["2025-10-19", "2025-10-18"]
        index_path = collector.update_index(dates)
        
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert 'last_updated' in data
        assert 'available_dates' in data
        assert 'total_days' in data
        
        assert isinstance(data['available_dates'], list)
        assert data['total_days'] == 2
    
    def test_update_index_sorts_dates(self, collector):
        """Test that index.json sorts dates in descending order."""
        dates = ["2025-10-17", "2025-10-19", "2025-10-18"]
        index_path = collector.update_index(dates)
        
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data['available_dates'] == ["2025-10-19", "2025-10-18", "2025-10-17"]
    
    def test_get_available_dates(self, collector, real_result):
        """Test getting list of available dates from files."""
        # Create some date files with real data
        collector.generate_json(real_result, "2025-10-19.json")
        collector.generate_json(real_result, "2025-10-18.json")
        collector.generate_json(real_result, "2025-10-17.json")
        
        dates = collector.get_available_dates()
        
        assert len(dates) == 3
        assert "2025-10-19" in dates
        assert "2025-10-18" in dates
        assert "2025-10-17" in dates
        assert dates == sorted(dates, reverse=True)  # Should be sorted descending
    
    def test_cleanup_old_files(self, collector, real_result):
        """Test cleanup of old files with real data."""
        # Create 10 date files with real data
        for i in range(10, 0, -1):
            date_str = f"2025-10-{i:02d}"
            collector.generate_json(real_result, f"{date_str}.json")
        
        # Cleanup with retention of 7 days
        deleted = collector.cleanup_old_files(retention_days=7)
        
        assert len(deleted) == 3  # Should delete 3 oldest files
        
        # Verify only 7 files remain
        remaining_dates = collector.get_available_dates()
        assert len(remaining_dates) == 7
    
    def test_cleanup_no_files_to_delete(self, collector, real_result):
        """Test cleanup when no files need deletion."""
        # Create only 5 files
        for i in range(5, 0, -1):
            date_str = f"2025-10-{i:02d}"
            collector.generate_json(real_result, f"{date_str}.json")
        
        # Cleanup with retention of 7 days
        deleted = collector.cleanup_old_files(retention_days=7)
        
        assert len(deleted) == 0
        
        # All files should remain
        remaining_dates = collector.get_available_dates()
        assert len(remaining_dates) == 5
    
    def test_cleanup_keeps_most_recent(self, collector, real_result):
        """Test that cleanup keeps the most recent files."""
        # Create files
        dates = ["2025-10-15", "2025-10-16", "2025-10-17", "2025-10-18", "2025-10-19"]
        for date_str in dates:
            collector.generate_json(real_result, f"{date_str}.json")
        
        # Cleanup keeping only 3
        deleted = collector.cleanup_old_files(retention_days=3)
        
        assert len(deleted) == 2
        
        remaining_dates = collector.get_available_dates()
        assert "2025-10-19" in remaining_dates
        assert "2025-10-18" in remaining_dates
        assert "2025-10-17" in remaining_dates
        assert "2025-10-15" not in remaining_dates
        assert "2025-10-16" not in remaining_dates
    
    def test_create_today_symlink(self, collector, real_result):
        """Test creating today.json file with real data."""
        date_str = "2025-10-19"
        collector.generate_json(real_result, f"{date_str}.json")
        collector.create_today_symlink(date_str)
        
        today_path = Path(collector.data_dir) / "today.json"
        assert today_path.exists()
        
        # Verify content matches
        with open(today_path, 'r', encoding='utf-8') as f:
            today_data = json.load(f)
        
        assert 'date' in today_data
        assert 'sources' in today_data
    
    def test_json_utf8_encoding(self, collector, real_result):
        """Test that JSON files use UTF-8 encoding with real data."""
        filepath = collector.generate_json(real_result, "test-unicode.json")
        
        # Read and verify it can be loaded
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verify structure is intact
        assert 'sources' in data
        assert isinstance(data['sources'], dict)
    
    def test_json_indentation(self, collector, real_result):
        """Test that JSON is properly indented for readability."""
        filepath = collector.generate_json(real_result, "test-indent.json")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for indentation (should have spaces)
        assert '  "date"' in content or '\t"date"' in content
        # Should be multi-line
        assert content.count('\n') > 5
