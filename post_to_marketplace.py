import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

def login_facebook(driver):
    # Replace these with your Facebook login credentials
    username = "abhilashmhaisne@gmail.com"
    password = "LorikCanaar_123"

    driver.get("https://www.facebook.com")
    driver.find_element(By.NAME, "email").send_keys(username)
    driver.find_element(By.NAME, "pass").send_keys(password)
    driver.find_element(By.NAME, "login").click()

def skip_existing_listings(driver, listings):
    driver.get("https://www.facebook.com/marketplace/you/selling")
    listings_dup = listings

    for listing in listings_dup:
        xpath_expr = f"//*[contains(text(), '{listing['title']}')]"
        try:
            existing_listing = driver.find_element(By.XPATH, xpath_expr)
            if existing_listing.text == listing.title:
                listings.remove(listing)
                print("DEBUG: Existing listing: " + listing['text'] + " will be skipped.")
        except Exception as err:
            print("DEBUG: Listing doesn't exist")
            continue
    return listings


def create_facebook_listing(driver, data):
    try: 
        login_facebook(driver)

        for car_data in data: 
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

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Replace 'car_details.json' with the actual path to your JSON file
    json_file = "car_listings.json"
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)  # You can use Firefox WebDriver as well

    with open(json_file, "r") as file:
        data = json.load(file)
        create_facebook_listing(driver, skip_existing_listings(driver, data))
