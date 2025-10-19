#!/usr/bin/env python3
"""
Eternal AI News Aggregator - Main Collection Script

This script orchestrates the collection of AI news from multiple sources,
generates structured JSON output, and manages the 7-day rolling data store.

Usage:
    python collector/generate_news.py [options]

Options:
    --date YYYY-MM-DD    Specify date for output file (default: today)
    --verbose, -v        Enable verbose logging
    --dry-run            Run without writing files
    --retention DAYS     Number of days to retain (default: 7)
"""

import sys
import argparse
import logging
from datetime import datetime, timezone
from pathlib import Path
import os

# Add parent directory to Python path BEFORE imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Now import from collector package
from collector.collector import NewsCollector
from collector.sources import (
    ArxivFetcher,
    HuggingFaceFetcher,
    ProductHuntFetcher,
    RedditFetcher,
    AINewsFetcher,
    CrescendoFetcher
)


def setup_logging(verbose: bool = False):
    """
    Configure logging for the application.
    
    Args:
        verbose: If True, set log level to DEBUG, otherwise INFO
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Eternal AI News Aggregator - Collect and organize AI news',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--date',
        type=str,
        default=None,
        help='Date for output file in YYYY-MM-DD format (default: today)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run collection without writing files (for testing)'
    )
    
    parser.add_argument(
        '--retention',
        type=int,
        default=7,
        help='Number of days to retain data files (default: 7)'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='data',
        help='Directory for storing JSON files (default: data)'
    )
    
    return parser.parse_args()


def main():
    """
    Main execution function.
    Orchestrates the entire news collection process.
    """
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Eternal AI News Aggregator - Starting Collection")
    logger.info("=" * 60)
    
    try:
        # Initialize collector
        collector = NewsCollector(data_dir=args.data_dir)
        logger.info(f"Initialized collector with data directory: {args.data_dir}")
        
        # Register all source fetchers
        logger.info("Registering source fetchers...")
        fetchers = [
            ArxivFetcher(),
            HuggingFaceFetcher(),
            ProductHuntFetcher(),
            RedditFetcher(),
            AINewsFetcher(),
            CrescendoFetcher()
        ]
        
        for fetcher in fetchers:
            collector.register_fetcher(fetcher)
        
        logger.info(f"Registered {len(fetchers)} source fetchers")
        
        # Collect from all sources
        logger.info("Starting collection from all sources...")
        result = collector.collect_all_sources()
        
        # Log collection summary
        logger.info("-" * 60)
        logger.info("Collection Summary:")
        logger.info(f"  Date: {result.date}")
        logger.info(f"  Total Sources: {result.collection_status['total_sources']}")
        logger.info(f"  Successful: {result.collection_status['successful']}")
        logger.info(f"  Failed: {result.collection_status['failed']}")
        logger.info(f"  Total Items: {result.collection_status['total_items']}")
        
        if result.collection_status['failed_sources']:
            logger.warning(f"  Failed Sources: {', '.join(result.collection_status['failed_sources'])}")
        
        # Log items per source
        logger.info("-" * 60)
        logger.info("Items per source:")
        for source_name, items in result.sources.items():
            logger.info(f"  {source_name}: {len(items)} items")
        
        logger.info("-" * 60)
        
        # Determine output date
        if args.date:
            output_date = args.date
            logger.info(f"Using specified date: {output_date}")
        else:
            output_date = result.date
            logger.info(f"Using current date: {output_date}")
        
        if not args.dry_run:
            # Generate JSON file for this date
            filename = f"{output_date}.json"
            filepath = collector.generate_json(result, filename)
            logger.info(f"Generated JSON file: {filepath}")
            
            # Create/update today.json
            collector.create_today_symlink(output_date)
            logger.info("Updated today.json")
            
            # Update index.json with available dates
            available_dates = collector.get_available_dates()
            index_path = collector.update_index(available_dates)
            logger.info(f"Updated index.json with {len(available_dates)} dates")
            
            # Cleanup old files
            logger.info(f"Cleaning up files older than {args.retention} days...")
            deleted_files = collector.cleanup_old_files(retention_days=args.retention)
            
            if deleted_files:
                logger.info(f"Deleted {len(deleted_files)} old files:")
                for deleted_file in deleted_files:
                    logger.info(f"  - {deleted_file}")
            else:
                logger.info("No old files to delete")
            
            # Final summary
            logger.info("=" * 60)
            logger.info("Collection Complete!")
            logger.info(f"  Output file: {filepath}")
            logger.info(f"  Total items collected: {result.collection_status['total_items']}")
            logger.info(f"  Available dates: {len(available_dates)}")
            logger.info("=" * 60)
            
        else:
            logger.info("DRY RUN - No files written")
            logger.info(f"Would have generated: {output_date}.json")
            logger.info(f"Total items: {result.collection_status['total_items']}")
        
        # Exit with success
        return 0
        
    except KeyboardInterrupt:
        logger.warning("Collection interrupted by user")
        return 130
        
    except Exception as e:
        logger.error(f"Collection failed with error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
