# Design Document

## Overview

Eternal is architected as a serverless, event-driven news aggregation system leveraging GitHub's free infrastructure. The design follows a pipeline architecture: scheduled collection → structured storage → static hosting → client-side rendering. All components are stateless and idempotent, ensuring reliability and zero operational cost.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions (Scheduler)               │
│  Triggers: 05:00 UTC, 17:00 UTC                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Collector Module (Python)                       │
│  - Fetch from 7+ sources                                     │
│  - Parse & deduplicate                                       │
│  - Generate JSON                                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Store (GitHub Repository)                  │
│  /data/YYYY-MM-DD.json (7-day rolling window)               │
│  /data/index.json (date manifest)                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              GitHub Pages (Static Hosting)                   │
│  HTTPS endpoint for JSON + Web App                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Web Application (HTML/CSS/JS)                   │
│  - Normal Mode (today)                                       │
│  - Advanced Mode (7-day history)                            │
│  - localStorage caching                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Android WebView (Optional)                      │
│  Loads hosted Web Application                               │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **Scheduled Trigger**: GitHub Actions cron triggers at specified UTC times
2. **Collection Phase**: Python script fetches from all sources in parallel
3. **Processing Phase**: Deduplicate, filter, and structure data
4. **Storage Phase**: Write JSON to /data/, update index.json, commit to repo
5. **Cleanup Phase**: Delete files older than 7 days
6. **Hosting Phase**: GitHub Pages automatically serves updated files
7. **Client Phase**: Web app fetches JSON and renders UI
8. **Caching Phase**: localStorage stores data for offline access

## Components and Interfaces

### 1. Collector Module (`/collector/generate_news.py`)

**Purpose**: Fetch, parse, and structure AI news from multiple sources

**Key Classes/Functions**:

```python
class NewsCollector:
    """Main orchestrator for news collection"""
    
    def __init__(self):
        self.sources = []
        self.collected_items = []
    
    def collect_all_sources(self) -> dict:
        """Execute collection from all configured sources"""
        pass
    
    def deduplicate(self, items: list) -> list:
        """Remove duplicate news items by title similarity"""
        pass
    
    def generate_json(self, data: dict, filename: str) -> None:
        """Write structured JSON to /data/ directory"""
        pass

class SourceFetcher:
    """Base class for source-specific fetchers"""
    
    def fetch(self) -> list:
        """Fetch and parse content from source"""
        pass
    
    def parse(self, raw_content) -> list:
        """Convert raw content to structured format"""
        pass

# Specific implementations
class ArxivFetcher(SourceFetcher):
    """Fetch from arXiv cs.AI RSS feed"""
    RSS_URL = "http://export.arxiv.org/rss/cs.AI"

class HuggingFaceFetcher(SourceFetcher):
    """Scrape Hugging Face blog"""
    BLOG_URL = "https://huggingface.co/blog"

class ProductHuntFetcher(SourceFetcher):
    """Fetch from Product Hunt AI category"""
    API_URL = "https://www.producthunt.com/topics/artificial-intelligence"

class RedditFetcher(SourceFetcher):
    """Fetch from Reddit subreddits via RSS"""
    SUBREDDITS = ["MachineLearning", "ClaudeAI"]

class AINewsFetcher(SourceFetcher):
    """Scrape ArtificialIntelligence-News.com"""
    BASE_URL = "https://www.artificialintelligence-news.com"

class CrescendoFetcher(SourceFetcher):
    """Scrape Crescendo AI News"""
    BASE_URL = "https://crescendo.ai/news"
```

**Dependencies**:
- `feedparser`: RSS/Atom feed parsing
- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `json`: JSON serialization
- `datetime`: Timestamp generation
- `os`: File system operations

**Error Handling Strategy**:
- Each fetcher wrapped in try-except block
- Failed sources logged but don't halt execution
- Partial results still written to JSON
- Error summary included in output metadata

### 2. GitHub Actions Workflow (`/.github/workflows/auto-update.yml`)

**Purpose**: Automate collection execution and repository updates

**Workflow Structure**:

```yaml
name: Auto Update AI News
on:
  schedule:
    - cron: '0 5 * * *'   # 05:00 UTC
    - cron: '0 17 * * *'  # 17:00 UTC
  workflow_dispatch:       # Manual trigger option

jobs:
  collect-and-publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
      - name: Setup Python 3.11
      - name: Install dependencies
      - name: Run collector
      - name: Cleanup old files
      - name: Commit and push changes
```

**Configuration**:
- Runner: `ubuntu-latest` (free tier)
- Python version: 3.11
- Git identity: `github-actions[bot]`
- Commit message format: `"Auto-update: YYYY-MM-DD HH:MM UTC"`

**Permissions Required**:
- `contents: write` (for committing files)
- `pages: write` (for GitHub Pages deployment)

### 3. Data Store Structure

**File Organization**:

```
/data/
├── 2025-10-19.json
├── 2025-10-18.json
├── 2025-10-17.json
├── 2025-10-16.json
├── 2025-10-15.json
├── 2025-10-14.json
├── 2025-10-13.json
├── index.json
└── today.json (symlink or copy of latest)
```

**JSON Schema for Daily Files** (`YYYY-MM-DD.json`):

```json
{
  "date": "2025-10-19",
  "last_updated": "2025-10-19T17:05:32Z",
  "collection_status": {
    "total_sources": 7,
    "successful": 6,
    "failed": ["crescendo"],
    "total_items": 42
  },
  "sources": {
    "arxiv": [
      {
        "title": "Novel Approach to Transformer Optimization",
        "summary": "Researchers propose a new method...",
        "link": "https://arxiv.org/abs/2025.12345",
        "published": "2025-10-19T10:30:00Z"
      }
    ],
    "huggingface": [...],
    "producthunt": [...],
    "reddit_machinelearning": [...],
    "reddit_claudeai": [...],
    "ai_news": [...],
    "crescendo": []
  }
}
```

**Index File Schema** (`index.json`):

```json
{
  "last_updated": "2025-10-19T17:05:32Z",
  "available_dates": [
    "2025-10-19",
    "2025-10-18",
    "2025-10-17",
    "2025-10-16",
    "2025-10-15",
    "2025-10-14",
    "2025-10-13"
  ],
  "total_days": 7
}
```

### 4. Web Application (`/webapp/`)

**File Structure**:
```
/webapp/
├── index.html
├── style.css
├── script.js
└── assets/
    └── logo.svg (optional)
```

**HTML Structure** (`index.html`):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eternal - AI News Aggregator</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="logo">Eternal</div>
        <div class="controls">
            <button id="normalMode" class="active">Normal</button>
            <button id="advancedMode">Advanced</button>
            <button id="refreshBtn">↻ Refresh</button>
        </div>
    </header>
    
    <main>
        <div id="advancedControls" class="hidden">
            <label for="dateSelector">Select Date:</label>
            <select id="dateSelector"></select>
        </div>
        
        <div id="statusBar">
            <span id="lastUpdated"></span>
            <span id="offlineIndicator" class="hidden">Offline Mode</span>
        </div>
        
        <div id="newsContainer">
            <!-- Dynamically populated -->
        </div>
        
        <div id="errorMessage" class="hidden"></div>
    </main>
    
    <footer>
        <p>Powered by GitHub Actions • Updated twice daily</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>
```

**CSS Design Principles** (`style.css`):

- **Color Scheme**: Light theme with pastel accents
  - Background: `#f8f9fa`
  - Cards: `#ffffff`
  - Primary accent: `#6366f1` (indigo)
  - Text: `#1f2937`
  
- **Typography**:
  - Font family: System fonts (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto`)
  - Base size: 16px
  - Headings: 1.5rem - 2rem
  
- **Layout**:
  - Mobile-first responsive design
  - Breakpoints: 640px (sm), 768px (md), 1024px (lg)
  - Max content width: 1200px
  - Grid system for news cards
  
- **Components**:
  - Rounded corners: 8px
  - Box shadows: Subtle elevation
  - Smooth transitions: 200ms ease
  - Button hover states

**JavaScript Architecture** (`script.js`):

```javascript
// State management
const AppState = {
    mode: 'normal',
    currentDate: null,
    cachedData: null,
    isOnline: navigator.onLine
};

// API endpoints
const API_BASE = 'https://USERNAME.github.io/eternal/data';

// Core functions
async function fetchTodayNews() { }
async function fetchDateNews(date) { }
async function fetchAvailableDates() { }
function renderNews(data) { }
function renderSourceGroup(sourceName, items) { }
function cacheData(key, data) { }
function getCachedData(key) { }
function showError(message) { }
function updateLastUpdatedTime(timestamp) { }

// Event listeners
document.getElementById('normalMode').addEventListener('click', switchToNormal);
document.getElementById('advancedMode').addEventListener('click', switchToAdvanced);
document.getElementById('refreshBtn').addEventListener('click', refreshNews);
document.getElementById('dateSelector').addEventListener('change', onDateChange);

// Initialization
window.addEventListener('load', init);
window.addEventListener('online', handleOnline);
window.addEventListener('offline', handleOffline);
```

**Caching Strategy**:
- Use `localStorage` for persistence
- Cache keys: `eternal_today`, `eternal_index`, `eternal_date_YYYY-MM-DD`
- Cache expiry: 12 hours
- Fallback to cache when offline or fetch fails

### 5. Android WebView Integration

**Minimal Android Code** (Java):

```java
public class MainActivity extends AppCompatActivity {
    private WebView webView;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        webView = findViewById(R.id.webview);
        WebSettings webSettings = webView.getSettings();
        
        // Enable JavaScript
        webSettings.setJavaScriptEnabled(true);
        
        // Enable DOM storage for localStorage
        webSettings.setDomStorageEnabled(true);
        
        // Enable caching
        webSettings.setCacheMode(WebSettings.LOAD_DEFAULT);
        
        // Load the hosted page
        webView.loadUrl("https://USERNAME.github.io/eternal/");
    }
}
```

**Layout XML** (`activity_main.xml`):

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    
    <WebView
        android:id="@+id/webview"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />
</LinearLayout>
```

**Required Permissions** (`AndroidManifest.xml`):

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

## Data Models

### NewsItem

```python
@dataclass
class NewsItem:
    title: str
    summary: str
    link: str
    published: str  # ISO 8601 format
    source: str
    
    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'summary': self.summary,
            'link': self.link,
            'published': self.published
        }
```

### CollectionResult

```python
@dataclass
class CollectionResult:
    date: str
    last_updated: str
    collection_status: dict
    sources: dict[str, list[NewsItem]]
    
    def to_json(self) -> str:
        return json.dumps({
            'date': self.date,
            'last_updated': self.last_updated,
            'collection_status': self.collection_status,
            'sources': {
                source: [item.to_dict() for item in items]
                for source, items in self.sources.items()
            }
        }, indent=2)
```

## Error Handling

### Collector Module Error Handling

1. **Network Errors**:
   - Retry failed requests up to 3 times with exponential backoff
   - Timeout: 30 seconds per request
   - Log failed sources but continue execution

2. **Parsing Errors**:
   - Skip malformed items
   - Log parsing errors with source context
   - Continue processing remaining items

3. **File System Errors**:
   - Ensure /data/ directory exists before writing
   - Handle permission errors gracefully
   - Validate JSON before writing

### GitHub Actions Error Handling

1. **Collection Failures**:
   - Exit code 0 even if some sources fail (partial success)
   - Exit code 1 only if no data collected at all
   - Create error log file for debugging

2. **Git Operation Failures**:
   - Retry push operations up to 3 times
   - Handle merge conflicts (should not occur with automated commits)
   - Send notification on persistent failures

### Web Application Error Handling

1. **Fetch Failures**:
   - Display user-friendly error message
   - Fall back to cached data if available
   - Show offline indicator

2. **Parsing Errors**:
   - Validate JSON structure before rendering
   - Display partial data if some sources are valid
   - Log errors to console for debugging

3. **Rendering Errors**:
   - Catch and log JavaScript errors
   - Prevent page crash
   - Display error boundary message

## Testing Strategy

### Unit Testing (Python)

**Test Coverage**:
- Each SourceFetcher class
- Deduplication logic
- JSON generation
- Date handling and cleanup logic

**Framework**: `pytest`

**Test Structure**:
```python
# tests/test_collectors.py
def test_arxiv_fetcher_parses_rss():
    fetcher = ArxivFetcher()
    items = fetcher.fetch()
    assert len(items) > 0
    assert all('title' in item for item in items)

def test_deduplication_removes_similar_titles():
    collector = NewsCollector()
    items = [
        {'title': 'New AI Model Released', ...},
        {'title': 'New AI Model Released', ...},
        {'title': 'Different News', ...}
    ]
    result = collector.deduplicate(items)
    assert len(result) == 2

# tests/test_json_generation.py
def test_json_output_structure():
    collector = NewsCollector()
    data = collector.collect_all_sources()
    assert 'date' in data
    assert 'sources' in data
    assert isinstance(data['sources'], dict)
```

### Integration Testing

**GitHub Actions Testing**:
- Use `workflow_dispatch` for manual test runs
- Verify JSON files created correctly
- Verify old files deleted
- Verify commits pushed successfully

**End-to-End Testing**:
- Test complete flow from collection to display
- Verify data appears in web app within 5 minutes of collection
- Test both Normal and Advanced modes

### Frontend Testing

**Manual Testing Checklist**:
- [ ] Normal mode displays today's news
- [ ] Advanced mode shows date selector
- [ ] Date selector populated with 7 dates
- [ ] Selecting date loads correct data
- [ ] Refresh button updates display
- [ ] Offline mode shows cached data
- [ ] Mobile responsive (320px - 768px)
- [ ] WebView compatibility

**Browser Testing**:
- Chrome/Edge (Chromium)
- Firefox
- Safari (iOS)
- Android WebView

### Performance Testing

**Metrics to Monitor**:
- Collection time: < 10 minutes per run
- JSON file size: < 500KB per day
- Page load time: < 2 seconds on 3G
- Time to interactive: < 3 seconds

**Optimization Strategies**:
- Parallel source fetching
- Minimize JSON payload (remove unnecessary fields)
- Compress responses (gzip)
- Lazy load images if added later

## Security Considerations

### Data Integrity

- All data served over HTTPS
- GitHub Pages provides SSL certificates automatically
- Repository branch protection prevents unauthorized commits

### API Key Management

- Store any required API keys in GitHub Secrets
- Never log or expose keys in output
- Use environment variables in Python script

### Content Security

- Sanitize scraped content before storing
- Validate URLs before including in JSON
- Prevent XSS by escaping HTML in web app

### Access Control

- Repository: Public read, protected write
- GitHub Actions: Restricted to repository maintainers
- No user authentication required (read-only public service)

## Deployment Strategy

### Initial Setup

1. Create GitHub repository
2. Enable GitHub Pages (source: main branch, /webapp folder)
3. Configure GitHub Actions permissions
4. Add any required secrets
5. Run initial collection manually
6. Verify web app loads correctly

### Continuous Deployment

- Every commit to main branch triggers GitHub Pages rebuild
- Changes to workflow file require manual approval
- JSON updates happen automatically twice daily

### Rollback Strategy

- Git revert for code issues
- Manual workflow run to regenerate data
- GitHub Pages serves previous version until new build completes

## Monitoring and Maintenance

### Monitoring

- GitHub Actions run history (success/failure status)
- Repository commit log (data update frequency)
- Manual spot-checks of web app

### Maintenance Tasks

- Monthly: Review and update source URLs
- Quarterly: Update Python dependencies
- As needed: Add new sources or remove defunct ones
- As needed: Update Changelog.md with all modifications

### Scaling Considerations

- Current design supports up to 100 items per source
- If data grows beyond 500KB per day, implement pagination
- If collection time exceeds 10 minutes, optimize or parallelize further
- GitHub Actions free tier: 2000 minutes/month (sufficient for twice-daily 10-minute runs)
