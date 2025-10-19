# 🧠 Eternal - AI News Aggregator System

Eternal is a zero-cost, fully automated AI news aggregation system that collects, organizes, and displays AI-related updates from multiple authoritative sources twice daily.

## ✨ Features

- **Automated Collection**: Runs twice daily (05:00 & 17:00 UTC) via GitHub Actions
- **Multiple Sources**: Aggregates from arXiv, Hugging Face, Product Hunt, Reddit, and AI news sites
- **7-Day History**: Access news from the past week
- **Zero Cost**: Runs entirely on free GitHub infrastructure (Actions + Pages)
- **Responsive Web App**: Clean, mobile-friendly interface
- **Android Compatible**: Works seamlessly in Android WebView
- **Offline Support**: Caches data for offline reading

## 🏗️ Architecture

```
GitHub Actions (Scheduler)
         ↓
Python Collector (Scraper)
         ↓
JSON Data Store (7-day rolling)
         ↓
GitHub Pages (HTTPS Hosting)
         ↓
Web Application (HTML/CSS/JS)
         ↓
Android WebView (Optional)
```

## 📁 Project Structure

```
eternal/
├── collector/              # Python scraper module
│   └── generate_news.py   # Main collection script
├── .github/
│   └── workflows/
│       └── auto-update.yml # GitHub Actions workflow
├── data/                   # JSON data files (auto-generated)
│   ├── YYYY-MM-DD.json    # Daily news files
│   ├── index.json         # Date manifest
│   └── today.json         # Latest news
├── webapp/                 # Frontend application
│   ├── index.html         # Main page
│   ├── style.css          # Styling
│   └── script.js          # Client-side logic
├── docs/                   # Documentation
│   └── Changelog.md       # Change history
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Setup Instructions

### 1. Fork/Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/eternal.git
cd eternal
```

### 2. Install Python Dependencies (for local testing)

```bash
pip install -r requirements.txt
```

### 3. Enable GitHub Actions

1. Go to repository Settings → Actions → General
2. Enable "Allow all actions and reusable workflows"
3. Set workflow permissions to "Read and write permissions"

### 4. Enable GitHub Pages

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / Folder: `/` (root)
4. Save and wait for deployment

### 5. Update Configuration

Edit `webapp/script.js` and replace `USERNAME` with your GitHub username:

```javascript
const API_BASE = 'https://YOUR_USERNAME.github.io/eternal/data';
```

### 6. Trigger First Collection

1. Go to Actions tab
2. Select "Auto Update AI News" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait for completion (~5-10 minutes)

### 7. Access Your News Aggregator

Visit: `https://YOUR_USERNAME.github.io/eternal/`

## 📱 Android WebView Integration

### Basic Implementation

```java
public class MainActivity extends AppCompatActivity {
    private WebView webView;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        webView = findViewById(R.id.webview);
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        
        webView.loadUrl("https://YOUR_USERNAME.github.io/eternal/");
    }
}
```

### Required Permissions (AndroidManifest.xml)

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

## 🎯 Usage

### Normal Mode
- Displays today's aggregated AI news
- Automatically loads on page open
- Click "Refresh" to update

### Advanced Mode
- Access news from the past 7 days
- Select date from dropdown
- View historical updates

### Offline Mode
- Automatically caches latest data
- Works without internet connection
- Shows "Offline Mode" indicator

## 🔧 Customization

### Add New Sources

Edit `collector/generate_news.py`:

```python
class NewSourceFetcher(SourceFetcher):
    def fetch(self):
        # Your scraping logic
        pass
```

### Change Collection Schedule

Edit `.github/workflows/auto-update.yml`:

```yaml
schedule:
  - cron: '0 5 * * *'   # 05:00 UTC
  - cron: '0 17 * * *'  # 17:00 UTC
```

### Modify Retention Period

Edit `collector/generate_news.py` to change from 7 days:

```python
RETENTION_DAYS = 7  # Change this value
```

## 🛠️ Development

### Run Collector Locally

```bash
python collector/generate_news.py
```

### Test Web App Locally

```bash
# Serve webapp directory
python -m http.server 8000
# Visit http://localhost:8000/webapp/
```

## 📊 Data Sources

- **arXiv**: AI research papers (cs.AI section)
- **Hugging Face**: Model releases and blog posts
- **Product Hunt**: New AI tools and products
- **Reddit**: r/MachineLearning, r/ClaudeAI discussions
- **AI News Sites**: ArtificialIntelligence-News.com, Crescendo AI News

## 🔒 Security

- All content served over HTTPS
- No user data collection
- Public read-only access
- API keys stored in GitHub Secrets
- Automated commits from github-actions[bot]

## 📈 Monitoring

- Check Actions tab for workflow status
- View commit history for data updates
- Monitor GitHub Pages deployment status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - feel free to use and modify

## 🙏 Acknowledgments

Built with free and open-source tools:
- GitHub Actions for automation
- GitHub Pages for hosting
- Python ecosystem for scraping
- Vanilla JavaScript for frontend

---

**Made with ❤️ for the AI community**
