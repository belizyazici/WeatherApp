# Beliz Yazıcı-20210601066, Aykan Berk Ayvazoğlu-20210601007, Utku Mert Çırakoğlu-20210601017
# -*- coding: utf-8 -*-
import io
import tkinter.ttk
from tkinter import Tk, Frame, Menu, PhotoImage, Label, Button, Entry, StringVar, messagebox
from PIL import ImageTk, Image
import requests

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

    temp_value = 0.0
    temp_unit = "Celsius"

    def __init__(self, tval=0.0, tunit ="Celsius"):
        if isinstance(self.temp_value, float):
            self.temp_value = tval
        if tunit == "Celsius" or tunit == "Fahrenheit":
            self.temp_unit = tunit

    def toggle(self):
        if self.temp_unit == "Celsius":
            self.temp_value = celsius_to_fahrenheit(self.temp_value)
            self.temp_unit = "Fahrenheit"

        elif self.temp_unit == "Fahrenheit":
            self.temp_value = fahrenheit_to_celsius(self.temp_value)
            self.temp_unit = "Celsius"

    def print(self):
        print("Temperature: " + str(self.temp_value))
        print("Unit: " + self.temp_unit)

day_temp = Temperature(0.0, tempunit)
night_temp = Temperature(0.0, tempunit)
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
    day_temp.toggle()
    night_temp.toggle()

    if day_temp.temp_unit == "Celsius":
        temperature_day_lbl.config(text=f"{round(day_temp.temp_value,1)}°C")
    else:
        temperature_day_lbl.config(text=f"{round(day_temp.temp_value,1)}°F")

    if night_temp.temp_unit == "Celsius":
        temperature_night_lbl.config(text=f"{round(night_temp.temp_value,1)}°C")
    else:
        temperature_night_lbl.config(text=f"{round(night_temp.temp_value,1)}°F")


    
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    try:
        location = data['name']
        day_temp_holder.temp_unit = "Celsius" # Resetting holders to Celsius in case they're stuck at Fahrenheit from a prior call
        night_temp_holder.temp_unit = "Celsius"
        day_temp_holder.temp_value = round(data['main']['temp_max'] - 273.15) # This data always starts out as Kelvin, so -273.15 degrees to convert to Celsius
        night_temp_holder.temp_value = round(data['main']['temp_min'] - 273.15)
        description = data['weather'][0]['description']
        icon_url = f"http://openweathermap.org/img/w/{data['weather'][0]['icon']}.png"  # there should be image for night weather too!!!
        wind_speed = data['wind']['speed']

        if day_temp.temp_unit == "Fahrenheit":
            day_temp_holder.toggle()
        if night_temp.temp_unit == "Fahrenheit":
            night_temp_holder.toggle()

        day_temp.temp_value = day_temp_holder.temp_value
        night_temp.temp_value = night_temp_holder.temp_value

        location_lbl.config(text=location)
        if day_temp.temp_unit == "Celsius":
            temperature_day_lbl.config(text=f"{round(day_temp.temp_value,1)}°C")
        else:
            temperature_day_lbl.config(text=f"{round(day_temp.temp_value,1)}°F")

        if night_temp.temp_unit == "Celsius":
            temperature_night_lbl.config(text=f"{round(night_temp.temp_value,1)}°C")
        else:
            temperature_night_lbl.config(text=f"{round(night_temp.temp_value,1)}°F")
        descr_lbl.config(text=f"{description}")
        windday_speed_lbl.configure(text=f"{wind_speed}m/s")

        # loading the weather icon from the URL
        response = requests.get(icon_url)
        icon_data = response.content
        icon_image = Image.open(io.BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_lbl.config(image=icon_photo)
        icon_lbl.image = icon_photo

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
    This part does not work on hard exits such as Alt+F4, the stop button (if on an IDE) or a hammer to the computer."""

    print("-----SHUTTING DOWN-----")
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        print("-----SAVING PREFERENCES-----")
        if location_lbl.cget("text") != "":
            print("Current city: " + location_lbl.cget("text").split()[0])
        print("Temp unit: " + day_temp.temp_unit)
        save(day_temp.temp_unit, location_lbl.cget("text"))
        print("-----SAVING PREFERENCES DONE-----")
        r.destroy()

# elements for file in menu
file = Menu(menubar)
menubar.add_cascade(label="File", menu=file)
file.add_command(label='Save', command=file_func)
file.add_command(label='Close')
file.add_separator()
file.add_command(label='Exit', command=r.destroy)


# options in menu
option = Menu(menubar)
menubar.add_cascade(label="Options", menu=option)
option.add_command(label='Find', command=commands)
option.add_command(label='Find Next', command=commands)

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

