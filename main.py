import tkinter.ttk
from tkinter import Tk, Frame, Menu, PhotoImage, Label, Button, Entry, StringVar
from PIL import ImageTk, Image
import requests
from bs4 import BeautifulSoup

API_KEY = "***REMOVED***"

#url = "https://weather.com/tr-TR/weather/today/l/%C4%B0zmir+%C4%B0zmir?canonicalCityId=a3722d3ba43ddbef656021ba77ee61bf4c6fae20636732a1f2958d22beb70107"


# creating window
r = Tk()
r.geometry('414x636')
# bg_image = Image.open('C:/Users/HP/OneDrive/Masaüstü/mainbg.png')
# bg_photo = ImageTk.PhotoImage(bg_image)
# background_label = Label(r, image=bg_photo)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)
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


def get_weather():  # üzerinde uğraşılacak (html class linkleri konulacak)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cities}&appid=" + API_KEY

    web_page = requests.get(url)

    if weather_lbl.get("cod") == 200:  # Verify the response status
        # Extract specific weather details using BeautifulSoup
        soup = BeautifulSoup(web_page.content, "html.parser")
        location_element = soup.find("div", class_="location-class")  # Adjust the class name accordingly
        temperature_element = soup.find("div", class_="temperature-class")  # Adjust the class name accordingly

        location = location_element.text if location_element else "N/A"
        temperature = temperature_element.text if temperature_element else "N/A"

        location_lbl.config(text="Location: " + location)
        temperature_lbl.config(text="Temperature: " + temperature)
    else:
        location_lbl.config(text="Location: N/A")
        temperature_lbl.config(text="Temperature: N/A")


    '''
    web_page = requests.get(url)
    soup = BeautifulSoup(web_page.content, "html.parser")
    location = soup.find('h1', class_="CurrentConditions--location--1YWj_").text
    # .text is for printing location info only and not other texts
    temperature = soup.find('span', class_="CurrentConditions--tempValue--MHmYY").text
    weather_prediction = soup.find('div', class_="CurrentConditions--phraseValue--mZC_p").text
    print(weather_prediction)

    location_lbl.config(text=location)
    temperature_lbl.config(text=temperature)
    weather_lbl.config(text=weather_prediction)

    temperature_lbl.after(60000, get_weather)
    r.update()
    '''

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
logo_image = Image.open('C:/Users/HP/OneDrive/Masaüstü/wthrlogo1.png')

# Resize the logo image if needed
logo_image = logo_image.resize((300, 225))

# Create a PhotoImage object using ImageTk
logo_photo = ImageTk.PhotoImage(logo_image)

# Create a Label and set the logo image as its content /// bg='#6BD5F7'
logo_label = Label(r, image=logo_photo, bg='#77DCEB')
logo_label.pack()

cities = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan",
              "Artvin",
              "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur",
              "Bursa",
              "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan",
              "Erzurum",
              "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkâri", "Hatay", "Iğdır", "Isparta", "İstanbul",
              "İzmir",
              "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kilis", "Kırıkkale", "Kırklareli",
              "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş",
              "Nevşehir",
              "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", "Sivas",
              "Şırnak",
              "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"]

clicked = StringVar()
clicked.set(cities[0])
# creating drop box
drop_box = tkinter.ttk.Combobox(r, values=cities)
drop_box.current(0)
drop_box.pack(pady=20)



search_btn = Button(r, text='Search', width=12, command=get_weather)
search_btn.pack()

# location label
location_lbl = Label(r, text='', font=('bold', 20), bg='#77DCEB')
location_lbl.pack()

# weather image
image = Label(r, bitmap='', bg='#77DCEB')
image.pack()

# temperature label
temperature_lbl = Label(r, text='', bg='#77DCEB')
temperature_lbl.pack()

# weather label
weather_lbl = Label(r, text='', bg='#77DCEB')
weather_lbl.pack()


r.mainloop()
