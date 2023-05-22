import tkinter.ttk
from tkinter import Tk, Frame, Menu, PhotoImage, Label, Button, Entry
from PIL import ImageTk, Image
import requests
from bs4 import BeautifulSoup
from configparser import ConfigParser

url = ''


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


def search():
    pass


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

cities = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin",
          "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa",
          "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum",
          "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkâri", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir",
          "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kilis", "Kırıkkale", "Kırklareli",
          "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir",
          "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", "Sivas", "Şırnak",
          "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"]


# Adding logo
logo_image = Image.open('C:/Users/HP/OneDrive/Masaüstü/wthrlogo1.png')

# Resize the logo image if needed
logo_image = logo_image.resize((300, 225))

# Create a PhotoImage object using ImageTk
logo_photo = ImageTk.PhotoImage(logo_image)

# Create a Label and set the logo image as its content /// bg='#6BD5F7'
logo_label = Label(r, image=logo_photo, bg='#77DCEB')
logo_label.pack()

# creating drop box
drop_box = tkinter.ttk.Combobox(r, values=cities)
drop_box.pack(pady=20)

search_btn = Button(r, text='Search', width=12, command=search)
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
