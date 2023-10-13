from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time

# Initialize Selenium WebDriver for Firefox
driver = webdriver.Firefox(executable_path='path/to/geckodriver')

# Navigate to the target URL
driver.get('https://operamundi.uol.com.br/opiniao')

# Loop to keep clicking the "Mais" button until it's no longer available
while True:
    try:
        print("Trying to locate 'Mais' button...")
        
        # Wait until the "Mais" button is visible
        load_more_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//button[@data-action="load-more"]'))
        )
        
        print("'Mais' button located. Attempting to click...")
        
        # Scroll the "Mais" button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        
        # Click the button
        load_more_button.click()
        
        print("'Mais' button clicked.")
        
        # Scroll up a little bit to ensure the "Mais" button is in the view window next time
        driver.execute_script("window.scrollBy(0, -100);")
        
        # Allow time for new content to load
        time.sleep(2)
        
    except ElementClickInterceptedException:
        print("ElementClickInterceptedException encountered.")
        
    except NoSuchElementException:
        print("'Mais' button not found. Exiting...")
        break
        
    except Exception as e:
        print("Reached the end or encountered an unknown error:", e)
        break

# Save the final HTML content to a file
final_html = driver.page_source
with open('final_page_opiniao.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

# Close the browser
driver.quit()
