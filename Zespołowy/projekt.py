import tkinter as tk
from tkinter import messagebox
import sqlite3



### Panel logowania ###



class Login(tk.Tk):
            
    def __init__(self, *args, **kwargs):        
        tk.Tk.__init__(self, *args, **kwargs)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
     
        username_label = tk.Label(self, text="Nazwa użytkownika:").pack()
        username_entry = tk.Entry(self, textvariable=self.username).pack()
        password_label = tk.Label(self, text="Hasło").pack()
        password_entry = tk.Entry(self, textvariable=self.password, show="*").pack()     
        login_button = tk.Button(self, text="Zaloguj się", command= self.login).pack()


    def login(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Błąd logowania", "Wszystkie pola muszą być wypełnione!")
        else:
            with sqlite3.connect("database.db") as db:
                c = db.cursor()
                c.execute("select password from user where username = '%s'" % self.username.get())

                try:
                    haslo = c.fetchone()[0]
                except Exception:
                    haslo = " "

                c.close()

            if self.password.get() == str(haslo):
                self.withdraw()
                Switch()
            else:
                messagebox.showerror("Błąd logowania", "Nazwa użytkownika albo hasło jest nieprawidłowe!")





### Przełącznik między kategoriami ###


        
class Switch(tk.Tk):
    def __init__(self, *args, **kwargs):        
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        self.geometry("800x600")
        self.resizable(0, 0)  
        self.switch_frame(Menu)

    def switch_frame(self, frame_class):        
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()               
        self._frame = new_frame
        self._frame.pack()

    def close(self):
        self.destroy()



### Widok FAKTURY ###



class Menu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Faktura VAT").pack(side="top", fill="x", pady=100, padx=100)
        tk.Button(self, text="Konto użytkownika",
                  command=lambda: master.switch_frame(Profile)).pack()
        tk.Button(self, text="Klienci",
                  command=lambda: master.switch_frame(Client)).pack()
        tk.Button(self, text='Produkty',
                  command=lambda: master.switch_frame(Product)).pack()
        tk.Button(self, text="Zamknij",
                  command=lambda: master.close()).pack()



### Widok KONTA UŻYTKOWNIKA ###



class Profile(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.connection = sqlite3.connect('database.db')
        self.con = self.connection.cursor()

        tk.Button(self, text="Cofnij",
                  command=lambda: master.switch_frame(Menu)).pack(side="top", fill="y", pady=100, padx=100)

        self.show()

    def show(self):
        data = self.read()
        for index, dat in enumerate(data):
            #tk.Label(self, text=dat[0]).pack()
            tk.Label(self, text="Nazwa firmy: " + dat[1]).pack()
            tk.Label(self, text="Adres: " + dat[2]).pack()
            tk.Label(self, text=dat[3] + " " + dat[4]).pack()
            #tk.Label(self, text=dat[4]).pack()
            tk.Label(self, text="NIP: " + dat[5]).pack()
            tk.Label(self, text="Telefon: +48 " + dat[6]).pack()
        
    def read(self):
        self.con.execute("select * from profile where id=1")
        return self.con.fetchall()



### Widok KLIENTÓW ###



class Client(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Coś tu prędzej, czy później będzie...").pack(side="top", fill="x", pady=100)
        tk.Button(self, text="Cofnij",
                  command=lambda: master.switch_frame(Menu)).pack(side="top", fill="y", pady=100, padx=100)



### Widok PRODUKTÓW ###



class Product(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Coś tu prędzej, czy później będzie...").pack(side="top", fill="x", pady=100)
        tk.Button(self, text="Cofnij",
                  command=lambda: master.switch_frame(Menu)).pack(side="top", fill="y", pady=100, padx=100)



### KONIEC ###



if __name__ == "__main__":

    app = Login()
    app.geometry("800x600")
    app.resizable(0, 0)
    app.mainloop()



### Twórcy: ####
    
# 1. Radosław Gzyl
# 2. Mateusz Trzebiński
# 3. Maciej Jopek
# 4. Zuzanna Lenczyk-Wąsowska
# 5. Kamil Stefaniuk 
