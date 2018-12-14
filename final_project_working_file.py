##importing logistics
from secrets import *
from bs4 import BeautifulSoup
from alternate_advanced_caching import Cache
import requests
from datetime import datetime
import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

#################################
# PART 1: SCRAPING DATA FROM TA #
#################################

CACHE_FNAME = "top_destination.json"
url_to_scrape = "https://www.tripadvisor.com/TravelersChoice-Destinations"
cache_html = Cache(CACHE_FNAME)

while cache_html.get(url_to_scrape) is None:
    data = requests.get(url_to_scrape)
    html_text = data.text
    cache_html.set(url_to_scrape,html_text,10)
    print("DATA NOT IN CACHE, SCRAPING FROM URL NOW")

soup = BeautifulSoup(cache_html.get(url_to_scrape), features="html.parser")
mainnames = soup.find_all("div", class_ = "mainName")
destination_name_lst = []
for mainname in mainnames:
    name = mainname.find("a").text
    destination_name_lst.append(name)
city_name_lst = []
for items in destination_name_lst:
    city_name = items.split(",")[0]
    city_name_lst.append(city_name)
#print(city_name_lst)

##################################################
# PART 2: USING SKYSCANNER API FOR LOWEST PRICES #
##################################################

CACHE_FNAME_API = "skyscanner.json"
cache_api = Cache(CACHE_FNAME_API)

if rapid_api_key == "" or not rapid_api_key:
    print("Your rapid api key is missing from the file. Enter your rapid api key where directed and save the program!")
    exit()

def params_unique_combination(baseurl, params_d):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k != "key":
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

def api_unique_combination(baseurl, params_d):
    alphabetized_keys = params_d.keys()
    res = []
    for k in alphabetized_keys:
        if k != "key":
            res.append(params_d[k])
    return baseurl + "/".join(res) + "?X-RapidAPI-Key=" + rapid_api_key

class CityInfo():
    def __init__(self, citystring):
        self.citystring = citystring

    def return_code_for_city(self):
        baseurl = "http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/US/USD/en-us?"
        params_d = {}
        params_d["X-RapidAPI-Key"] = rapid_api_key
        params_d["query"] = self.citystring
        identifier = params_unique_combination(baseurl, params_d)
        city_info = cache_api.get(identifier)
        if city_info != None:
            print("Data already in cache")
        else:
            requestp = requests.get(baseurl, params=params_d)
            city_info = json.loads(requestp.text)
            #print(city_info)
            cache_api.set(identifier,city_info,10)
        try:
            city_code = city_info["Places"][1]["PlaceId"]
        except:
            city_code = city_info["Places"][0]["PlaceId"]
        return city_code

    def return_airport_name(self):
        baseurl = "http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/US/USD/en-us?"
        params_d = {}
        params_d["X-RapidAPI-Key"] = rapid_api_key
        params_d["query"] = self.citystring
        identifier = params_unique_combination(baseurl, params_d)
        city_info = cache_api.get(identifier)
        if city_info != None:
            print("Data already in cache")
        else:
            requestp = requests.get(baseurl, params=params_d)
            city_info = json.loads(requestp.text)
            #print(city_info)
            cache_api.set(identifier,city_info,10)
        try:
            airport_name = city_info["Places"][1]["PlaceName"]
        except:
            airport_name = city_info["Places"][0]["PlaceName"]
        return airport_name

class SkyscannerApiInput():
    def __init__(self,original_city,destination_city,outbound_date = "anytime",inbound_date="anytime"):
        self.original_city_code = CityInfo(original_city).return_code_for_city()
        self.destination_city_code = CityInfo(destination_city).return_code_for_city()
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date

    def __str__(self):
        format = "{} TO {}: FROM {} TO {}".format(self.original_city_code,self.destination_city_code,self.outbound_date,self.inbound_date)
        return format

    def return_date_price(self):
        baseurl = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/"
        params_d = {}
        headers = {}
        headers["X-RapidAPI-Key"] = rapid_api_key
        headers["Accept"] = "application/json"
        params_d["originPlace"] = self.original_city_code
        params_d["destinationPlace"] = self.destination_city_code
        params_d["outboundPartialDate"] = self.outbound_date
        params_d["inboundPartialDate"] = self.inbound_date
        identifier = api_unique_combination(baseurl, params_d)
        #print(identifier)
        quotes_info = cache_api.get(identifier)
        if quotes_info != None:
            print("Data already in cache")
        else:
            requestp = requests.get(identifier,headers=headers)
            #print(requestp)
            quotes_info = json.loads(requestp.text)
            #print(city_info)
            cache_api.set(identifier,quotes_info,10)

        quotes_dict = {}
        for quote in quotes_info["Quotes"]:
            quoteprice = quote["MinPrice"]
            #print(quoteprice)
            outboundtime = quote["OutboundLeg"]["DepartureDate"]
            inboundtime = quote["InboundLeg"]["DepartureDate"]
            if quote["Direct"] is True:
                direct = "Direct Flight"
            elif quote["Direct"] is False:
                direct = "Indirect Flight"
            outbound_inbound_time = "{} | {},{}".format(direct,outboundtime,inboundtime)
            quotes_dict[outbound_inbound_time]=quoteprice

        return quotes_dict

def sort_lowest_price(quotes_dict):
    sorted_dict_by_value = sorted(quotes_dict.keys(), key=lambda k: quotes_dict[k])
    try:
        lowest_date = sorted_dict_by_value[0]
        lowest_price = quotes_dict[lowest_date]
        pretty_print = "Lowest Price: ${}, Travel Info: {}".format(lowest_price, lowest_date)
        return pretty_print
    except:
        print("No avaliable flight data in the system")



#########################################
# PART 3: USING GOOGLE API FOR GEO INFO #
#########################################
if google_places_key == "" or not google_places_key:
    print("Your google api key is missing from the file. Enter your google api key where directed and save the program!")
    exit()

CACHE_FNAME_GOOGLE_API = "googleplace.json"
cache_google_api = Cache(CACHE_FNAME_GOOGLE_API)

def get_gps_for_airport(airport_name):
    baseurl = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
    params_d = {}
    params_d["key"] = google_places_key
    params_d["input"] = airport_name
    params_d["inputtype"] = 'textquery'
    params_d["fields"] = 'geometry'
    identifier = params_unique_combination(baseurl, params_d)
    geo = cache_google_api.get(identifier)
    if geo != None:
        print("Data already in cache")
    else:
        requestp = requests.get(baseurl, params=params_d)
        geo = json.loads(requestp.text)
        cache_google_api.set(identifier,geo,10)
    try:
        geo_dict = geo['candidates'][0]['geometry']['location']
        geo_format = "{},{}".format(geo_dict["lat"],geo_dict["lng"])
        return geo_format

    except:
        pass


##############################################
# PART 4: USING PLOTLY FOR MAP VISUALIZATION #
##############################################

plotly.tools.set_credentials_file(username=plotly_username, api_key=plotly_apikey)

def plot_sites_for_cities(home_city,destination_city):
    home_city_geo = get_gps_for_airport(CityInfo(home_city).return_airport_name())
    home_city_lst = home_city_geo.split(",")
    home_city_lat = home_city_lst[0]
    home_city_lon = home_city_lst[1]

    destination_geo = get_gps_for_airport(CityInfo(destination_city).return_airport_name())
    destination_lst = destination_geo.split(",")
    destination_lat = destination_lst[0]
    destination_lon = destination_lst[1]

    price_dict = SkyscannerApiInput(home_city,destination_city).return_date_price()
    lowest_price = sort_lowest_price(price_dict)

    trace1 = dict(
            name = 'Route',
            type = 'scattergeo',
            lat = [ home_city_lat, destination_lat ],
            lon = [ home_city_lon, destination_lon ],
            mode = 'lines',
            line = dict(
                width = 1,
                color = 'red',
            ),)

    trace2 = dict(
            name = 'Plot City',
            type = 'scattergeo',
            lat = [ home_city_lat, destination_lat ],
            lon = [ home_city_lon, destination_lon ],
            mode='markers',
            marker=dict(
                size=5,
                color='rgb(242, 177, 172)',
                opacity=0.7
            ),
            text=[home_city,destination_city],
        )

    data = [trace1, trace2]

    min_lat = 10000
    max_lat = -10000
    min_lon = 10000
    max_lon = -10000

    city_lat_total = []
    city_lon_total = []

    city_lat_total.append(home_city_lat)
    city_lat_total.append(destination_lat)
    city_lon_total.append(home_city_lon)
    city_lon_total.append(destination_lon)

    for str_v in city_lat_total:
        v = float(str_v)
        if v < min_lat:
            min_lat = v
        if v > max_lat:
            max_lat = v
    for str_v in city_lon_total:
        v = float(str_v)
        if v < min_lon:
            min_lon = v
        if v > max_lon:
            max_lon = v

    lat_axis = [min_lat -5, max_lat + 5]
    lon_axis = [min_lon - 5, max_lon + 5]

    center_lat = (max_lat+min_lat) / 2
    center_lon = (max_lon+min_lon) / 2

    layout = dict(
            title = 'Your Inspirational Vacational Plan: {} TO {} | {}'.format(home_city,destination_city,lowest_price),
            geo = dict(
                projection=dict( type='equirectangular' ),
                lataxis = dict(range = lat_axis),
                lonaxis = dict(range = lon_axis),
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(100, 217, 217)",
                center = {'lat': center_lat, 'lon': center_lon },
                countrycolor = "rgb(217, 100, 217)",
                countrywidth = 3,
                subunitwidth = 3
            ),
        )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='plot_cities')



################################
# PART 4: PUTTING ALL TOGETHER #
################################

exit_program = False
while not exit_program:
    introduction = print("\n"*3,"Dear user, this is an inspirational interactive system, which serves the purpose to provide suggestions on your travel plans to world's top destinations (rated by TripAdvisor)!")
    home_city = input("Please enter your home city to start the interaction (e.g. Boston, New York City): ")
    instructions = print("Okay, your home city is: ",home_city,"\n","Here's a list of the popular destinations:")
    for i in range(len(city_name_lst)):
        print(i,")", city_name_lst[i])
    while not exit_program:
        option = input("Please input the number of the city you choose here (enter '404' if you want to exit the program):")
        option_num = int(option)
        if option_num in range(len(city_name_lst)):
            destination = city_name_lst[option_num]
            plot_sites_for_cities(home_city,destination)
        elif option_num == 404:
            exit_program = True
        else:
            print("Please enter a valid number to proceed (e.g. 1).")
