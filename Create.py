import requests, json
from tkinter import *
from functools import partial

in_USA = False 

# Gather U.S. location information
while in_USA == False:
  user_input = input("Enter an address, street name, zip code, significant landmark, or state in the United States: ") 



  # This code takes inspiration from the Nominatim API, which allows users to access the longitude and latitude of a place from its name or address. 
  # Nominatim 4.2.1. Nominatim API. Accessed March 16, 2023, from https://nominatim.org/release-docs/latest/api/Search/
  # requests 2.28.2. 2023 Python Software Foundation. Accessed March 16, 2023, from https://requests.readthedocs.io/en/latest/user/quickstart/

# This function returns the exact longitude and latitude of the place that the user entered
  def geocode():
    r = requests.get(f'https://nominatim.openstreetmap.org/search?q={user_input}&format=json')
    return r 


  data = geocode().json() 

  # Iterate through elements in the JSON file to find latitude and longitude
  for key in data[0]: 
      if key == "lat":
          lat = (data[0][key]) 
      elif key == "lon":
          long = (data[0][key]) 
      elif key == "display_name": 
          entered_place = (f'Place You Entered: {data[0][key]}') 
  if "United States" in entered_place: 
    in_USA = True
  else: 
    print("Please enter a valid United States address, street name, zip code, significant landmark, or state.") 
    continue # return to the beginning of the while loop


# Use the National Weather Service API to get weather information for the entered location
# National Weather Service. Weather.gov. Accessed March 16, 2023, from https://www.weather.gov/documentation/services-web-api

url = f'https://api.weather.gov/points/{lat},{long}' 

r = requests.get(url) 
information = json.loads(r.text) 

my_dict = information['properties'] 


for key in my_dict: 
  if key == "forecast": 
    weather_info = (my_dict[key]) 

# Gather weather data for the location
r1 = requests.get(weather_info) 
forecast = json.loads(r1.text) 
parse = forecast['properties']
daily_data = parse['periods'] 



# Parse and store weather data for each day

def parse_data(): 
  x = 0 
  global Forecast_Information 

  Forecast_Information = [] 
  dict2 = daily_data[x]
  for x in range(len(daily_data)): 
    for key in dict2: 
        index1 = daily_data[x][key]
        if key == 'name':
            Day = index1 
        elif key == 'temperature':
            Temperature = index1
        elif key == "detailedForecast": 
            Forecast = index1 
    Forecast_Information.append([Day, f'{Temperature} degrees Fahrenheit.', Forecast]) 

parse_data()

# Python Software Foundation 2023. tkinter - Python interface. Accessed March 17, 2023 https://docs.python.org/3/library/tkinter.html
# Takes inspiration from GeeksForGeeks tkinter Python introduction
# GeeksForGeeks. akshay_sharma08. Accessed March 19, 2023 https://www.geeksforgeeks.org/create-first-gui-application-using-python-tkinter/
# GeeksForGeeks. abhigoya. Accessed March 19, 2023 https://www.geeksforgeeks.org/how-to-use-images-as-backgrounds-in-tkinter/
# Stack Overflow. ignoramus. Accessed March 19, 2023. https://stackoverflow.com/questions/2297336/tkinter-specifying-arguments-for-a-function-thats-called-when-you-press-a-butt

# Create a graphical user interface(GUI) using tkinter
root = Tk()
root.title("Weather Forecaster")
root.geometry('1920x1080') 

# Set the background of the GUI
background = PhotoImage(file = "weather.png")
image = Label(root, image = background) 
image.place(x=0,y=0)

# Create a label to display the user's entered place
prompt = Label(root, text = f"{entered_place}", bg="sky blue")
prompt.grid() 

# This function creates buttons for all 14 days

def create_button(y):
    btn = Button(root, text = f'{Forecast_Information[y][0]}', command = partial(text, Forecast_Information[y]), width = 13) 
    Forecast_Information[y].append((y)) 
    if y == 0: 
        btn.place(x=15, y = 50) 
    else: 
        btn.place(x=15, y= (y+1) * 50) 

# This function formats and displays weather information when the button is clicked

def text(word): 
  text1 = "" 
  for x in word:
    text1 = text1 + ' ' + str(x) 
  remove1 = text1.split() 
  if remove1[1] == "Night" or remove1[1] == "Afternoon": 
    text1 = (remove1[2:]) 
  else:           
    text1 = (remove1[1:]) 
  index = text1[:-1] 
  label = Label(root, text = index, bg="sky blue") 
  a = 130 
  label_dict = {
    "0": (a, 50), "1": (a, 100), "2": (a, 150), "3": (a, 200), "4": (a, 250), "5": (a, 300), "6": (a, 350), "7": (a, 400), "8": (a, 450), "9": (a, 500), "10": (a, 550), "11": (a, 600), "12": (a, 650), "13": (a, 700)
  }
  a = text1[-1] 
  if a in label_dict: 
    label.place(x = label_dict[a][0], y = label_dict[a][1]) 


# Create the buttons for each day

create_button(0) 
create_button(1) 
create_button(2)
create_button(3) 
create_button(4) 
create_button(5)
create_button(6)
create_button(7)
create_button(8) 
create_button(9) 
create_button(10) 
create_button(11) 
create_button(12)
create_button(13) 

# Tutorialspoint. How to put a Tkinkter window on top of others? Dev Prakash Sharma. Accessed March 19, 2023. https://www.tutorialspoint.com/how-to-put-a-tkinter-window-on-top-of-the-others
root.attributes('-topmost', True) # make the tkinter window the the active window
root.mainloop() # start the tkinter window
