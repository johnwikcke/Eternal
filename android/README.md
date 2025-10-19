# Eternal - Android WebView App

This directory contains the Android WebView integration for Eternal AI News Aggregator.

## Overview

The Android app is a simple WebView wrapper that loads the Eternal web application from GitHub Pages. It provides:
- Full offline support with caching
- Native Android app experience
- localStorage persistence
- Network status detection
- Back button navigation

## Prerequisites

- Android Studio (latest version)
- Android SDK (API 24+)
- Java Development Kit (JDK 8+)

## Setup Instructions

### 1. Create New Android Project

1. Open Android Studio
2. Click "New Project"
3. Select "Empty Activity"
4. Configure:
   - Name: `Eternal`
   - Package name: `com.eternal.ainews`
   - Language: `Java`
   - Minimum SDK: `API 24 (Android 7.0)`

### 2. Add Files

Copy the files from this directory to your Android project:

```
app/src/main/
├── AndroidManifest.xml          → Replace existing
├── java/com/eternal/ainews/
│   └── MainActivity.java        → Replace existing
├── res/
│   ├── layout/
│   │   └── activity_main.xml    → Replace existing
│   └── values/
│       └── strings.xml          → Update
└── build.gradle                 → Update dependencies
```

### 3. Update GitHub Pages URL

Edit `MainActivity.java` and update the URL:

```java
private static final String WEB_APP_URL = "https://johnwikcke.github.io/Eternal/";
```

Replace with your actual GitHub Pages URL.

### 4. Build the App

1. In Android Studio, click "Build" → "Make Project"
2. Wait for Gradle sync to complete
3. Fix any errors if they appear

### 5. Run on Device/Emulator

1. Connect an Android device or start an emulator
2. Click "Run" → "Run 'app'"
3. Select your device
4. Wait for installation

## Features

### WebView Configuration

The app is configured with:
- ✅ JavaScript enabled
- ✅ DOM storage enabled (for localStorage)
- ✅ Database storage enabled
- ✅ Caching enabled (for offline support)
- ✅ Zoom controls
- ✅ Responsive layout
- ✅ Mixed content support

### Offline Support

- Caches web app and data automatically
- Works offline after first load
- Shows cached news when offline
- Detects network status

### Navigation

- Back button navigates WebView history
- Stays within the app (no external browser)
- Handles errors gracefully

### Lifecycle Management

- Pauses WebView when app is backgrounded
- Resumes WebView when app returns
- Cleans up resources on destroy

## Permissions

Required permissions in `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

## Testing

### Test Checklist

- [ ] App launches successfully
- [ ] Web app loads from GitHub Pages
- [ ] News displays correctly
- [ ] Normal/Advanced modes work
- [ ] Refresh button works
- [ ] Clear All button works
- [ ] Offline mode works (airplane mode)
- [ ] Back button navigates correctly
- [ ] localStorage persists data
- [ ] Rotation works correctly

### Test Offline Mode

1. Open app and load news
2. Enable airplane mode
3. Close and reopen app
4. Verify cached news displays
5. Check offline indicator shows

## Building APK

### Debug APK

```bash
./gradlew assembleDebug
```

Output: `app/build/outputs/apk/debug/app-debug.apk`

### Release APK

1. Generate signing key:
```bash
keytool -genkey -v -keystore eternal-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias eternal
```

2. Update `build.gradle`:
```gradle
android {
    signingConfigs {
        release {
            storeFile file("eternal-release-key.jks")
            storePassword "your-password"
            keyAlias "eternal"
            keyPassword "your-password"
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

3. Build:
```bash
./gradlew assembleRelease
```

Output: `app/build/outputs/apk/release/app-release.apk`

## Customization

### App Icon

Replace icons in `res/mipmap/`:
- `ic_launcher.png` (various sizes)
- `ic_launcher_round.png` (various sizes)

### App Name

Edit `res/values/strings.xml`:
```xml
<string name="app_name">Eternal</string>
```

### Theme

Edit `res/values/themes.xml` to customize colors and styles.

### Splash Screen

Add a splash screen by creating `SplashActivity.java` and updating the manifest.

## Troubleshooting

### WebView Not Loading

- Check internet permission in manifest
- Verify GitHub Pages URL is correct
- Check device has internet connection
- Clear app data and try again

### JavaScript Not Working

- Ensure `setJavaScriptEnabled(true)` is called
- Check WebView settings are configured
- Verify web app works in mobile browser

### localStorage Not Persisting

- Ensure `setDomStorageEnabled(true)` is set
- Check app has storage permissions
- Verify data isn't cleared on app close

### Blank Screen

- Check Logcat for errors
- Verify URL is accessible
- Test in mobile browser first
- Check network connectivity

## Distribution

### Google Play Store

1. Create developer account
2. Build signed release APK
3. Create store listing
4. Upload APK
5. Submit for review

### Direct Distribution

1. Build release APK
2. Host on your website
3. Users enable "Unknown sources"
4. Download and install APK

## Updates

To update the app:
1. Increment `versionCode` and `versionName` in `build.gradle`
2. Build new APK
3. Distribute to users

The web app updates automatically from GitHub Pages - no app update needed for content changes!

## Support

For issues:
- Check Android Studio Logcat
- Test web app in mobile browser
- Verify GitHub Pages is accessible
- Check device Android version (min API 24)

---

**Note**: This is a WebView wrapper. The actual app logic runs in the web app hosted on GitHub Pages. No mock data - everything fetches real AI news!
