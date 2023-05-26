import io
import tkinter.ttk
from tkinter import Tk, Frame, Menu, PhotoImage, Label, Button, Entry, StringVar, messagebox
from PIL import ImageTk, Image
import requests
from bs4 import BeautifulSoup

keyfile = open('.apikey')
API_KEY = keyfile.readline()

# creating window
r = Tk()
r.geometry('414x636')
r.configure(bg='#77DCEB')
r.title('Weather App')


# creating menu bar
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


def fahrenheit_to_celsius():
    pass


def toggle_temperature_unit():
    global temperature_unit
    if temperature_unit == "Celsius":
        temperature_unit = "Fahrenheit"
    else:
        temperature_unit = "Celsius"
    update_temperature()

    
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    location = data['name']
    temperature = round(data['main']['temp'] - 273.15)
    description = data['weather'][0]['description']
    icon_url = f"http://openweathermap.org/img/w/{data['weather'][0]['icon']}.png"
    wind_speed = data['wind']['speed']

    location_lbl.config(text=location)
    temperature_lbl.config(text=f"{temperature}°C")
    descr_lbl.config(text=f"{description}")
    wind_speed_lbl.configure(text=f"{wind_speed}m/s")

    # Load the weather icon from the URL
    response = requests.get(icon_url)
    icon_data = response.content
    icon_image = Image.open(io.BytesIO(icon_data))
    icon_photo = ImageTk.PhotoImage(icon_image)
    icon_lbl.config(image=icon_photo)
    icon_lbl.image = icon_photo

    update_temperature()


def update_temperature():
    global temperature_unit
    celsius = float(temperature_lbl.cget("text").split("°")[0])  # this extracts the current temperature in Celsius

    if temperature_unit == "Celsius":
        temperature_lbl.config(text=f"{celsius:.2f}°C")
    else:
        fahrenheit = celsius_to_fahrenheit(celsius)
        temperature_lbl.config(text=f"{fahrenheit:.2f}°F")


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


# creating drop box
selected_city = StringVar()
drop_box = tkinter.ttk.Combobox(r, values=cities, textvariable=selected_city)
drop_box.pack(pady=20)


# to search for the weather info
search_btn = Button(r, text='Search', width=12, command=search)
search_btn.pack()

# toggle botton to change the temperature unit
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

# temperature label
temperature_lbl = Label(r, text='', bg='#77DCEB', font=('bold', 14))
temperature_lbl.pack()

# weather label
weather_lbl = Label(r, text='', bg='#77DCEB')
weather_lbl.pack()

# description label
descr_lbl = Label(r, text='', bg='#77DCEB', font=10)
descr_lbl.pack()

r.mainloop()
