import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

def login_facebook(driver, username, password):
    # Replace these with your Facebook login credentials

    driver.get("https://www.facebook.com")
    driver.find_element(By.NAME, "email").send_keys(username)
    driver.find_element(By.NAME, "pass").send_keys(password)
    driver.find_element(By.NAME, "login").click()

def skip_existing_listings(driver, listings):
    driver.get("https://www.facebook.com/marketplace/you/selling")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)

    listings_dup = listings.copy()
    skipped_listings = []
    tbc_listings = []

    for listing in listings_dup:
        xpath_expr = f"//span[contains(text(), '{listing['title']}')]"
        try:
            existing_listing = driver.find_element(By.XPATH, xpath_expr)
            if existing_listing.text == listing['title']:
                print("DEBUG: Existing listing: " + listing['title'] + " will be skipped.")
                skipped_listings.append(listing)                
                listings.remove(listing)
        except Exception as err:
            print("DEBUG: Listing doesn't exist")
            tbc_listings.append(listing)
            continue
    return {'skipped_listings': skipped_listings, 'tbc_listings': tbc_listings}


def create_facebook_listings(driver, data):
    success_listings = []
    failed_listings = []
    for car_data in data:
        try:  
            print("DEBUG: Starting listing creation for Car: " + str(car_data['year']) + " " + car_data['name'] + " " + car_data['model'])

            driver.get("https://www.facebook.com/marketplace/create/vehicle") 
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//label[@role='combobox']")))
            dropdowns = driver.find_elements(By.XPATH, f"//label[@role='combobox']")

            # Vehicle Type = Car/Vans
            listing_dropdown = dropdowns[0] 
            listing_dropdown.click()
            listing_dropdown.send_keys(Keys.ARROW_DOWN)
            listing_dropdown.send_keys(Keys.ENTER)

            print("DEBUG: Vehicle Type: Done")

            dropdowns = driver.find_elements(By.XPATH, f"//label[@role='combobox']")    

            # Year
            year_dropdown = dropdowns[1]
            year_dropdown.click()
            year_dropdown.send_keys(Keys.ARROW_DOWN)
            for _ in range(2024 - int(car_data["year"])):
                year_dropdown.send_keys(Keys.ARROW_DOWN)
            year_dropdown.send_keys(Keys.ENTER)
            print("DEBUG: Year: Done")

            # Make
            xpath_expr = f"//*[contains(text(), 'Make')]"
            input_element = driver.find_elements(By.XPATH, xpath_expr)
            input_span = next((element for element in input_element if element.tag_name == 'span'), None)
            input = input_span.find_element(By.XPATH, f"following-sibling::input")
            input.click()
            input.send_keys(car_data["name"])
            print("DEBUG: Make: Done")

            # Model
            xpath_expr = f"//*[contains(text(), 'Model')]"
            input_element = driver.find_elements(By.XPATH, xpath_expr)
            input_span = next((element for element in input_element if element.tag_name == 'span'), None)
            input = input_span.find_element(By.XPATH, f"following-sibling::input")
            input.click()
            input.send_keys(car_data["model"])
            print("DEBUG: Model: Done")

            # Mileage
            xpath_expr = f"//*[contains(text(), 'Mileage')]"
            input_element = driver.find_elements(By.XPATH, xpath_expr)
            input_span = next((element for element in input_element if element.tag_name == 'span'), None)
            input = input_span.find_element(By.XPATH, f"following-sibling::input")
            input.click()
            input.send_keys(car_data["KMs"])
            print("DEBUG: Mileage: Done")

            # Price
            xpath_expr = f"//*[contains(text(), 'Price')]"
            input_element = driver.find_elements(By.XPATH, xpath_expr)
            for element in input_element:
                try:
                    input = element.find_element(By.XPATH, f"following-sibling::input")
                except Exception as er:
                    continue
            input.click()
            input.send_keys(car_data["price"])
            print("DEBUG: Price: Done")

            # Description
            xpath_expr = f"//*[contains(text(), 'Description')]"
            input_element = driver.find_elements(By.XPATH, xpath_expr)
            for element in input_element:
                try:
                    input = element.find_element(By.XPATH, f"following-sibling::textarea")
                except Exception as er:
                    continue
            input.click()
            input.send_keys(car_data["description"] if car_data["description"] else '')
            print("DEBUG: Description: Done")

            # Body Style
            bs_dropdown = dropdowns[2]
            bs_dropdown.click()
            for _ in range(10):
                bs_dropdown.send_keys(Keys.ARROW_DOWN)
            bs_dropdown.send_keys(Keys.ENTER)
            print("DEBUG: Body Style: Done")

            # Condition
            vh_dropdown = dropdowns[3]
            vh_dropdown.click()
            for _ in range(5):
                vh_dropdown.send_keys(Keys.ARROW_DOWN)
            vh_dropdown.send_keys(Keys.ENTER)
            print("DEBUG: Condition: Done")

            # Fuel
            fuel_dropdown = dropdowns[4]
            fuel_dropdown.click()
            for _ in range(5):
                fuel_dropdown.send_keys(Keys.ARROW_DOWN)
            fuel_dropdown.send_keys(Keys.ENTER)
            print("DEBUG: Fuel: Done")

            # Picture
            xpath_expr = f"//input[@type='file'][contains(@accept,'image')]"
            input_element = driver.find_element(By.XPATH, xpath_expr)
            time.sleep(3)

            input_element.send_keys(car_data["picture"])
            time.sleep(10)

            print("DEBUG: Picture Upload: Done")

            # Press Next Button
            xpath_expr = f"//*[contains(text(), 'Next')]"
            input_element = driver.find_element(By.XPATH, xpath_expr)
            input_element.click()
            time.sleep(5)

            print("DEBUG: Next Button Press: Done")

            # Press Publish Button
            xpath_expr = f"//*[contains(text(), 'Publish')]"
            input_element = driver.find_element(By.XPATH, xpath_expr)
            input_element.click()
            print("DEBUG: Publish Button Press: Done")

            print("DEBUG: Car: " + str(car_data['year']) + " " + car_data['name'] + " " + car_data['model'] + " listed successfully.")
            time.sleep(10)

            success_listings.append(car_data)

        except Exception as e:
            print("DEBUG: Error with " + car_data['title'])
            print(f"Error: {e}")
            failed_listings.append(car_data)
            continue
    return {'success': success_listings, 'failed': failed_listings}

def post_fb(username, password):
    # Replace 'car_details.json' with the actual path to your JSON file
    json_file = "car_listings.json"
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)  # You can use Firefox WebDriver as well

    login_facebook(driver, username, password)
    time.sleep(3)

    with open(json_file, "r") as file:
        data = json.load(file)
        listings_seg = skip_existing_listings(driver, data)
        post_fb_results = create_facebook_listings(driver, listings_seg['tbc_listings'])
        post_fb_results['skipped'] =  listings_seg['skipped_listings']
    
    return post_fb_results
