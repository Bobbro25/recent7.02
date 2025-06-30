# Chrome Web Store Submission Guide

## 🎉 Your Block Trump Extension is Ready for Submission!

This guide will walk you through submitting your extension to the Chrome Web Store.

## 📁 Package Contents

Your extension package includes:

### Core Extension Files
- `manifest.json` - Extension configuration
- `content.js` - Main blocking functionality
- `content.css` - Styling for blocked content
- `popup.html` - Extension popup interface
- `popup.js` - Popup functionality
- `icons/` - Professional extension icons (16x16, 48x48, 128x128)

### Store Assets
- `promotional_assets/tile_440x280.png` - Store tile image
- `promotional_assets/marquee_1400x560.png` - Featured promotional banner  
- `promotional_assets/screenshot_1280x800.png` - Functionality screenshot
- `STORE_LISTING.md` - Complete store listing content
- `PRIVACY_POLICY.md` - Required privacy policy

## 🚀 Submission Steps

### Step 1: Create Developer Account
1. Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
2. Sign in with your Google account
3. Pay the one-time $5 developer registration fee
4. Complete your developer profile

### Step 2: Create Extension ZIP Package
```bash
# Create the submission ZIP file (excluding development files)
cd chrome-extension-package
zip -r block-trump-extension-v1.0.zip . -x "*.py" "promotional_assets/*" "*.md" "create_*"
```

The ZIP should contain ONLY:
- manifest.json
- content.js
- content.css  
- popup.html
- popup.js
- icons/ (folder with all PNG files)

### Step 3: Upload Extension
1. In Developer Dashboard, click "Add new item"
2. Upload your `block-trump-extension-v1.0.zip` file
3. Wait for upload and initial processing

### Step 4: Complete Store Listing

#### Basic Information
- **Name**: Block Trump Extension
- **Summary**: Block Trump-related content from all websites. Clean browsing experience with proceeds supporting ACLU.
- **Category**: Productivity
- **Language**: English (United States)

#### Detailed Description
Use the content from `STORE_LISTING.md` - copy the "Detailed Description" section.

#### Graphics Assets
Upload these files from `promotional_assets/`:
- **Store Icon**: Use `icons/icon128.png`
- **Screenshots**: Upload `screenshot_1280x800.png`
- **Promotional Tile**: Upload `tile_440x280.png`
- **Marquee**: Upload `marquee_1400x560.png` (if applying for featuring)

#### Additional Details
- **Website**: Your support website URL
- **Support Email**: Your support email
- **Privacy Policy**: Copy content from `PRIVACY_POLICY.md` or host it on your website

### Step 5: Pricing & Distribution
- **Pricing**: Set to $2.50 (as mentioned in description)
- **Countries**: Select all countries or your target markets
- **Mature Content**: No (extension blocks content, doesn't display mature content)

### Step 6: Privacy Practices
Fill out the privacy questionnaire:
- **Does your extension collect user data?**: No
- **Does your extension use analytics?**: No
- **Does your extension use third-party services?**: No

### Step 7: Review & Submit
1. Review all information for accuracy
2. Check that all required fields are completed
3. Click "Submit for Review"

## ⏱ Review Timeline
- **Standard Review**: 1-3 business days
- **First-time Developer**: May take up to 7 days
- **Content Blocking Extensions**: May require additional review

## 📋 Pre-Submission Checklist

- [ ] Extension ZIP contains only necessary files
- [ ] All icons are properly sized and high quality
- [ ] Store listing description is compelling and accurate
- [ ] Privacy policy addresses content blocking functionality
- [ ] Screenshots clearly show extension functionality
- [ ] Support contact information is provided
- [ ] Pricing is set correctly ($2.50)
- [ ] Target markets are selected

## 🔧 Common Issues & Solutions

### Review Rejection Reasons
1. **Metadata Mismatch**: Ensure extension name in manifest matches store listing
2. **Privacy Policy**: Must clearly state no data collection
3. **Permissions**: All requested permissions must be justified
4. **Content Policy**: Ensure extension doesn't violate political content policies

### If Rejected
1. Read rejection email carefully
2. Address all mentioned issues
3. Update extension files or store listing as needed
4. Resubmit for review

## 💰 **Updated Pricing Structure**

### **Basic Version 1.0: $4.98**
- All core Trump content blocking functionality
- Works on all websites
- Toggle enable/disable
- Real-time statistics
- Basic keyword blocking

### **Pro Version 1.0.1: $7.98**
- Everything in Basic version PLUS:
- Custom keyword additions
- Advanced filtering options
- Export/import settings
- Premium support
- Early access to new features

### **Revenue Distribution (Basic $4.98)**:
```
• Chrome Store Fee: 30% ($1.49)
• Your Revenue: 70% ($3.49)  
• ACLU Donation: $2.50 (from gross price)
• Your Net Profit: $0.99 per sale
```

### **Revenue Distribution (Pro $7.98)**:
```
• Chrome Store Fee: 30% ($2.39)
• Your Revenue: 70% ($5.59)
• ACLU Donation: $2.50 (from gross price)  
• Your Net Profit: $3.09 per sale
```

## 📞 Support Resources

- [Chrome Web Store Developer Policies](https://developer.chrome.com/docs/webstore/program-policies/)
- [Extension Manifest Reference](https://developer.chrome.com/docs/extensions/mv3/manifest/)
- [Developer Support](https://support.google.com/chrome_webstore/contact/dev_support)

## 🎯 Post-Launch Tasks

1. **Monitor Reviews**: Respond to user feedback promptly
2. **Track Performance**: Monitor downloads and revenue
3. **Plan Updates**: Gather user feedback for improvements
4. **ACLU Donations**: Set up regular donation schedule
5. **Marketing**: Promote through social media and relevant channels

---

**Your extension is professionally built and ready for the Chrome Web Store! Good luck with your submission! 🚀**