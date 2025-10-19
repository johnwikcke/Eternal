# Implementation Plan

- [x] 1. Set up project structure and configuration files



  - Create directory structure: /collector, /.github/workflows, /data, /webapp, /docs
  - Create .gitignore file to exclude Python cache and temporary files
  - Create requirements.txt with dependencies: feedparser, requests, beautifulsoup4
  - Create README.md with project overview and setup instructions
  - _Requirements: 10.1, 10.3_

- [x] 2. Implement base collector infrastructure



  - _Requirements: 2.1, 2.2, 2.3, 8.1, 8.2_


- [x] 2.1 Create NewsItem and CollectionResult data models

  - Write NewsItem dataclass with fields: title, summary, link, published, source
  - Write CollectionResult dataclass with fields: date, last_updated, collection_status, sources
  - Implement to_dict() and to_json() methods for serialization
  - _Requirements: 2.4_

- [x] 2.2 Create base SourceFetcher class


  - Implement abstract SourceFetcher class with fetch() and parse() methods
  - Add error handling wrapper with try-except and logging
  - Implement timeout configuration (30 seconds default)
  - Add retry logic with exponential backoff (3 attempts)
  - _Requirements: 8.1, 8.2_

- [x] 2.3 Create NewsCollector orchestrator class


  - Implement NewsCollector class with collect_all_sources() method
  - Write deduplicate() method using title similarity comparison
  - Implement generate_json() method to write structured output to /data/
  - Add logging for collection status and errors
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 3. Implement source-specific fetchers



  - _Requirements: 1.2, 2.3_


- [x] 3.1 Implement ArxivFetcher

  - Create ArxivFetcher class extending SourceFetcher
  - Use feedparser to fetch RSS from http://export.arxiv.org/rss/cs.AI
  - Parse entries to extract title, summary, link, published date
  - _Requirements: 1.2_

- [x] 3.2 Implement HuggingFaceFetcher

  - Create HuggingFaceFetcher class extending SourceFetcher
  - Use requests and BeautifulSoup to scrape https://huggingface.co/blog
  - Extract blog post titles, summaries, and links
  - _Requirements: 1.2_


- [x] 3.3 Implement ProductHuntFetcher

  - Create ProductHuntFetcher class extending SourceFetcher
  - Scrape Product Hunt AI category page
  - Extract product names, descriptions, and links
  - _Requirements: 1.2_

- [x] 3.4 Implement RedditFetcher

  - Create RedditFetcher class extending SourceFetcher
  - Use feedparser to fetch RSS from r/MachineLearning and r/ClaudeAI
  - Parse Reddit posts to extract title, selftext, and permalink
  - _Requirements: 1.2_



- [x] 3.5 Implement AINewsFetcher

  - Create AINewsFetcher class extending SourceFetcher
  - Scrape https://www.artificialintelligence-news.com
  - Extract article titles, summaries, and links
  - _Requirements: 1.2_




- [x] 3.6 Implement CrescendoFetcher
  - Create CrescendoFetcher class extending SourceFetcher
  - Scrape https://crescendo.ai/news
  - Extract news titles, summaries, and links
  - _Requirements: 1.2_

- [x] 4. Implement main collection script



  - _Requirements: 2.3, 2.4, 2.5, 3.3, 3.4, 7.5_

- [x] 4.1 Create generate_news.py main script


  - Instantiate NewsCollector and all source fetchers
  - Execute collection from all sources
  - Generate YYYY-MM-DD.json file with current date
  - Create/update index.json with available dates list
  - Create/update today.json as copy of latest file
  - _Requirements: 2.4, 3.3, 3.4_

- [x] 4.2 Implement file cleanup logic

  - Write function to identify JSON files older than 7 days
  - Delete old files from /data/ directory
  - Update index.json to reflect current available dates
  - _Requirements: 3.3, 3.4_

- [x] 4.3 Add command-line interface

  - Add argparse for optional date parameter (for testing)
  - Add verbose logging flag
  - Add dry-run mode for testing without writing files
  - _Requirements: 2.3_

- [x] 4.4 Write unit tests for collector module





  - Create tests/test_collectors.py with tests for each fetcher
  - Create tests/test_deduplication.py for deduplication logic
  - Create tests/test_json_generation.py for output validation
  - Use pytest framework with mock responses
  - _Requirements: 7.1, 7.2, 7.3_

- [x] 5. Create GitHub Actions workflow



  - _Requirements: 2.1, 2.2, 2.5, 5.1, 5.2, 5.5, 8.3, 8.4_

- [x] 5.1 Create auto-update.yml workflow file


  - Define workflow name and schedule triggers (cron: 0 5 * * * and 0 17 * * *)
  - Add workflow_dispatch for manual triggering
  - Configure ubuntu-latest runner
  - _Requirements: 2.1, 2.2, 5.1_

- [x] 5.2 Implement workflow steps

  - Add checkout step with actions/checkout@v3
  - Add Python setup step with actions/setup-python@v4 (version 3.11)
  - Add dependency installation step (pip install -r requirements.txt)
  - Add collector execution step (python collector/generate_news.py)
  - _Requirements: 2.5, 5.5_


- [x] 5.3 Implement git commit and push steps

  - Configure git user.name and user.email as github-actions[bot]
  - Add git add for /data/ directory
  - Create commit with message format "Auto-update: YYYY-MM-DD HH:MM UTC"
  - Push changes to main branch with retry logic
  - _Requirements: 2.5, 8.4_

- [x] 5.4 Add error handling and notifications

  - Add conditional step to create error log on failure
  - Configure workflow to continue on partial failures
  - Set appropriate exit codes
  - _Requirements: 8.3_

- [x] 6. Build web application frontend



  - _Requirements: 1.1, 1.3, 1.4, 1.5, 3.1, 3.2, 4.1, 4.2, 4.4, 6.1, 6.2, 6.3, 6.4, 6.5_


- [x] 6.1 Create HTML structure

  - Create webapp/index.html with semantic HTML5 structure
  - Add header with logo and mode toggle buttons (Normal/Advanced)
  - Add refresh button in header controls
  - Create main content area with newsContainer div
  - Add advanced controls section with date selector (hidden by default)
  - Add status bar for last updated time and offline indicator
  - Add error message container (hidden by default)
  - Add footer with attribution
  - _Requirements: 1.1, 3.1, 6.1_



- [x] 6.2 Create CSS styling

  - Create webapp/style.css with mobile-first responsive design
  - Define color scheme: light background (#f8f9fa), white cards, indigo accent (#6366f1)
  - Style header with flexbox layout for logo and controls
  - Style mode toggle buttons with active state
  - Create news card component styles with rounded corners and shadows
  - Implement responsive grid layout for news items
  - Add media queries for breakpoints: 640px, 768px, 1024px
  - Style date selector and status bar
  - Add smooth transitions and hover effects
  - _Requirements: 1.5, 4.1_


- [x] 6.3 Implement core JavaScript functionality

  - Create webapp/script.js with AppState object for state management
  - Define API_BASE constant with GitHub Pages URL
  - Implement fetchTodayNews() function to fetch /data/today.json
  - Implement fetchDateNews(date) function to fetch specific date JSON
  - Implement fetchAvailableDates() function to fetch /data/index.json
  - Add error handling for all fetch operations with try-catch
  - _Requirements: 1.1, 3.2, 6.2, 6.3, 8.5_



- [x] 6.4 Implement rendering functions

  - Write renderNews(data) function to display news items grouped by source
  - Write renderSourceGroup(sourceName, items) to create source section with cards
  - Implement updateLastUpdatedTime(timestamp) to display formatted time
  - Write showError(message) function to display user-friendly error messages
  - Add loading indicator during fetch operations
  - _Requirements: 1.3, 1.4_




- [x] 6.5 Implement mode switching and controls

  - Add event listener for Normal mode button to show today's news
  - Add event listener for Advanced mode button to show date selector
  - Populate date selector dropdown from index.json
  - Add event listener for date selector change to fetch selected date
  - Implement refresh button to reload current view
  - Toggle visibility of advanced controls based on mode
  - _Requirements: 3.1, 3.2, 6.1, 6.5_





- [x] 6.6 Implement localStorage caching

  - Write cacheData(key, data) function to store JSON in localStorage
  - Write getCachedData(key) function to retrieve cached data
  - Implement cache expiry logic (12 hours)
  - Cache today's news, index, and viewed historical dates
  - Fall back to cached data when fetch fails or offline
  - _Requirements: 4.4, 4.5_






- [ ] 6.7 Implement offline detection and handling
  - Add event listeners for online/offline events
  - Update offline indicator visibility based on connection status
  - Automatically load cached data when offline
  - Display warning message when showing cached data

  - _Requirements: 4.4, 4.5, 8.5_





- [ ] 6.8 Add initialization and page load logic
  - Implement init() function to run on window load
  - Check online status and load appropriate data
  - Set default mode to Normal
  - Fetch and display today's news on initial load
  - Handle errors during initialization gracefully
  - _Requirements: 1.1, 4.5_

- [x] 7. Configure GitHub Pages hosting



  - _Requirements: 5.2, 5.3, 9.1, 9.3_


- [x] 7.1 Set up GitHub Pages

  - Enable GitHub Pages in repository settings
  - Configure source as main branch with /webapp folder (or root with proper structure)
  - Verify HTTPS is enabled (automatic with GitHub Pages)
  - Test access to hosted URL: https://USERNAME.github.io/eternal/
  - _Requirements: 5.2, 9.1_


- [x] 7.2 Configure CORS and access permissions

  - Verify JSON files are accessible from web app (same origin)
  - Test cross-origin requests if needed
  - Ensure repository is public for GitHub Pages access
  - _Requirements: 9.3_



- [ ] 7.3 Update JavaScript with correct API endpoints
  - Replace USERNAME placeholder in script.js with actual GitHub username
  - Verify all API_BASE URLs point to correct GitHub Pages domain
  - Test all fetch operations against live endpoints
  - _Requirements: 1.1, 3.2_

- [ ] 8. Create Android WebView integration
  - _Requirements: 4.1, 4.2, 4.3_

- [ ] 8.1 Create Android project structure
  - Create basic Android project with MainActivity
  - Add WebView to activity_main.xml layout
  - Configure AndroidManifest.xml with INTERNET and ACCESS_NETWORK_STATE permissions
  - _Requirements: 4.1_

- [ ] 8.2 Implement WebView configuration
  - Enable JavaScript in WebView settings
  - Enable DOM storage for localStorage support
  - Configure cache mode to LOAD_DEFAULT
  - Set WebViewClient to handle navigation
  - Load GitHub Pages URL in WebView
  - _Requirements: 4.2, 4.3_

- [ ] 8.3 Test WebView functionality
  - Verify web app loads correctly in WebView
  - Test Normal and Advanced modes
  - Test refresh functionality
  - Test offline mode with cached data
  - Verify localStorage persistence
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 9. Create documentation
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 9.1 Write comprehensive README.md
  - Add project overview and features section
  - Document architecture with diagram
  - Write setup instructions for GitHub repository
  - Document how to enable GitHub Actions and Pages
  - Add usage instructions for Normal and Advanced modes
  - Include Android WebView integration guide
  - Add troubleshooting section
  - _Requirements: 10.1_

- [ ] 9.2 Create initial Changelog.md
  - Create docs/Changelog.md file
  - Add initial entry with project creation date
  - Document initial implementation of all components
  - Set up format for future updates: date, component, description
  - _Requirements: 10.2, 10.5_

- [ ] 9.3 Add inline code documentation
  - Add docstrings to all Python classes and functions
  - Add comments explaining complex logic in collector module
  - Add JSDoc comments to JavaScript functions
  - Document each source fetcher's scraping strategy
  - _Requirements: 10.4_

- [ ] 9.4 Create contributing guidelines

  - Document how to add new sources
  - Explain how to modify collection schedule
  - Provide guidelines for testing changes
  - Add code style guidelines
  - _Requirements: 10.1_

- [ ] 10. Integration testing and deployment
  - _Requirements: 2.1, 2.2, 5.5, 8.3, 8.4_

- [ ] 10.1 Test complete collection pipeline
  - Run generate_news.py manually to verify all sources work
  - Check generated JSON files for correct structure
  - Verify deduplication removes duplicate items
  - Confirm index.json updates correctly
  - Test file cleanup for old dates
  - _Requirements: 2.3, 3.3, 3.4, 7.1, 7.2_

- [ ] 10.2 Test GitHub Actions workflow
  - Trigger workflow manually using workflow_dispatch
  - Verify Python environment setup succeeds
  - Confirm collector executes without errors
  - Check that JSON files are committed to repository
  - Verify old files are deleted correctly
  - Monitor execution time (should be under 10 minutes)
  - _Requirements: 2.1, 2.2, 2.5, 5.5, 8.3, 8.4_

- [ ] 10.3 Test web application end-to-end
  - Load web app in browser and verify Normal mode displays today's news
  - Switch to Advanced mode and verify date selector appears
  - Select different dates and verify correct data loads
  - Test refresh button updates display
  - Simulate offline mode and verify cached data displays
  - Test on mobile devices (320px - 768px widths)
  - _Requirements: 1.1, 1.5, 3.1, 3.2, 4.4, 4.5, 6.1, 6.2, 6.3_

- [ ] 10.4 Test Android WebView integration
  - Build and install Android APK
  - Verify web app loads in WebView
  - Test all functionality within WebView
  - Verify localStorage works correctly
  - Test offline behavior in Android app
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 10.5 Verify security and access controls
  - Confirm all content served over HTTPS
  - Verify no API keys or secrets exposed in code or logs
  - Test repository permissions (public read, protected write)
  - Verify GitHub Actions has correct permissions
  - _Requirements: 5.4, 9.1, 9.2, 9.4, 9.5_

- [ ] 10.6 Final deployment verification
  - Verify scheduled workflow runs at 05:00 and 17:00 UTC
  - Monitor first few automated runs for errors
  - Confirm GitHub Pages updates automatically
  - Verify web app displays new data after each run
  - Update Changelog.md with deployment date and final notes
  - _Requirements: 2.1, 2.2, 10.5_
