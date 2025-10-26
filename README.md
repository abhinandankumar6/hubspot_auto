# HubSpot Recycling Bin Automation Script

A Python Selenium automation script designed to automatically delete records from the HubSpot recycling bin. This script automates the process of logging into HubSpot, navigating to the recycling bin, and systematically deleting all records with confirmation.

## 🚀 Features

- **Automated Login**: Handles HubSpot authentication with Google sign-in
- **Smart Record Detection**: Automatically finds and processes table rows
- **Robust Error Handling**: Continues processing even when individual records fail
- **Popup Management**: Handles confirmation dialogs and popups
- **Multiple Fallback Strategies**: Uses various selectors to find elements
- **Detailed Logging**: Comprehensive debug output for troubleshooting
- **Anti-Detection**: Configured to avoid bot detection mechanisms

## 📋 Prerequisites

### Required Software
- **Python 3.7+**
- **Google Chrome Canary** (installed at `/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary`)
- **ChromeDriver** (compatible with your Chrome Canary version)

### Python Dependencies
```bash
pip install selenium
```

### System Requirements
- macOS (script configured for macOS Chrome Canary path)
- Internet connection
- Valid HubSpot account with Google sign-in enabled

## 🛠️ Installation

1. **Clone or Download** this script to your local machine
2. **Install Dependencies**:
   ```bash
   pip install selenium
   ```
3. **Install ChromeDriver**:
   - Download ChromeDriver from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)
   - Ensure it's compatible with your Chrome Canary version
   - Add to your system PATH or place in the same directory as the script

4. **Verify Chrome Canary Installation**:
   - Ensure Chrome Canary is installed at the specified path
   - Update the path in the script if your installation differs

## ⚙️ Configuration

### Basic Configuration
The script requires minimal configuration. Key settings can be modified in the script:

```python
# Update these values as needed
username_field.send_keys("your-email@example.com")  # Line 35
# go to your object and click on actions and then restore. 
# it will take you to your recyclebin. Copy the page url and paste here.
driver.get("https://app-na2.hubspot.com/recycling-bin/12345678/restore/0-2")  # Line 28
```

### Chrome Options
The script includes several Chrome options to avoid detection:
- Disables automation indicators
- Removes webdriver properties
- Disables web security (for testing purposes)
- Disables extensions and sandbox

## 🚀 Usage

### Basic Usage
1. **Run the script**:
   ```bash
   python selenium_automation.py
   ```

2. **Follow the prompts**:
   - The script will open Chrome Canary
   - Navigate to HubSpot login page
   - Enter your email and press Enter
   - Click Google sign-in button
   - Wait for authentication to complete

3. **Monitor the process**:
   - Watch the console output for progress updates
   - The script will show detailed information about each record processed

### Advanced Usage
For debugging or customization, you can modify the script parameters:

```python
# Adjust wait times
time.sleep(10)  # Initial page load wait

# Modify selectors
selectors_to_try = [
    ".//button[contains(text(), 'Delete')]",
    # Add more selectors as needed
]

# Change failure threshold
max_failed_attempts = 5  # Stop after 5 consecutive failures
```

## 📊 Script Workflow

### 1. Initialization
- Sets up Chrome WebDriver with anti-detection options
- Opens HubSpot recycling bin URL
- Removes webdriver properties to avoid detection

### 2. Authentication
- Finds username field and enters email
- Presses Enter to submit
- Clicks Google sign-in button
- Waits for authentication to complete

### 3. Record Processing Loop
- Finds all table rows (`<tr>` elements)
- For each row:
  - Hovers over the row to make delete button visible
  - Searches for delete button using multiple selectors
  - Clicks delete button (with JavaScript fallback)
  - Handles confirmation popup
  - Clicks "Permanently Delete" button
  - Waits for deletion to complete

### 4. Error Handling
- Continues processing even if individual records fail
- Provides detailed error messages and stack traces
- Skips problematic records and moves to the next one

## 🔧 Troubleshooting

### Common Issues

#### 1. ChromeDriver Not Found
**Error**: `WebDriverException: 'chromedriver' executable needs to be in PATH`
**Solution**: 
- Download ChromeDriver and add to PATH
- Or place chromedriver in the same directory as the script

#### 2. Chrome Canary Not Found
**Error**: `WebDriverException: unknown error: cannot find Chrome binary`
**Solution**: 
- Install Google Chrome Canary
- Update the binary path in the script if needed

#### 3. Element Not Found
**Error**: `NoSuchElementException`
**Solution**: 
- Check if the page has loaded completely
- Verify the selectors are correct for the current page structure
- Increase wait times if needed

#### 4. Authentication Issues
**Error**: Login fails or gets stuck
**Solution**: 
- Verify your email address is correct
- Check if Google sign-in is enabled for your HubSpot account
- Ensure you have proper permissions to access the recycling bin

### Debug Mode
The script includes extensive debugging output. Look for:
- Row detection information
- Button discovery details
- Selector matching results
- Error messages with stack traces

## 📝 Output Examples

### Successful Execution
```
Entered email address in username field
Pressed Enter after entering username
Clicked Google sign-in button
Found 26 records to process
Processing record 1 of 26
Found 1 buttons in row 1
  Button 1: text='Delete', tag='button', class='PrivateButton__StyledButton-eRHhiA gflxTx'
Found delete button using selector: .//button[contains(text(), 'Delete')]
Successfully clicked delete button for record 1
Found 'Permanently Delete' button using selector: //button[@data-test-id='confirm-hard-delete']
Successfully clicked 'Permanently Delete' button for record 1
Successfully deleted record 1
```

### Error Handling
```
Processing record 2 of 26
Found 0 buttons in row 2
No delete button found for record 2
Processing record 3 of 26
```

## ⚠️ Important Notes

### Security Considerations
- **Credentials**: Never hardcode sensitive information in production
- **Permissions**: Ensure you have proper permissions to delete records
- **Testing**: Test on a small dataset before running on production data

### Legal and Ethical Considerations
- **Terms of Service**: Ensure compliance with HubSpot's terms of service
- **Data Privacy**: Be mindful of data privacy regulations
- **Rate Limiting**: The script includes delays to avoid overwhelming the server

### Limitations
- **Page Structure Changes**: May break if HubSpot updates their UI
- **Network Issues**: Requires stable internet connection
- **Browser Compatibility**: Designed specifically for Chrome Canary

## 🔄 Maintenance

### Regular Updates
- **ChromeDriver**: Update when Chrome Canary updates
- **Selectors**: May need updates if HubSpot changes their UI
- **Dependencies**: Keep Python packages updated

### Monitoring
- Check console output for errors
- Monitor success rates
- Verify deletions in HubSpot interface

## 📞 Support

### Getting Help
1. **Check Console Output**: Look for detailed error messages
2. **Verify Prerequisites**: Ensure all dependencies are installed
3. **Test Selectors**: Use browser dev tools to verify element selectors
4. **Check Permissions**: Verify HubSpot account permissions

### Common Solutions
- **Update ChromeDriver**: Download latest version
- **Check Internet Connection**: Ensure stable connectivity
- **Verify Account Access**: Confirm recycling bin permissions
- **Review Error Logs**: Check detailed error messages

## 📄 License

This script is provided as-is for educational and automation purposes. Use at your own risk and ensure compliance with all applicable terms of service and regulations.

## 🤝 Contributing

If you encounter issues or have improvements:
1. Check the troubleshooting section
2. Review the debug output
3. Test with a small dataset first
4. Document any new issues or solutions

---

**Disclaimer**: This script is for educational and automation purposes only. Users are responsible for ensuring compliance with HubSpot's terms of service and applicable laws and regulations.
