"""
Main news collector orchestrator.
Manages collection from multiple sources, deduplication, and JSON generation.
"""

import os
import json
import logging
from datetime import datetime, timezone
from typing import List, Dict
from pathlib import Path

from collector.models import NewsItem, CollectionResult
from collector.fetchers import SourceFetcher


logger = logging.getLogger(__name__)


class NewsCollector:
    """
    Orchestrates news collection from multiple sources.
    Handles deduplication, aggregation, and output generation.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the news collector.
        
        Args:
            data_dir: Directory path for storing JSON output files
        """
        self.data_dir = Path(data_dir)
        self.fetchers: List[SourceFetcher] = []
        self.collected_items: List[NewsItem] = []
        
        # Ensure data directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"NewsCollector initialized with data_dir: {self.data_dir}")
    
    def register_fetcher(self, fetcher: SourceFetcher) -> None:
        """
        Register a source fetcher to be used during collection.
        
        Args:
            fetcher: SourceFetcher instance to register
        """
        self.fetchers.append(fetcher)
        logger.info(f"Registered fetcher: {fetcher.source_name}")
    
    def collect_all_sources(self) -> CollectionResult:
        """
        Execute collection from all registered sources.
        
        Returns:
            CollectionResult with aggregated data from all sources
        """
        logger.info(f"Starting collection from {len(self.fetchers)} sources")
        
        # Initialize result
        current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        current_timestamp = datetime.now(timezone.utc).isoformat()
        
        result = CollectionResult(
            date=current_date,
            last_updated=current_timestamp
        )
        
        successful_sources = []
        failed_sources = []
        total_items = 0
        
        # Collect from each source
        for fetcher in self.fetchers:
            try:
                items = fetcher.fetch_with_retry()
                
                if items:
                    # Deduplicate within source
                    unique_items = self._deduplicate_items(items)
                    result.add_source_items(fetcher.source_name, unique_items)
                    successful_sources.append(fetcher.source_name)
                    total_items += len(unique_items)
                    logger.info(f"{fetcher.source_name}: Collected {len(unique_items)} unique items")
                else:
                    result.add_source_items(fetcher.source_name, [])
                    failed_sources.append(fetcher.source_name)
                    logger.warning(f"{fetcher.source_name}: No items collected")
                    
            except Exception as e:
                logger.error(f"{fetcher.source_name}: Collection failed with error: {str(e)}")
                result.add_source_items(fetcher.source_name, [])
                failed_sources.append(fetcher.source_name)
        
        # Update collection status
        result.collection_status = {
            'total_sources': len(self.fetchers),
            'successful': len(successful_sources),
            'failed': len(failed_sources),
            'failed_sources': failed_sources,
            'total_items': total_items
        }
        
        logger.info(f"Collection complete: {total_items} items from {len(successful_sources)}/{len(self.fetchers)} sources")
        
        return result
    
    def _deduplicate_items(self, items: List[NewsItem]) -> List[NewsItem]:
        """
        Remove duplicate news items based on title similarity.
        
        Args:
            items: List of NewsItem objects
            
        Returns:
            List of unique NewsItem objects
        """
        if not items:
            return []
        
        # Use set to remove exact duplicates (based on __hash__ and __eq__ in NewsItem)
        unique_items = list(dict.fromkeys(items))
        
        removed_count = len(items) - len(unique_items)
        if removed_count > 0:
            logger.info(f"Removed {removed_count} duplicate items")
        
        return unique_items
    
    def deduplicate_across_sources(self, result: CollectionResult) -> CollectionResult:
        """
        Remove duplicates across all sources (optional advanced deduplication).
        
        Args:
            result: CollectionResult with items from all sources
            
        Returns:
            CollectionResult with cross-source duplicates removed
        """
        # Collect all items with their source
        all_items_with_source = []
        for source_name, items in result.sources.items():
            for item in items:
                all_items_with_source.append((source_name, item))
        
        # Track seen titles
        seen_titles = set()
        deduplicated_sources = {source: [] for source in result.sources.keys()}
        
        for source_name, item in all_items_with_source:
            title_normalized = item.title.lower().strip()
            if title_normalized not in seen_titles:
                seen_titles.add(title_normalized)
                deduplicated_sources[source_name].append(item)
        
        # Update result
        for source_name, items in deduplicated_sources.items():
            result.sources[source_name] = items
        
        return result
    
    def generate_json(self, result: CollectionResult, filename: str) -> str:
        """
        Write CollectionResult to JSON file.
        
        Args:
            result: CollectionResult to serialize
            filename: Name of the output file (without path)
            
        Returns:
            Full path to the created file
        """
        filepath = self.data_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(result.to_json())
            
            logger.info(f"Generated JSON file: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to write JSON file {filepath}: {str(e)}")
            raise
    
    def update_index(self, available_dates: List[str]) -> str:
        """
        Update the index.json file with list of available dates.
        
        Args:
            available_dates: List of dates in YYYY-MM-DD format
            
        Returns:
            Path to the index file
        """
        index_data = {
            'last_updated': datetime.now(timezone.utc).isoformat(),
            'available_dates': sorted(available_dates, reverse=True),
            'total_days': len(available_dates)
        }
        
        index_path = self.data_dir / 'index.json'
        
        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Updated index.json with {len(available_dates)} dates")
            return str(index_path)
            
        except Exception as e:
            logger.error(f"Failed to update index.json: {str(e)}")
            raise
    
    def get_available_dates(self) -> List[str]:
        """
        Get list of dates for which JSON files exist.
        
        Returns:
            List of date strings in YYYY-MM-DD format
        """
        dates = []
        
        for file in self.data_dir.glob('????-??-??.json'):
            date_str = file.stem
            dates.append(date_str)
        
        return sorted(dates, reverse=True)
    
    def cleanup_old_files(self, retention_days: int = 7) -> List[str]:
        """
        Delete JSON files older than retention period.
        
        Args:
            retention_days: Number of days to retain files
            
        Returns:
            List of deleted file paths
        """
        available_dates = self.get_available_dates()
        
        if len(available_dates) <= retention_days:
            logger.info(f"No cleanup needed: {len(available_dates)} files <= {retention_days} retention days")
            return []
        
        # Keep only the most recent files
        dates_to_keep = available_dates[:retention_days]
        dates_to_delete = available_dates[retention_days:]
        
        deleted_files = []
        
        for date_str in dates_to_delete:
            filepath = self.data_dir / f"{date_str}.json"
            try:
                if filepath.exists():
                    filepath.unlink()
                    deleted_files.append(str(filepath))
                    logger.info(f"Deleted old file: {filepath}")
            except Exception as e:
                logger.error(f"Failed to delete {filepath}: {str(e)}")
        
        logger.info(f"Cleanup complete: Deleted {len(deleted_files)} old files")
        
        return deleted_files
    
    def create_today_symlink(self, date_str: str) -> None:
        """
        Create or update today.json to point to the latest date file.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
        """
        source_file = self.data_dir / f"{date_str}.json"
        today_file = self.data_dir / "today.json"
        
        if not source_file.exists():
            logger.error(f"Source file does not exist: {source_file}")
            return
        
        try:
            # Read source and write to today.json (copy instead of symlink for GitHub Pages)
            with open(source_file, 'r', encoding='utf-8') as src:
                content = src.read()
            
            with open(today_file, 'w', encoding='utf-8') as dst:
                dst.write(content)
            
            logger.info(f"Updated today.json to point to {date_str}.json")
            
        except Exception as e:
            logger.error(f"Failed to create today.json: {str(e)}")
