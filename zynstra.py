import requests, json, math

from sympy import false

class colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


## SETUP 
api_candidate = '34'
api_endpoint = 'http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api'

api_cities = api_endpoint + '/cities'
api_weather = api_endpoint + '/weather/%s' % api_candidate
day_list = ['monday' , 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

# response_API_weather = requests.get(api_weather + '/edinburgh')
# print(response_API_weather.text)
# weather_json = json.loads(response_API_weather.text)
# print("Fri in edinburgh: ", json.dumps(weather_json['friday'][:2], indent=2))
# print(len(weather_json['friday']))

def run_program():
    print('\n')
    print(colours.OKGREEN + 'Welcome to the weather checking program' + colours.RESET)


    get_temperature('bath', 10, 'wednesday')
    q1city = 'Bath'
    q1time = 10
    q1day = 'wednesday'
    print('((Question 1)) The temperature in {} at {}:00 on {} is: '.format(q1city, q1time, q1day), end = ' ') 
    print(colours.OKBLUE + colours.BOLD + str(get_temperature(q1city, q1time, q1day)) + colours.RESET)

    q2city = 'Edinburgh'
    q2day = 'FRIDAY'
    q2pressure = 1000
    print('((Question 2)) The pressure in {} on {} falls below {} millibars: '.format(q2city, q2day, q2pressure), end = ' ') 
    print(colours.OKBLUE + colours.BOLD + str(get_pressure_below(q2city, q2pressure, q2day)) + colours.RESET)

    q3city = 'CARDIFF'
    print('((Question 3)) The median temperature of the week in {} is: '.format(q3city), end= ' ')
    print(colours.OKBLUE + colours.BOLD + str(get_median_temp(q3city)) + colours.RESET)

    print('((Question 4)) The highest wind speed recorded this week was in: ', end = ' ')
    print(colours.OKBLUE + colours.BOLD + str(get_highest_wind()) + colours.RESET)

    print('((Question 5)) It will snow in at least one of the cities this week: ', end = ' ')
    print(colours.OKBLUE + colours.BOLD + str(snow_check()) + colours.RESET)
    # print(colours.OKBLUE + colours.BOLD + str(snow_check()) + colours.RESET)

    return

def get_temperature(city, time, day):
    weather_check = requests.get(api_weather + '/' + city.lower()) # object not subscriptable error due to not loading json obj first
    check_json = json.loads(weather_check.text)
    # print(json.dumps(check_json[day][:10], indent=2))
    # print('\n')
    # print(json.dumps(check_json[day][time-1], indent=1))

    temperature = check_json[day.lower()][time-1]['temperature']
    # print(type(check_json[day][time-1])) # know its a dictionary so to access the value we want is simply dict['value']

    return temperature

def get_pressure_below(city, millibars, day):
    is_below = False

    pressure_check = requests.get(api_weather + '/' + city.lower())
    check_json = json.loads(pressure_check.text)
    day_list = check_json[day.lower()]
    # print(json.dumps(day_list[:24], indent=1))
    for i in day_list:
        if(i['pressure'] < millibars):
            is_below = True

    return is_below

def get_median_temp(city):
    json_temp = json.loads(requests.get(api_weather + '/' + city.lower()).text)
    temperature_list = []
    # print(json_temp.keys()) # checking keys after knowing its a dict, keys are days
    for day in json_temp.keys():
        for i in json_temp[day]:
            temperature_list.append(i['temperature'])

    # print(len(temperature_list)) # know i have temperatures of all days now
    temperature_list.sort()
    mid_index = math.floor(len(temperature_list)/2)  

    return temperature_list[mid_index]

def get_highest_wind():
    city = ''
    
    # print(json.dumps(cities['cities'], indent=1))
    city_wind_speed = {} # create empty dict
    
    cities = json.loads(requests.get(api_cities).text)
    cities = sorted(cities['cities'])

    for city in cities:
        json_temp = json.loads(requests.get(api_weather + '/' + city.lower()).text)
        wind_speed_list = []
        for day in day_list:
            for i in json_temp[day]:
                wind_speed_list.append(i['wind_speed'])
        wind_speed_list.sort()
        city_wind_speed[city] = wind_speed_list[-1]

    # print(json.dumps(city_wind_speed, indent=1))

    # https://docs.python.org/3/library/functions.html#max 'If multiple items are maximal, the function returns the first one encountered. '
    city = max(city_wind_speed, key=city_wind_speed.get) # organised it alphabetically above as max returns the first value found 

    return city

# Checking to see if there is at least one city, that at one time from one day has a temp of < 2 and a precip value of > 1
def snow_check():
    is_snow = False
    cities = json.loads(requests.get(api_cities).text)
    cities = cities['cities']

    for city in cities:
        json_temp = json.loads(requests.get(api_weather + '/' + city.lower()).text)
        for day in day_list:
            for i in json_temp[day]:
                if (i['temperature'] < 2 & i['precipitation'] > 0):
                    is_snow = True

    return is_snow

run_program()