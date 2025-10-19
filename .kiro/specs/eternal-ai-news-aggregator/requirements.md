# Requirements Document

## Introduction

Eternal is a zero-cost, fully automated AI news aggregation system that collects, organizes, and displays AI-related updates from multiple authoritative sources. The system runs on GitHub infrastructure (Actions + Pages), executes Python scrapers twice daily, stores structured JSON data for 7 days, and presents information through a responsive web application compatible with Android WebView.

## Glossary

- **Eternal System**: The complete AI news aggregation platform including collector, automation, storage, and frontend components
- **Collector Module**: Python-based scraper that fetches AI news from multiple sources
- **GitHub Actions Runner**: Automated execution environment that runs the Collector Module on schedule
- **Data Store**: JSON file repository maintaining 7-day rolling history of collected news
- **Web Application**: HTML/CSS/JS frontend that displays aggregated news
- **Normal Mode**: Display mode showing only today's collected news
- **Advanced Mode**: Display mode allowing users to view news from any of the last 7 days
- **WebView Container**: Android WebView component that hosts the Web Application

## Requirements

### Requirement 1

**User Story:** As an AI enthusiast, I want to view today's aggregated AI news from multiple authoritative sources in one place, so that I can stay updated without visiting multiple websites.

#### Acceptance Criteria

1. WHEN the user accesses the Web Application, THE Eternal System SHALL display today's collected news by default
2. THE Eternal System SHALL aggregate news from arXiv cs.AI section, Hugging Face Blog, Product Hunt AI category, ArtificialIntelligence-News.com, Crescendo AI News, Reddit r/MachineLearning, and Reddit r/ClaudeAI
3. THE Eternal System SHALL organize displayed news by source category with clear visual separation
4. THE Eternal System SHALL display each news item with title, summary, and clickable link to original source
5. THE Web Application SHALL render correctly on mobile devices with screen widths between 320px and 768px

### Requirement 2

**User Story:** As a researcher, I want the system to automatically collect AI news twice daily, so that I receive timely updates without manual intervention.

#### Acceptance Criteria

1. THE GitHub Actions Runner SHALL execute the Collector Module at 05:00 UTC daily
2. THE GitHub Actions Runner SHALL execute the Collector Module at 17:00 UTC daily
3. WHEN the Collector Module executes, THE Eternal System SHALL fetch content from all configured sources within 10 minutes
4. WHEN collection completes, THE Eternal System SHALL generate a JSON file named with format YYYY-MM-DD.json
5. THE GitHub Actions Runner SHALL commit generated JSON files to the repository with timestamp and automated commit message

### Requirement 3

**User Story:** As a power user, I want to access news from the previous 6 days, so that I can review updates I may have missed.

#### Acceptance Criteria

1. WHERE Advanced Mode is selected, THE Web Application SHALL display a date selector showing the last 7 days
2. WHEN the user selects a specific date, THE Web Application SHALL fetch and display news from that date's JSON file
3. THE Data Store SHALL maintain exactly 7 days of historical JSON files at any time
4. WHEN a new JSON file is created, THE Eternal System SHALL delete JSON files older than 7 days
5. THE Eternal System SHALL maintain an index.json file listing all available dates in the Data Store

### Requirement 4

**User Story:** As a mobile user, I want to access the news aggregator through an Android app, so that I can read updates conveniently on my phone.

#### Acceptance Criteria

1. THE Web Application SHALL function correctly when loaded in an Android WebView Container
2. THE Web Application SHALL NOT require any external JavaScript frameworks or libraries beyond vanilla JavaScript
3. WHEN the WebView Container loads the Web Application, THE Eternal System SHALL enable JavaScript execution
4. THE Web Application SHALL cache the most recent news data in localStorage for offline access
5. WHEN offline, THE Web Application SHALL display cached news data with a visual indicator showing last update time

### Requirement 5

**User Story:** As a developer, I want the entire system to run on free GitHub infrastructure, so that I can operate the service without ongoing costs.

#### Acceptance Criteria

1. THE Eternal System SHALL use only GitHub Actions free tier resources for automation
2. THE Eternal System SHALL host all static files through GitHub Pages with HTTPS enabled
3. THE Eternal System SHALL NOT require any paid API keys or external services for core functionality
4. WHERE external APIs require authentication, THE Eternal System SHALL store credentials in GitHub Secrets
5. THE GitHub Actions Runner SHALL complete each collection cycle within the free tier time limits (6 hours per run maximum)

### Requirement 6

**User Story:** As a user, I want to manually refresh the news feed, so that I can check for updates without waiting for the scheduled collection.

#### Acceptance Criteria

1. THE Web Application SHALL display a refresh button visible on all screen sizes
2. WHEN the user clicks the refresh button, THE Web Application SHALL fetch the latest available JSON data
3. WHEN refresh completes, THE Web Application SHALL update the displayed content within 2 seconds
4. WHEN refresh fails, THE Web Application SHALL display an error message indicating the failure reason
5. THE Web Application SHALL update the "last updated" timestamp after successful refresh

### Requirement 7

**User Story:** As a content consumer, I want news items to be deduplicated and organized, so that I don't see repeated information.

#### Acceptance Criteria

1. WHEN the Collector Module processes sources, THE Eternal System SHALL identify duplicate news items by comparing titles
2. WHEN duplicates are detected, THE Eternal System SHALL retain only the first occurrence of each news item
3. THE Collector Module SHALL group news items by source category in the output JSON structure
4. THE Collector Module SHALL include metadata fields for date, last_updated timestamp, and source attribution
5. THE Collector Module SHALL filter out spam content and non-AI-related items based on keyword matching

### Requirement 8

**User Story:** As a system administrator, I want the automation to handle errors gracefully, so that temporary failures don't break the entire system.

#### Acceptance Criteria

1. WHEN a source fails to respond, THE Collector Module SHALL log the error and continue processing remaining sources
2. WHEN the Collector Module encounters a parsing error, THE Eternal System SHALL skip the problematic item and continue
3. IF all sources fail, THE GitHub Actions Runner SHALL create an error log file and send a notification
4. THE GitHub Actions Runner SHALL retry failed git operations up to 3 times before reporting failure
5. WHEN the Web Application cannot fetch JSON data, THE Eternal System SHALL display cached data with a warning message

### Requirement 9

**User Story:** As a security-conscious user, I want the system to be transparent and secure, so that I can trust the news source and data integrity.

#### Acceptance Criteria

1. THE Eternal System SHALL serve all content over HTTPS through GitHub Pages
2. THE Eternal System SHALL NOT store or transmit any user personal data
3. THE Data Store SHALL be publicly readable but write-protected through GitHub repository permissions
4. THE Eternal System SHALL version all code and data changes in the public GitHub repository
5. WHERE API keys are required, THE Eternal System SHALL store them exclusively in GitHub Secrets and never expose them in code or logs

### Requirement 10

**User Story:** As a developer, I want clear documentation and project structure, so that I can understand, maintain, and extend the system.

#### Acceptance Criteria

1. THE Eternal System SHALL include a README.md file with setup instructions, architecture overview, and usage guide
2. THE Eternal System SHALL maintain a Changelog.md file in the docs folder documenting all code changes
3. THE Eternal System SHALL organize code into logical directories: /collector, /.github/workflows, /data, /webapp
4. THE Collector Module SHALL include inline comments explaining scraping logic for each source
5. WHEN any code is modified, THE Eternal System SHALL update the Changelog.md file with the change description and timestamp
