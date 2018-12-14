Developer: Yunqi Qian

Welcome! This is an interactive system that serves the purpose to give you some inspirations for your next travel plan.
This program extracts the top 25 destination in the world (rated by TripAdvisor) and the lowest flight cost from your home city to one of the top destination you choose. It also visualize the route on a map so that you have a better visual sense of how long will you travel.

*In terms of using the program*
To start, run the final_project_working_file.py file. The program is fairly easy to use. Simply type in your home city and a list of the top 25 popular destination will show up on your screen in a list. What you can do next is to type in the assigned number of the city you are interested in and a map will pop up in your default browser. The title of the map contains the flights information, which included the lowest prince, direct or indirect, and the departure and arrive dates that have the lowest price. Continue on your next choice by typing in the number in the prompt. If you want to quit the program simply type 404 in the prompt.

*In terms of installation and logistics*
After fork and clone this program, you are welcome to make any additional changes to the files. You will notice that the api return much more valuable information about a specific route that could be relevant to some folks. This is a good starting point to do more creative things with the resources used in this program.

Here are some of the logistics in order to make the program run on its basic functions:
1.You will need to install BeautifulSoup to your drive. Documentation and installation procedures can be found in this link (https://www.crummy.com/software/BeautifulSoup/bs4/doc/).  
2.You will need a Rapid API credential specifically on the Skyscanner API. Search Skyscanner API in Rapid API marketplace, and generate a key token. Copy and Paste your key to the secrets.py file in the rapid_api_key variable.
3. You will need a Google Place credential. Register for a Google Place API and generate your key in the profile page. Copy and Paste your key to the secrets.py file in the google_places_key variable.
4. You will need a plot.ly map credential. Register for a plot.ly map account and generate your key in the profile page. Copy and paste both of your username and api key to the secrets.py file into the plotly_username and plotly_apikey variable.

Note: The above APIs should not generate any cost if used properly. The Skyscanner API has a limit of 500 requests per minute and Google Place API has a limit of 200 per month. Both have the settings to resume the request when reaching the limit so that you don't need to worry of the charges. But that should be the case if a user follows the instructions.

*In terms of caching*
This program has used caching procedures and stored the data in the alternate_advanced_caching.py file, so don't worry about scraping too many times from being charged by Google with too many requests.
All the data you requested from tripadvisor about the top destinations will be saved in top_destination.json file
All the data you requested from Skyscanner API about the route prices and informations will be stored in the skyscanner.json file
All the data requested from Google on the longitude and latitude will be saved in googleplace.json

Note: All of the files will appear after the first run on the main file.

*In terms of requirement to fulfill*
1. At least two data sources used in total (APIs, pages to scrape, datasets you access): Skyscanner API (data can be seen in skyscanner.json file), TripAdvisor Top 25 destination page (data can be seen in top_destination.json file)
2. Everyone should include at least two of the following (second level requirements): Scraping data that comes in HTML or XML form using BeautifulSoup, Accessing a REST API or a new endpoint of a REST API that we have not included in any course (lecture or section) meeting or assignment
3. Everyone should include at least one of the following as part of their project (third level requirement): A clear visualization of data (A plot.ly map)
