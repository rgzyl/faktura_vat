import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import tix
import sqlite3



### Panel logowania ###



class Login(tk.Tk):
            
    def __init__(self, *args, **kwargs):        
        tk.Tk.__init__(self, *args, **kwargs)

        title = ttk.Label(self, text="Faktura VAT", font=("Calibri", 24, 'bold'))
        title.pack(padx=100, pady=100)

        labelframe = tk.LabelFrame(self, text="Panel logowania", padx=10, pady=10, font=("Calibri", 12))  
        labelframe.pack()

        self.username = tk.StringVar()
        self.password = tk.StringVar()
     
        username_label = ttk.Label(labelframe, text="Nazwa użytkownika: ", width=20, font=("Calibri", 12))
        username_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        username_entry = ttk.Entry(labelframe, textvariable=self.username, width=25, font=("Calibri", 12))
        username_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.username.set("admin")
        
        password_label = ttk.Label(labelframe, text="Hasło: ", width=20, font=("Calibri", 12))
        password_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        password_entry = ttk.Entry(labelframe, textvariable=self.password, show="*", width=25, font=("Calibri", 12))
        password_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.password.set("1234")

        s = ttk.Style()
        s.configure("my.TButton", font=("Calibri", 12))
        
        login_button = ttk.Button(labelframe, text="Zaloguj się", command=self.login, width=20, style="my.TButton")
        login_button.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        data = ttk.Label(self, text="Autorzy: Radosław Gzyl, Mateusz Trzebiński, Maciej Jopek, Kamil Stefaniuk, Zuzanna Lenczyk-Wąsowska", font=("Calibri", 8, ""))
        data.pack(side=tk.BOTTOM, pady=10)


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

        ttk.Label(self, text="Faktura VAT", font=("Calibri", 24, "bold")).pack(pady=20)

        style = ttk.Style(self)
        style.configure("my.TButton", font=("Calibri", 20, "bold"))
        
        panel = ttk.Button(self, text="Panel użytkownika", command=lambda: master.switch_frame(Profile), style="my.TButton")
        panel.pack(side=tk.LEFT, padx=5, ipadx=10)
        
        klient = ttk.Button(self, text="Klienci", command=lambda: master.switch_frame(Client), style="my.TButton")
        klient.pack(side=tk.LEFT)
        
        produkt = ttk.Button(self, text='Produkty', command=lambda: master.switch_frame(Product), style="my.TButton")
        produkt.pack(side=tk.LEFT, padx=5)
        
        przycisk = ttk.Button(self, text="Zamknij", command=lambda: master.close(), style="my.TButton")
        przycisk.pack(side=tk.LEFT, padx=0)



### Widok KONTA UŻYTKOWNIKA ###



class Profile(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)            

        ttk.Label(self, text="Faktura VAT - panel użytkownika", font=("Calibri", 24, "bold")).pack(pady=30)

        bold = ttk.Style(self)
        bold.configure("bold.TButton", font=("Calibri", 14, "bold"))

        normal = ttk.Style(self)
        normal.configure("normal.TButton", font=("Calibri", 12))

        labelframe = ttk.LabelFrame(self, text="Panel użytkownika")
        labelframe.pack(padx=10, pady=10)

        frame = ttk.LabelFrame(self, text="Dane logowania")
        frame.pack(padx=10, pady=10)

        con = sqlite3.connect('database.db')
        c = con.cursor()
        query = c.execute('SELECT * FROM profile WHERE id=1')
        
        for dat in query:           
            nazwa_opis = ttk.Label(labelframe, text="Nazwa firmy", font=("Calibri", 12))
            nazwa_opis.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            nazwa = ttk.Label(labelframe, text=dat[1], font=("Calibri", 12))
            nazwa.grid(row=0, column=1, padx=10, pady=5)
            
            ulica_opis = ttk.Label(labelframe, text="Adres siedziby", font=("Calibri", 12))
            ulica_opis.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
            ulica = ttk.Label(labelframe, text=dat[2], font=("Calibri", 12))
            ulica.grid(row=1, column=1, padx=10, pady=5)
            
            kod_opis = ttk.Label(labelframe, text="Kod pocztowy/miasto", font=("Calibri", 12))
            kod_opis.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
            kod = ttk.Label(labelframe, text=dat[3]+" "+dat[4], font=("Calibri", 12))
            kod.grid(row=2, column=1, padx=10, pady=5)
            
            telefon_opis = ttk.Label(labelframe, text="Telefon kontaktowy", font=("Calibri", 12))
            telefon_opis.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
            telefon = ttk.Label(labelframe, text="+48 "+dat[6], font=("Calibri", 12))
            telefon.grid(row=3, column=1, padx=10, pady=5)
            
            nip_opis = ttk.Label(labelframe, text="Numer identyfikacji podatkowej", font=("Calibri", 12))
            nip_opis.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
            nip = ttk.Label(labelframe, text=dat[5], font=("Calibri", 12))
            nip.grid(row=4, column=1, padx=10, pady=5)

            edit_profile_button = ttk.Button(labelframe, text="Edytuj panel użytkownika",command=self.update, width=80, style="normal.TButton")
            edit_profile_button.grid(row=5, columnspan=2, padx=15, pady=15)
        
        edit_login_button = ttk.Button(frame, text="Zaktualizuj/zmień nazwe użytkownika",command=self.login, width=80, style="normal.TButton")
        edit_login_button.grid(padx=15, pady=10)

        edit_password_button = ttk.Button(frame, text="Zaktualizuj/zmień hasło",command=self.password, width=80, style="normal.TButton")
        edit_password_button.grid(padx=15, pady=10)

        button = ttk.Button(self, text="Cofnij", command=lambda: master.switch_frame(Menu), style="bold.TButton")
        button.pack(fill="x", padx=5, pady=20, side=tk.BOTTOM)
            
        
    def password(self):
        window = tk.Toplevel()
        window.resizable(0,0)

        old_password = tk.StringVar()
        password = tk.StringVar()
        re_password = tk.StringVar()
        
        title=ttk.Label(window, text="Formularz zmiany hasła w panelu użytkownika", font=("Calibri", 12, "bold"))
        title.grid(row=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

        password_label=ttk.Label(window, text="Podaj obecne hasło", font=("Calibri", 12))
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        password_entry=ttk.Entry(window, textvariable=old_password, font=("Calibri", 12), width=30, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        new_password_label=ttk.Label(window, text="Podaj nowe hasło", font=("Calibri", 12))
        new_password_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        new_password_entry=ttk.Entry(window, textvariable=password, font=("Calibri", 12), width=30, show="*")
        new_password_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        re_new_password_label=ttk.Label(window, text="Powtórz nowe hasło", font=("Calibri", 12))
        re_new_password_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        re_new_password_entry=ttk.Entry(window, textvariable=re_password, font=("Calibri", 12), width=30, show="*")
        re_new_password_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        
        def password_update():
            if old_password.get()=="" or password.get()=="" or re_password.get()=="":
                messagebox.showerror('Błąd','Wszystkie pola powinny zostać uzupełnione.')
            else:
                with sqlite3.connect("database.db") as db:
                    c = db.cursor()
                    c.execute("select password from user where id=1")
                    try:
                        haslo = c.fetchone()[0]
                    except Exception:
                        haslo = " "
                    if old_password.get() == str(haslo) and password.get() == re_password.get():
                        c.execute("update user set password='"+password.get()+"' where id=1")
                        c.close()
                        window.withdraw()
                        messagebox.showinfo("Sukces", "Hasło zostało zaktualizowane.")
                    else:
                        messagebox.showerror("Błąd", "Wprowadzono nieprawidłowe dane. Spróbuj ponownie.")
                        
        normal = ttk.Style(window)
        normal.configure("normal.TButton", font=("Calibri", 12))

        button = ttk.Button(window, text="Zaktualizuj", style="normal.TButton", width=18, command=password_update)
        button.grid(row=4, column=0, padx=10, pady=10)


    def login(self):
        window = tk.Toplevel()
        window.resizable(0,0)

        window.old_login = tk.StringVar()
        window.login = tk.StringVar()
        window.re_login = tk.StringVar()
        
        title=ttk.Label(window, text="Formularz zmiany nazwy użytkownika w panelu użytkownika", font=("Calibri", 12, "bold"))
        title.grid(row=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

        login_label=ttk.Label(window, text="Podaj obecną nazwę użytkownika", font=("Calibri", 12))
        login_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        login_entry=ttk.Entry(window, textvariable=window.old_login, font=("Calibri", 12), width=40)
        login_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        new_login_label=ttk.Label(window, text="Podaj nową nazwę użytkownika", font=("Calibri", 12))
        new_login_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        new_login_entry=ttk.Entry(window, textvariable=window.login, font=("Calibri", 12), width=40)
        new_login_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        re_new_login_label=ttk.Label(window, text="Powtórz nowa nazwę użytkownika", font=("Calibri", 12))
        re_new_login_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        re_new_login_entry=ttk.Entry(window, textvariable=window.re_login, font=("Calibri", 12), width=40)
        re_new_login_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        normal = ttk.Style(window)
        normal.configure("normal.TButton", font=("Calibri", 12))

        button = ttk.Button(window, text="Zaktualizuj", style="normal.TButton", width=26, command=lambda: self.login_update(window))
        button.grid(row=4, column=0, padx=10, pady=10)
              
    def login_update(self, window):
        if window.old_login.get()=="" or window.login.get()=="" or window.re_login.get()=="":
            messagebox.showerror('Błąd','Wszystkie pola powinny zostać uzupełnione.')
        else:
            with sqlite3.connect("database.db") as db:
                c = db.cursor()
                c.execute("select username from user where id=1")
                try:
                    login = c.fetchone()[0]
                except Exception:
                    login = " "
                if window.old_login.get() == str(login) and window.login.get() == window.re_login.get():
                    c.execute("update user set username='"+window.login.get()+"' where id=1")
                    c.close()
                    window.withdraw()
                    messagebox.showinfo("Sukces", "Nazwa użytkownika została zaktualizowana.")
                else:
                    messagebox.showerror("Błąd", "Wprowadzono nieprawidłowe dane. Spróbuj ponownie.")
                        


    def update(self):
        window = tk.Toplevel()
        window.resizable(0,0)
        db=sqlite3.connect('database.db')
        c=db.cursor()
        result=c.execute("select * from profile where id=1")

        for index in result:
            nazwa=tk.StringVar()
            ulica=tk.StringVar()
            kod=tk.StringVar()
            miasto = tk.StringVar()
            nip = tk.StringVar()
            telefon = tk.StringVar()

            title = ttk.Label(window, text="Formularz edytowania danych panelu użytkownika", font=("Calibri", 12, "bold"))
            title.grid(row=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
                             
            nazwa_label=ttk.Label(window,text="Nazwa firmy", font=("Calibri", 12))
            nazwa_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)                
            nazwa_entry=ttk.Entry(window,textvariable=nazwa, font=("Calibri", 12), width=35)
            nazwa_entry.insert(0,index[1])
            nazwa_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

            ulica_label=ttk.Label(window,text="Adres siedziby", font=("Calibri", 12))
            ulica_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
            ulica_entry=ttk.Entry(window,textvariable=ulica, font=("Calibri", 12), width=35)
            ulica_entry.insert(0,index[2])
            ulica_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

            kod_label=ttk.Label(window,text="Kod pocztowy", font=("Calibri", 12))
            kod_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
            kod_entry=ttk.Entry(window,textvariable=kod, font=("Calibri", 12), width=35)
            kod_entry.insert(0,index[3])
            kod_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

            miasto_label=ttk.Label(window,text="Miasto", font=("Calibri", 12))
            miasto_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
            miasto_entry=ttk.Entry(window,textvariable=miasto, font=("Calibri", 12), width=35)
            miasto_entry.insert(0,index[4])
            miasto_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

            telefon_label=ttk.Label(window,text="Telefon kontaktowy", font=("Calibri", 12))
            telefon_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
            telefon_entry=ttk.Entry(window,textvariable=telefon, font=("Calibri", 12), width=35)
            telefon_entry.insert(0,index[6])
            telefon_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

            nip_label=ttk.Label(window,text="Numer identyfikacji podatkowej", font=("Calibri", 12))
            nip_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
            nip_entry=ttk.Entry(window,textvariable=nip, font=("Calibri", 12), width=35)
            nip_entry.insert(0,index[5])
            nip_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
            
        
        def updatedetail():
            if nazwa.get()=="" or ulica.get()=="" or kod.get()=="" or miasto.get()=="" or nip.get()=="" or telefon.get()=="":
                messagebox.showerror('Błąd','Wszystkie pola powinny zostać uzupełnione.')
            else:
                db=sqlite3.connect('database.db')
                c=db.cursor()
                c.execute("update profile set nazwa='"+nazwa.get()+"',ulica='"+ulica.get()+"',kod='"+kod.get()+"',miasto='"+miasto.get()+"',nip='"+nip.get()+"',telefon='"+telefon.get()+"' where id=1")
                db.commit()
                db.close()
                window.withdraw()
                messagebox.showinfo('Sukces','Profil użytkownika został zaktualizowany.')
        
        normal = ttk.Style(window)
        normal.configure("normal.TButton", font=("Calibri", 12))
        
        button=ttk.Button(window, text="Zaktualizuj", command=updatedetail, style="normal.TButton", width=28)
        button.grid(row=7, column=0, padx=10, pady=10)



### Widok KLIENTÓW ###



class Client(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        bold = ttk.Style(self)
        bold.configure("bold.TButton", font=("Calibri", 14, "bold"))

        ttk.Label(self, text="Faktura VAT - klienci", font=("Calibri", 24, "bold")).pack(pady=20)

        ttk.Button(self, text="COFNIJ", style="bold.TButton",
                  command=lambda: master.switch_frame(Menu)).pack(side="bottom", fill="x", pady=10, padx=10)

        normal = ttk.Style(self)
        normal.configure("nor.TButton", font=("Calibri", 14))

        ttk.Button(self, text="DODAJ NOWY PRODUKT", command=self.okno_zapisz, style="nor.TButton").pack(padx=20, pady=0, side="top", fill='x')

        ttk.Button(self, text="ODŚWIEŻ", command=lambda: master.switch_frame(Client), style="nor.TButton").pack(padx=20, pady=10, side="top", fill='x') 

        ttk.Label(self, text="TABELA Z PRODUKTAMI", font=("Calibri", 14, "bold")).pack(side="top", pady=10)
        frame = tk.Frame(self)
        self.my_show(frame, 0)
        frame.pack(side="top")



    def my_show(self, w, offset):  # Tabelka
        limit = 8
        q = "SELECT C_ID, Nabywca from clients LIMIT " + str(offset) + "," + str(limit)
        h = "select count(*) from clients"
        i=0

        normal = ttk.Style(w)
        normal.configure("normal.TButton", font=("Calibri", 12))

        
        with sqlite3.connect("database.db") as db:  # Wypisanie recordow
            c = db.cursor()
            c.execute(q)
            r_set = c.fetchall()
            c.execute(h)
            no_rec = c.fetchone()[0]
            c.close()
        l = ["Lp",
             "Nabywca"]

        r_set.insert(0, l)  # Dodanie nazw kolumn

        for client in r_set:
            for j in range(len(client)):
                e = ttk.Label(w, text=client[j], font=("Calibri", 12))
                e.grid(row=i, column=j)

            if r_set.index(client) != 0:
                e = ttk.Button(w, text='SZCZEGÓŁY', command=lambda d=client[0]: self.detail(d), style="normal.TButton")
                e.grid(row=i, column=j + 1, padx=5)
                f = ttk.Button(w, text='EDYTUJ', command=lambda d=client[0]: self.update(d), style="normal.TButton")
                f.grid(row=i, column=j + 2)
                f = ttk.Button(w, text='USUŃ', command=lambda d=client[0]: self.usun(d), style="normal.TButton")
                f.grid(row=i, column=j + 3, padx=5)
            i = i + 1

        while (i < limit):  # required to blank the balance rows if they are less
            for j in range(10):
                e = tk.Label(w, text=" ", width=9)
                e.grid(row=i, column=j)

            i = i + 1

            # Show buttons
        back = offset - limit  # This value is used by Previous button
        next = offset + limit  # This value is used by Next button
        b1 = ttk.Button(w, text='Następny >', command=lambda: self.my_show(w,next), style="normal.TButton")
        b1.grid(row=12, column=3)
        b2 = ttk.Button(w, text='< Poprzedni', command=lambda: self.my_show(w, back), style="normal.TButton")
        b2.grid(row=12, column=1, pady=10)

        if (no_rec <= next):
            b1["state"] = "disabled"  # disable next button
        else:
            b1["state"] = "active"  # enable next button

        if (back >= 0):
            b2["state"] = "active"  # enable Prev button
        else:
            b2["state"] = "disabled"  # disable Prev button



    def okno_zapisz(self):  # Nowe okno do zapisu
        okno = tk.Toplevel(self)
        okno.resizable(0, 0)  
        okno.nabywca = tk.StringVar(okno)
        okno.ulica = tk.StringVar(okno)
        okno.miasto = tk.StringVar(okno)
        okno.kod = tk.StringVar(okno)
        okno.wybor2 = tk.StringVar(okno)
        okno.id = tk.StringVar(okno)

        frame = ttk.Frame(okno)
        ttk.Label(frame, text="Formularz dodawania klienta", font=("Calibri", 12, "bold")).grid(pady=10, sticky=tk.W)
        frame.pack()

        frame_napisy = ttk.Frame(okno)  # Ramka z napisami pol
        frame_napisy.pack(side="left", fill="both")
        ttk.Label(frame_napisy, text="Nabywca", font=("Calibri", 12)).grid(pady = 6, padx = 5, sticky=tk.W)
        ttk.Label(frame_napisy, text="Ulica", font=("Calibri", 12)).grid(pady = 6, padx = 5, sticky=tk.W)
        ttk.Label(frame_napisy, text="Miasto", font=("Calibri", 12)).grid(pady = 6, padx = 5, sticky=tk.W)
        ttk.Label(frame_napisy, text="Kod pocztowy", font=("Calibri", 12)).grid(pady = 6, padx = 5, sticky=tk.W)

        menu = ttk.Style(okno)
        menu.configure("menu.TMenubutton", font=("Calibri", 12))

        choices = ("NIP", "REGON", "VAT EU", "PESEL", "Numer firmy", "Osoba fizyczna")
        okno.variable = tk.StringVar(okno)
        okno.variable.set("Osoba fizyczna")
        ttk.OptionMenu(frame_napisy, okno.variable, *choices, command=self.choice, style="menu.TMenubutton").grid(pady = 5, padx = 5, sticky=tk.W)

        frame_entry = ttk.Frame(okno)  # Ramka z polami
        frame_entry.pack(side="left", fill="both")
        ttk.Entry(frame_entry, textvariable=okno.nabywca, font=("Calibri", 12), width=30).pack(pady = 5, padx = 5)
        ttk.Entry(frame_entry, textvariable=okno.ulica, font=("Calibri", 12), width=30).pack(pady = 5, padx = 5)
        ttk.Entry(frame_entry, textvariable=okno.miasto, font=("Calibri", 12), width=30).pack(pady = 5, padx = 5)
        ttk.Entry(frame_entry, textvariable=okno.kod, font=("Calibri", 12), width=30).pack(pady = 5, padx = 5)
        self.pole_do_wpisania_wyboru = ttk.Entry(frame_entry, textvariable=okno.wybor2, font=("Calibri", 12), width=30)

        normal = ttk.Style(okno)
        normal.configure("normal.TButton", font=("Calibri", 12))
        
        ttk.Button(frame_napisy, text="ZAPISZ", command=lambda : self.zapisz(okno), style="normal.TButton", width=15).grid(pady = 5, padx = 5)


    def zapisz(self, okno):  # Funkcja zapisu
        nabywca = okno.nabywca.get() if okno.nabywca.get() != "" else "-"

        if okno.nabywca.get()=="" or okno.ulica.get()=="" or okno.kod.get()=="" or okno.miasto.get()=="":
            messagebox.showerror('Błąd', 'Sprawdź, czy wszystkie pola zostały uzupełnione.')
        else:
            if okno.variable.get() == "Osoba fizyczna":
                wybor = "T"
            else:
                wybor = okno.wybor2.get() if okno.wybor2.get() != "" else "-"

            ulica = okno.ulica.get() if okno.ulica.get() != "" else "-"
            kod_miasto = okno.kod.get()+" "+okno.miasto.get() if okno.kod.get() != "" and okno.miasto.get() != "" else "-"
        
            text = messagebox.showinfo('Sukces','Klienta dodano prawidłowo.')
            if text:
                query = (f"insert into clients('nabywca', '{okno.variable.get().replace(' ','_')}', 'ulica', 'miasto_kod')values('{nabywca}', '{wybor}', '{ulica}', '{kod_miasto}')")
                with sqlite3.connect("database.db") as db:
                    c = db.cursor()
                    c.execute(query)
                    c.close()
                okno.withdraw()


    def usun(self, id_client):
        text=messagebox.askyesnocancel("Usuń","Czy na pewno chcesz usunąć klienta?",icon='warning',default='no')
        if text:
            with sqlite3.connect("database.db") as db:
                c = db.cursor()
                c.execute(f"delete from clients where c_id = {id_client}")
                c.close()

    def update(self, id_client):  # Nowe okno do update
        window = tk.Toplevel(self)
        window.resizable(0,0)
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

        frame = ttk.Frame(window)
        ttk.Label(frame, text="Formularz edytowania klienta", font=("Calibri", 12, "bold")).grid(pady=10, sticky=tk.W)
        frame.pack()
        
        frame_napisy = ttk.Frame(window)  # Ramka z opisami kolumn
        frame_napisy.pack(side="left", fill="both")
        ttk.Label(frame_napisy, text="Nabywca", font=("Calibri", 12)).pack( padx=5, pady=2, anchor="w")
        ttk.Label(frame_napisy, text="NIP", font=("Calibri", 12)).pack( padx=5, pady=2, anchor="w")
        ttk.Label(frame_napisy, text="REGON", font=("Calibri", 12)).pack( padx=5, pady=2, anchor="w")
        ttk.Label(frame_napisy, text="VAT EU", font=("Calibri", 12)).pack(padx=5, pady=2, anchor="w")
        ttk.Label(frame_napisy, text="PESEL", font=("Calibri", 12)).pack( padx=5, pady=2, anchor="w")
        ttk.Label(frame_napisy, text="Numer firmy", font=("Calibri", 12)).pack( padx=5, pady=2, anchor="w")
        ttk.Label(frame_napisy, text="Osoba fizyczna", font=("Calibri", 12)).pack(padx=5, pady=2, anchor="w")
        ttk.Label(frame_napisy, text="Ulica", font=("Calibri", 12)).pack( padx=5, pady=2, anchor="w")
        ttk.Label(frame_napisy, text="Miasto", font=("Calibri", 12)).pack( padx=5, pady=2, anchor="w")
        ttk.Label(frame_napisy, text="Kod pocztowy", font=("Calibri", 12)).pack( padx=5, pady=2, anchor="w")


        frame_dane = ttk.Frame(window)  # Ramka z polami do edycji
        frame_dane.pack(side="left", fill="both")

        normal = ttk.Style(window)
        normal.configure("normal.TButton", font=("Calibri", 12))

        for i in stare_dane:  # Wstawia dane do pol entry
            for j in range(1, len(i)):
                if i[j] == i[-1]:
                    kod, miasto = i[j].split(" ",1)
                    self.e = ttk.Entry(frame_dane, textvariable=lista_kolumn[j-1], font=("Calibri", 12), width=25)
                    self.e.insert(-1, miasto)
                    self.e.pack(pady=1 ,padx=5)

                    self.e = ttk.Entry(frame_dane, textvariable=lista_kolumn[j], font=("Calibri", 12), width=25)
                    self.e.insert(-1, kod)
                    self.e.pack(pady=1, padx=5)
                else:
                    self.e = ttk.Entry(frame_dane, textvariable=lista_kolumn[j-1], font=("Calibri", 12), width=25)
                    self.e.insert(-1, i[j])
                    self.e.pack(pady=1, padx=5)

            button = ttk.Button(frame_napisy, text="Aktualizuj", command= lambda : self.query_update(id_client), style="normal.TButton", width=15)
            button.pack(side="bottom", pady=10, padx=10)


    def detail(self, id_client):  # Nowe okno do update
        window = tk.Toplevel(self)
        window.resizable(0,0)

        db=sqlite3.connect('database.db')
        c=db.cursor()
        query=c.execute("select * from clients where c_id='"+str(id_client)+"'")

        frame = tk.Frame(window)  # Ramka z opisami kolumn
        frame.pack()

        for i in query:     
            tk.Label(frame, text="Szczegóły dotyczące klienta", font=("Calibri", 12, "bold")).grid(pady=10, padx=10, sticky=tk.W, row=0, columnspan=2)
            
            tk.Label(frame, text="Nabywca", font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=1, column=0)
            tk.Label(frame, text=i[1], font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=1, column=1)
            
            tk.Label(frame, text="NIP", font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=2, column=0)
            tk.Label(frame, text=i[2], font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=2, column=1)
            
            tk.Label(frame, text="REGON", font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=3, column=0)
            tk.Label(frame, text=i[3], font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=3, column=1)
            
            tk.Label(frame, text="VAT EU", font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=4, column=0)
            tk.Label(frame, text=i[4], font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=4, column=1)
            
            tk.Label(frame, text="PESEL", font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=5, column=0)
            tk.Label(frame, text=i[5], font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=5, column=1)
            
            tk.Label(frame, text="Numer firmy", font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=6, column=0)
            tk.Label(frame, text=i[6], font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=6, column=1)
            
            tk.Label(frame, text="Osoba fizyczna", font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=7, column=0)
            tk.Label(frame, text=i[7], font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=7, column=1)
            
            tk.Label(frame, text="Ulica", font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=8, column=0)
            tk.Label(frame, text=i[8], font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=8, column=1)
            
            tk.Label(frame, text="Kod pocztowy/miasto", font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=9, column=0)
            tk.Label(frame, text=i[9], font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=9, column=1)


    def query_update(self, id_client):  # Komenda update
        miasto_kod = self.nowy_kod.get() + " " + self.nowe_miasto.get()
        if self.nowy_nabywca.get()=="" or self.nip.get()=="" or self.regon.get()=="" or self.vat_eu.get()=="" or self.pesel.get()=="" or self.numer_firmy.get()=="" or self.osoba_fizyczna.get()=="" or self.nowa_ulica.get()=="" or miasto_kod=="":
            messagebox.showerror('Błąd', 'Sprawdź, czy wszystkie pola zostały uzupełnione.')
        else:
            query = (f"update clients set nabywca = '{self.nowy_nabywca.get()}', nip = '{self.nip.get()}', regon = '{self.regon.get()}', vat_eu = '{self.vat_eu.get()}', pesel = '{self.pesel.get()}', numer_firmy = '{self.numer_firmy.get()}', osoba_fizyczna = '{self.osoba_fizyczna.get()}', ulica = '{self.nowa_ulica.get()}',  miasto_kod = '{miasto_kod}' where c_id = {id_client};")
            with sqlite3.connect("database.db") as db:
                c = db.cursor()
                c.execute(query)
                c.close()
                messagebox.showinfo('Sukces','Klient został zaktualizowany.')
            

    def choice(self, v):  # Dodanie pola po wyborze innym niz osoba fizyczna
        if v == "Osoba fizyczna":
            self.pole_do_wpisania_wyboru.pack_forget()
        else:
            self.pole_do_wpisania_wyboru.pack(pady = 7, padx = 5)



### Widok PRODUKTÓW ###



class Product(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        normal = ttk.Style(self)
        normal.configure("normal.TButton", font=("Calibri", 14))

        bold = ttk.Style(self)
        bold.configure("bo.TButton", font=("Calibri", 14, "bold"))

        ttk.Label(self, text="Faktura VAT - produkty", font=("Calibri", 24, "bold")).pack(pady=20)

        ttk.Button(self, text="COFNIJ", style="bo.TButton", 
                  command=lambda: master.switch_frame(Menu)).pack(side="bottom", fill="x", pady=10, padx=10)

        ttk.Button(self, text="DODAJ NOWY PRODUKT", command=self.insert_window, style="normal.TButton").pack(padx=20, pady=0, side="top", fill='x')

        ttk.Button(self, text="ODŚWIEŻ", command=lambda: master.switch_frame(Product), style="normal.TButton").pack(padx=20, pady=10, side="top", fill='x') 

        ttk.Label(self, text="TABELA Z PRODUKTAMI", font=("Calibri", 14, "bold")).pack(side="top", pady=10)
        frame = tk.Frame(self)
        self.table(frame, 0)
        frame.pack()

        
    def insert_window(self):
        window = tk.Toplevel(self)
        window.resizable(0, 0)  
        window.name = tk.StringVar(window)
        window.price = tk.StringVar(window)

        normal = ttk.Style(window)
        normal.configure("nor.TButton", font=("Calibri", 12))

        title= ttk.Label(window, text="Formularz dodawania nowego produktu:", font=("Calibri", 12, "bold"), justify=tk.LEFT)
        title.grid(row=0, columnspan=2, padx=5, pady=5, sticky = tk.W)

        name_label = ttk.Label(window, text="Nazwa", font=("Calibri", 12), justify=tk.LEFT)
        name_label.grid(row=1, column=0, padx=5, pady=5, sticky = tk.W)
        name_entry = ttk.Entry(window, textvariable=window.name, font=("Calibri", 12), width=30)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky = tk.W)

        price_label = ttk.Label(window, text="Cena brutto", font=("Calibri", 12), justify=tk.LEFT)
        price_label.grid(row=2, column=0, padx=5, pady=5, sticky = tk.W)
        price_entry = ttk.Entry(window, textvariable=window.price, font=("Calibri", 12), width=30)
        price_entry.grid(row=2, column=1, padx=5, pady=5, sticky = tk.W)

        button = ttk.Button(window, text="Dodaj", command=lambda: self.insert(window), style="nor.TButton", width=10)
        button.grid(row=3, column=0, padx=5, pady=5, sticky = tk.W)
        

    def insert(self, window):
        name = window.name.get()
        price = window.price.get()

        if price=="" or name=="":
            messagebox.showerror('Błąd', 'Sprawdź, czy wszystkie pola zostały uzupełnione.')
        else:  
            text = messagebox.showinfo('Sukces','Rekord dodano prawidłowo.')
            if text:
                query = (f"insert into products('name', 'price') values ('{name}', '{price}')")
                with sqlite3.connect("database.db") as db:
                    c = db.cursor()
                    c.execute(query)
                    c.close()
                window.withdraw()
    

    def table(self, w, offset):  
        limit = 8
        q = "SELECT * from products LIMIT " + str(offset) + "," + str(limit)
        h = "select count(*) from products"
        i=0
        with sqlite3.connect("database.db") as db:  
            c = db.cursor()
            c.execute(q)
            r_set = c.fetchall()
            c.execute(h)
            no_rec = c.fetchone()[0]
            c.close()
        l = ["Lp.",
             "Nazwa",
             "Cena brutto"]

        r_set.insert(0, l)

        bold = ttk.Style(self)
        bold.configure("bold.TButton", font=("Calibri", 12))

        for product in r_set:
            for j in range(len(product)):
                e = ttk.Label(w, text=product[j], font=("Calibri", 12))
                e.grid(row=i, column=j)

            if r_set.index(product) != 0:
                e = ttk.Button(w, text='Edytuj', command=lambda d=product[0]: self.update(d), style="bold.TButton")
                e.grid(row=i, column=j + 1, padx=10)
                f = ttk.Button(w, text='Usuń', command=lambda d=product[0]: self.delete(d), style="bold.TButton")
                f.grid(row=i, column=j + 2)
            i = i + 1

        while (i < limit): 
            for j in range(10):
                e = ttk.Label(w, text=" ", width=12)
                e.grid(row=i, column=j)

            i = i + 1

        back = offset - limit  
        next = offset + limit  
        b1 = ttk.Button(w, text='Następny >', command=lambda: self.table(w, next), style="bold.TButton")
        b1.grid(row=12, column=3, pady=10)
        b2 = ttk.Button(w, text='< Poprzedni', command=lambda: self.table(w, back), style="bold.TButton")
        b2.grid(row=12, column=1)

        if (no_rec <= next):
            b1["state"] = "disabled"  
        else:
            b1["state"] = "active"  

        if (back >= 0):
            b2["state"] = "active"  
        else:
            b2["state"] = "disabled"  

    def delete(self, id_product):
        text=messagebox.askyesnocancel("Usuń","Czy na pewno chcesz usunąć rekord?",icon='warning',default='no')
        if text:
            with sqlite3.connect("database.db") as db:
                c = db.cursor()
                c.execute(f"delete from products where id = {id_product}")
                c.close()


    def update(self, id_product):
        window = tk.Toplevel()
        window.resizable(0, 0)
        db=sqlite3.connect('database.db')
        c=db.cursor()
        query=c.execute(f"select * from products where id= {id_product}")

        title= ttk.Label(window, text="Formularz edycji produktu:", font=("Calibri", 12, "bold"), justify=tk.LEFT)
        title.grid(row=0, columnspan=2, padx=5, pady=5, sticky = tk.W)

        for i in query:
            nazwa=tk.StringVar()
            cena=tk.StringVar()
                             
            nazwa_label=ttk.Label(window,text="Nazwa", font=("Calibri", 12), justify=tk.LEFT)
            nazwa_label.grid(row=1, column=0, padx=5, pady=5, sticky = tk.W)
            nazwa_entry=ttk.Entry(window,textvariable=nazwa, font=("Calibri", 12), width=30)
            nazwa_entry.insert(0,i[1])
            nazwa_entry.grid(row=1, column=1, padx=5, pady=5, sticky = tk.W)

            cena_label=ttk.Label(window,text="Cena brutto", font=("Calibri", 12), justify=tk.LEFT)
            cena_label.grid(row=2, column=0, padx=5, pady=5, sticky = tk.W)
            cena_entry=ttk.Entry(window,textvariable=cena, font=("Calibri", 12), width=30)
            cena_entry.insert(0,i[2])
            cena_entry.grid(row=2, column=1, padx=5, pady=5, sticky = tk.W)


        def updatedetail(id_product):
            if nazwa.get()=="" or cena.get()=="":
                messagebox.showerror('Błąd','Wszystkie pola powinny zostać uzupełnione.')
            else:
                db=sqlite3.connect('database.db')
                c=db.cursor()
                c.execute("update products set name='"+nazwa.get()+"',price='"+cena.get()+"' where id='"+str(id_product)+"'")
                db.commit()
                db.close()
                window.withdraw()
                messagebox.showinfo('Sukces','Produkt został zaktualizowany.')

        normal = ttk.Style(window)
        normal.configure("norm.TButton", font=("Calibri", 12))

        button=ttk.Button(window, text="Zaktualizuj", command=lambda: updatedetail(id_product), style="norm.TButton", width=10)
        button.grid(row=3, column=0, padx=5, pady=5, sticky = tk.W)
        


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
