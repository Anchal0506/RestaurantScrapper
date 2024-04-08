import requests
import re
from bs4 import BeautifulSoup
import csv 

def get_user_input(prompt):
    return input(prompt).strip().lower()

def scrape_restaurants(city):
    url = f'https://www.swiggy.com/city/{city}/best-restaurants'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print('Failed to retrieve the webpage.')
            return

        print(f"Status Code: {response.status_code}")
        with open(f'{city.capitalize()}.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Restaurant Name', 'Rating', 'Cuisine', 'Location'])

            soup = BeautifulSoup(response.text, 'html.parser')
            restaurant_elements = soup.find_all('div', class_='styled__StyledRestaurantGridCard-sc-fcg6mi-0 lgOeYp')

            for restaurant in restaurant_elements:
                details = restaurant.contents[1]
                rating_match = re.search(r'(\d+\.\d+)', details.contents[1].contents[1].text.strip())
                rating = rating_match.group(1) if rating_match else "N/A"
                restaurant_name = details.contents[0].contents[0].text.strip()
                cuisine = details.contents[2].contents[0].text.strip()
                location = details.contents[2].contents[1].text.strip()
                
                print(f'Restaurant Name: {restaurant_name}')
                print(f'Rating: {rating}')
                print(f'Cuisine: {cuisine}')
                print(f'Location: {location}')
                
                writer.writerow([restaurant_name, rating, cuisine, location])

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error Occurred: {err}")
        print(err)

def main():
    city = get_user_input("Enter the city: ")
    scrape_restaurants(city)

if __name__ == "__main__":
    main()
