# Changelog

All notable changes to the Eternal AI News Aggregator project will be documented in this file.

## [Initial Release] - 2025-10-19

### Added
- Project structure and configuration files
- Python collector module infrastructure
- GitHub Actions workflow for automated collection
- Web application frontend (HTML/CSS/JS)
- GitHub Pages hosting configuration
- Android WebView integration support
- Comprehensive documentation (README.md)
- Support for 7 AI news sources:
  - arXiv cs.AI section
  - Hugging Face Blog
  - Product Hunt AI category
  - Reddit r/MachineLearning
  - Reddit r/ClaudeAI
  - ArtificialIntelligence-News.com
  - Crescendo AI News

### Features
- Twice-daily automated news collection (05:00 & 17:00 UTC)
- 7-day rolling data retention
- Normal mode (today's news) and Advanced mode (7-day history)
- Offline support with localStorage caching
- Mobile-responsive design
- Zero-cost operation on GitHub infrastructure

---

## [2025-10-19 14:30 UTC] - Project Setup

### Task 1: Set up project structure and configuration files

**Changes:**
- Created complete directory structure: /collector, /.github/workflows, /data, /webapp, /docs
- Created .gitignore with Python, IDE, and OS exclusions
- Created requirements.txt with dependencies: feedparser==6.0.11, requests==2.31.0, beautifulsoup4==4.12.3, lxml==5.1.0
- Created comprehensive README.md with setup instructions, architecture overview, and usage guide
- Created docs/Changelog.md for tracking project changes

**Files Created:**
- .gitignore
- requirements.txt
- README.md
- docs/Changelog.md
- collector/.gitkeep
- data/.gitkeep
- webapp/.gitkeep
- .github/workflows/.gitkeep

**Requirements Addressed:** 10.1, 10.2, 10.3

---

## [2025-10-19 15:00 UTC] - Base Collector Infrastructure

### Task 2: Implement base collector infrastructure

**Changes:**
- Created NewsItem and CollectionResult data models with serialization methods
- Implemented base SourceFetcher class with retry logic, timeout management, and error handling
- Created NewsCollector orchestrator class for managing multi-source collection
- Added deduplication logic based on title similarity
- Implemented JSON generation and file management utilities
- Added cleanup functionality for old files (7-day retention)
- Included AI-related content filtering and text cleaning utilities

**Files Created:**
- collector/models.py - Data models for NewsItem and CollectionResult
- collector/fetchers.py - Base SourceFetcher class with retry and error handling
- collector/collector.py - NewsCollector orchestrator class

**Key Features:**
- Exponential backoff retry strategy (3 attempts, 2-4-8 second delays)
- 30-second timeout per request
- Automatic deduplication using normalized title comparison
- Configurable retention period (default 7 days)
- Comprehensive logging for debugging and monitoring
- today.json automatic update mechanism

**Requirements Addressed:** 2.1, 2.2, 2.3, 2.4, 3.3, 3.4, 7.1, 7.2, 7.3, 7.4, 8.1, 8.2

---

## [2025-10-19 15:30 UTC] - Source-Specific Fetchers

### Task 3: Implement source-specific fetchers

**Changes:**
- Implemented 6 production-ready source fetchers with real scraping logic
- Each fetcher extends SourceFetcher base class with custom parsing
- All fetchers use retry logic, error handling, and timeout management
- No mock data - all fetchers retrieve real content from live sources

**Files Created:**
- collector/sources.py - All source-specific fetcher implementations

**Fetchers Implemented:**

1. **ArxivFetcher**
   - Fetches from arXiv cs.AI RSS feed (http://export.arxiv.org/rss/cs.AI)
   - Uses feedparser for RSS parsing
   - Extracts title, summary, link, published date
   - Limits to 20 most recent papers

2. **HuggingFaceFetcher**
   - Scrapes Hugging Face blog (https://huggingface.co/blog)
   - Uses BeautifulSoup for HTML parsing
   - Extracts blog post titles, descriptions, and links
   - Limits to 15 most recent posts

3. **ProductHuntFetcher**
   - Scrapes Product Hunt AI category (https://www.producthunt.com/topics/artificial-intelligence)
   - Uses BeautifulSoup with flexible selectors
   - Filters for AI-related products using keyword matching
   - Extracts product names, taglines, and links

4. **RedditFetcher**
   - Fetches from r/MachineLearning and r/ClaudeAI via RSS
   - Uses feedparser for multiple subreddit feeds
   - Cleans HTML content from post bodies
   - Prefixes titles with subreddit name for context
   - Limits to 10 posts per subreddit

5. **AINewsFetcher**
   - Scrapes ArtificialIntelligence-News.com
   - Uses BeautifulSoup with regex-based selectors
   - Extracts article titles, excerpts, and links
   - Handles relative URLs properly

6. **CrescendoFetcher**
   - Scrapes Crescendo AI News (https://crescendo.ai/news)
   - Uses BeautifulSoup for parsing
   - Extracts news titles, descriptions, and links
   - Flexible selector patterns for robustness

**Key Features:**
- All fetchers inherit retry logic and error handling from base class
- Text cleaning and summary truncation (250 chars max)
- ISO 8601 timestamp formatting
- Comprehensive logging for each source
- Graceful failure handling - one source failure doesn't stop others

**Requirements Addressed:** 1.2, 2.3

---

## [2025-10-19 16:00 UTC] - Main Collection Script

### Task 4: Implement main collection script

**Changes:**
- Created complete main execution script that orchestrates the entire collection process
- Integrated all source fetchers with the NewsCollector orchestrator
- Implemented comprehensive command-line interface with multiple options
- Added file cleanup logic for 7-day rolling retention
- Included detailed logging and error handling throughout

**Files Created:**
- collector/generate_news.py - Main executable script

**Key Features:**

1. **Main Script (generate_news.py)**
   - Instantiates NewsCollector and registers all 6 source fetchers
   - Executes collection from all sources in sequence
   - Generates YYYY-MM-DD.json file with collected data
   - Creates/updates today.json as copy of latest file
   - Updates index.json with list of available dates
   - Automatically cleans up files older than retention period

2. **Command-Line Interface**
   - `--date YYYY-MM-DD`: Specify custom date for output file
   - `--verbose, -v`: Enable DEBUG level logging
   - `--dry-run`: Test collection without writing files
   - `--retention DAYS`: Configure retention period (default: 7)
   - `--data-dir PATH`: Specify custom data directory

3. **File Cleanup Logic**
   - Identifies JSON files older than retention period
   - Deletes old files from /data/ directory
   - Updates index.json to reflect current available dates
   - Logs all cleanup operations

4. **Execution Flow**
   - Parse command-line arguments
   - Setup logging (INFO or DEBUG)
   - Initialize NewsCollector
   - Register all source fetchers
   - Collect from all sources (with error handling per source)
   - Generate dated JSON file
   - Update today.json and index.json
   - Cleanup old files
   - Display comprehensive summary

5. **Error Handling**
   - Graceful handling of KeyboardInterrupt
   - Comprehensive exception logging with stack traces
   - Appropriate exit codes (0=success, 1=error, 130=interrupted)
   - Per-source error isolation (one failure doesn't stop others)

**Usage Examples:**
```bash
# Normal execution
python collector/generate_news.py

# Verbose logging
python collector/generate_news.py --verbose

# Dry run (test without writing)
python collector/generate_news.py --dry-run

# Custom retention period
python collector/generate_news.py --retention 14

# Specify custom date
python collector/generate_news.py --date 2025-10-18
```

**Requirements Addressed:** 2.3, 2.4, 2.5, 3.3, 3.4, 7.5

---

## [2025-10-19 16:30 UTC] - Unit Tests

### Task 4.4: Write unit tests for collector module

**Changes:**
- Created comprehensive test suite using pytest framework
- All tests use real data from actual fetchers - NO MOCK DATA
- Tests verify functionality with live HTTP requests to real sources
- Added pytest configuration for test organization

**Files Created:**
- tests/__init__.py - Test package initialization
- tests/test_models.py - Tests for NewsItem and CollectionResult models
- tests/test_deduplication.py - Tests for deduplication logic
- tests/test_json_generation.py - Tests for JSON file operations with real data
- tests/test_fetchers.py - Integration tests for all 6 real fetchers
- pytest.ini - Pytest configuration

**Test Coverage:**

1. **test_models.py** (Unit Tests)
   - NewsItem creation, serialization, equality, hashing
   - Case-insensitive title comparison
   - CollectionResult creation and manipulation
   - Source item management
   - JSON serialization

2. **test_deduplication.py** (Unit Tests)
   - Exact duplicate removal
   - Case-insensitive deduplication
   - Whitespace normalization
   - Cross-source deduplication
   - Edge cases (empty lists, single items)

3. **test_json_generation.py** (Integration Tests with Real Data)
   - Uses real ArxivFetcher to get actual data
   - JSON file creation and structure validation
   - Index.json generation and management
   - File cleanup with 7-day retention
   - today.json creation
   - UTF-8 encoding verification
   - All tests use real collected data, not mocks

4. **test_fetchers.py** (Integration Tests with Live Sources)
   - Tests all 6 fetchers with real HTTP requests
   - ArxivFetcher: RSS feed parsing
   - HuggingFaceFetcher: Blog scraping
   - ProductHuntFetcher: Product scraping with AI filtering
   - RedditFetcher: Multiple subreddit RSS feeds
   - AINewsFetcher: News site scraping
   - CrescendoFetcher: News scraping
   - Error handling verification
   - NewsItem structure validation

**Key Features:**
- NO MOCK DATA - all tests use real sources
- Integration tests make actual HTTP requests
- Graceful handling of network failures
- Pytest markers for test categorization
- Comprehensive coverage of core functionality
- Tests verify real-world behavior

**Running Tests:**
```bash
# Run all tests
pytest

# Run only unit tests (fast)
pytest tests/test_models.py tests/test_deduplication.py

# Run integration tests (requires network)
pytest tests/test_fetchers.py tests/test_json_generation.py

# Verbose output
pytest -v

# With coverage
pytest --cov=collector
```

**Requirements Addressed:** 7.1, 7.2, 7.3

---

## [2025-10-19 17:00 UTC] - GitHub Actions Workflow

### Task 5: Create GitHub Actions workflow

**Changes:**
- Created complete GitHub Actions workflow for automated news collection
- Configured twice-daily execution at 05:00 and 17:00 UTC
- Implemented full CI/CD pipeline with real data collection
- Added git automation for committing and pushing collected data
- Included error handling and retry logic

**Files Created:**
- .github/workflows/auto-update.yml - Complete automation workflow

**Workflow Features:**

1. **Scheduled Execution**
   - Runs automatically at 05:00 UTC daily
   - Runs automatically at 17:00 UTC daily
   - Manual trigger available via workflow_dispatch

2. **Environment Setup**
   - Uses ubuntu-latest runner (free tier)
   - Python 3.11 with pip caching for faster builds
   - Installs all dependencies from requirements.txt

3. **Collection Process**
   - Executes `python collector/generate_news.py --verbose`
   - Collects real data from all 6 sources
   - Generates dated JSON files
   - Updates today.json and index.json
   - Cleans up files older than 7 days

4. **Git Automation**
   - Configures git with github-actions[bot] identity
   - Adds all changes in data/ directory
   - Creates commit with timestamp: "Auto-update: YYYY-MM-DD HH:MM UTC"
   - Pushes to main branch with 3-attempt retry logic
   - Skips commit if no changes detected

5. **Error Handling**
   - Fails workflow if collection fails (continue-on-error: false)
   - Creates error.log on failure with timestamp and run ID
   - Commits error log for debugging
   - Retry logic for git push operations (3 attempts with 5-second delays)

6. **Permissions**
   - contents: write - Required for committing and pushing changes
   - Minimal permissions for security

**Workflow Steps:**
1. Checkout repository (full history)
2. Set up Python 3.11 with pip cache
3. Install dependencies
4. Run news collector with verbose logging
5. Configure Git identity
6. Commit and push changes (with retry)
7. Create error log on failure (conditional)

**Usage:**
- Automatic: Runs twice daily on schedule
- Manual: Go to Actions tab → "Auto Update AI News" → "Run workflow"
- Monitor: Check Actions tab for execution logs

**Requirements Addressed:** 2.1, 2.2, 2.5, 5.1, 5.2, 5.5, 8.3, 8.4

---

## [2025-10-19 17:30 UTC] - Web Application Frontend

### Task 6: Build web application frontend

**Changes:**
- Created complete responsive web application with HTML, CSS, and JavaScript
- Implemented Normal and Advanced viewing modes
- Added real-time data fetching from JSON files (NO MOCK DATA)
- Integrated localStorage caching for offline support
- Built mobile-first responsive design

**Files Created:**
- webapp/index.html - Semantic HTML5 structure
- webapp/style.css - Complete responsive styling
- webapp/script.js - Full client-side functionality

**Key Features:**

1. **HTML Structure (index.html)**
   - Semantic HTML5 with proper accessibility
   - Header with logo, mode toggle, and refresh button
   - Advanced controls section with date selector
   - Status bar showing last updated time and offline indicator
   - Loading indicator and error message containers
   - News container for dynamic content
   - Footer with attribution

2. **CSS Styling (style.css)**
   - Mobile-first responsive design
   - CSS custom properties for theming
   - Color scheme: Light background (#f8f9fa), white cards, indigo accent (#6366f1)
   - Flexbox and Grid layouts
   - Smooth transitions and hover effects
   - Media queries for 480px, 768px breakpoints
   - Card-based news item design with shadows
   - Loading spinner animation

3. **JavaScript Functionality (script.js)**
   - Fetches real data from JSON files (today.json, date-specific, index.json)
   - NO MOCK DATA - all data comes from actual collector output
   - State management with AppState object
   - API functions: fetchTodayNews(), fetchDateNews(), fetchAvailableDates()
   - Rendering functions: renderNews(), renderSourceGroup(), createNewsCard()
   - localStorage caching with 12-hour expiry
   - Offline detection and handling
   - Mode switching (Normal/Advanced)
   - Date selector population and handling
   - Error handling with user-friendly messages
   - Automatic initialization on page load

4. **Normal Mode**
   - Displays today's news from today.json
   - Single-click refresh
   - Clean, focused interface

5. **Advanced Mode**
   - Date selector with last 7 days
   - Fetches specific date JSON files
   - Historical news browsing

6. **Offline Support**
   - Caches all fetched data in localStorage
   - 12-hour cache expiry
   - Automatic fallback to cache when offline
   - Offline indicator in UI
   - Works without internet after first load

7. **Responsive Design**
   - Mobile-first approach
   - Breakpoints: 480px, 768px, 1024px
   - Touch-friendly controls
   - Optimized for screens 320px - 1200px+
   - Grid layout adapts to screen size

8. **User Experience**
   - Loading indicators during fetch
   - Error messages with retry options
   - Smooth transitions and animations
   - Hover effects on interactive elements
   - Source-grouped news display
   - Formatted dates and timestamps
   - External links open in new tabs

**Data Flow:**
1. User opens page → Fetches today.json
2. Displays news grouped by source
3. Caches data in localStorage
4. User can switch to Advanced mode
5. Select date → Fetches specific date JSON
6. All data comes from real collector output

**Configuration:**
- API_BASE automatically detects localhost vs production
- Update `YOUR_USERNAME` in script.js after GitHub Pages deployment
- No build process required - pure HTML/CSS/JS

**Requirements Addressed:** 1.1, 1.3, 1.4, 1.5, 3.1, 3.2, 4.1, 4.2, 4.4, 6.1, 6.2, 6.3, 6.4, 6.5

---

## [2025-10-19 18:00 UTC] - GitHub Pages Configuration

### Task 7: Configure GitHub Pages hosting

**Changes:**
- Created comprehensive deployment documentation
- Added GitHub Pages configuration files
- Set up root redirect to webapp
- Configured for HTTPS and CORS compatibility

**Files Created:**
- docs/DEPLOYMENT.md - Complete deployment guide
- .nojekyll - Disables Jekyll processing
- index.html - Root redirect to webapp

**Deployment Guide Features:**

1. **Step-by-Step Instructions**
   - Push code to GitHub
   - Enable GitHub Pages
   - Configure Actions permissions
   - Update API configuration
   - Trigger first collection
   - Verify deployment

2. **GitHub Pages Setup**
   - Source: main branch, / (root) folder
   - HTTPS automatically enabled
   - No Jekyll processing (.nojekyll file)
   - Root index.html redirects to webapp/

3. **API Configuration**
   - script.js includes localhost detection
   - Production URL: https://YOUR_USERNAME.github.io/eternal/data
   - Automatic environment detection
   - No CORS issues (same-origin)

4. **Verification Steps**
   - Check web app loads
   - Verify JSON endpoints accessible
   - Test Normal and Advanced modes
   - Confirm automated updates work

5. **Troubleshooting Guide**
   - Workflow failures
   - No data showing
   - 404 errors
   - CORS errors
   - Solutions for common issues

6. **Monitoring**
   - Check Actions tab for workflow status
   - View commit history for data updates
   - Monitor GitHub Pages deployment

7. **Optional Features**
   - Custom domain setup
   - DNS configuration
   - Backup and restore procedures

**GitHub Pages Configuration:**
- Serves static files over HTTPS
- No build process required
- Automatic deployment on push
- Free tier: 100GB bandwidth/month
- Estimated usage: 1-2GB/month

**Data Endpoints:**
- Today's news: `/data/today.json`
- Index: `/data/index.json`
- Specific dates: `/data/YYYY-MM-DD.json`
- All served over HTTPS
- Public read-only access

**Security:**
- HTTPS enforced by GitHub Pages
- No API keys exposed
- Public repository (read-only data)
- GitHub Actions secrets protected
- CORS handled automatically (same-origin)

**Performance:**
- Static file serving (fast)
- CDN-backed by GitHub
- Gzip compression automatic
- Browser caching enabled
- Minimal bandwidth usage

**Next Steps for Users:**
1. Push code to GitHub
2. Enable GitHub Pages in Settings
3. Set Actions permissions to read/write
4. Update YOUR_USERNAME in script.js
5. Trigger first workflow run
6. Access at https://YOUR_USERNAME.github.io/eternal/

**Requirements Addressed:** 5.2, 5.3, 9.1, 9.3

---

## [2025-10-19 18:30 UTC] - Android WebView Integration

### Task 8: Create Android WebView integration

**Changes:**
- Created complete Android WebView wrapper for the web app
- Configured WebView with optimal settings for functionality
- Added offline support and caching
- Included comprehensive setup documentation

**Files Created:**
- android/AndroidManifest.xml - App manifest with permissions
- android/MainActivity.java - Main activity with WebView configuration
- android/activity_main.xml - Layout file
- android/build.gradle - Build configuration
- android/strings.xml - String resources
- android/README.md - Complete setup and build guide

**Android App Features:**

1. **WebView Configuration**
   - JavaScript enabled (required for app)
   - DOM storage enabled (localStorage support)
   - Database storage enabled
   - Caching enabled for offline support
   - Zoom controls (hidden UI)
   - Responsive layout support
   - Mixed content compatibility

2. **Offline Support**
   - Automatic caching of web app and data
   - Works offline after first load
   - Network status detection
   - Falls back to cache when offline
   - localStorage persistence

3. **Navigation**
   - Back button navigates WebView history
   - Stays within app (no external browser)
   - Handles URL loading internally
   - Graceful error handling

4. **Lifecycle Management**
   - Pauses WebView when backgrounded
   - Resumes WebView when app returns
   - Cleans up resources on destroy
   - Handles configuration changes

5. **Permissions**
   - INTERNET - Required for loading web app
   - ACCESS_NETWORK_STATE - For offline detection

**Setup Process:**
1. Create new Android Studio project
2. Copy provided files to project
3. Update GitHub Pages URL in MainActivity
4. Build and run on device/emulator

**Build Options:**
- Debug APK for testing
- Release APK for distribution
- Google Play Store ready
- Direct APK distribution supported

**Testing Checklist:**
- App launches and loads web app
- All web app features work
- Offline mode functions correctly
- localStorage persists data
- Back button navigation works
- Rotation handled properly

**Key Implementation:**
```java
// WebView loads real GitHub Pages URL
private static final String WEB_APP_URL = "https://johnwikcke.github.io/Eternal/";

// Full WebView configuration
webSettings.setJavaScriptEnabled(true);
webSettings.setDomStorageEnabled(true);
webSettings.setCacheMode(WebSettings.LOAD_DEFAULT);
```

**Distribution:**
- Google Play Store submission ready
- Direct APK distribution supported
- Auto-updates from GitHub Pages (no app update needed for content)

**Requirements Addressed:** 4.1, 4.2, 4.3

---

## Update Log Format

Future updates will follow this format:

**[Date] - [Component]**
- Description of changes
- Files modified
- Requirements addressed
