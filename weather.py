
import requests, json
from tkinter import *
from functools import partial

in_USA = False 


while in_USA == False:
  user_input = input("Enter a location in the United States: ") 

# Call the Nominatim API to retrieve longitude and latitude data for entered location
  def geocode():
    r = requests.get(f'https://nominatim.openstreetmap.org/search?q={user_input}&format=json', headers={'User-Agent': 'Mozilla/5.0'})
    return r 

  data = geocode().json() 

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
    continue 


# Retrieve weather data through the National Weather Service's API

url = f'https://api.weather.gov/points/{lat},{long}' 

r = requests.get(url) 
information = json.loads(r.text) 

my_dict = information['properties'] 


for key in my_dict: 
  if key == "forecast": 
    weather_info = (my_dict[key]) 

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

# Create a graphical user interface(GUI) using Tkinter
root = Tk()
root.title("Weather Forecaster")
root.geometry('1920x1080') 


background = PhotoImage(file = "weather.png")
image = Label(root, image = background) 
image.place(x=0,y=0)

prompt = Label(root, text = f"{entered_place}", bg="sky blue")
prompt.grid() 

# Create buttons for each day

def create_button(y):
    btn = Button(root, text = f'{Forecast_Information[y][0]}', command = partial(text, Forecast_Information[y]), width = 13) 
    Forecast_Information[y].append((y)) 
    if y == 0: 
        btn.place(x=15, y = 50) 
    else: 
        btn.place(x=15, y= (y+1) * 50) 

# Display weather data whenever button is clicked

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


root.attributes('-topmost', True) 
root.mainloop() 
