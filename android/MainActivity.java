package com.eternal.ainews;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.view.KeyEvent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.content.Context;

/**
 * MainActivity for Eternal AI News Aggregator
 * Displays the web app in a WebView with full functionality
 */
public class MainActivity extends Activity {
    
    private WebView webView;
    
    // GitHub Pages URL - update this with your actual URL
    private static final String WEB_APP_URL = "https://johnwikcke.github.io/Eternal/";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // Initialize WebView
        webView = findViewById(R.id.webview);
        
        // Configure WebView settings
        configureWebView();
        
        // Load the web app
        loadWebApp();
    }
    
    /**
     * Configure WebView with optimal settings for the web app
     */
    private void configureWebView() {
        WebSettings webSettings = webView.getSettings();
        
        // Enable JavaScript (required for the app)
        webSettings.setJavaScriptEnabled(true);
        
        // Enable DOM storage for localStorage
        webSettings.setDomStorageEnabled(true);
        
        // Enable database storage
        webSettings.setDatabaseEnabled(true);
        
        // Enable caching for offline support
        webSettings.setCacheMode(WebSettings.LOAD_DEFAULT);
        webSettings.setAppCacheEnabled(true);
        
        // Enable zoom controls
        webSettings.setBuiltInZoomControls(true);
        webSettings.setDisplayZoomControls(false);
        
        // Enable responsive layout
        webSettings.setUseWideViewPort(true);
        webSettings.setLoadWithOverviewMode(true);
        
        // Enable mixed content (if needed)
        webSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE);
        
        // Set user agent
        webSettings.setUserAgentString(webSettings.getUserAgentString() + " EternalApp/1.0");
        
        // Set WebViewClient to handle navigation
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                // Keep navigation within WebView
                view.loadUrl(url);
                return true;
            }
            
            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                // Handle errors gracefully
                super.onReceivedError(view, errorCode, description, failingUrl);
            }
        });
        
        // Set WebChromeClient for better JavaScript support
        webView.setWebChromeClient(new WebChromeClient());
    }
    
    /**
     * Load the web app URL
     */
    private void loadWebApp() {
        if (isNetworkAvailable()) {
            webView.loadUrl(WEB_APP_URL);
        } else {
            // Try to load from cache if offline
            webView.getSettings().setCacheMode(WebSettings.LOAD_CACHE_ELSE_NETWORK);
            webView.loadUrl(WEB_APP_URL);
        }
    }
    
    /**
     * Check if network is available
     */
    private boolean isNetworkAvailable() {
        ConnectivityManager connectivityManager = 
            (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetworkInfo = connectivityManager.getActiveNetworkInfo();
        return activeNetworkInfo != null && activeNetworkInfo.isConnected();
    }
    
    /**
     * Handle back button to navigate WebView history
     */
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
            webView.goBack();
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }
    
    /**
     * Pause WebView when activity is paused
     */
    @Override
    protected void onPause() {
        super.onPause();
        webView.onPause();
    }
    
    /**
     * Resume WebView when activity is resumed
     */
    @Override
    protected void onResume() {
        super.onResume();
        webView.onResume();
    }
    
    /**
     * Clean up WebView when activity is destroyed
     */
    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.destroy();
        }
        super.onDestroy();
    }
}
