from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv
import time

# Configure Chrome options to run in the background
options = Options()
options.add_experimental_option("detach", True)

# Initialize Chrome driver with automatic installation
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to grab product names and prices from a URL
def data_grabber(url):
    driver.get(url)  # Open the provided URL

    # Wait for all h3 elements (likely product names) to be present
    h3_elements = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "h3"))
    )

    # Wait for all elements with data-testid='price-final' (likely prices) to be present
    price_elements = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='price-final']"))
    )

    # Extract product names and prices
    products = []
    prices = []
    for h3_element, price_element in zip(h3_elements, price_elements):
        products.append(h3_element.text.strip())  # Extract text and remove leading/trailing whitespace
        prices.append(price_element.text.strip())  # Extract text and remove leading/trailing whitespace

    # Create a list of lists for the CSV data
    return [(product, price) for product, price in zip(products, prices)]

# Define the base URL for product listings
base_url = 'https://www.digikala.com/search/category-shaver/?page='

# Open CSV file in append mode with UTF-8 encoding for proper character handling
with open(r"your csv file that will store data", 'a', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Loop through pages 1 to 10 (inclusive)
    for i in range(1, 10+1): 
        new_url = base_url + str(i)  # Construct the URL for the current page (using string changing instead clicking by selenium; a creative way :) )

        # Call the data_grabber function to get product data
        data = data_grabber(new_url)

        # Write the scraped data to the CSV file
        csv_writer.writerows(data)

        # Add a short delay (10 seconds) between page scraping
        time.sleep(10)

driver.quit() # Close the browser window

print("Data scraped and written to CSV!")

### at the end say how to come through that problem and show it in html of the page 