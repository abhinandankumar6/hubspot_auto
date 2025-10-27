from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up Chrome Canary WebDriver with options to avoid detection
options = Options()
options.binary_location = "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"

# Add options to make browser appear more like a regular user session
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Execute script to remove webdriver property
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Open desired webpage
driver.get("https://app-na2.hubspot.com/recycling-bin/123456/restore/0-2")   # Replace with your target URL


time.sleep(2)  # Wait for page to load
# Find username field and enter email
username_field = driver.find_element(By.ID, "username")
username_field.clear()  # Clear any existing text
username_field.send_keys("yourusername06@gmail.com")
print("Entered email address in username field")

# Press Enter after entering username
username_field.send_keys(Keys.RETURN)
print("Pressed Enter after entering username")

time.sleep(3)  # Wait for page to process

# Click on Google sign-in button
google_signin_button = driver.find_element(By.CSS_SELECTOR, '[data-test-id="google-sign-in"]')
google_signin_button.click()
print("Clicked Google sign-in button")

time.sleep(10)  # Wait for page to load

# Create ActionChains object for hover and click actions
actions = ActionChains(driver)

while True:
    table_rows = driver.find_elements(By.TAG_NAME, "tr")
    print(f"Found {len(table_rows)} records to process")
    if len(table_rows) == 0:
        break
    # Find all table rows (tr elements) in the tbody

    # Loop through each table row
    for i, row in enumerate(table_rows):
        try:
            print(f"Processing record {i + 1} of {len(table_rows)}")
            i-=1
            # Hover over the table row to make delete button visible
            actions.move_to_element(row).perform()
            time.sleep(1)  # Increased wait time for hover effect
            
            # Debug: Print all buttons in the row
            all_buttons = row.find_elements(By.TAG_NAME, "button")
            print(f"Found {len(all_buttons)} buttons in row {i + 1}")
            for j, btn in enumerate(all_buttons):
                try:
                    print(f"  Button {j + 1}: text='{btn.text}', tag='{btn.tag_name}', class='{btn.get_attribute('class')}'")
                except:
                    print(f"  Button {j + 1}: Could not get details")
            
            # Try multiple selectors to find the delete button
            delete_button = None
            selectors_to_try = [
                ".//button[contains(text(), 'Delete')]",
                ".//button[contains(text(), 'delete')]",  # Case insensitive
                ".//a[contains(text(), 'Delete')]",  # In case it's a link
                ".//button[contains(@class, 'delete')]",  # By class name
                ".//button[contains(@aria-label, 'Delete')]",  # By aria-label
                ".//*[contains(text(), 'Delete')]",  # Any element with Delete text
                ".//button[contains(@title, 'Delete')]",  # By title attribute
            ]
            
            for selector in selectors_to_try:
                try:
                    delete_button = row.find_element(By.XPATH, selector)
                    print(f"Found delete button using selector: {selector}")
                    break
                except:
                    continue
            
            if delete_button is None:
                print(f"No delete button found for record {i + 1}")
                continue
                
            # Check if button is visible and enabled
            if not delete_button.is_displayed():
                print(f"Delete button not visible for record {i + 1}")
                continue
                
            if not delete_button.is_enabled():
                print(f"Delete button not enabled for record {i + 1}")
                continue
            
            # Scroll the button into view if needed
            driver.execute_script("arguments[0].scrollIntoView(true);", delete_button)
            time.sleep(1)
            
            # Try clicking with JavaScript if regular click fails
            try:
                delete_button.click()
                print(f"Successfully clicked delete button for record {i + 1}")
            except Exception as click_error:
                print(f"Regular click failed for record {i + 1}, trying JavaScript click: {str(click_error)}")
                driver.execute_script("arguments[0].click();", delete_button)
                print(f"Successfully clicked delete button with JavaScript for record {i + 1}")
            
            # Wait for popup to appear and handle it
            time.sleep(2)  # Wait for popup to appear
            
            try:
                # Look for the "Permanently Delete" button in the popup/modal
                permanently_delete_button = None
                popup_selectors = [
                    "//button[@data-test-id='confirm-hard-delete']",  # Specific data-test-id selector
                    "//*[@data-test-id='confirm-hard-delete']",  # Any element with this data-test-id
                    "//button[contains(text(), 'Permanently Delete')]",
                    "//button[contains(text(), 'permanently delete')]",  # Case insensitive
                    "//button[contains(text(), 'Delete') and contains(@class, 'danger')]",  # Danger button
                    "//button[contains(@class, 'danger') and contains(text(), 'Delete')]",
                    "//*[contains(text(), 'Permanently Delete')]",  # Any element
                    "//button[contains(@aria-label, 'Permanently Delete')]",
                    "//button[contains(@title, 'Permanently Delete')]",
                    "//button[contains(text(), 'Delete')]",  # Generic delete button in popup
                    "//div[contains(@class, 'modal')]//button[contains(text(), 'Delete')]",
                    "//div[contains(@class, 'popup')]//button[contains(text(), 'Delete')]",
                    "//div[contains(@class, 'dialog')]//button[contains(text(), 'Delete')]",
                ]
                
                for popup_selector in popup_selectors:
                    try:
                        permanently_delete_button = driver.find_element(By.XPATH, popup_selector)
                        print(f"Found 'Permanently Delete' button using selector: {popup_selector}")
                        break
                    except:
                        continue
                
                if permanently_delete_button is None:
                    print(f"Could not find 'Permanently Delete' button for record {i + 1}")
                    # Try to find any button in a modal/popup for debugging
                    try:
                        modal_buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'modal')]//button | //div[contains(@class, 'popup')]//button | //div[contains(@class, 'dialog')]//button")
                        print(f"Found {len(modal_buttons)} buttons in modal/popup")
                        for j, btn in enumerate(modal_buttons):
                            try:
                                print(f"  Modal Button {j + 1}: text='{btn.text}', class='{btn.get_attribute('class')}'")
                            except:
                                print(f"  Modal Button {j + 1}: Could not get details")
                    except:
                        print("No modal/popup found")
                    continue  # Skip this record if popup button not found
                
                # Check if button is visible and enabled
                if not permanently_delete_button.is_displayed():
                    print(f"'Permanently Delete' button not visible for record {i + 1}")
                    continue
                    
                if not permanently_delete_button.is_enabled():
                    print(f"'Permanently Delete' button not enabled for record {i + 1}")
                    continue
                
                # Scroll the button into view if needed
                driver.execute_script("arguments[0].scrollIntoView(true);", permanently_delete_button)
                time.sleep(2)
                
                # Click the "Permanently Delete" button
                try:
                    permanently_delete_button.click()
                    print(f"Successfully clicked 'Permanently Delete' button for record {i + 1}")
                except Exception as popup_click_error:
                    print(f"Regular click failed for 'Permanently Delete' button, trying JavaScript click: {str(popup_click_error)}")
                    driver.execute_script("arguments[0].click();", permanently_delete_button)
                    print(f"Successfully clicked 'Permanently Delete' button with JavaScript for record {i + 1}")
                
                # Wait for the deletion to complete and popup to close
                #time.sleep(1)
                print(f"Successfully deleted record {i + 1}")
                
            except Exception as popup_error:
                print(f"Error handling popup for record {i + 1}: {str(popup_error)}")
                import traceback
                traceback.print_exc()
                continue  # Continue with next record on popup error
            
            time.sleep(1)  # Wait between records

        except Exception as e:
            print(f"Error processing record {i + 1}: {str(e)}")
            # Print more detailed error information
            import traceback
            traceback.print_exc()
            continue



# Keep the browser window open until user closes it manually
input("Press Enter to close the browser...")
driver.quit()