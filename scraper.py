# Import necessary libraries
import requests
import re
from bs4 import BeautifulSoup 
import csv # Import the csv module

# Open (or create) a CSV file with write permissions
with open('Michelin_Restaurants_USA.csv', 'w', newline='') as file:
    writer = csv.writer(file) # Create a csv writer object
    writer.writerow(["Name", "Distinction", "Cuisine"]) # Write the header row

    for i in range(1, 78):
        # The URL of the website you want to scrape
        url = "https://guide.michelin.com/us/en/selection/united-states/restaurants/page/" + str(i)

    # Send a GET request to the website
	# The code inside the 'try' block is executed
        try: 
            response = requests.get(url)
            response.raise_for_status() 
        except requests.exceptions.HTTPError as errh:
            response = requests.get(url) 

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for the specific HTML tags that contain the restaurant info
        restaurants = soup.find_all('div', class_="card__menu-content card__menu-content--flex js-match-height-content")

        # Loop through the list of restaurant tags
        for restaurant in restaurants: 
            # Extract the restaurant's name
            name = restaurant.find('h3', class_='card__menu-content--title pl-text pl-big js-match-height-title').text.strip() 
            # Extract the restaurant's stars and cuisine
            stars = str(restaurant.find('img', class_='michelin-award'))
            if stars.count("1star") == 3:
                distinction = "3 Stars"
            elif stars.count("1star") == 2:
                distinction = "2 Stars"
            elif stars.count("1star") == 1:
                distinction = "1 Star"
            elif stars.find("bib-gourmand") != -1:
                distinction = "Bib Gourmand"
            else:
                distinction = " "

            cuisine = re.findall('[a-zA-Z]+', restaurant.find('div', class_='card__menu-footer--price pl-text').text)[0]
            # Save the name, distinction and cuisine
            writer.writerow([name, distinction, cuisine])
