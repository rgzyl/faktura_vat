import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3



### Panel logowania ###



class Login(tk.Tk):
            
    def __init__(self, *args, **kwargs):        
        tk.Tk.__init__(self, *args, **kwargs)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
     
        username_label = tk.Label(self, text="Nazwa użytkownika:").pack()
        username_entry = tk.Entry(self, textvariable=self.username).pack()
        self.username.set("admin")
        password_label = tk.Label(self, text="Hasło").pack()
        password_entry = tk.Entry(self, textvariable=self.password, show="*").pack()
        self.password.set("1234")
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


        self.nabywca = tk.StringVar(self)
        self.ulica = tk.StringVar(self)
        self.miasto = tk.StringVar(self)
        self.kod = tk.StringVar(self)
        self.wybor2 = tk.StringVar(self)
        self.id = tk.StringVar(self)

        frame_napisy = tk.Frame(self)  # Ramka z napisami pol
        frame_napisy.pack(side="left", fill="both")
        tk.Label(frame_napisy, text="Nabywca").pack(pady = 5, padx = 5)
        tk.Label(frame_napisy, text="Ulica").pack(pady = 5, padx = 5)
        tk.Label(frame_napisy, text="Miasto").pack(pady = 5, padx = 5)
        tk.Label(frame_napisy, text="Kod").pack(pady = 5, padx = 5)

        choices = ("NIP", "REGON", "VAT EU", "PESEL", "Numer firmy", "Osoba fizyczna")
        self.variable = tk.StringVar(self)
        self.variable.set("Osoba fizyczna")
        tk.OptionMenu(frame_napisy, self.variable, *choices, command=self.choice).pack(pady = 5, padx = 5)


        frame_entry = tk.Frame(self)  # Ramka z polami
        frame_entry.pack(side="left", fill="both")
        tk.Entry(frame_entry, textvariable=self.nabywca).pack(pady = 5, padx = 5)
        tk.Entry(frame_entry, textvariable=self.ulica).pack(pady = 8, padx = 5)
        tk.Entry(frame_entry, textvariable=self.miasto).pack(pady = 4, padx = 5)
        tk.Entry(frame_entry, textvariable=self.kod).pack(pady = 9, padx = 5)
        self.pole_do_wpisania_wyboru = tk.Entry(frame_entry, textvariable=self.wybor2)


        frame_id = tk.Frame(self)  # Ramka z ID
        frame_id.pack(side="left")
        tk.Label(frame_id, text="ID").pack(pady = 5, padx = 5)
        tk.Entry(frame_id, textvariable=self.id).pack(side="bottom",pady=5, padx = 5)


        tk.Button(self, text="DELETE", command=lambda : self.usun(self.id.get())).pack(side="bottom", pady = 5, padx = 5)
        tk.Button(self, text="UPDATE", command=lambda: self.update(self.id.get())).pack(side="bottom", pady = 5, padx = 5)
        tk.Button(self, text="ZAPISZ", command=self.zapisz).pack(side="bottom", pady = 5, padx = 5)


        tk.Button(self, text="Cofnij", command=lambda: master.switch_frame(Menu)).pack()
        with sqlite3.connect("database.db") as db:  # Wypisanie recordow
            c = db.cursor()
            c.execute("select * from clients")
            wynik = c.fetchall()
            c.close()

        wyniki = tk.Toplevel(self)
        total_rows = len(wynik)
        total_columns = len(wynik[0])

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = tk.Entry(wyniki, width=10, fg='blue',
                               font=('Arial', 10, 'bold'))
                self.e.insert(-1, wynik[i][j])
                self.e.configure(state='readonly')
                self.e.grid(row=i, column=j)




    def zapisz(self):
        nabywca = self.nabywca.get() if self.nabywca.get() != "" else "-"

        if self.variable.get() == "Osoba fizyczna":
            wybor = "T"
        else:
            wybor = self.wybor2.get() if self.wybor2.get() != "" else "-"

        ulica = self.ulica.get() if self.ulica.get() != "" else "-"
        kod_miasto = self.kod.get()+" "+self.miasto.get() if self.kod.get() != "" and self.miasto.get() != "" else "-"

        query = (f"insert into clients('nabywca', '{self.variable.get() if self.variable.get() != 'Osoba fizyczna' else 'osoba_fizyczna'}', 'ulica', 'miasto_kod')values('{nabywca}', '{wybor}', '{ulica}', '{kod_miasto}')")

        with sqlite3.connect("database.db") as db:
            c = db.cursor()
            c.execute(query)
            c.close()

    def usun(self, id_client):
        with sqlite3.connect("database.db") as db:
            c = db.cursor()
            c.execute(f"delete from clients where c_id = {id_client}")
            c.close()

    def update(self, id_client):  # Nowe okno do update
        window = tk.Toplevel(self)
        with sqlite3.connect("database.db") as db:
            c = db.cursor()
            c.execute(f"select * from clients where c_id = {id_client}")
            stare_dane = c.fetchall()
            c.close()


        self.nowy_nabywca = tk.StringVar(self)
        self.nip = tk.StringVar(self)
        self.regon = tk.StringVar(self)
        self.vat_eu = tk.StringVar(self)
        self.pesel = tk.StringVar(self)
        self.numer_firmy = tk.StringVar(self)
        self.osoba_fizyczna = tk.StringVar(self)
        self.nowa_ulica = tk.StringVar(self)
        self.nowe_miasto = tk.StringVar(self)
        self.nowy_kod = tk.StringVar(self)

        lista_kolumn = [
            self.nowy_nabywca,
            self.nip,
            self.regon,
            self.vat_eu,
            self.pesel,
            self.numer_firmy,
            self.osoba_fizyczna,
            self.nowa_ulica,
            self.nowe_miasto,
            self.nowy_kod
        ]

        frame_napisy = tk.Frame(window)  # Ramka z opisami kolumn
        frame_napisy.pack(side="left", fill="both")
        tk.Label(frame_napisy, text="Nabywca").pack( padx=5)
        tk.Label(frame_napisy, text="NIP").pack( padx=5)
        tk.Label(frame_napisy, text="REGON").pack( padx=5)
        tk.Label(frame_napisy, text="VAT EU").pack(padx=5)
        tk.Label(frame_napisy, text="PESEL").pack( padx=5)
        tk.Label(frame_napisy, text="Numer firmy").pack( padx=5)
        tk.Label(frame_napisy, text="Osoba fizyczna").pack(padx=5)
        tk.Label(frame_napisy, text="Ulica").pack( padx=5)
        tk.Label(frame_napisy, text="Miasto").pack( padx=5)
        tk.Label(frame_napisy, text="Kod pocztowy").pack( padx=5)


        frame_dane = tk.Frame(window)  # Ramka z polami do edycji
        frame_dane.pack(side="left", fill="both")

        for i in stare_dane:  # Wstawia dane do pol entry
            for j in range(1, len(i)):
                if i[j] == i[-1]:
                    kod, miasto = i[j].split(" ",1)
                    self.e = tk.Entry(frame_dane, textvariable=lista_kolumn[j-1])
                    self.e.insert(-1, miasto)
                    self.e.pack(pady=1 ,padx=5)

                    self.e = tk.Entry(frame_dane, textvariable=lista_kolumn[j])
                    self.e.insert(-1, kod)
                    self.e.pack(pady=1, padx=5)
                else:
                    self.e = tk.Entry(frame_dane, textvariable=lista_kolumn[j-1])
                    self.e.insert(-1, i[j])
                    self.e.pack(pady=1, padx=5)



            tk.Button(window, text="UPDATE", command= lambda : self.query_update(id_client)).pack(side="bottom")

    def query_update(self, id_client):  # Komenda update
        miasto_kod = self.nowy_kod.get() + " " + self.nowe_miasto.get()
        with sqlite3.connect("database.db") as db:
            c = db.cursor()
            c.execute(f"update clients set nabywca = '{self.nowy_nabywca.get()}', nip = '{self.nip.get()}', regon = '{self.regon.get()}', vat_eu = '{self.vat_eu.get()}', pesel = '{self.pesel.get()}', numer_firmy = '{self.numer_firmy.get()}', osoba_fizyczna = '{self.osoba_fizyczna.get()}', ulica = '{self.nowa_ulica.get()}',  miasto_kod = '{miasto_kod}' where c_id = {id_client};")
            c.close()

    def choice(self, v):  # Dodanie pola po wyborze innym niz osoba fizyczna
        if v == "Osoba fizyczna":
            self.pole_do_wpisania_wyboru.pack_forget()
        else:
            self.pole_do_wpisania_wyboru.pack(pady = 7, padx = 5)







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
