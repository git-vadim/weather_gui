import requests
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox


class Main(tk.Frame):
    
    response = ''

    def __init__(self, root):
        super().__init__(root)
        self.init_main()
    
    def init_main(self):
        label = tk.Label(root, text='VVV ENTER CITY NAME VVV', bg='#ffe76c')
        label.pack(side=tk.TOP)
        self.entry = tk.Entry(root, bd=1, justify='center')
        self.entry.pack(side=tk.TOP)

        self.weather_img = tk.PhotoImage(file='icon.png')
        self.btn = tk.Button(root, command=self.get_weather, image=self.weather_img,)

        self.btn.pack(side=tk.TOP)
        self.btn.bind('<Enter>', self.enter)
        self.btn.bind('<Leave>', self.leave)

        gener_label = tk.Label(root, text='General conditions:', bg='#0e7eef')
        self.general = tk.Entry(root, justify='center', bd=1)
        gener_label.pack()
        self.general.pack()

        self.temp_label = tk.Label(root, text='Actual Temperature, \N{DEGREE SIGN}C', bg='#0e7eff')
        self.temperature = tk.Entry(root, justify='center', bd=1)
        self.temp_label.pack()
        self.temperature.pack()

        self.wind_img = tk.PhotoImage(file='wind.png')
        wind_btn = tk.Button(root, image=self.wind_img, command=self.get_wind)
        wind_btn.pack()

    def enter(self, e):
        self.new_image = tk.PhotoImage(file='new_icon.png')
        self.btn['image'] = self.new_image
    
    def leave(self, e):
        self.btn['image'] = self.weather_img
   
    def get_weather(self):
        city = self.entry.get().capitalize()
        if city:
            api = '6a521adc91f974a2e271bce8d80adf91'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}'
            self.response = requests.get(url).json()
            if self.response != {"cod":"404","message":"city not found"}:
                self.general.delete(0,'end')
                self.general.insert(0, self.response['weather'][0]['main'])

                self.temperature.delete(0, 'end')
                self.temperature.insert(0, round(self.response['main']['temp'] - 273))
            else:
                messagebox.showwarning('MISTAKE', 'City Not Found')
        else:
            messagebox.showwarning('UVAGA!!!', 'Enter right city name!')

    def get_wind(self):
        
        if self.response != '':
            deg = self.response['wind']['deg']
            speed = self.response['wind']['speed']
            
            fig = plt.figure()
            ax = fig.add_subplot('111', polar=True)
        
            ax.set_theta_zero_location("N")
            ax.set_theta_direction(-1)

            ax.set_ylim((0, 33.0))
            ax.set_yticklabels(['calm',
                                'light',
                                'fresh',
                                'strong',
                                'storm',
                                'stay home'],
                                )
            ax.set_xticklabels(['North',
                                'N-E',
                                'East',
                                'S-E',
                                'South',
                                'S-W',
                                'West',
                                'N-W'],
                                )
            colors = {'darkblue':[0,10],
                    'blue':[10,15],
                    'green':[15,20],
                    'yellow':[20,25],
                    'orange':[25,30],
                    'red':[30,35],
                    }

            for color, loc in colors.items():
                ax.fill_between(
                    np.linspace(0, np.pi*2, 100),
                    loc[0],
                    loc[1],
                    color=color,)

            plt.arrow(deg/180.*np.pi, 0.5, 0, speed, alpha = 5.0, width = 0.3,
                            edgecolor = 'black', facecolor = 'white', lw = 1.3, zorder = 5)

            plt.title(f'Speed: {speed}m/s; Direction: {deg}\N{DEGREE SIGN}')
            plt.show()
        else:
            messagebox.showwarning('VNIMANIE', 'First, u need to enter city name, then press SUN')

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title('Weather')
    root.geometry('250x350+300+200')
    root.resizable(False, False)
    root.mainloop()
