from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)


# Navigate to the target URL
driver.get('https://operamundi.uol.com.br/politica-e-economia')

# Loop to keep clicking the "Mais" button until it's no longer available
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
        
        # Allow time for new content to load
        time.sleep(2)
        
    except ElementClickInterceptedException:
        print("ElementClickInterceptedException encountered. Removing interfering element...")
        
        # Remove the interfering element by its XPath
        interfering_element = driver.find_element(By.XPATH,"/html/body/div[3]/section[2]/div")
        driver.execute_script("arguments[0].remove();", interfering_element)
        
    except NoSuchElementException:
        print("'Mais' button not found. Exiting...")
        break
        
    except Exception as e:
        print("Reached the end or encountered an unknown error:", e)
        break

# Save the final HTML content to a file
final_html = driver.page_source
with open('final_page_politica_economia.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

# Close the browser
driver.quit()
