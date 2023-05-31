# Beliz Yazıcı-20210601066, Aykan Berk Ayvazoğlu-20210601007, Utku Mert Çırakoğlu-20210601017
# -*- coding: utf-8 -*-
import io
import tkinter.ttk
from tkinter import Tk, Frame, Menu, PhotoImage, Label, Button, Entry, StringVar, messagebox
from PIL import ImageTk, Image
import requests
from datetime import datetime as dt, timedelta, date

cities = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan",
              "Artvin",
              "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur",
              "Bursa",
              "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan",
              "Erzurum",
              "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkâri", "Hatay", "Iğdır", "Isparta", "İstanbul",
              "İzmir","Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kilis", "Kırıkkale",
              "Kırklareli",
              "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş",
              "Nevşehir",
              "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", "Sivas",
              "Şırnak", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"]

try:
    """This block deals with reading from a save. The file it looks for is 'settings.txt'.
    The file should have two lines, the first containing 'temperature_unit=something'
    and the second containing 'fav_city=anotherthing'. The guide words are there to ease manual editing, and not actually
    required. The system regenerates the guides on save. The first line must be either 'Celsius' or 'Fahrenheit',
    and the second must be in the list above. In any case the reading section goes wrong,
    the tempunit defaults to 'Celsius' and fav_city defaults to an empty string."""

    print("-----LOADING PREFERENCES-----")
    settings = open('settings.txt', encoding='utf-8') # Make sure all file operations are encoded with UTF-8. Turkish characters otherwise get to be an issue.
    settinglist = settings.readlines()
    settings.close()

    # Formatting the strings, stripping \n and guiding objects, technically, if the guides don't exist, it won't matter
    settinglist[0] = settinglist[0].replace('temperature_unit=','')
    settinglist[0] = settinglist[0].rstrip()
    settinglist[1] = settinglist[1].replace('fav_city=','')
    settinglist[1] = settinglist[1].split()[0] # Take first word only, because the API returns "... Province" on some cities
    settinglist[1] = settinglist[1].rstrip()

    if settinglist[0] == "Celsius" or settinglist[0] == "Fahrenheit": # The 'or' clauses need to be separate, or unintended effects occur
        tempunit = settinglist[0]
        print("Temperature setting read from file: " + settinglist[0])
    else:
        tempunit = "C" # Assures that C is used if anything goes wrong with it
    if settinglist[1] in cities:
        favcity = settinglist[1]
        print("Favorite city read from file: " + favcity)

except FileNotFoundError:
    print("File not found. Loading defaults...")
    tempunit = "C"
    favcity = ""
except IndexError:
    print("File is not valid. Loading defaults...")
    tempunit = "C"
    favcity = ""
    settings.close()

print("-----LOADING PREFERENCES DONE-----")

try:
    """This block here loads an API key to the memory to use with the system. It currently checks if it
    can read from the file, as well as if the pulled string is nonempty. It does not check the validity
    of the API key. This check could be added, however, we are already shipping this project with a key
    and there shouldn't be any complications whatsoever about this."""

    print("-----LOADING API KEY-----")
    keyfile = open('.apikey')
    API_KEY = keyfile.readline()
    if API_KEY != '':
        print("Content read from .apikey file.")
    keyfile.close()
    print("-----LOADING API KEY DONE-----")
except:
    print("API keyfile cannot be read. Make sure that .apikey file exists and the file contains only the key string.")
    exit(0)

class Temperature:

    day_temp_value = 0.0
    night_temp_value = 0.0
    wind_speed = 0.0
    temp_unit = "Celsius"
    temp_time = date(1,1,1)

    def __init__(self, dtval=0.0, ntval=0.0, wspeed=0.0, tunit="Celsius", dtime=date.today()):
        if isinstance(dtval, float):
            self.day_temp_value = dtval
        if isinstance(ntval, float):
            self.night_temp_value = ntval
        if isinstance(wspeed, float):
            self.wind_speed = wspeed
        if tunit == "Celsius" or tunit == "Fahrenheit":
            self.temp_unit = tunit
        if isinstance(dtime, dt):
            self.temp_time = dtime

    def toggle(self):
        if self.temp_unit == "Celsius":
            self.day_temp_value = celsius_to_fahrenheit(self.day_temp_value)
            self.night_temp_value = celsius_to_fahrenheit(self.night_temp_value)
            self.temp_unit = "Fahrenheit"

        elif self.temp_unit == "Fahrenheit":
            self.day_temp_value = fahrenheit_to_celsius(self.day_temp_value)
            self.night_temp_value = fahrenheit_to_celsius(self.night_temp_value)
            self.temp_unit = "Celsius"

    def print(self):
        print("Date: " + str(self.temp_time))
        print("Day temperature: " + str(self.day_temp_value))
        print("Night temperature: " + str(self.night_temp_value))
        print("Unit: " + self.temp_unit)
        print("Wind speed: " + str(self.wind_speed) + " m/s")

#Initializing objects
today_temp = Temperature()
today_temp.temp_time = date.today()
today_temp.temp_unit = tempunit

tomorrow_temp = Temperature()
tomorrow_temp.temp_time = (date.today() + timedelta(days=1))
tomorrow_temp.temp_unit = tempunit

dayaftertomorrow_temp = Temperature()
dayaftertomorrow_temp.temp_time = (date.today() + timedelta(days=2))
dayaftertomorrow_temp.temp_unit = tempunit

threedays = [today_temp, tomorrow_temp, dayaftertomorrow_temp]
futuredays = [tomorrow_temp, dayaftertomorrow_temp]

day_temp_holder = Temperature()
night_temp_holder = Temperature()

# creating window
r = Tk()
r.geometry('414x636')
r.configure(bg='#77DCEB')
r.title('Weather App')

menubar = Menu(r)
r.config(menu=menubar)


def commands():
    pass


def file_func():
    hide_all_frames()
    file_new_frame.pack(fill="both", expand=1)


def hide_all_frames():
    file_new_frame.pack_forget()


def celsius_to_fahrenheit(celsius):
    fahrenheit = celsius * (9/5) + 32
    return fahrenheit


def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5 / 9
    return celsius
    

def toggle_temperature_unit():
    global threedays
    for x in threedays:
        x.toggle()

    if today_temp.temp_unit == "Celsius": # Needs to be updated to correct labeling
        temperature_day_lbl.config(text=f"{round(today_temp.day_temp_value,1)}°C")
        temperature_night_lbl.config(text=f"{round(today_temp.night_temp_value, 1)}°C")
    else:
        temperature_day_lbl.config(text=f"{round(today_temp.day_temp_value,1)}°F")
        temperature_night_lbl.config(text=f"{round(today_temp.night_temp_value, 1)}°F")

    for t in futuredays:
        t.print()
    today_temp.print()


    
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()


    try:
        location = data['name']
        day_temp_holder.temp_unit = "Celsius" # Resetting holders to Celsius in case they're stuck at Fahrenheit from a prior call
        night_temp_holder.temp_unit = "Celsius"
        day_temp_holder.day_temp_value = round(data['main']['temp_max'] - 273.15) # This data always starts out as Kelvin, so -273.15 degrees to convert to Celsius
        night_temp_holder.night_temp_value = round(data['main']['temp_min'] - 273.15)
        description = data['weather'][0]['description']
        icon_url = f"http://openweathermap.org/img/w/{data['weather'][0]['icon']}.png"  # there should be image for night weather too!!!
        today_temp.wind_speed = data['wind']['speed']

        if today_temp.temp_unit == "Fahrenheit":
            day_temp_holder.toggle()
            night_temp_holder.toggle()

        today_temp.day_temp_value = day_temp_holder.day_temp_value
        today_temp.night_temp_value = night_temp_holder.night_temp_value

        global tomorrow_temp
        global dayaftertomorrow_temp
        global futuredays
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()

        dayurl = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
        dresponse = requests.get(dayurl).json()
        date_var = (date.today() + timedelta(days=1))
        date_ctr = 0
        while date_var <= (date.today() + timedelta(days=2)):
            tomorrowstamps = []
            for x in dresponse['list']:
                if dt.fromtimestamp(x['dt']).date() == (date_var):
                    tomorrowstamps.append(x)

            if futuredays[date_ctr].temp_unit == "Celsius":
                futuredays[date_ctr].day_temp_value = round(
                    ((tomorrowstamps[3]['main']['temp_min'] + tomorrowstamps[3]['main']['temp_max']) / 2) - 273.15, 2)
                futuredays[date_ctr].night_temp_value = round(
                    ((tomorrowstamps[7]['main']['temp_min'] + tomorrowstamps[7]['main']['temp_max']) / 2) - 273.15, 2)
                futuredays[date_ctr].wind_speed = round(
                    (tomorrowstamps[3]['wind']['speed'] + tomorrowstamps[7]['wind']['speed']) / 2, 2)

            if futuredays[date_ctr].temp_unit == "Fahrenheit":
                futuredays[date_ctr].toggle()  # Sets it back to C
                futuredays[date_ctr].day_temp_value = round(
                    ((tomorrowstamps[3]['main']['temp_min'] + tomorrowstamps[3]['main']['temp_max']) / 2) - 273.15, 2)
                futuredays[date_ctr].night_temp_value = round(
                    ((tomorrowstamps[7]['main']['temp_min'] + tomorrowstamps[7]['main']['temp_max']) / 2) - 273.15, 2)
                futuredays[date_ctr].wind_speed = round(
                    (tomorrowstamps[3]['wind']['speed'] + tomorrowstamps[7]['wind']['speed']) / 2, 2)
                futuredays[date_ctr].toggle()  # Toggles all above values to F

            date_var += timedelta(days=1)
            date_ctr += 1

        location_lbl.config(text=location)
        if today_temp.temp_unit == "Celsius":
            temperature_day_lbl.config(text=f"{round(today_temp.day_temp_value,1)}°C")
            temperature_night_lbl.config(text=f"{round(today_temp.night_temp_value, 1)}°C")
        else:
            temperature_day_lbl.config(text=f"{round(today_temp.day_temp_value,1)}°F")
            temperature_night_lbl.config(text=f"{round(today_temp.night_temp_value, 1)}°F")

        descr_lbl.config(text=f"{description}")
        date_lbl.config(text=f"{today_temp.temp_time}")
        windday_speed_lbl.configure(text=f"{today_temp.wind_speed}m/s")

        # loading the weather icon from the URL
        response = requests.get(icon_url)
        icon_data = response.content
        icon_image = Image.open(io.BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_lbl.config(image=icon_photo)
        icon_lbl.image = icon_photo

        for t in futuredays: # Replace these with correct frame functions
            t.print()
        today_temp.print()

    except KeyError:
        messagebox.showerror("Error", "City not found")


def save(temperatureunit, favoritecity):
    """This one handles saving to the file. It pulls the current city's name and the unit of temperature,
    and then **overwrites** the settings file with the strings, with the guides added."""

    savesettings = open('settings.txt', 'w', encoding='utf-8')
    temperatureunit_guide = 'temperature_unit=' + temperatureunit
    favoritecity_guide = 'fav_city=' + favoritecity
    savesettings.write(temperatureunit_guide)
    savesettings.write('\n')
    favoritecity_guide_enc = favoritecity_guide.encode('utf-8')
    savesettings.write(favoritecity_guide_enc.decode('utf-8'))
    savesettings.close()


def search():
    city = selected_city.get()
    result = get_weather(city)
    if result is None:
        return

    icon_url, temperature, wind_speed, description, city = result
    location_lbl.configure(text=f'{city}')

    img = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(img)
    icon_lbl.configure(image=icon)


def on_close():
    """Any exit operations go here. The exits caught by this function are soft exits, e.g. pressing X or Menu ->Exit
    This part does not work on hard exits such as Alt+F4, the 'Exit' button on the top bar of the program or a hammer to the computer."""

    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        print("-----SHUTTING DOWN-----")
        print("-----SAVING PREFERENCES-----")
        if location_lbl.cget("text") != "":
            print("Current city: " + location_lbl.cget("text").split()[0])
        print("Temp unit: " + today_temp.temp_unit)
        save(today_temp.temp_unit, location_lbl.cget("text"))
        print("-----SAVING PREFERENCES DONE-----")
        r.destroy()

def saveprefs():
    if location_lbl.cget("text") != "":
        print("Current city: " + location_lbl.cget("text").split()[0])
    print("Temp unit: " + today_temp.temp_unit)
    save(today_temp.temp_unit, location_lbl.cget("text"))
    print("-----SAVING PREFERENCES DONE-----")

# elements for file in menu
file = Menu(menubar)
menubar.add_cascade(label="File", menu=file)
file.add_command(label='Save', command=saveprefs)
file.add_separator()
file.add_command(label='Exit', command=r.destroy)

file_new_frame = Frame(r, width=414, height=636, bg='#E9967A')

# Adding logo
logo_image = Image.open('wthrlogo1.png')
logo_image = logo_image.resize((300, 225))

# Creating a PhotoImage object using ImageTk
logo_photo = ImageTk.PhotoImage(logo_image)

# Creating a Label and set the logo image as its content /// bg='#6BD5F7'
logo_label = Label(r, image=logo_photo, bg='#77DCEB')
logo_label.pack()

# Cities taken above to be used in init

# creating drop box
selected_city = StringVar()
drop_box = tkinter.ttk.Combobox(r, values=cities, textvariable=selected_city)
drop_box.pack(pady=20)


# to search for the weather info
search_btn = Button(r, text='Search', width=12, bg='#F49B3D', command=search)
search_btn.config(fg='white')
search_btn.pack()

# toggle button to change the temperature unit
toggle_btn = Button(r, text='Toggle Unit', width=12, bg='#F49B3D', command=toggle_temperature_unit)
toggle_btn.config(fg='white')
toggle_btn.pack()

# location label
location_lbl = Label(r, text='', font=('bold', 20), bg='#77DCEB')
location_lbl.pack()

# to show date
date_lbl = tkinter.Label(r, text='', bg='#77DCEB', font=('bold', 14))
date_lbl.pack()

# to show weather icon
icon_lbl = tkinter.Label(r, bg='#77DCEB')
icon_lbl.pack()

# weather image - can be removed later
image = Label(r, bitmap='', bg='#77DCEB')
image.pack()

# day temperature label
temperature_day_lbl = Label(r, text='', bg='#77DCEB', font=('bold', 14))
temperature_day_lbl.config(fg='#236A82')
temperature_day_lbl.pack()  # side=LEFT, padx=40


# night temperature label - labels related to night are represented with #123456 color
temperature_night_lbl = Label(r, text='', bg='#77DCEB', font=('bold', 14))
temperature_night_lbl.config(fg='#123456')
temperature_night_lbl.pack()

# wind speed label-day
windday_speed_lbl = Label(r, text='', bg='#77DCEB', font=('bold', 14))
windday_speed_lbl.config(fg='#236A82')
windday_speed_lbl.pack()

# wind speed label-night
windnight_speed_lbl = Label(r, text='', bg='#77DCEB', font=('bold', 14))
windnight_speed_lbl.config(fg='#123456')
windnight_speed_lbl.pack()

# weather label
weather_lbl = Label(r, text='', bg='#77DCEB')
weather_lbl.pack()

# description label
descr_lbl = Label(r, text='', bg='#77DCEB', font=10)
descr_lbl.pack()

print("-----STARTING TK WINDOW-----")

r.protocol("WM_DELETE_WINDOW", on_close) # Run on_close when the window is about to be destroyed
if favcity != "":
    get_weather(favcity) # Initializes the program with the fav_city if there is one


r.mainloop()

