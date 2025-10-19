# Eternal - Deployment Guide

This guide walks you through deploying the Eternal AI News Aggregator to GitHub Pages.

## Prerequisites

- GitHub account
- Git installed locally
- Repository created on GitHub

## Step 1: Push Code to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Eternal AI News Aggregator"

# Add remote repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/eternal.git

# Push to GitHub
git push -u origin main
```

## Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings** tab
3. Scroll down to **Pages** section in the left sidebar
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
5. Click **Save**
6. Wait 1-2 minutes for deployment

Your site will be available at: `https://YOUR_USERNAME.github.io/eternal/`

## Step 3: Configure GitHub Actions Permissions

1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
3. Click **Save**

This allows the workflow to commit collected data.

## Step 4: Update API Configuration

Edit `webapp/script.js` and update the API_BASE URL:

```javascript
const CONFIG = {
    API_BASE: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? '../data'
        : 'https://YOUR_USERNAME.github.io/eternal/data',  // Update this line
    // ...
};
```

Replace `YOUR_USERNAME` with your actual GitHub username.

Commit and push the change:

```bash
git add webapp/script.js
git commit -m "Update API base URL for GitHub Pages"
git push
```

## Step 5: Trigger First Collection

1. Go to **Actions** tab in your repository
2. Click on **Auto Update AI News** workflow
3. Click **Run workflow** button
4. Select branch: `main`
5. Click **Run workflow**

Wait 5-10 minutes for the workflow to complete. This will:
- Collect real AI news from all sources
- Generate JSON files in `/data/`
- Commit and push the data
- Make it available on GitHub Pages

## Step 6: Verify Deployment

1. Visit `https://YOUR_USERNAME.github.io/eternal/`
2. You should see the Eternal web application
3. Click "Refresh" to load today's news
4. Try "Advanced" mode to see the date selector

## Step 7: Verify Data Endpoints

Check that JSON files are accessible:

- Today's news: `https://YOUR_USERNAME.github.io/eternal/data/today.json`
- Index: `https://YOUR_USERNAME.github.io/eternal/data/index.json`
- Specific date: `https://YOUR_USERNAME.github.io/eternal/data/2025-10-19.json`

## Automated Updates

The system will now automatically:
- Run at 05:00 UTC daily
- Run at 17:00 UTC daily
- Collect real AI news from all sources
- Update JSON files
- Commit and push changes

## Monitoring

### Check Workflow Status

1. Go to **Actions** tab
2. View recent workflow runs
3. Click on a run to see detailed logs

### Check Data Updates

1. Go to **Code** tab
2. Navigate to `/data/` folder
3. Check commit history to see automated updates

## Troubleshooting

### Workflow Fails

**Problem**: Workflow shows red X (failed)

**Solutions**:
1. Check Actions logs for error messages
2. Verify GitHub Actions permissions are set correctly
3. Check if any source is blocking requests
4. Manually trigger workflow again

### No Data Showing

**Problem**: Web app loads but shows no news

**Solutions**:
1. Check if workflow has run successfully
2. Verify JSON files exist in `/data/` folder
3. Check browser console for errors
4. Verify API_BASE URL is correct in script.js

### 404 Errors

**Problem**: GitHub Pages shows 404

**Solutions**:
1. Verify GitHub Pages is enabled
2. Check that source is set to `main` branch, `/ (root)` folder
3. Wait a few minutes for deployment
4. Clear browser cache

### CORS Errors

**Problem**: Browser console shows CORS errors

**Solutions**:
- GitHub Pages automatically handles CORS for same-origin requests
- Ensure you're accessing via the GitHub Pages URL, not file://
- Check that API_BASE URL matches your GitHub Pages domain

## Custom Domain (Optional)

To use a custom domain:

1. Go to **Settings** → **Pages**
2. Under **Custom domain**, enter your domain
3. Click **Save**
4. Configure DNS records at your domain provider:
   - Add CNAME record pointing to `YOUR_USERNAME.github.io`
5. Update API_BASE in script.js to use your custom domain

## Security Notes

- All data is public (read-only)
- No API keys are exposed in the code
- GitHub Actions secrets are secure
- HTTPS is enforced by GitHub Pages

## Performance

- GitHub Pages has bandwidth limits (100GB/month soft limit)
- Each JSON file is ~100-500KB
- Estimated usage: ~1-2GB/month for typical traffic
- Well within free tier limits

## Backup

Your data is automatically backed up in Git history:

```bash
# View all data commits
git log --oneline -- data/

# Restore specific date
git checkout <commit-hash> -- data/2025-10-19.json
```

## Next Steps

1. ✅ Deploy to GitHub Pages
2. ✅ Verify automated collection works
3. ✅ Share your Eternal instance URL
4. 📱 Optional: Create Android WebView app
5. 🎨 Optional: Customize styling in style.css
6. 🔧 Optional: Add more news sources in collector/sources.py

## Support

For issues or questions:
- Check GitHub Actions logs
- Review browser console errors
- Verify all configuration steps
- Check that sources are accessible

---

**Congratulations!** Your Eternal AI News Aggregator is now live and collecting real AI news twice daily! 🎉
