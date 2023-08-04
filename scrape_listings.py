import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_car_listings(url):
    # Send an HTTP request to the URL
    response = requests.get(url)
    car_listings = []

    if response.status_code == 200:
        listings = json.loads(response.text)['vehicles']
        exit
        for listing in listings:
            # Extract relevant information from the listing
            car_info = {
                'year': listing['year'],
                'name': listing['make']['name'],
                'model': listing['model']['name'],
                'KMs': listing['odometer'],
                'title': str(listing['year']) + " " + listing['make']['name'] + " " + listing['model']['name'],
                'vehicle_id': listing['vehicleId'],
                'description': listing['description'],
                'price': listing['listPrice']
            }
            
            # Download and save the car picture
            main_picture_url = listing['multimedia']['mainPictureCompleteUrl']
            car_info['picture'] = ""

            if main_picture_url:
                resp_pic = requests.get(main_picture_url)


                picture_filename = os.path.basename(str(listing['vehicleId']) + '.jpg')
                picture_path = os.path.abspath(os.path.join('car_pictures', picture_filename))

                with open(picture_path, 'wb') as picture_file:
                    picture_file.write(resp_pic.content)
                
                car_info['picture'] = picture_path  

            car_listings.append(car_info)

        return car_listings

    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        return None

def scrape_listings():
    url = "https://www.vancouverhonda.com/en/used-inventory/api/listing?namedSorting=featuredDESC&limit=24&page=1&imageSize=w400h300c"

    # Create a folder to store car pictures
    if not os.path.exists('car_pictures'):
        os.makedirs('car_pictures')

    # Scrape car listings
    car_listings = scrape_car_listings(url)

    if car_listings:
        # Store the output in a JSON file
        with open("car_listings.json", "w") as json_file:
            json.dump(car_listings, json_file, indent=2)

        print("Car listings scraped and stored in car_listings.json")
    else:
        print("Failed to scrape car listings.")
    return car_listings