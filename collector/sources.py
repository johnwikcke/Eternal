"""
Source-specific fetcher implementations for AI news aggregation.
Each fetcher handles a specific source with custom parsing logic.
"""

import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from typing import List
import logging
import re

from collector.fetchers import SourceFetcher
from collector.models import NewsItem


logger = logging.getLogger(__name__)


class ArxivFetcher(SourceFetcher):
    """
    Fetches AI research papers from arXiv cs.AI section via RSS feed.
    """
    
    RSS_URL = "http://export.arxiv.org/rss/cs.AI"
    
    def __init__(self):
        super().__init__("arxiv")
    
    def fetch(self) -> List[NewsItem]:
        """
        Fetch latest papers from arXiv cs.AI RSS feed.
        
        Returns:
            List of NewsItem objects for recent papers
        """
        logger.info(f"Fetching from {self.RSS_URL}")
        
        # Parse RSS feed
        feed = feedparser.parse(self.RSS_URL)
        
        if not feed.entries:
            logger.warning("No entries found in arXiv feed")
            return []
        
        items = []
        
        for entry in feed.entries[:20]:  # Limit to 20 most recent
            try:
                # Extract data
                title = self.clean_text(entry.get('title', ''))
                summary = self.clean_text(entry.get('summary', ''))
                link = entry.get('link', '')
                
                # Parse published date
                published = entry.get('published', '')
                if published:
                    try:
                        dt = datetime.strptime(published, '%Y-%m-%dT%H:%M:%SZ')
                        published = dt.isoformat()
                    except:
                        published = datetime.now(timezone.utc).isoformat()
                else:
                    published = datetime.now(timezone.utc).isoformat()
                
                # Truncate summary
                summary = self.truncate_summary(summary, 250)
                
                if title and link:
                    item = NewsItem(
                        title=title,
                        summary=summary,
                        link=link,
                        published=published,
                        source=self.source_name
                    )
                    items.append(item)
                    
            except Exception as e:
                logger.warning(f"Failed to parse arXiv entry: {str(e)}")
                continue
        
        logger.info(f"Parsed {len(items)} items from arXiv")
        return items


class HuggingFaceFetcher(SourceFetcher):
    """
    Fetches blog posts from Hugging Face blog.
    """
    
    BLOG_URL = "https://huggingface.co/blog"
    
    def __init__(self):
        super().__init__("huggingface")
    
    def fetch(self) -> List[NewsItem]:
        """
        Scrape latest blog posts from Hugging Face.
        
        Returns:
            List of NewsItem objects for blog posts
        """
        logger.info(f"Fetching from {self.BLOG_URL}")
        
        response = self.session.get(self.BLOG_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = []
        
        # Find blog post articles
        articles = soup.find_all('article', limit=15)
        
        if not articles:
            # Try alternative selectors
            articles = soup.find_all('div', class_=re.compile(r'blog|post|article'), limit=15)
        
        for article in articles:
            try:
                # Find title
                title_elem = article.find(['h2', 'h3', 'h4'])
                if not title_elem:
                    continue
                
                title = self.clean_text(title_elem.get_text())
                
                # Find link
                link_elem = article.find('a', href=True)
                if not link_elem:
                    continue
                
                link = link_elem['href']
                if link.startswith('/'):
                    link = f"https://huggingface.co{link}"
                
                # Find summary/description
                summary_elem = article.find(['p', 'div'], class_=re.compile(r'description|summary|excerpt'))
                if summary_elem:
                    summary = self.clean_text(summary_elem.get_text())
                else:
                    # Get first paragraph
                    p_elem = article.find('p')
                    summary = self.clean_text(p_elem.get_text()) if p_elem else title
                
                summary = self.truncate_summary(summary, 250)
                
                # Use current time as published date
                published = datetime.now(timezone.utc).isoformat()
                
                if title and link:
                    item = NewsItem(
                        title=title,
                        summary=summary,
                        link=link,
                        published=published,
                        source=self.source_name
                    )
                    items.append(item)
                    
            except Exception as e:
                logger.warning(f"Failed to parse Hugging Face article: {str(e)}")
                continue
        
        logger.info(f"Parsed {len(items)} items from Hugging Face")
        return items


class ProductHuntFetcher(SourceFetcher):
    """
    Fetches AI products from Product Hunt AI category.
    """
    
    CATEGORY_URL = "https://www.producthunt.com/topics/artificial-intelligence"
    
    def __init__(self):
        super().__init__("producthunt")
    
    def fetch(self) -> List[NewsItem]:
        """
        Scrape AI products from Product Hunt.
        
        Returns:
            List of NewsItem objects for AI products
        """
        logger.info(f"Fetching from {self.CATEGORY_URL}")
        
        response = self.session.get(self.CATEGORY_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = []
        
        # Find product listings
        products = soup.find_all(['article', 'div'], attrs={'data-test': re.compile(r'post|product')}, limit=15)
        
        if not products:
            # Try alternative selectors
            products = soup.find_all(['div', 'article'], class_=re.compile(r'post|product|item'), limit=15)
        
        for product in products:
            try:
                # Find title/name
                title_elem = product.find(['h2', 'h3', 'a'], class_=re.compile(r'name|title'))
                if not title_elem:
                    title_elem = product.find(['h2', 'h3'])
                
                if not title_elem:
                    continue
                
                title = self.clean_text(title_elem.get_text())
                
                # Find link
                link_elem = product.find('a', href=re.compile(r'/posts/'))
                if not link_elem:
                    link_elem = product.find('a', href=True)
                
                if not link_elem:
                    continue
                
                link = link_elem['href']
                if link.startswith('/'):
                    link = f"https://www.producthunt.com{link}"
                
                # Find tagline/description
                desc_elem = product.find(['p', 'div'], class_=re.compile(r'tagline|description'))
                if desc_elem:
                    summary = self.clean_text(desc_elem.get_text())
                else:
                    summary = f"New AI product on Product Hunt: {title}"
                
                summary = self.truncate_summary(summary, 200)
                
                published = datetime.now(timezone.utc).isoformat()
                
                if title and link and self.is_ai_related(title + ' ' + summary):
                    item = NewsItem(
                        title=title,
                        summary=summary,
                        link=link,
                        published=published,
                        source=self.source_name
                    )
                    items.append(item)
                    
            except Exception as e:
                logger.warning(f"Failed to parse Product Hunt item: {str(e)}")
                continue
        
        logger.info(f"Parsed {len(items)} items from Product Hunt")
        return items


class RedditFetcher(SourceFetcher):
    """
    Fetches posts from Reddit AI-related subreddits via RSS.
    """
    
    SUBREDDITS = {
        'machinelearning': 'https://www.reddit.com/r/MachineLearning/.rss',
        'claudeai': 'https://www.reddit.com/r/ClaudeAI/.rss'
    }
    
    def __init__(self):
        super().__init__("reddit")
    
    def fetch(self) -> List[NewsItem]:
        """
        Fetch posts from multiple AI-related subreddits.
        
        Returns:
            List of NewsItem objects for Reddit posts
        """
        all_items = []
        
        for subreddit_name, rss_url in self.SUBREDDITS.items():
            try:
                logger.info(f"Fetching from r/{subreddit_name}")
                
                feed = feedparser.parse(rss_url)
                
                if not feed.entries:
                    logger.warning(f"No entries found in r/{subreddit_name}")
                    continue
                
                for entry in feed.entries[:10]:  # Limit per subreddit
                    try:
                        title = self.clean_text(entry.get('title', ''))
                        
                        # Get content or summary
                        content = entry.get('content', [{}])[0].get('value', '')
                        if not content:
                            content = entry.get('summary', '')
                        
                        # Clean HTML from content
                        if content:
                            soup = BeautifulSoup(content, 'html.parser')
                            summary = self.clean_text(soup.get_text())
                        else:
                            summary = title
                        
                        summary = self.truncate_summary(summary, 250)
                        
                        link = entry.get('link', '')
                        
                        # Parse published date
                        published = entry.get('published', '')
                        if published:
                            try:
                                dt = datetime.strptime(published, '%Y-%m-%dT%H:%M:%S%z')
                                published = dt.isoformat()
                            except:
                                published = datetime.now(timezone.utc).isoformat()
                        else:
                            published = datetime.now(timezone.utc).isoformat()
                        
                        if title and link:
                            item = NewsItem(
                                title=f"[r/{subreddit_name}] {title}",
                                summary=summary,
                                link=link,
                                published=published,
                                source=self.source_name
                            )
                            all_items.append(item)
                            
                    except Exception as e:
                        logger.warning(f"Failed to parse Reddit entry: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.error(f"Failed to fetch from r/{subreddit_name}: {str(e)}")
                continue
        
        logger.info(f"Parsed {len(all_items)} items from Reddit")
        return all_items


class AINewsFetcher(SourceFetcher):
    """
    Fetches articles from ArtificialIntelligence-News.com.
    """
    
    BASE_URL = "https://www.artificialintelligence-news.com"
    
    def __init__(self):
        super().__init__("ai_news")
    
    def fetch(self) -> List[NewsItem]:
        """
        Scrape latest articles from AI News website.
        
        Returns:
            List of NewsItem objects for articles
        """
        logger.info(f"Fetching from {self.BASE_URL}")
        
        response = self.session.get(self.BASE_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = []
        
        # Find article elements
        articles = soup.find_all(['article', 'div'], class_=re.compile(r'post|article|entry'), limit=15)
        
        for article in articles:
            try:
                # Find title
                title_elem = article.find(['h1', 'h2', 'h3'], class_=re.compile(r'title|headline'))
                if not title_elem:
                    title_elem = article.find(['h1', 'h2', 'h3'])
                
                if not title_elem:
                    continue
                
                title = self.clean_text(title_elem.get_text())
                
                # Find link
                link_elem = title_elem.find('a', href=True)
                if not link_elem:
                    link_elem = article.find('a', href=True)
                
                if not link_elem:
                    continue
                
                link = link_elem['href']
                if link.startswith('/'):
                    link = f"{self.BASE_URL}{link}"
                
                # Find excerpt/summary
                summary_elem = article.find(['p', 'div'], class_=re.compile(r'excerpt|summary|description'))
                if summary_elem:
                    summary = self.clean_text(summary_elem.get_text())
                else:
                    p_elem = article.find('p')
                    summary = self.clean_text(p_elem.get_text()) if p_elem else title
                
                summary = self.truncate_summary(summary, 250)
                
                published = datetime.now(timezone.utc).isoformat()
                
                if title and link:
                    item = NewsItem(
                        title=title,
                        summary=summary,
                        link=link,
                        published=published,
                        source=self.source_name
                    )
                    items.append(item)
                    
            except Exception as e:
                logger.warning(f"Failed to parse AI News article: {str(e)}")
                continue
        
        logger.info(f"Parsed {len(items)} items from AI News")
        return items


class CrescendoFetcher(SourceFetcher):
    """
    Fetches news from Crescendo AI News.
    """
    
    BASE_URL = "https://crescendo.ai/news"
    
    def __init__(self):
        super().__init__("crescendo")
    
    def fetch(self) -> List[NewsItem]:
        """
        Scrape latest news from Crescendo AI.
        
        Returns:
            List of NewsItem objects for news articles
        """
        logger.info(f"Fetching from {self.BASE_URL}")
        
        response = self.session.get(self.BASE_URL, timeout=self.TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = []
        
        # Find news items
        news_items = soup.find_all(['article', 'div'], class_=re.compile(r'news|post|item|card'), limit=15)
        
        for news_item in news_items:
            try:
                # Find title
                title_elem = news_item.find(['h1', 'h2', 'h3', 'h4'])
                if not title_elem:
                    continue
                
                title = self.clean_text(title_elem.get_text())
                
                # Find link
                link_elem = news_item.find('a', href=True)
                if not link_elem:
                    continue
                
                link = link_elem['href']
                if link.startswith('/'):
                    link = f"https://crescendo.ai{link}"
                
                # Find description
                desc_elem = news_item.find(['p', 'div'], class_=re.compile(r'description|summary|excerpt'))
                if desc_elem:
                    summary = self.clean_text(desc_elem.get_text())
                else:
                    p_elem = news_item.find('p')
                    summary = self.clean_text(p_elem.get_text()) if p_elem else title
                
                summary = self.truncate_summary(summary, 250)
                
                published = datetime.now(timezone.utc).isoformat()
                
                if title and link:
                    item = NewsItem(
                        title=title,
                        summary=summary,
                        link=link,
                        published=published,
                        source=self.source_name
                    )
                    items.append(item)
                    
            except Exception as e:
                logger.warning(f"Failed to parse Crescendo item: {str(e)}")
                continue
        
        logger.info(f"Parsed {len(items)} items from Crescendo")
        return items
