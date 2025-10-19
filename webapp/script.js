/**
 * Eternal AI News Aggregator - Frontend JavaScript
 * Fetches and displays real AI news data from JSON files
 * NO MOCK DATA - All data comes from actual collection
 */

// ===== Configuration =====
const CONFIG = {
    // Automatically detect the correct API base URL
    API_BASE: (() => {
        const hostname = window.location.hostname;
        
        // Local development
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return '../data';
        }
        
        // Production - use relative path for same-origin (no CORS issues)
        // This works for both GitHub Pages and custom domains
        const basePath = window.location.pathname.replace(/\/webapp\/.*$/, '');
        return `${window.location.origin}${basePath}/data`;
    })(),
    CACHE_EXPIRY: 12 * 60 * 60 * 1000, // 12 hours in milliseconds
    CACHE_PREFIX: 'eternal_'
};

// ===== Application State =====
const AppState = {
    mode: 'normal',
    currentDate: null,
    cachedData: null,
    isOnline: navigator.onLine,
    availableDates: []
};

// ===== DOM Elements =====
const elements = {
    normalModeBtn: document.getElementById('normalMode'),
    advancedModeBtn: document.getElementById('advancedMode'),
    refreshBtn: document.getElementById('refreshBtn'),
    advancedControls: document.getElementById('advancedControls'),
    dateSelector: document.getElementById('dateSelector'),
    statusBar: document.getElementById('statusBar'),
    lastUpdated: document.getElementById('lastUpdated'),
    offlineIndicator: document.getElementById('offlineIndicator'),
    itemCount: document.getElementById('itemCount'),
    loadingIndicator: document.getElementById('loadingIndicator'),
    errorMessage: document.getElementById('errorMessage'),
    errorText: document.getElementById('errorText'),
    newsContainer: document.getElementById('newsContainer')
};

// ===== Utility Functions =====

/**
 * Format ISO timestamp to readable date
 */
function formatDate(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Format date for display
 */
function formatDateShort(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Show loading indicator
 */
function showLoading() {
    elements.loadingIndicator.classList.remove('hidden');
    elements.newsContainer.innerHTML = '';
    elements.errorMessage.classList.add('hidden');
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    elements.loadingIndicator.classList.add('hidden');
}

/**
 * Show error message
 */
function showError(message) {
    elements.errorText.textContent = message;
    elements.errorMessage.classList.remove('hidden');
    hideLoading();
}

/**
 * Hide error message
 */
function hideError() {
    elements.errorMessage.classList.add('hidden');
}

/**
 * Update last updated timestamp
 */
function updateLastUpdatedTime(timestamp) {
    elements.lastUpdated.textContent = `Last updated: ${formatDate(timestamp)}`;
}

/**
 * Update item count
 */
function updateItemCount(count) {
    elements.itemCount.textContent = `${count} items`;
}

// ===== Cache Management =====

/**
 * Get cache key with prefix
 */
function getCacheKey(key) {
    return `${CONFIG.CACHE_PREFIX}${key}`;
}

/**
 * Save data to localStorage with timestamp
 */
function cacheData(key, data) {
    try {
        const cacheEntry = {
            data: data,
            timestamp: Date.now()
        };
        localStorage.setItem(getCacheKey(key), JSON.stringify(cacheEntry));
        console.log(`Cached data for key: ${key}`);
    } catch (error) {
        console.warn('Failed to cache data:', error);
    }
}

/**
 * Get data from localStorage if not expired
 */
function getCachedData(key) {
    try {
        const cached = localStorage.getItem(getCacheKey(key));
        if (!cached) return null;
        
        const cacheEntry = JSON.parse(cached);
        const age = Date.now() - cacheEntry.timestamp;
        
        if (age > CONFIG.CACHE_EXPIRY) {
            localStorage.removeItem(getCacheKey(key));
            return null;
        }
        
        console.log(`Using cached data for key: ${key}`);
        return cacheEntry.data;
    } catch (error) {
        console.warn('Failed to get cached data:', error);
        return null;
    }
}

// ===== API Functions =====

/**
 * Fetch today's news from today.json
 */
async function fetchTodayNews() {
    const url = `${CONFIG.API_BASE}/today.json`;
    console.log(`Fetching today's news from: ${url}`);
    
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        cacheData('today', data);
        return data;
    } catch (error) {
        console.error('Failed to fetch today news:', error);
        
        // Try to use cached data
        const cached = getCachedData('today');
        if (cached) {
            console.log('Using cached today data');
            showError('Using cached data (offline or network error)');
            return cached;
        }
        
        throw error;
    }
}

/**
 * Fetch news for a specific date
 */
async function fetchDateNews(date) {
    const url = `${CONFIG.API_BASE}/${date}.json`;
    console.log(`Fetching news for ${date} from: ${url}`);
    
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        cacheData(`date_${date}`, data);
        return data;
    } catch (error) {
        console.error(`Failed to fetch news for ${date}:`, error);
        
        // Try to use cached data
        const cached = getCachedData(`date_${date}`);
        if (cached) {
            console.log(`Using cached data for ${date}`);
            showError('Using cached data (offline or network error)');
            return cached;
        }
        
        throw error;
    }
}

/**
 * Fetch available dates from index.json
 */
async function fetchAvailableDates() {
    const url = `${CONFIG.API_BASE}/index.json`;
    console.log(`Fetching available dates from: ${url}`);
    
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        cacheData('index', data);
        return data.available_dates || [];
    } catch (error) {
        console.error('Failed to fetch available dates:', error);
        
        // Try to use cached data
        const cached = getCachedData('index');
        if (cached) {
            console.log('Using cached index data');
            return cached.available_dates || [];
        }
        
        throw error;
    }
}

// ===== Rendering Functions =====

/**
 * Render news items grouped by source
 */
function renderNews(data) {
    hideError();
    elements.newsContainer.innerHTML = '';
    
    if (!data || !data.sources) {
        showError('No news data available');
        return;
    }
    
    // Update metadata
    if (data.last_updated) {
        updateLastUpdatedTime(data.last_updated);
    }
    
    // Count total items
    let totalItems = 0;
    Object.values(data.sources).forEach(items => {
        totalItems += items.length;
    });
    updateItemCount(totalItems);
    
    // Render each source section
    const sourceNames = Object.keys(data.sources).sort();
    
    sourceNames.forEach(sourceName => {
        const items = data.sources[sourceName];
        if (items && items.length > 0) {
            renderSourceGroup(sourceName, items);
        }
    });
    
    if (totalItems === 0) {
        elements.newsContainer.innerHTML = '<p class="text-center">No news items available for this date.</p>';
    }
}

/**
 * Render a source group with its news items
 */
function renderSourceGroup(sourceName, items) {
    const section = document.createElement('div');
    section.className = 'source-section';
    
    // Create header
    const header = document.createElement('div');
    header.className = 'source-header';
    
    const title = document.createElement('h2');
    title.className = 'source-title';
    title.textContent = formatSourceName(sourceName);
    
    const count = document.createElement('span');
    count.className = 'source-count';
    count.textContent = `${items.length} items`;
    
    header.appendChild(title);
    header.appendChild(count);
    section.appendChild(header);
    
    // Create grid of news cards
    const grid = document.createElement('div');
    grid.className = 'news-grid';
    
    items.forEach(item => {
        const card = createNewsCard(item);
        grid.appendChild(card);
    });
    
    section.appendChild(grid);
    elements.newsContainer.appendChild(section);
}

/**
 * Create a news card element
 */
function createNewsCard(item) {
    const card = document.createElement('div');
    card.className = 'news-card';
    
    // Title
    const title = document.createElement('h3');
    title.className = 'news-title';
    const titleLink = document.createElement('a');
    titleLink.href = item.link;
    titleLink.target = '_blank';
    titleLink.rel = 'noopener noreferrer';
    titleLink.textContent = item.title;
    title.appendChild(titleLink);
    card.appendChild(title);
    
    // Summary
    if (item.summary) {
        const summary = document.createElement('p');
        summary.className = 'news-summary';
        summary.textContent = item.summary;
        card.appendChild(summary);
    }
    
    // Meta information
    const meta = document.createElement('div');
    meta.className = 'news-meta';
    
    const date = document.createElement('span');
    date.className = 'news-date';
    date.textContent = formatDateShort(item.published);
    
    const link = document.createElement('a');
    link.className = 'news-link';
    link.href = item.link;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = 'Read more →';
    
    meta.appendChild(date);
    meta.appendChild(link);
    card.appendChild(meta);
    
    return card;
}

/**
 * Format source name for display
 */
function formatSourceName(sourceName) {
    const nameMap = {
        'arxiv': 'arXiv',
        'huggingface': 'Hugging Face',
        'producthunt': 'Product Hunt',
        'reddit': 'Reddit',
        'ai_news': 'AI News',
        'crescendo': 'Crescendo AI'
    };
    
    return nameMap[sourceName] || sourceName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// ===== Mode Switching =====

/**
 * Switch to Normal mode
 */
async function switchToNormal() {
    AppState.mode = 'normal';
    elements.normalModeBtn.classList.add('active');
    elements.advancedModeBtn.classList.remove('active');
    elements.advancedControls.classList.add('hidden');
    
    await loadTodayNews();
}

/**
 * Switch to Advanced mode
 */
async function switchToAdvanced() {
    AppState.mode = 'advanced';
    elements.advancedModeBtn.classList.add('active');
    elements.normalModeBtn.classList.remove('active');
    elements.advancedControls.classList.remove('hidden');
    
    // Load available dates
    await loadAvailableDates();
}

/**
 * Load today's news
 */
async function loadTodayNews() {
    showLoading();
    
    try {
        const data = await fetchTodayNews();
        renderNews(data);
        AppState.cachedData = data;
    } catch (error) {
        showError('Failed to load news. Please check your connection and try again.');
        console.error('Error loading today news:', error);
    } finally {
        hideLoading();
    }
}

/**
 * Load available dates and populate selector
 */
async function loadAvailableDates() {
    try {
        const dates = await fetchAvailableDates();
        AppState.availableDates = dates;
        
        // Populate date selector
        elements.dateSelector.innerHTML = '';
        
        if (dates.length === 0) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'No dates available';
            elements.dateSelector.appendChild(option);
            return;
        }
        
        dates.forEach(date => {
            const option = document.createElement('option');
            option.value = date;
            option.textContent = formatDateShort(date);
            elements.dateSelector.appendChild(option);
        });
        
        // Load first date
        if (dates.length > 0) {
            elements.dateSelector.value = dates[0];
            await loadDateNews(dates[0]);
        }
    } catch (error) {
        showError('Failed to load available dates.');
        console.error('Error loading dates:', error);
    }
}

/**
 * Load news for selected date
 */
async function loadDateNews(date) {
    showLoading();
    
    try {
        const data = await fetchDateNews(date);
        renderNews(data);
        AppState.cachedData = data;
        AppState.currentDate = date;
    } catch (error) {
        showError(`Failed to load news for ${date}. Please try again.`);
        console.error(`Error loading news for ${date}:`, error);
    } finally {
        hideLoading();
    }
}

/**
 * Refresh current view
 */
async function refreshNews() {
    if (AppState.mode === 'normal') {
        await loadTodayNews();
    } else {
        const selectedDate = elements.dateSelector.value;
        if (selectedDate) {
            await loadDateNews(selectedDate);
        }
    }
}

// ===== Online/Offline Handling =====

function handleOnline() {
    AppState.isOnline = true;
    elements.offlineIndicator.classList.add('hidden');
    console.log('Connection restored');
}

function handleOffline() {
    AppState.isOnline = false;
    elements.offlineIndicator.classList.remove('hidden');
    console.log('Connection lost - using cached data');
}

// ===== Event Listeners =====

elements.normalModeBtn.addEventListener('click', switchToNormal);
elements.advancedModeBtn.addEventListener('click', switchToAdvanced);
elements.refreshBtn.addEventListener('click', refreshNews);
elements.dateSelector.addEventListener('change', (e) => {
    const selectedDate = e.target.value;
    if (selectedDate) {
        loadDateNews(selectedDate);
    }
});

window.addEventListener('online', handleOnline);
window.addEventListener('offline', handleOffline);

// ===== Initialization =====

async function init() {
    console.log('Initializing Eternal AI News Aggregator...');
    console.log('API Base:', CONFIG.API_BASE);
    
    // Check online status
    if (!navigator.onLine) {
        handleOffline();
    }
    
    // Load today's news by default
    await loadTodayNews();
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
