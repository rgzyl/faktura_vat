###  Wymagania systemowe  ###
### --------------------- ###
# tkinter
# tkscrolledframe
# tkcalendar
# sqlite3
# FPDF
### --------------------- ###

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import tix as tx
import sqlite3
from tkscrolledframe import ScrolledFrame
from tkcalendar import *
import datetime
from fpdf import FPDF
from tkinter import filedialog
import csv
import os



### Panel logowania ###



class Login(tk.Tk):
            
    def __init__(self, master):        
        self.master = master

        master.title("Faktura VAT - panel logowania")

        def sql_commands():
            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            cur = con.cursor()

            c.execute("DROP TABLE IF EXISTS user;") 

            c.execute("CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR, password VARCHAR);")
            con.commit()

            c.execute("INSERT INTO user VALUES (1, 'admin', '1234');")
            con.commit()

            c.execute("DROP TABLE IF EXISTS profile;") 

            c.execute("CREATE TABLE profile (id INTEGER PRIMARY KEY AUTOINCREMENT, nazwa VARCHAR, ulica VARCHAR, kod VARCHAR, miasto VARCHAR, nip VARCHAR, telefon VARCHAR);")
            con.commit()

            c.execute("INSERT INTO profile VALUES (1, 'Faktura VAT Sp. z. o. o.', 'pl. Maxa Borna 9', '50-204', 'Wroclaw', '884-183-09-52', '22 884 54 86');")
            con.commit()

            c.execute("DROP TABLE IF EXISTS products;") 
            c.execute("CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL);")
            con.commit()

            c.execute("INSERT INTO products VALUES (1, 'Sofa', '999.99');")
            con.commit()

            c.execute("DROP TABLE IF EXISTS clients;") 
            c.execute("CREATE TABLE clients (C_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nabywca VARCHAR (5, 100) DEFAULT [-], NIP VARCHAR (5, 20) DEFAULT [-], REGON VARCHAR (5, 50) DEFAULT [-], VAT_EU VARCHAR (5, 20) DEFAULT [-], PESEL VARCHAR (5, 20) DEFAULT [-], NUMER_FIRMY VARCHAR (5, 50) DEFAULT [-], OSOBA_FIZYCZNA VARCHAR (1, 1) DEFAULT [-], ULICA TIME (5, 50) DEFAULT [-], MIASTO VARCHAR (5, 100) DEFAULT [-], KOD VARCHAR (5, 20) DEFAULT [-]);")
            con.commit()

            c.execute("INSERT INTO clients VALUES (1, 'Radosław Gzyl', '', '', '', '', '', 'T', 'Wymyślona 28', 'Strzegom', '58-150');")

            c.execute("DROP TABLE IF EXISTS invoice;") 
            c.execute("CREATE TABLE invoice (id INTEGER PRIMARY KEY AUTOINCREMENT, number VARCHAR, sale_date DATE, issue_date DATETIME, place VARCHAR, choice VARCHAR, payment_date DATE, nabywca VARCHAR, ulica VARCHAR, kod_miasto VARCHAR, vat VARCHAR, nazwa VARCHAR, ilosc INTEGER, cena REAL, stawka REAL, nazwa_1 VARCHAR, ilosc_1 INTEGER, cena_1 REAL, stawka_1 REAL, nazwa_2 VARCHAR, ilosc_2 INTEGER, cena_2 REAL, stawka_2 REAL, nazwa_3 VARCHAR, ilosc_3 INTEGER, cena_3 INTEGER, stawka_3 REAL);")
            con.commit()

            c.execute("INSERT INTO invoice VALUES (1, 1, '27-12-2020', '27-12-2020', 'Wroclaw', 'Przelew', '27-12-2020', 'Radoslaw Gzyl', 'Olszowa 14', '58-150 Strzegom', 'T', 'Sofa', '1', '999.99', '23', '', '', '', '', '', '', '', '', '', '', '', '' );")
            con.commit()

            c.close()
            con.close()

        def getBoolean(event):
            self.bool.get()

        sql_commands()

        title = ttk.Label(master, text="Faktura VAT", font=("Calibri", 24, 'bold'))
        title.pack(padx=100, pady=100)

        labelframe = tk.LabelFrame(master, text="Panel logowania", padx=10, pady=10, font=("Calibri", 12))  
        labelframe.pack()

        self.bool=tk.BooleanVar()
        self.bool.set("False")
        self.username = tk.StringVar()
        self.password = tk.StringVar()
     
        username_label = ttk.Label(labelframe, text="Nazwa użytkownika: ", width=20, font=("Calibri", 12))
        username_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        username_entry = ttk.Entry(labelframe, textvariable=self.username, width=25, font=("Calibri", 12))
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        password_label = ttk.Label(labelframe, text="Hasło: ", width=20, font=("Calibri", 12))
        password_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        password_entry = ttk.Entry(labelframe, textvariable=self.password, show="*", width=25, font=("Calibri", 12))
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        styl = ttk.Style()
        styl.configure("my.TCheckbutton", font=("Calibri", 12))

        check_button = ttk.Checkbutton(labelframe, text="Zapamiętaj mnie", width=20, style="my.TCheckbutton", variable=self.bool)
        check_button.bind("<Button-1>", getBoolean)
        check_button.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5, ipadx=2)

        if os.path.isfile('log/choice.txt'):
            with open('log/choice.txt','r') as file:
                self.bool.set(file.read())
                
        if self.bool.get()==True:
            if os.path.isfile('log/username.txt'):
                with open('log/username.txt','r') as file:
                    self.username.set(file.read())

        if self.bool.get()==True:
            if os.path.isfile('log/password.txt'):
                with open('log/password.txt','r') as file:
                    self.password.set(file.read())

        s = ttk.Style()
        s.configure("my.TButton", font=("Calibri", 12))
        
        login_button = ttk.Button(labelframe, text="Zaloguj się", command=lambda:self.login(master), width=25, style="my.TButton")
        login_button.grid(row=2, column=1, padx=5, pady=5)

        data = ttk.Label(master, text="Autorzy: Radosław Gzyl, Mateusz Trzebiński, Maciej Jopek, Kamil Stefaniuk, Zuzanna Lenczyk-Wąsowska", font=("Calibri", 8, ""))
        data.pack(side=tk.BOTTOM, pady=10)


    def login(self, master):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Błąd logowania", "Wszystkie pola muszą być wypełnione!")
        else:
            with sqlite3.connect("db/database.db") as db:
                c = db.cursor()
                c.execute("select password from user where username = '%s'" % self.username.get())

                try:
                    haslo = c.fetchone()[0]
                except Exception:
                    haslo = " "

                c.close()

            if self.password.get() == str(haslo):
                master.destroy()
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

        master.title("Faktura VAT")
        

        def combo_data():

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute('SELECT nabywca FROM clients ORDER BY nabywca')

            data = []
            for row in c.fetchall():
                data.append(row[0])
            return data
        

        def combo_product():

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute('SELECT name FROM products ORDER BY name')

            data = []
            for row in c.fetchall():
                data.append(row[0])
            return data


        def details(event):

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute("SELECT ulica, miasto, osoba_fizyczna, nip, regon, vat_eu, pesel, kod FROM clients WHERE nabywca='"+event.widget.get()+"'")

            for row in query:
                ulica_entry.config(state = tk.NORMAL)
                ulica_entry.delete(0, tk.END)
                ulica_entry.insert(0, row[0])
                ulica_entry.config(state = "readonly")

                kod_miasto_entry.config(state = tk.NORMAL)
                kod_miasto_entry.delete(0, tk.END)
                kod_miasto_entry.insert(0, row[7]+" "+row[1])
                kod_miasto_entry.config(state = "readonly")

                if row[2] == "T":
                    osoba_entry.config(state = tk.NORMAL)
                    osoba_entry.delete(0, tk.END)
                    osoba_entry.insert(0, row[2])
                    osoba_entry.config(state = "readonly")
                    osoba_label = ttk.Label(window,text="Osoba fizyczna:", font=("Calibri", 12))
                    osoba_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
                elif len(row[3]) == 10:
                    osoba_entry.config(state = tk.NORMAL)
                    osoba_entry.delete(0, tk.END)
                    osoba_entry.insert(0, row[3])
                    osoba_entry.config(state = "readonly")
                    osoba_label = ttk.Label(window,text="NIP:                   ", font=("Calibri", 12))
                    osoba_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
                elif len(row[4]) == 14:
                    osoba_entry.config(state = tk.NORMAL)
                    osoba_entry.delete(0, tk.END)
                    osoba_entry.insert(0, row[4])
                    osoba_entry.config(state = "readonly")
                    osoba_label = ttk.Label(window,text="REGON:                 ", font=("Calibri", 12))
                    osoba_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
                elif len(row[5]) == 13:
                    osoba_entry.config(state = tk.NORMAL)
                    osoba_entry.delete(0, tk.END)
                    osoba_entry.insert(0, row[5])
                    osoba_entry.config(state = "readonly")
                    osoba_label = ttk.Label(window,text="VAT EU:                 ", font=("Calibri", 12))
                    osoba_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
                elif len(row[6]) == 11:
                    osoba_entry.config(state = tk.NORMAL)
                    osoba_entry.delete(0, tk.END)
                    osoba_entry.insert(0, row[6])
                    osoba_entry.config(state = "readonly")
                    osoba_label = ttk.Label(window,text="PESEL:                 ", font=("Calibri", 12))
                    osoba_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
                    
            c.close()
            con.close()


        def detail_first(event):

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute("SELECT price FROM products WHERE name='"+event.widget.get()+"'")

            for row in query:
                cena_e.config(state = tk.NORMAL)
                cena_e.delete(0, tk.END)
                cena_e.insert(0, row[0])
                cena_e.config(state = "readonly")

            c.close()
            con.close()


        def detail_second(event):

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute("SELECT price FROM products WHERE name='"+event.widget.get()+"'")

            for row in query:
                cena_ee.config(state = tk.NORMAL)
                cena_ee.delete(0, tk.END)
                cena_ee.insert(0, row[0])
                cena_ee.config(state = "readonly")

            c.close()
            con.close()

            
        def detail_third(event):

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute("SELECT price FROM products WHERE name='"+event.widget.get()+"'")

            for row in query:
                cena_eee.config(state = tk.NORMAL)
                cena_eee.delete(0, tk.END)
                cena_eee.insert(0, row[0])
                cena_eee.config(state = "readonly")

            c.close()
            con.close()

            
        def detail_fourth(event):

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute("SELECT price FROM products WHERE name='"+event.widget.get()+"'")

            for row in query:
                cena_eeee.config(state = tk.NORMAL)
                cena_eeee.delete(0, tk.END)
                cena_eeee.insert(0, row[0])
                cena_eeee.config(state = "readonly")

            c.close()
            con.close()

    
        ttk.Label(self, text="Faktura VAT", font=("Calibri", 24, "bold")).pack(pady=10)

        style = ttk.Style(self)
        style.configure("my.TButton", font=("Calibri", 19, "bold"))

        szczegoly = ttk.Style(self)
        szczegoly.configure("sz.TButton", font=("Calibri", 18))

        menu = ttk.Frame(self)
        menu.pack()
        
        panel = ttk.Button(menu, text="Panel użytkownika", command=lambda: master.switch_frame(Profile), style="my.TButton")
        panel.pack(padx=5, ipadx=10, side=tk.LEFT, ipady=1)
        
        klient = ttk.Button(menu, text="Klienci", command=lambda: master.switch_frame(Client), style="my.TButton")
        klient.pack(side=tk.LEFT, ipady=1)
        
        produkt = ttk.Button(menu, text='Produkty', command=lambda: master.switch_frame(Product), style="my.TButton")
        produkt.pack(side=tk.LEFT, padx=5, ipady=1)
        
        #przycisk = ttk.Button(menu, text="Zamknij", command=lambda: master.close(), style="my.TButton")
        #przycisk.pack(side=tk.LEFT, ipady=1)

        przycisk = ttk.Button(menu, text="Pliki", command=lambda: master.switch_frame(Files), style="my.TButton")
        przycisk.pack(side=tk.LEFT, ipady=1)

        ttk.Button(self, text="Faktura VAT - szczegóły", command=lambda: master.switch_frame(Invoice), style="sz.TButton").pack(pady=10, ipady=2, ipadx=240)

        frame = ttk.LabelFrame(self, text="Dane do faktury")
        frame.pack(padx=10, pady=0, fill="x")

        self.numer = tk.StringVar(self)      
        self.miejsce = tk.StringVar(self)       
        self.sprzedaz = tk.StringVar(self)
        self.wystawienia = tk.StringVar(self)
        self.sposob = tk.StringVar(self)
        self.termin = tk.StringVar(self)

        db=sqlite3.connect('db/database.db')
        c=db.cursor()
        query=c.execute("SELECT number FROM invoice ORDER BY number DESC LIMIT 1;")

        if c.fetchall() == []:
            numer_label = ttk.Label(frame, text="Numer faktury:", font=("Calibri", 12))
            numer_label.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W)
            numer_entry = ttk.Entry(frame, width=27, textvariable=self.numer, font=("Calibri", 12))
            numer_entry.insert(0, int(1))
            numer_entry.config(state = "readonly")
            numer_entry.grid(padx=5, pady=5, row=0, column=1, sticky=tk.W)
        else:
            query=c.execute("SELECT number FROM invoice ORDER BY number DESC LIMIT 1;")
            for i in query:
                numer_label = ttk.Label(frame, text="Numer faktury:", font=("Calibri", 12))
                numer_label.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W)
                numer_entry = ttk.Entry(frame, width=27, textvariable=self.numer, font=("Calibri", 12))
                numer_entry.insert(0, str(int(i[0])+int(1)))
                numer_entry.config(state = "readonly")
                numer_entry.grid(padx=5, pady=5, row=0, column=1, sticky=tk.W)

        wystawiona_label = ttk.Label(frame, text="Data wystawienia:", font=("Calibri", 12))
        wystawiona_label.grid(padx=5, pady=5, row=1, column=0, sticky=tk.W)
        wystawiona_entry = DateEntry(frame, width=25, textvariable=self.wystawienia,  font=("Calibri", 12), locale='en_US', date_pattern='dd-mm-y')  
        wystawiona_entry.grid(padx=5, pady=5, row=1, column=1, sticky=tk.W)

        sprzedaz_label = ttk.Label(frame, text="Data sprzedaży:", font=("Calibri", 12))
        sprzedaz_label.grid(padx=5, pady=5, row=0, column=2, sticky=tk.W)
        sprzedaz_entry = DateEntry(frame, width=25, textvariable=self.sprzedaz, font=("Calibri", 12), locale='en_US', date_pattern='dd-mm-y')
        sprzedaz_entry.grid(padx=5, pady=5, row=0, column=3, sticky=tk.W)

        miejsce_label = ttk.Label(frame, text="Miejsce wystawienia:", font=("Calibri", 12))
        miejsce_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
        miejsce_entry = ttk.Entry(frame, width=27, textvariable=self.miejsce, font=("Calibri", 12))
        miejsce_entry.insert(0, "Wrocław")
        miejsce_entry.grid(padx=5, pady=5, row=1, column=3, sticky=tk.W)

        sposob_label = ttk.Label(frame, text="Sposób zapłaty:", font=("Calibri", 12))
        sposob_label.grid(padx=5, pady=5, row=2, column=0, sticky=tk.W)
            
        sposob_combobox = ttk.Combobox(frame, textvariable=self.sposob, font=("Calibri", 12), width=25)
        sposob_combobox.grid(padx=5, pady=5, row=2, column=1, sticky=tk.W)
        sposob_combobox['values'] = ('Gotówka', ' Przelew') 
        sposob_combobox.current(0) 

        termin_label = ttk.Label(frame, text="Termin zapłaty:", font=("Calibri", 12))
        termin_label.grid(padx=5, pady=5, row=2, column=2, sticky=tk.W)
        termin_entry = DateEntry(frame, width=25, textvariable=self.termin,  font=("Calibri", 12), locale='en_US', date_pattern='dd-mm-y')  
        termin_entry.grid(padx=5, pady=5, row=2, column=3, sticky=tk.W)

        window = ttk.LabelFrame(self, text="Klienci")
        window.pack(padx=10, pady=5, fill="x")

        self.nabywca = tk.StringVar(self)
        self.ulica = tk.StringVar(self)
        self.kod_miasto = tk.StringVar(self) 
        self.osoba = tk.StringVar(self)

            
        ulica_label = ttk.Label(window, width=17, text="Ulica:", font=("Calibri", 12))
        ulica_label.grid(padx=5, pady=5, row=0, column=2, sticky=tk.W)
        ulica_entry = ttk.Entry(window, width=27 ,state="readonly", textvariable=self.ulica, font=("Calibri", 12))
        ulica_entry.grid(padx=5, pady=5, row=0, column=3, sticky=tk.W)

        kod_miasto_label = ttk.Label(window,text="Kod/miasto:", font=("Calibri", 12))
        kod_miasto_label.grid(padx=5, pady=5, row=1, column=0, sticky=tk.W)
        kod_miasto_entry = ttk.Entry(window, width=27, state="readonly", textvariable=self.kod_miasto, font=("Calibri", 12))
        kod_miasto_entry.grid(padx=5, pady=5, row=1, column=1, sticky=tk.W)

        osoba_entry = ttk.Entry(window, width=27, state="readonly", textvariable=self.osoba, font=("Calibri", 12))
        osoba_entry.grid(padx=5, pady=5, row=1, column=3, sticky=tk.W)
                    
        nabywca_name = ttk.Label(window, width=15, text="Nabywca:", font=("Calibri", 12))
        nabywca_name.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W)

        combo_nabywca_name = ttk.Combobox(window, width=25, textvariable=self.nabywca, font=("Calibri", 12))
        combo_nabywca_name.grid(padx=5, pady=5, row=0, column=1, sticky=tk.W)
        combo_nabywca_name['values'] = combo_data()
        combo_nabywca_name.bind("<<ComboboxSelected>>", details)

        style = ttk.Style()
        style.configure("font.TButton", font=("Calibri", 12))

        products = ttk.LabelFrame(self, text="Produkty")
        products.pack(padx=10, pady=5, fill="x")
           
        self.nazwa = tk.StringVar(self)
        self.cena = tk.StringVar(self)
        self.ilosc = tk.StringVar(self)
        self.stawka = tk.StringVar(self)
                    
        nazwa_l = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
        nazwa_l.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W)
        nazwa_c = ttk.Combobox(products, textvariable=self.nazwa, font=("Calibri", 12), width=20)
        nazwa_c.grid(padx=5, pady=5, row=0, column=1, sticky=tk.W)
        nazwa_c['values'] = combo_product()
        nazwa_c.bind("<<ComboboxSelected>>", detail_first)

        style = ttk.Style()
        style.configure("font.TButton", font=("Calibri", 12))

        ilosc_l = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
        ilosc_l.grid(padx=5, pady=5, row=0, column=2, sticky=tk.W)
        ilosc_e = ttk.Entry(products, textvariable=self.ilosc, font=("Calibri", 12), width=7)
        ilosc_e.grid(padx=5, pady=5, row=0, column=3, sticky=tk.W)

        cena_l = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
        cena_l.grid(padx=5, pady=5, row=0, column=4, sticky=tk.W)
        cena_e = ttk.Entry(products,state="readonly", textvariable=self.cena, font=("Calibri", 12), width=13)
        cena_e.grid(padx=5, pady=5, row=0, column=5, sticky=tk.W)

        stawka_l = ttk.Label(products,text="Stawka VAT:", font=("Calibri", 12))
        stawka_l.grid(padx=5, pady=5, row=0, column=6, sticky=tk.W)
        stawka_combobox = ttk.Combobox(products, textvariable=self.stawka, font=("Calibri", 12), width=5)
        stawka_combobox.grid(padx=5, pady=5, row=0, column=7, sticky=tk.W)
        stawka_combobox['values'] = ('23', '27', '25', '24', '22', '21', '20', '19', '17', '16', '15', '10', '9.5', '9', '8.5', '8', '7.7', '7', '6.5', '5.5', '5', '4', '3', '0') 
        #stawka_combobox.current(0) 

        self.nazwa_1 = tk.StringVar(self)
        self.cena_1 = tk.StringVar(self)
        self.ilosc_1 = tk.StringVar(self)
        self.stawka_1 = tk.StringVar(self)
                    
        nazwa_ll = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
        nazwa_ll.grid(padx=5, pady=5, row=1, column=0, sticky=tk.W)
        nazwa_cc = ttk.Combobox(products, textvariable=self.nazwa_1, font=("Calibri", 12), width=20)
        nazwa_cc.grid(padx=5, pady=5, row=1, column=1, sticky=tk.W)
        nazwa_cc['values'] = combo_product()
        nazwa_cc.bind("<<ComboboxSelected>>", detail_second)

        ilosc_ll = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
        ilosc_ll.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
        ilosc_ee = ttk.Entry(products, textvariable=self.ilosc_1, font=("Calibri", 12), width=7)
        ilosc_ee.grid(padx=5, pady=5, row=1, column=3, sticky=tk.W)

        cena_ll = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
        cena_ll.grid(padx=5, pady=5, row=1, column=4, sticky=tk.W)
        cena_ee = ttk.Entry(products,state="readonly", textvariable=self.cena_1, font=("Calibri", 12), width=13)
        cena_ee.grid(padx=5, pady=5, row=1, column=5, sticky=tk.W)

        stawka_ll = ttk.Label(products,text="Stawka VAT:", font=("Calibri", 12))
        stawka_ll.grid(padx=5, pady=5, row=1, column=6, sticky=tk.W)
        stawka_aa_combobox = ttk.Combobox(products, textvariable=self.stawka_1, font=("Calibri", 12), width=5)
        stawka_aa_combobox.grid(padx=5, pady=5, row=1, column=7, sticky=tk.W)
        stawka_aa_combobox['values'] = ('23', '27', '25', '24', '22', '21', '20', '19', '17', '16', '15', '10', '9.5', '9', '8.5', '8', '7.7', '7', '6.5', '5.5', '5', '4', '3', '0')  

        self.nazwa_2 = tk.StringVar(self)
        self.cena_2 = tk.StringVar(self)
        self.ilosc_2 = tk.StringVar(self)
        self.stawka_2 = tk.StringVar(self)
                    
        nazwa_lll = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
        nazwa_lll.grid(padx=5, pady=5, row=2, column=0, sticky=tk.W)
        nazwa_ccc = ttk.Combobox(products, textvariable=self.nazwa_2, font=("Calibri", 12), width=20)
        nazwa_ccc.grid(padx=5, pady=5, row=2, column=1, sticky=tk.W)
        nazwa_ccc['values'] = combo_product()
        nazwa_ccc.bind("<<ComboboxSelected>>", detail_third)

        ilosc_lll = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
        ilosc_lll.grid(padx=5, pady=5, row=2, column=2, sticky=tk.W)
        ilosc_eee = ttk.Entry(products, textvariable=self.ilosc_2, font=("Calibri", 12), width=7)
        ilosc_eee.grid(padx=5, pady=5, row=2, column=3, sticky=tk.W)

        cena_lll = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
        cena_lll.grid(padx=5, pady=5, row=2, column=4, sticky=tk.W)
        cena_eee = ttk.Entry(products,state="readonly", textvariable=self.cena_2, font=("Calibri", 12), width=13)
        cena_eee.grid(padx=5, pady=5, row=2, column=5, sticky=tk.W)

        stawka_lll = ttk.Label(products,text="Stawka VAT:", font=("Calibri", 12))
        stawka_lll.grid(padx=5, pady=5, row=2, column=6, sticky=tk.W)
        stawka_aaa_combobox = ttk.Combobox(products, textvariable=self.stawka_2, font=("Calibri", 12), width=5)
        stawka_aaa_combobox.grid(padx=5, pady=5, row=2, column=7, sticky=tk.W)
        stawka_aaa_combobox['values'] = ('23', '27', '25', '24', '22', '21', '20', '19', '17', '16', '15', '10', '9.5', '9', '8.5', '8', '7.7', '7', '6.5', '5.5', '5', '4', '3', '0')

        self.nazwa_3 = tk.StringVar(self)
        self.cena_3 = tk.StringVar(self)
        self.ilosc_3 = tk.StringVar(self)
        self.stawka_3 = tk.StringVar(self)
                    
        nazwa_llll = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
        nazwa_llll.grid(padx=5, pady=5, row=3, column=0, sticky=tk.W)
        nazwa_cccc = ttk.Combobox(products, textvariable=self.nazwa_3, font=("Calibri", 12), width=20)
        nazwa_cccc.grid(padx=5, pady=5, row=3, column=1, sticky=tk.W)
        nazwa_cccc['values'] = combo_product()
        nazwa_cccc.bind("<<ComboboxSelected>>", detail_fourth)

        ilosc_llll = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
        ilosc_llll.grid(padx=5, pady=5, row=3, column=2, sticky=tk.W)
        ilosc_eeee = ttk.Entry(products, textvariable=self.ilosc_3, font=("Calibri", 12), width=7)
        ilosc_eeee.grid(padx=5, pady=5, row=3, column=3, sticky=tk.W)

        cena_llll = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
        cena_llll.grid(padx=5, pady=5, row=3, column=4, sticky=tk.W)
        cena_eeee = ttk.Entry(products,state="readonly", textvariable=self.cena_3, font=("Calibri", 12), width=13)
        cena_eeee.grid(padx=5, pady=5, row=3, column=5, sticky=tk.W)

        stawka_llll = ttk.Label(products,text="Stawka VAT:", font=("Calibri", 12))
        stawka_llll.grid(padx=5, pady=5, row=3, column=6, sticky=tk.W)
        stawka_aaaa_combobox = ttk.Combobox(products, textvariable=self.stawka_3, font=("Calibri", 12), width=5)
        stawka_aaaa_combobox.grid(padx=5, pady=5, row=3, column=7, sticky=tk.W)
        stawka_aaaa_combobox['values'] = ('23', '27', '25', '24', '22', '21', '20', '19', '17', '16', '15', '10', '9.5', '9', '8.5', '8', '7.7', '7', '6.5', '5.5', '5', '4', '3', '0')

        ins = ttk.Style(self)
        ins.configure("ins.TButton", font=("Calibri", 12, "bold"))
        
        ttk.Button(self, text="DODAJ FAKTURĘ", command = lambda: self.insert(master), style="ins.TButton", width=25).pack(side=tk.RIGHT, ipady=2, padx=10)


    def insert(self, master):
            
        numerr = self.numer.get()
        miejscee = self.miejsce.get()
        sprzedazz = self.sprzedaz.get()
        wystawieniaa = self.wystawienia.get()
        sposobb = self.sposob.get()
        terminn = self.termin.get()

        nabywcaa = self.nabywca.get()
        ulicaa = self.ulica.get()
        kod_miastoo = self.kod_miasto.get()
        osobaa = self.osoba.get()

        nazwaa = self.nazwa.get()
        cenaa = self.cena.get()
        iloscc = self.ilosc.get()
        stawkaa = self.stawka.get()

        nazwa_11 = self.nazwa_1.get()
        cena_11 = self.cena_1.get()
        ilosc_11 = self.ilosc_1.get()
        stawka_11 = self.stawka_1.get()
            
        nazwa_22 = self.nazwa_2.get()
        cena_22 = self.cena_2.get()
        ilosc_22 = self.ilosc_2.get()
        stawka_22 = self.stawka_2.get()

        nazwa_33 = self.nazwa_3.get()
        cena_33 = self.cena_3.get()
        ilosc_33 = self.ilosc_3.get()
        stawka_33 = self.stawka_3.get()
          
        if miejscee=="" or nabywcaa=="" or nazwaa=="" or iloscc=="" or stawkaa=="":
            messagebox.showerror('Błąd','Wszystkie pola powinny zostać uzupełnione.')
        else:
            text = messagebox.showinfo('Sukces','Faktura została dodana.')
            if text:
                query = (f"insert into invoice('number', 'sale_date', 'issue_date', 'place', 'choice', 'payment_date', 'nabywca', 'ulica', 'kod_miasto', 'vat', 'nazwa', 'ilosc', 'cena', 'stawka', 'nazwa_1', 'ilosc_1', 'cena_1', 'stawka_1', 'nazwa_2', 'ilosc_2', 'cena_2', 'stawka_2', 'nazwa_3', 'ilosc_3', 'cena_3', 'stawka_3') values ('{numerr}', '{sprzedazz}', '{wystawieniaa}', '{miejscee}', '{sposobb}', '{terminn}', '{nabywcaa}', '{ulicaa}', '{kod_miastoo}', '{osobaa}','{nazwaa}', '{iloscc}', '{cenaa}', '{stawkaa}', '{nazwa_11}', '{ilosc_11}', '{cena_11}','{stawka_11}', '{nazwa_22}', '{ilosc_22}', '{cena_22}','{stawka_22}', '{nazwa_33}', '{ilosc_33}', '{cena_33}', '{stawka_33}')")
                with sqlite3.connect("db/database.db") as db:
                    c = db.cursor()
                    c.execute(query)
                    c.close()
                master.switch_frame(Menu)



### Widok PLIKÓW ###



class Files(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        master.title("Faktura VAT - pliki")
        
        ttk.Label(self, text="Faktura VAT - pliki", font=("Calibri", 24, "bold"), anchor="center").grid(pady=20, padx=234, columnspan=2)

        ttk.Label(self, text="Poniżej znajdują się przyciski do importowania/exportowania plików.", font=("Calibri", 14, "bold"), anchor="center").grid(columnspan=2)
        
        frame_import = ttk.LabelFrame(self, text="Zaimportuj pliki zewnętrzne")
        frame_import.grid(padx=10, pady=10)

        style = ttk.Style(self)
        style.configure("mo.TButton", font=("Calibri", 12))

        label = ttk.Label(frame_import, text="Wybierz plik do zaimportowania klientów", font=("Calibri", 12), width=45)
        label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        button = ttk.Button(frame_import, text="WYBIERZ PLIK", command=self.upload_clients, style="mo.TButton", width=45)
        button.grid(row=0, column=1, padx=5, pady=5, ipadx=10)

        label_1 = ttk.Label(frame_import, text="Wybierz plik do zaimportowania produktów", font=("Calibri", 12), width=45)
        label_1.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        button_1 = ttk.Button(frame_import, text="WYBIERZ PLIK", command=self.upload_products, style="mo.TButton", width=45)
        button_1.grid(row=1, column=1, padx=5, pady=5, ipadx=10)

        label_2 = ttk.Label(frame_import, text="Wybierz plik do zaimportowania faktur", font=("Calibri", 12), width=45)
        label_2.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        button_2 = ttk.Button(frame_import, text="WYBIERZ PLIK", command=self.upload_invoices, style="mo.TButton", width=45)
        button_2.grid(row=2, column=1, padx=5, pady=5, ipadx=10)

        frame_export = ttk.LabelFrame(self, text="Eksportuj pliki wewnętrzne")
        frame_export.grid(padx=10, pady=10)

        sty = ttk.Style(self)
        sty.configure("mi.TButton", font=("Calibri", 12))

        label = ttk.Label(frame_export, text="Wyeksportuj dane dotyczące klientów", font=("Calibri", 12), width=45)
        label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        button = ttk.Button(frame_export, text="KLIKNIJ TUTAJ", command=self.export_clients, style="mi.TButton", width=45)
        button.grid(row=0, column=1, padx=5, pady=5, ipadx=10)

        label_1 = ttk.Label(frame_export, text="Wyeksportuj dane dotyczące produktów", font=("Calibri", 12), width=45)
        label_1.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        button_1 = ttk.Button(frame_export, text="KLIKNIJ TUTAJ", command=self.export_products, style="mi.TButton", width=45)
        button_1.grid(row=1, column=1, padx=5, pady=5, ipadx=10)

        label_2 = ttk.Label(frame_export, text="Wyeksportuj dane dotyczące faktur", font=("Calibri", 12), width=45)
        label_2.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        button_2 = ttk.Button(frame_export, text="KLIKNIJ TUTAJ", command=self.export_invoices, style="mi.TButton", width=45)
        button_2.grid(row=2, column=1, padx=5, pady=5, ipadx=10)
        
        boldd = ttk.Style(self)
        boldd.configure("bol.TButton", font=("Calibri", 14, "bold"))
        
        ttk.Button(self, text="COFNIJ", style="bol.TButton",
                   command=lambda: master.switch_frame(Menu)).grid(pady=135, padx=5, columnspan=6, sticky="nswe")
        

    def upload_clients(self, event=None):
        filename = filedialog.asksaveasfilename(title = "Zapisywanie jako", filetypes = (("CSV (rozdzielony przecinkami)","*.csv"),("Wszystkie pliki","*.*")))
        
        con = sqlite3.connect("db/database.db")
        cursor = con.cursor()

        file = open(filename, encoding="utf-8")

        rows = csv.reader(file)
        cursor.executemany("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
        con.commit()
        con.close()

        if file:
            messagebox.showinfo("Sukces", "Dane dotyczące klientów zostały dodane.")
        else:
            messagebox.showerror("Błąd", "Coś poszło nie tak")
            

    def upload_products(self, event=None):
        filename = filedialog.asksaveasfilename(title = "Zapisywanie jako", filetypes = (("CSV (rozdzielony przecinkami)","*.csv"),("Wszystkie pliki","*.*")))
        
        con = sqlite3.connect("db/database.db")
        cursor = con.cursor()

        file = open(filename, encoding="utf-8")

        rows = csv.reader(file)
        cursor.executemany("INSERT INTO products VALUES (?, ?, ?)", rows)
        con.commit()
        con.close()

        if file:
            messagebox.showinfo("Sukces", "Dane dotyczące produktów zostały dodane.")
        else:
            messagebox.showerror("Błąd", "Coś poszło nie tak")
            

    def upload_invoices(self, event=None):
        filename = filedialog.asksaveasfilename(title = "Zapisywanie jako", filetypes = (("CSV (rozdzielony przecinkami)","*.csv"),("Wszystkie pliki","*.*")))
        
        con = sqlite3.connect("db/database.db")
        cursor = con.cursor()

        file = open(filename, encoding="utf-8")

        rows = csv.reader(file)
        cursor.executemany("INSERT INTO invoice VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
        con.commit()
        con.close()

        if file:
            messagebox.showinfo("Sukces", "Dane dotyczące faktur zostały dodane.")
        else:
            messagebox.showerror("Błąd", "Coś poszło nie tak")


    def export_clients(self):
        choice = messagebox.askyesno("Export", "Czy na pewno chcesz exportować tabelę klienci?")
        if choice == True:
            conn = sqlite3.connect("db/database.db")
            c = conn.cursor()
            c.execute("SELECT * FROM clients")    
            columns = [column[0] for column in c.description]
            results = []
            for row in c.fetchall():
                results.append(dict(zip(columns, row)))
            with open("export/klienci.csv", "w", newline='') as new_file:
                fieldname = columns
                writer = csv.DictWriter(new_file,fieldnames=fieldname)
                writer.writeheader()
                for line in results:
                    writer.writerow(line)
            conn.close()
            messagebox.showinfo("Export", "Tabela klienci została wyexportowana.")


    def export_products(self):
        choice = messagebox.askyesno("Export", "Czy na pewno chcesz exportować tabelę produkty?")
        if choice == True:
            conn = sqlite3.connect("db/database.db")
            c = conn.cursor()
            c.execute("SELECT * FROM products")    
            columns = [column[0] for column in c.description]
            results = []
            for row in c.fetchall():
                results.append(dict(zip(columns, row)))
            with open("export/produkty.csv", "w", newline='') as new_file:
                fieldname = columns
                writer = csv.DictWriter(new_file,fieldnames=fieldname)
                writer.writeheader()
                for line in results:
                    writer.writerow(line)
            conn.close()
            messagebox.showinfo("Export", "Tabela produkty została wyexportowana.")


    def export_invoices(self):
        choice = messagebox.askyesno("Export", "Czy na pewno chcesz exportować tabelę faktury?")
        if choice == True:
            conn = sqlite3.connect("db/database.db")
            c = conn.cursor()
            c.execute("SELECT * FROM invoice")    
            columns = [column[0] for column in c.description]
            results = []
            for row in c.fetchall():
                results.append(dict(zip(columns, row)))
            with open("export/faktury.csv", "w", newline='') as new_file:
                fieldname = columns
                writer = csv.DictWriter(new_file,fieldnames=fieldname)
                writer.writeheader()
                for line in results:
                    writer.writerow(line)
            conn.close()
            messagebox.showinfo("Export", "Tabela faktury została wyexportowana.")


                  
### Widok FAKTURY ###



class Invoice(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        master.title("Faktura VAT - szczegóły")

        sf = ScrolledFrame(self, width=800, height=600)
        sf.pack(side="top", expand=1, fill="both")
        
        sf.bind_arrow_keys(self)
        sf.bind_scroll_wheel(self)

        frame = sf.display_widget(tk.Frame)
                
        normal = ttk.Style(frame)
        normal.configure("normal.TButton", font=("Calibri", 14))
        bold = ttk.Style(frame)
        bold.configure("bo.TButton", font=("Calibri", 14, "bold"))

        ttk.Label(frame, text="Faktura VAT - szczegóły", font=("Calibri", 24, "bold"), anchor="center").grid(pady=20, padx=234, columnspan=6)
        
        ttk.Button(frame, text="ODŚWIEŻ", command=lambda: master.switch_frame(Invoice), style="normal.TButton").grid(padx=5, columnspan=6, sticky="nswe")

        ttk.Button(frame, text="COFNIJ", style="bo.TButton",
                   command=lambda: master.switch_frame(Menu)).grid(pady=10, padx=5, columnspan=6, sticky="nswe")
        
        ttk.Label(frame, text="TABELA Z FAKTURAMI", font=("Calibri", 14, "bold"), anchor="center").grid(pady=20, padx=0, columnspan=6)

        self.table(frame, master)
        

    def table(self, w, master):  
        limit = 8
        q = "SELECT id, number, nabywca from invoice" 
        h = "select count(*) from invoice"
        i=0

        normal = ttk.Style(w)
        normal.configure("normaa.TButton", font=("Calibri", 12))
        
        with sqlite3.connect("db/database.db") as db:  
            c = db.cursor()
            c.execute(q)
            r_set = c.fetchall()
            c.execute(h)
            no_rec = c.fetchone()[0]
            c.close()
        l = ["ID",
             "Numer faktury",
             "Nabywca"]

        r_set.insert(0, l)  

        for invoice in r_set:
            for j in range(len(invoice)):
                e = ttk.Label(w, text=invoice[j], font=("Calibri", 12))
                e.grid(row=i+4, column=j, padx=10, pady=3)

            if r_set.index(invoice) != 0:
                f = ttk.Button(w, text='SZCZEGÓŁY', command=lambda d=invoice[0]: self.detail(d), style="normaa.TButton")
                f.grid(row=i+4, column=j + 1)
                f = ttk.Button(w, text='EDYTUJ', command=lambda d=invoice[0]: self.update(d, master), style="normaa.TButton")
                f.grid(row=i+4, column=j + 2)
                f = ttk.Button(w, text='USUŃ', command=lambda d=invoice[0]: self.delete(d, master), style="normaa.TButton")
                f.grid(row=i+4, column=j + 3, pady=3)
            i = i + 1

            
    def detail(self, id_invoice):
        window = tk.Toplevel()
        window.resizable(0,0)
        ttk.Label(window, text="Szczegóły dot. faktur o numerze ID = "+str(id_invoice), font=("Calibri", 16, "bold")).grid(pady=20)

        con = sqlite3.connect('db/database.db')
        c = con.cursor()
        query = c.execute("SELECT id, number, sale_date, issue_date, place, choice, payment_date, nabywca, ulica, kod_miasto, vat FROM invoice WHERE id='"+str(id_invoice)+"'")
        
        for i in query:

            dane = ttk.LabelFrame(window, text="Dane do faktury")
            dane.grid(padx=10, pady=10, sticky="nswe")
            
            ttk.Label(dane, text="Numer faktury:", font=("Calibri", 12)).grid(padx=5, pady=5, row=0, column=0, sticky=tk.W)
            ttk.Label(dane, text=str(i[1])+str("/2021"), font=("Calibri", 14, "bold")).grid(padx=5, pady=5, row=0, column=1, sticky=tk.W)

            ttk.Label(dane, text="Data sprzedaży:", font=("Calibri", 12)).grid(padx=5, pady=5, row=1, column=0, sticky=tk.W)
            ttk.Label(dane, text=str(i[2]), font=("Calibri", 12)).grid(padx=5, pady=5, row=1, column=1, sticky=tk.W)

            ttk.Label(dane, text="Data wystawienia:", font=("Calibri", 12)).grid(padx=5, pady=5, row=2, column=0, sticky=tk.W)
            ttk.Label(dane, text=str(i[3]), font=("Calibri", 12)).grid(padx=5, pady=5, row=2, column=1, sticky=tk.W)

            ttk.Label(dane, text="Miejsce wystawienia:", font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=0, sticky=tk.W)
            ttk.Label(dane, text=str(i[4]), font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=1, sticky=tk.W)

            nabywca = ttk.LabelFrame(window, text="Informacje o nabywce")
            nabywca.grid(padx=10, pady=0, sticky="nswe")

            ttk.Label(nabywca, text="Nabywca:", font=("Calibri", 12)).grid(padx=5, pady=5, row=0, column=0, sticky=tk.W)
            ttk.Label(nabywca, text=str(i[7]), font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=0, column=1, sticky=tk.W)

            ttk.Label(nabywca, text="Ulica:", font=("Calibri", 12)).grid(padx=5, pady=5, row=1, column=0, sticky=tk.W)
            ttk.Label(nabywca, text=str(i[8]), font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=1, column=1, sticky=tk.W)

            ttk.Label(nabywca, text="Kod pocztowy/miasto:", font=("Calibri", 12)).grid(padx=5, pady=5, row=2, column=0, sticky=tk.W)
            ttk.Label(nabywca, text=str(i[9]), font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=2, column=1, sticky=tk.W)

            if len(i[10]) == 10:
                ttk.Label(nabywca, text="NIP:", font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=0, sticky=tk.W)
                ttk.Label(nabywca, text=str(i[10]), font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=3, column=1, sticky=tk.W)
            elif len(i[10]) == 11:
                ttk.Label(nabywca, text="PESEL:", font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=0, sticky=tk.W)
                ttk.Label(nabywca, text=str(i[10]), font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=3, column=1, sticky=tk.W)
            elif len(i[10]) == 14:
                ttk.Label(nabywca, text="REGON:", font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=0, sticky=tk.W)
                ttk.Label(nabywca, text=str(i[10]), font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=3, column=1, sticky=tk.W)
            elif len(i[10]) == 9:
                ttk.Label(nabywca, text="Numer firmy:", font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=0, sticky=tk.W)
                ttk.Label(nabywca, text=str(i[10]), font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=3, column=1, sticky=tk.W)
            elif len(i[10]) == 13:
                ttk.Label(nabywca, text="VAT EU:", font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=0, sticky=tk.W)
                ttk.Label(nabywca, text=str(i[10]), font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=3, column=1, sticky=tk.W)
            else:
                ttk.Label(nabywca, text="Osoba fizyczna:", font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=0, sticky=tk.W)
                ttk.Label(nabywca, text=str(i[10]), font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=3, column=1, sticky=tk.W)

            product = ttk.LabelFrame(window, text="Informacje o produktach")
            product.grid(pady=10, padx=10)
            
            ttk.Label(product, text="Nazwa", font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=0, column=0)
            ttk.Label(product, text="Ilość", font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=0, column=1)
            ttk.Label(product, text="Cena netto", font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=0, column=2)
            ttk.Label(product, text="Kowta netto", font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=0, column=3)
            ttk.Label(product, text="Stawka VAT", font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=0, column=4)
            ttk.Label(product, text="Kwota VAT", font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=0, column=5)
            ttk.Label(product, text="Wartość brutto", font=("Calibri", 12, "bold")).grid(padx=5, pady=5, row=0, column=6)

        query = c.execute("SELECT nazwa, ilosc, printf('%.2f',cena) AS cena, printf('%.2f',stawka) AS stawka, printf('%.2f',ilosc*cena) AS netto, printf('%.2f',(ilosc*cena*stawka)/100) AS vat, printf('%.2f',(ilosc*cena)+((ilosc*cena*stawka)/100)) AS brutto FROM invoice WHERE id='"+str(id_invoice)+"'")
        
        for i in query:
            
            ttk.Label(product, text=str(i[0]), font=("Calibri", 12)).grid(padx=5, pady=5, row=1, column=0)
            ttk.Label(product, text=str(i[1]), font=("Calibri", 12)).grid(padx=5, pady=5, row=1, column=1)
            ttk.Label(product, text=str(i[2])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=1, column=2)
            ttk.Label(product, text=str(i[4])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=1, column=3)
            ttk.Label(product, text=str(i[3] + "%"), font=("Calibri", 12)).grid(padx=5, pady=5, row=1, column=4)
            ttk.Label(product, text=str(i[5])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=1, column=5)
            ttk.Label(product, text=str(i[6])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=1, column=6)

        query = c.execute("SELECT nazwa_1, ilosc_1, printf('%.2f',cena_1) AS cena_1, printf('%.2f',stawka_1) AS stawka_1, printf('%.2f',ilosc_1*cena_1) AS netto, printf('%.2f',(ilosc_1*cena_1*stawka_1)/100) AS vat, printf('%.2f',(ilosc_1*cena_1)+((ilosc_1*cena_1*stawka_1)/100)) AS brutto FROM invoice WHERE id='"+str(id_invoice)+"'")
        
        for i in query:
            
            if i[0] != "":
                ttk.Label(product, text=str(i[0]), font=("Calibri", 12)).grid(padx=5, pady=5, row=2, column=0)
                ttk.Label(product, text=str(i[1]), font=("Calibri", 12)).grid(padx=5, pady=5, row=2, column=1)
                ttk.Label(product, text=str(i[2])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=2, column=2)
                ttk.Label(product, text=str(i[4])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=2, column=3)
                ttk.Label(product, text=str(i[3] + "%"), font=("Calibri", 12)).grid(padx=5, pady=5, row=2, column=4)
                ttk.Label(product, text=str(i[5])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=2, column=5)
                ttk.Label(product, text=str(i[6])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=2, column=6)

        query = c.execute("SELECT nazwa_2, ilosc_2, printf('%.2f',cena_2) AS cena_2, printf('%.2f',stawka_2) AS stawka_2, printf('%.2f',ilosc_2*cena_2) AS netto, printf('%.2f',(ilosc_2*cena_2*stawka_2)/100) AS vat, printf('%.2f',(ilosc_2*cena_2)+((ilosc_2*cena_2*stawka_2)/100)) AS brutto FROM invoice WHERE id='"+str(id_invoice)+"'")
        
        for i in query:

            if i[0] != "":
                ttk.Label(product, text=str(i[0]), font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=0)
                ttk.Label(product, text=str(i[1]), font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=1)
                ttk.Label(product, text=str(i[2])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=2)
                ttk.Label(product, text=str(i[4])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=3)
                ttk.Label(product, text=str(i[3] + "%"), font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=4)
                ttk.Label(product, text=str(i[5])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=5)
                ttk.Label(product, text=str(i[6])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=3, column=6)

        query = c.execute("SELECT nazwa_3, ilosc_3, printf('%.2f',cena_3) AS cena_3, printf('%.2f',stawka_3) AS stawka_3, printf('%.2f',ilosc_3*cena_3) AS netto, printf('%.2f',(ilosc_3*cena_3*stawka_3)/100) AS vat, printf('%.2f',(ilosc_3*cena_3)+((ilosc_3*cena_3*stawka_3)/100)) AS brutto FROM invoice WHERE id='"+str(id_invoice)+"'")
        
        for i in query:

            if i[0] != "":
                ttk.Label(product, text=str(i[0]), font=("Calibri", 12)).grid(padx=5, pady=5, row=4, column=0)
                ttk.Label(product, text=str(i[1]), font=("Calibri", 12)).grid(padx=5, pady=5, row=4, column=1)
                ttk.Label(product, text=str(i[2])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=4, column=2)
                ttk.Label(product, text=str(i[4])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=4, column=3)
                ttk.Label(product, text=str(i[3] + "%"), font=("Calibri", 12)).grid(padx=5, pady=5, row=4, column=4)
                ttk.Label(product, text=str(i[5])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=4, column=5)
                ttk.Label(product, text=str(i[6])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, row=4, column=6)

        query = c.execute("SELECT printf('%.2f',((ilosc*cena)*stawka/100+(ilosc*cena))+((ilosc_1*cena_1)*stawka_1/100+(ilosc_1*cena_1))+((ilosc_2*cena_2)*stawka_2/100+(ilosc_2*cena_2))+((ilosc_3*cena_3)*stawka_3/100+(ilosc_3*cena_3))) as sum FROM invoice WHERE id='"+str(id_invoice)+"'")

        for row in query:
            ttk.Label(product, text="razem:", font=("Calibri", 12, "bold")).grid(padx=5, pady=5, column=5, row=6)
            ttk.Label(product, text=str(row[0])+str(" zł"), font=("Calibri", 12)).grid(padx=5, pady=5, column=6, row=6)

                        
        pdf = tk.Frame(window)
        pdf.grid()

        style = ttk.Style(window)
        style.configure("pd.TButton", font=("Calibri", 15, "bold"))
            
        ttk.Button(pdf, text="ORGINAŁ", style="pd.TButton", command=lambda: self.orginal(id_invoice)).grid(row=0, column=1, padx=10, pady=10, ipady=2)
        ttk.Button(pdf, text="KOPIA", style="pd.TButton", command=lambda: self.kopia(id_invoice)).grid(row=0, column=2, padx=10, pady=10, ipady=2)
        ttk.Button(pdf, text="DUPLIKAT", style="pd.TButton", command=lambda: self.duplikat(id_invoice)).grid(row=0, column=3, padx=10, pady=10, ipady=2)
                

    def orginal(self, id_invoice):
        con = sqlite3.connect('db/database.db')
        c = con.cursor()
        query = c.execute("SELECT * FROM invoice WHERE id='"+str(id_invoice)+"'")

        for i in query:
            numer_faktury = i[1]
            data_sprzedazy = i[2]
            data_wystawienia = i[3]
            miejsce_wystawienia = i[4]
            sposob_zaplaty = i[5]
            termin_zaplaty = i[6]
            nabywca = i[7]
            ulica = i[8]
            kod_miasto = i[9]
            vat = i[10]

        result = c.execute("SELECT * FROM profile WHERE id=1")

        for row in result:
            uzytkownik = row[1]
            ulica_u = row[2]
            kod = row[3] + " " + row[4]
            nip = row[5]

        pdf=FPDF(format='letter', unit='in')
     
        pdf.add_page()

        pdf.add_font('font', '', 'font/Calibri.ttf', uni=True)
        pdf.add_font('font_bold', '', 'font/Calibri_bold.ttf', uni=True) 
        pdf.set_font('font_bold','',16) 
        pdf.cell(7.8,0.5,'Faktura VAT', border=0, align="C")
        pdf.ln(0.5)

        pdf.set_font('font','',12) 
        pdf.cell(7.8,0.5,'orginał', border=0, align="R")
        pdf.ln(0.5)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'Numer faktury:', border=0, align="L")
        pdf.set_font('font_bold','',14) 
        pdf.cell(6.2,0.3,numer_faktury+"/2021", border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'Data wystawienia:', border=0, align="L")
        pdf.cell(6.2,0.3,data_wystawienia, border=0, align="L")
        pdf.ln(0.3)

        pdf.cell(1.6,0.3,'Data sprzedaży:', border=0, align="L")
        pdf.cell(6.2,0.3,data_sprzedazy, border=0, align="L")
        pdf.ln(0.3)

        pdf.cell(1.6,0.3,'Miejsce wystawienia:', border=0, align="L")
        pdf.cell(6.2,0.3,miejsce_wystawienia, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'Sprzedawca:', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(2.3,0.3,uzytkownik, border=0, align="L")
        pdf.set_font('font','',12) 
        pdf.cell(0.8,0.3,'Nabywca: ', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(1.6,0.3,nabywca, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(2.3,0.3,ulica_u, border=0, align="L")
        pdf.set_font('','',12) 
        pdf.cell(0.8,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(1.6,0.3,ulica, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(2.3,0.3,kod, border=0, align="L")
        pdf.set_font('font','',12) 
        pdf.cell(0.8,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(1.6,0.3,kod_miasto, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12)
        pdf.cell(2.3,0.3,'NIP: '+nip, border=0, align="L")
        pdf.set_font('font','',12) 
        pdf.cell(0.8,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12)

        if len(vat) == 10:
            pdf.cell(2.3,0.3,'NIP: '+vat, border=0, align="L") 
        elif len(vat) == 11:
            pdf.cell(2.3,0.3,'PESEL: '+vat, border=0, align="L")
        elif len(vat) == 14:
            pdf.cell(2.3,0.3,'REGON: '+vat, border=0, align="L")
        elif len(vat) == 9:
            pdf.cell(2.3,0.3,'Numer firmy: '+vat, border=0, align="L")
        elif len(vat) == 13:
            pdf.cell(2.3,0.3,'VAT EU: '+vat, border=0, align="L")
        else:
            pdf.cell(1.6,0.3,'Osoba fizyczna', border=0, align="L")


        pdf.ln(0.6)

        c.execute("SELECT nazwa, ilosc, printf('%.2f',cena) AS cena, printf('%.2f',stawka) AS stawka, printf('%.2f',ilosc*cena) AS netto, printf('%.2f',(ilosc*cena*stawka)/100) AS vat, printf('%.2f',(ilosc*cena)+((ilosc*cena*stawka)/100)) AS brutto, nazwa_1, ilosc_1, printf('%.2f',cena_1) AS cena_1, printf('%.2f',stawka_1) AS stawka_1, printf('%.2f',ilosc_1*cena_1) AS netto_1, printf('%.2f',(ilosc_1*cena_1*stawka_1)/100) AS vat_1, printf('%.2f',(ilosc_1*cena_1)+((ilosc_1*cena_1*stawka_1)/100)) AS brutto_1, nazwa_2, ilosc_2, printf('%.2f',cena_2) AS cena_2, printf('%.2f',stawka_2) AS stawka_2, printf('%.2f',ilosc_2*cena_2) AS netto_2, printf('%.2f',(ilosc_2*cena_2*stawka_2)/100) AS vat_2, printf('%.2f',(ilosc_2*cena_2)+((ilosc_2*cena_2*stawka_2)/100)) AS brutto_2, nazwa_3, ilosc_3, printf('%.2f',cena_3) AS cena_3, printf('%.2f',stawka_3) AS stawka_3, printf('%.2f',ilosc_3*cena_3) AS netto_3, printf('%.2f',(ilosc_3*cena_3*stawka_3)/100) AS vat_3, printf('%.2f',(ilosc_3*cena_3)+((ilosc_3*cena_3*stawka_3)/100)) AS brutto_3 FROM invoice WHERE id='"+str(id_invoice)+"'")

        #"{:.2f}".format(a)
        
        for i in query:
            nazwa = i[0]
            ilosc = i[1]
            cena = float(i[2])
            stawka = "{:.2f}".format(float(i[3]))
            netto = "{:.2f}".format(float(i[4]))
            vat = "{:.2f}".format(float(i[5]))
            brutto = "{:.2f}".format(float(i[6]))
            nazwa1 = i[7]
            ilosc1 = i[8]
            cena1 = "{:.2f}".format(float(i[9]))
            stawka1 = "{:.2f}".format(float(i[10]))
            nazwa2 = i[14]
            ilosc2 = i[15]
            cena2 = "{:.2f}".format(float(i[16]))
            stawka2 = "{:.2f}".format(float(i[17]))
            nazwa3 = i[21]
            ilosc3 = i[22]
            cena3 = "{:.2f}".format(float(i[23]))
            stawka3 = "{:.2f}".format(float(i[24]))
            
            pdf.set_font('font_bold', '', 12)
            pdf.cell(0.3,0.3,'LP', border=1, align="C")
            pdf.cell(1.8,0.3,'Nazwa', border=1, align="C")
            pdf.cell(0.5,0.3,'Ilość', border=1, align="C")
            pdf.cell(1.0,0.3,'Cena netto', border=1, align="C")
            pdf.cell(1.0,0.3,'Kwota netto', border=1, align="C")
            pdf.cell(1.0,0.3,'Stawka VAT', border=1, align="C")
            pdf.cell(1.0,0.3,'Kwota VAT', border=1, align="C")
            pdf.cell(1.2,0.3,'Wartość brutto', border=1, align="C")

            pdf.set_font('font','',12.0) 
            pdf.ln(0.3)
            pdf.cell(0.3,0.3,'1', border=1, align="C")
            pdf.cell(1.8,0.3,nazwa, border=1, align="C")
            pdf.cell(0.5,0.3,str(ilosc), border=1, align="C")
            pdf.cell(1.0,0.3,str(cena), border=1, align="C")
            pdf.cell(1.0,0.3,str(netto), border=1, align="C")
            pdf.cell(1.0,0.3,str(stawka), border=1, align="C")
            pdf.cell(1.0,0.3,str(vat), border=1, align="C")
            pdf.cell(1.2,0.3,str(brutto), border=1, align="C")
            
            if nazwa1 != "":
                pdf.ln(0.3)
                pdf.cell(0.3,0.3,'2', border=1, align="C")
                pdf.cell(1.8,0.3,nazwa1, border=1, align="C")
                pdf.cell(0.5,0.3,str(ilosc1), border=1, align="C")
                pdf.cell(1.0,0.3,str(cena1), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[11]))), border=1, align="C")
                pdf.cell(1.0,0.3,str(stawka1), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[12]))), border=1, align="C")
                pdf.cell(1.2,0.3,str("{:.2f}".format(float(i[13]))), border=1, align="C")
    
            if nazwa2 != "":
                         
                pdf.ln(0.3)
                pdf.cell(0.3,0.3,'3', border=1, align="C")
                pdf.cell(1.8,0.3,nazwa2, border=1, align="C")
                pdf.cell(0.5,0.3,str(ilosc2), border=1, align="C")
                pdf.cell(1.0,0.3,str(cena2), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[18]))), border=1, align="C")
                pdf.cell(1.0,0.3,str(stawka2), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[19]))), border=1, align="C")
                pdf.cell(1.2,0.3,str("{:.2f}".format(float(i[20]))), border=1, align="C")

            if nazwa3 != "":
                pdf.ln(0.3)
                pdf.cell(0.3,0.3,'4', border=1, align="C")
                pdf.cell(1.8,0.3,nazwa3, border=1, align="C")
                pdf.cell(0.5,0.3,str(ilosc3), border=1, align="C")
                pdf.cell(1.0,0.3,str(cena3), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[25]))), border=1, align="C")
                pdf.cell(1.0,0.3,str(stawka3), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[26]))), border=1, align="C")
                x = str("{:.2f}".format(float(i[27])))
                pdf.cell(1.2,0.3,x, border=1, align="C")

        query = c.execute("select printf('%.2f',ilosc*cena+ilosc_1*cena_1+ilosc_2*cena_2+ilosc_3*cena_3) as kwota_netto, printf('%.2f',stawka), printf('%.2f',(ilosc*cena*stawka+ilosc_1*cena_1*stawka_1+ilosc_2*cena_2*stawka_2+ilosc_3*cena_3*stawka_3)/100) as kwota_vat, printf('%.2f',ilosc*cena+ilosc_1*cena_1+ilosc_2*cena_2+ilosc_3*cena_3+(ilosc*cena*stawka+ilosc_1*cena_1*stawka_1+ilosc_2*cena_2*stawka_2+ilosc_3*cena_3*stawka_3)/100) as brutto, payment_date, choice from invoice where id='"+str(id_invoice)+"'")

        for i in query:
            netto = i[0]
            stawka = i[1]
            kwota = i[2]
            brutto = i[3]
            data = i[4]
            wybor = i[5]

            pdf.ln(0.3)
            pdf.cell(0.3,0.3,'', border=0, align="C")
            pdf.cell(1.8,0.3,'', border=0, align="C")
            pdf.cell(0.5,0.3,'', border=0, align="C")
            pdf.cell(1.0,0.3,'w tym:', border=1, align="C")
            pdf.cell(1.0,0.3,str(netto), border=1, align="C")
            pdf.cell(1.0,0.3,str(stawka), border=1, align="C")
            pdf.cell(1.0,0.3,str(kwota), border=1, align="C")
            pdf.cell(1.2,0.3,str(brutto), border=1, align="C")

            pdf.ln(0.3)
            pdf.cell(0.3,0.3,'', border=0, align="C")
            pdf.cell(1.8,0.3,'', border=0, align="C")
            pdf.cell(0.5,0.3,'', border=0, align="C")
            pdf.cell(1.0,0.3,'razem:', border=1, align="C")
            pdf.cell(1.0,0.3,str(netto), border=1, align="C")
            pdf.cell(1.0,0.3,str(stawka), border=1, align="C")
            pdf.cell(1.0,0.3,str(kwota), border=1, align="C")
            pdf.cell(1.2,0.3,str(brutto), border=1, align="C")
            

        LICZBY = [
                None,
                u'jeden', u'dwa', u'trzy', u'cztery', u'pięć', u'sześć', u'siedem',
                u'osiem', u'dziewięć', u'dziesięć', u'jedenaście', u'dwanaście',
                u'trzynaście', u'czternaście', u'pietnaście', u'szesnaście',
                u'siedemnaście', u'osiemnaście', u'dziewiętnaście',
        ]

        DZIESIATKI = [
                None,
                u'dziesięć', u'dwadzieścia', u'trzydzieści', u'czterdzieści',
                u'pięćdziesiąt', u'sześćdziesiąt', u'siedemdziesiąt', u'osiemdziesiąt',
                u'dziewięćdziesiąt',
        ]

        SETKI = [
                None,
                u'sto', u'dwieście', u'trzysta', u'czterysta', u'pięćset', u'sześćset',
                u'siedemset', u'osiemset', u'dziewięćset',
        ]

        TYSIACE = [
                None,
                (u'tysiąc', u'tysiące', u'tysięcy'),
                (u'milion', u'miliony', u'milionów'),
                (u'miliard', u'miliardy', u'miliardów'),
                (u'bilion', u'biliony', u'bilionów'),
                (u'biliard', u'biliardy', u'biliardów'),
        ]


        def num2words(x, unit=None):
            wynik = []
            if not x:
                return u'zero 0/100'
            y = x % 1
            numer = int(x)
            iteration = 0
            while numer:
                sub_tysiace = numer % 1000
                tysiace = numer // 1000
                if sub_tysiace:
                    reszta = []
                    przedrostek = TYSIACE[iteration]
                    sub_setki = sub_tysiace % 100
                    setki = sub_tysiace // 100
                    sub_dziesiatki = sub_setki % 10
                    dziesiatki = sub_setki // 10
                    if SETKI[setki]:
                        reszta.append(SETKI[setki])
                    if sub_tysiace == 1:
                        if iteration == 0:
                            if LICZBY[sub_tysiace]:
                                reszta.append(LICZBY[sub_tysiace])
                        if przedrostek:
                            reszta.append(przedrostek[0])
                    elif sub_setki < 20:
                        if LICZBY[sub_setki]:
                            reszta.append(LICZBY[sub_setki])
                        if przedrostek:
                            if sub_setki > 1 and sub_setki < 5:
                                reszta.append(przedrostek[1])
                            else:
                                reszta.append(przedrostek[2])
                    else:
                        if DZIESIATKI[dziesiatki]:
                            reszta.append(DZIESIATKI[dziesiatki])
                        if LICZBY[sub_dziesiatki]:
                            reszta.append(LICZBY[sub_dziesiatki])
                        if przedrostek:
                            if sub_dziesiatki > 0 and sub_dziesiatki < 5:
                                if dziesiatki and sub_dziesiatki == 1:
                                    reszta.append(przedrostek[2])
                                else:
                                    reszta.append(przedrostek[1])
                            else:
                                reszta.append(przedrostek[2])
                    wynik = reszta + wynik
                    del reszta
                numer = tysiace
                iteration += 1
            if unit:
                wynik.append(unit)
            wynik.append(u'%d/100 PLN' % int(y * 100))
            wynik = ' '.join(wynik)
            return wynik
        

        query = c.execute("select round(ilosc*cena+ilosc_1*cena_1+ilosc_2*cena_2+ilosc_3*cena_3+(ilosc*cena*stawka+ilosc_1*cena_1*stawka_1+ilosc_2*cena_2*stawka_2+ilosc_3*cena_3*stawka_3)/100,2) as num from invoice where id='"+str(id_invoice)+"'")

        for i in query:
            pdf.ln(0.7)
            pdf.cell(1.5,0.3,'Słownie:', border=0, align="L")
            pdf.cell(6.3,0.3,num2words(i[0]), border=0, align="L")
            
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Sposób zapłaty:', border=0, align="L")
        pdf.cell(6.3,0.3,wybor, border=0, align="L")
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Nazwa banku:', border=0, align="L")
        pdf.cell(6.3,0.3,'Santander Bank Polska S.A.', border=0, align="L")
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Numer konta:', border=0, align="L")
        pdf.cell(6.3,0.3,'70 1410 2006 0000 3200 0926 4671', border=0, align="L")
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Termin zapłaty:', border=0, align="L")
        pdf.cell(6.3,0.3,data, border=0, align="L")
        pdf.ln(0.5)

        pdf.cell(3.9,0.3, "Osoba upoważniona do odbioru", border=0, align="C")
        pdf.cell(3.9,0.3, "Osoba upoważniona do wystawienia faktury", border=0, align="C")
        pdf.ln(0.7)
        pdf.cell(3.9,0.3, "..................................................................", border=0, align="C")
        pdf.cell(3.9,0.3, "..................................................................", border=0, align="C")
        pdf.ln(0.9)
        pdf.cell(7.8,0.3, "Pieczęć", border=0, align="C")

        messagebox.showinfo("Sukces", "Plik PDF został utworzony pomyślnie - faktura(orginał).")
        
        query = c.execute("SELECT * FROM invoice WHERE id='"+str(id_invoice)+"'")
        for i in query:
            nabywca = i[7]
            pdf.output('pdf/'+i[7]+' - orginał.pdf','F')


    def kopia(self, id_invoice):
        con = sqlite3.connect('db/database.db')
        c = con.cursor()
        query = c.execute("SELECT * FROM invoice WHERE id='"+str(id_invoice)+"'")

        for i in query:
            numer_faktury = i[1]
            data_sprzedazy = i[2]
            data_wystawienia = i[3]
            miejsce_wystawienia = i[4]
            sposob_zaplaty = i[5]
            termin_zaplaty = i[6]
            nabywca = i[7]
            ulica = i[8]
            kod_miasto = i[9]
            vat = i[10]

        result = c.execute("SELECT * FROM profile WHERE id=1")

        for row in result:
            uzytkownik = row[1]
            ulica_u = row[2]
            kod = row[3] + " " + row[4]
            nip = row[5]

        pdf=FPDF(format='letter', unit='in')
     
        pdf.add_page()

        pdf.add_font('font', '', 'font/Calibri.ttf', uni=True)
        pdf.add_font('font_bold', '', 'font/Calibri_bold.ttf', uni=True) 
        pdf.set_font('font_bold','',16) 
        pdf.cell(7.8,0.5,'Faktura VAT', border=0, align="C")
        pdf.ln(0.5)

        pdf.set_font('font','',12) 
        pdf.cell(7.8,0.5,'kopia', border=0, align="R")
        pdf.ln(0.5)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'Numer faktury:', border=0, align="L")
        pdf.set_font('font_bold','',14) 
        pdf.cell(6.2,0.3,numer_faktury+"/2021", border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'Data wystawienia:', border=0, align="L")
        pdf.cell(6.2,0.3,data_wystawienia, border=0, align="L")
        pdf.ln(0.3)

        pdf.cell(1.6,0.3,'Data sprzedaży:', border=0, align="L")
        pdf.cell(6.2,0.3,data_sprzedazy, border=0, align="L")
        pdf.ln(0.3)

        pdf.cell(1.6,0.3,'Miejsce wystawienia:', border=0, align="L")
        pdf.cell(6.2,0.3,miejsce_wystawienia, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'Sprzedawca:', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(2.3,0.3,uzytkownik, border=0, align="L")
        pdf.set_font('font','',12) 
        pdf.cell(0.8,0.3,'Nabywca: ', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(1.6,0.3,nabywca, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(2.3,0.3,ulica_u, border=0, align="L")
        pdf.set_font('','',12) 
        pdf.cell(0.8,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(1.6,0.3,ulica, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(2.3,0.3,kod, border=0, align="L")
        pdf.set_font('font','',12) 
        pdf.cell(0.8,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(1.6,0.3,kod_miasto, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12)
        pdf.cell(2.3,0.3,'NIP: '+nip, border=0, align="L")
        pdf.set_font('font','',12) 
        pdf.cell(0.8,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12)

        if len(vat) == 10:
            pdf.cell(2.3,0.3,'NIP: '+vat, border=0, align="L") 
        elif len(vat) == 11:
            pdf.cell(2.3,0.3,'PESEL: '+vat, border=0, align="L")
        elif len(vat) == 14:
            pdf.cell(2.3,0.3,'REGON: '+vat, border=0, align="L")
        elif len(vat) == 9:
            pdf.cell(2.3,0.3,'Numer firmy: '+vat, border=0, align="L")
        elif len(vat) == 13:
            pdf.cell(2.3,0.3,'VAT EU: '+vat, border=0, align="L")
        else:
            pdf.cell(1.6,0.3,'Osoba fizyczna', border=0, align="L")


        pdf.ln(0.6)

        c.execute("SELECT nazwa, ilosc, printf('%.2f',cena) AS cena, printf('%.2f',stawka) AS stawka, printf('%.2f',ilosc*cena) AS netto, printf('%.2f',(ilosc*cena*stawka)/100) AS vat, printf('%.2f',(ilosc*cena)+((ilosc*cena*stawka)/100)) AS brutto, nazwa_1, ilosc_1, printf('%.2f',cena_1) AS cena_1, printf('%.2f',stawka_1) AS stawka_1, printf('%.2f',ilosc_1*cena_1) AS netto_1, printf('%.2f',(ilosc_1*cena_1*stawka_1)/100) AS vat_1, printf('%.2f',(ilosc_1*cena_1)+((ilosc_1*cena_1*stawka_1)/100)) AS brutto_1, nazwa_2, ilosc_2, printf('%.2f',cena_2) AS cena_2, printf('%.2f',stawka_2) AS stawka_2, printf('%.2f',ilosc_2*cena_2) AS netto_2, printf('%.2f',(ilosc_2*cena_2*stawka_2)/100) AS vat_2, printf('%.2f',(ilosc_2*cena_2)+((ilosc_2*cena_2*stawka_2)/100)) AS brutto_2, nazwa_3, ilosc_3, printf('%.2f',cena_3) AS cena_3, printf('%.2f',stawka_3) AS stawka_3, printf('%.2f',ilosc_3*cena_3) AS netto_3, printf('%.2f',(ilosc_3*cena_3*stawka_3)/100) AS vat_3, printf('%.2f',(ilosc_3*cena_3)+((ilosc_3*cena_3*stawka_3)/100)) AS brutto_3 FROM invoice WHERE id='"+str(id_invoice)+"'")

        #"{:.2f}".format(a)
        
        for i in query:
            nazwa = i[0]
            ilosc = i[1]
            cena = float(i[2])
            stawka = "{:.2f}".format(float(i[3]))
            netto = "{:.2f}".format(float(i[4]))
            vat = "{:.2f}".format(float(i[5]))
            brutto = "{:.2f}".format(float(i[6]))
            nazwa1 = i[7]
            ilosc1 = i[8]
            cena1 = "{:.2f}".format(float(i[9]))
            stawka1 = "{:.2f}".format(float(i[10]))
            nazwa2 = i[14]
            ilosc2 = i[15]
            cena2 = "{:.2f}".format(float(i[16]))
            stawka2 = "{:.2f}".format(float(i[17]))
            nazwa3 = i[21]
            ilosc3 = i[22]
            cena3 = "{:.2f}".format(float(i[23]))
            stawka3 = "{:.2f}".format(float(i[24]))
            
            pdf.set_font('font_bold', '', 12)
            pdf.cell(0.3,0.3,'LP', border=1, align="C")
            pdf.cell(1.8,0.3,'Nazwa', border=1, align="C")
            pdf.cell(0.5,0.3,'Ilość', border=1, align="C")
            pdf.cell(1.0,0.3,'Cena netto', border=1, align="C")
            pdf.cell(1.0,0.3,'Kwota netto', border=1, align="C")
            pdf.cell(1.0,0.3,'Stawka VAT', border=1, align="C")
            pdf.cell(1.0,0.3,'Kwota VAT', border=1, align="C")
            pdf.cell(1.2,0.3,'Wartość brutto', border=1, align="C")

            pdf.set_font('font','',12.0) 
            pdf.ln(0.3)
            pdf.cell(0.3,0.3,'1', border=1, align="C")
            pdf.cell(1.8,0.3,nazwa, border=1, align="C")
            pdf.cell(0.5,0.3,str(ilosc), border=1, align="C")
            pdf.cell(1.0,0.3,str(cena), border=1, align="C")
            pdf.cell(1.0,0.3,str(netto), border=1, align="C")
            pdf.cell(1.0,0.3,str(stawka), border=1, align="C")
            pdf.cell(1.0,0.3,str(vat), border=1, align="C")
            pdf.cell(1.2,0.3,str(brutto), border=1, align="C")
            
            if nazwa1 != "":
                pdf.ln(0.3)
                pdf.cell(0.3,0.3,'2', border=1, align="C")
                pdf.cell(1.8,0.3,nazwa1, border=1, align="C")
                pdf.cell(0.5,0.3,str(ilosc1), border=1, align="C")
                pdf.cell(1.0,0.3,str(cena1), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[11]))), border=1, align="C")
                pdf.cell(1.0,0.3,str(stawka1), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[12]))), border=1, align="C")
                pdf.cell(1.2,0.3,str("{:.2f}".format(float(i[13]))), border=1, align="C")
    
            if nazwa2 != "":
                         
                pdf.ln(0.3)
                pdf.cell(0.3,0.3,'3', border=1, align="C")
                pdf.cell(1.8,0.3,nazwa2, border=1, align="C")
                pdf.cell(0.5,0.3,str(ilosc2), border=1, align="C")
                pdf.cell(1.0,0.3,str(cena2), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[18]))), border=1, align="C")
                pdf.cell(1.0,0.3,str(stawka2), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[19]))), border=1, align="C")
                pdf.cell(1.2,0.3,str("{:.2f}".format(float(i[20]))), border=1, align="C")

            if nazwa3 != "":
                pdf.ln(0.3)
                pdf.cell(0.3,0.3,'4', border=1, align="C")
                pdf.cell(1.8,0.3,nazwa3, border=1, align="C")
                pdf.cell(0.5,0.3,str(ilosc3), border=1, align="C")
                pdf.cell(1.0,0.3,str(cena3), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[25]))), border=1, align="C")
                pdf.cell(1.0,0.3,str(stawka3), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[26]))), border=1, align="C")
                x = str("{:.2f}".format(float(i[27])))
                pdf.cell(1.2,0.3,x, border=1, align="C")

        query = c.execute("select printf('%.2f',ilosc*cena+ilosc_1*cena_1+ilosc_2*cena_2+ilosc_3*cena_3) as kwota_netto, printf('%.2f',stawka), printf('%.2f',(ilosc*cena*stawka+ilosc_1*cena_1*stawka_1+ilosc_2*cena_2*stawka_2+ilosc_3*cena_3*stawka_3)/100) as kwota_vat, printf('%.2f',ilosc*cena+ilosc_1*cena_1+ilosc_2*cena_2+ilosc_3*cena_3+(ilosc*cena*stawka+ilosc_1*cena_1*stawka_1+ilosc_2*cena_2*stawka_2+ilosc_3*cena_3*stawka_3)/100) as brutto, payment_date, choice from invoice where id='"+str(id_invoice)+"'")

        for i in query:
            netto = i[0]
            stawka = i[1]
            kwota = i[2]
            brutto = i[3]
            data = i[4]
            wybor = i[5]

            pdf.ln(0.3)
            pdf.cell(0.3,0.3,'', border=0, align="C")
            pdf.cell(1.8,0.3,'', border=0, align="C")
            pdf.cell(0.5,0.3,'', border=0, align="C")
            pdf.cell(1.0,0.3,'w tym:', border=1, align="C")
            pdf.cell(1.0,0.3,str(netto), border=1, align="C")
            pdf.cell(1.0,0.3,str(stawka), border=1, align="C")
            pdf.cell(1.0,0.3,str(kwota), border=1, align="C")
            pdf.cell(1.2,0.3,str(brutto), border=1, align="C")

            pdf.ln(0.3)
            pdf.cell(0.3,0.3,'', border=0, align="C")
            pdf.cell(1.8,0.3,'', border=0, align="C")
            pdf.cell(0.5,0.3,'', border=0, align="C")
            pdf.cell(1.0,0.3,'razem:', border=1, align="C")
            pdf.cell(1.0,0.3,str(netto), border=1, align="C")
            pdf.cell(1.0,0.3,str(stawka), border=1, align="C")
            pdf.cell(1.0,0.3,str(kwota), border=1, align="C")
            pdf.cell(1.2,0.3,str(brutto), border=1, align="C")


        LICZBY = [
                None,
                u'jeden', u'dwa', u'trzy', u'cztery', u'pięć', u'sześć', u'siedem',
                u'osiem', u'dziewięć', u'dziesięć', u'jedenaście', u'dwanaście',
                u'trzynaście', u'czternaście', u'pietnaście', u'szesnaście',
                u'siedemnaście', u'osiemnaście', u'dziewiętnaście',
        ]

        DZIESIATKI = [
                None,
                u'dziesięć', u'dwadzieścia', u'trzydzieści', u'czterdzieści',
                u'pięćdziesiąt', u'sześćdziesiąt', u'siedemdziesiąt', u'osiemdziesiąt',
                u'dziewięćdziesiąt',
        ]

        SETKI = [
                None,
                u'sto', u'dwieście', u'trzysta', u'czterysta', u'pięćset', u'sześćset',
                u'siedemset', u'osiemset', u'dziewięćset',
        ]

        TYSIACE = [
                None,
                (u'tysiąc', u'tysiące', u'tysięcy'),
                (u'milion', u'miliony', u'milionów'),
                (u'miliard', u'miliardy', u'miliardów'),
                (u'bilion', u'biliony', u'bilionów'),
                (u'biliard', u'biliardy', u'biliardów'),
        ]


        def num2words(x, unit=None):
            wynik = []
            if not x:
                return u'zero 0/100'
            y = x % 1
            numer = int(x)
            iteration = 0
            while numer:
                sub_tysiace = numer % 1000
                tysiace = numer // 1000
                if sub_tysiace:
                    reszta = []
                    przedrostek = TYSIACE[iteration]
                    sub_setki = sub_tysiace % 100
                    setki = sub_tysiace // 100
                    sub_dziesiatki = sub_setki % 10
                    dziesiatki = sub_setki // 10
                    if SETKI[setki]:
                        reszta.append(SETKI[setki])
                    if sub_tysiace == 1:
                        if iteration == 0:
                            if LICZBY[sub_tysiace]:
                                reszta.append(LICZBY[sub_tysiace])
                        if przedrostek:
                            reszta.append(przedrostek[0])
                    elif sub_setki < 20:
                        if LICZBY[sub_setki]:
                            reszta.append(LICZBY[sub_setki])
                        if przedrostek:
                            if sub_setki > 1 and sub_setki < 5:
                                reszta.append(przedrostek[1])
                            else:
                                reszta.append(przedrostek[2])
                    else:
                        if DZIESIATKI[dziesiatki]:
                            reszta.append(DZIESIATKI[dziesiatki])
                        if LICZBY[sub_dziesiatki]:
                            reszta.append(LICZBY[sub_dziesiatki])
                        if przedrostek:
                            if sub_dziesiatki > 0 and sub_dziesiatki < 5:
                                if dziesiatki and sub_dziesiatki == 1:
                                    reszta.append(przedrostek[2])
                                else:
                                    reszta.append(przedrostek[1])
                            else:
                                reszta.append(przedrostek[2])
                    wynik = reszta + wynik
                    del reszta
                numer = tysiace
                iteration += 1
            if unit:
                wynik.append(unit)
            wynik.append(u'%d/100 PLN' % int(y * 100))
            wynik = ' '.join(wynik)
            return wynik

        query = c.execute("select round(ilosc*cena+ilosc_1*cena_1+ilosc_2*cena_2+ilosc_3*cena_3+(ilosc*cena*stawka+ilosc_1*cena_1*stawka_1+ilosc_2*cena_2*stawka_2+ilosc_3*cena_3*stawka_3)/100,2) as num from invoice where id='"+str(id_invoice)+"'")

        for i in query:
            pdf.ln(0.7)
            pdf.cell(1.5,0.3,'Słownie:', border=0, align="L")
            pdf.cell(6.3,0.3,num2words(i[0]), border=0, align="L")
            
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Sposób zapłaty:', border=0, align="L")
        pdf.cell(6.3,0.3,wybor, border=0, align="L")
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Nazwa banku:', border=0, align="L")
        pdf.cell(6.3,0.3,'Santander Bank Polska S.A.', border=0, align="L")
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Numer konta:', border=0, align="L")
        pdf.cell(6.3,0.3,'70 1410 2006 0000 3200 0926 4671', border=0, align="L")
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Termin zapłaty:', border=0, align="L")
        pdf.cell(6.3,0.3,data, border=0, align="L")
        pdf.ln(0.5)

        pdf.cell(3.9,0.3, "Osoba upoważniona do odbioru", border=0, align="C")
        pdf.cell(3.9,0.3, "Osoba upoważniona do wystawienia faktury", border=0, align="C")
        pdf.ln(0.7)
        pdf.cell(3.9,0.3, "..................................................................", border=0, align="C")
        pdf.cell(3.9,0.3, "..................................................................", border=0, align="C")
        pdf.ln(0.9)
        pdf.cell(7.8,0.3, "Pieczęć", border=0, align="C")

        messagebox.showinfo("Sukces", "Plik PDF został utworzony pomyślnie - faktura(kopia).")
        
        query = c.execute("SELECT * FROM invoice WHERE id='"+str(id_invoice)+"'")
        for i in query:
            nabywca = i[7]
            pdf.output('pdf/'+i[7]+' - kopia.pdf','F')



    def duplikat(self, id_invoice):
        con = sqlite3.connect('db/database.db')
        c = con.cursor()
        query = c.execute("SELECT * FROM invoice WHERE id='"+str(id_invoice)+"'")

        for i in query:
            numer_faktury = i[1]
            data_sprzedazy = i[2]
            data_wystawienia = i[3]
            miejsce_wystawienia = i[4]
            sposob_zaplaty = i[5]
            termin_zaplaty = i[6]
            nabywca = i[7]
            ulica = i[8]
            kod_miasto = i[9]
            vat = i[10]

        result = c.execute("SELECT * FROM profile WHERE id=1")

        for row in result:
            uzytkownik = row[1]
            ulica_u = row[2]
            kod = row[3] + " " + row[4]
            nip = row[5]

        pdf=FPDF(format='letter', unit='in')
     
        pdf.add_page()

        pdf.add_font('font', '', 'font/Calibri.ttf', uni=True)
        pdf.add_font('font_bold', '', 'font/Calibri_bold.ttf', uni=True) 
        pdf.set_font('font_bold','',16) 
        pdf.cell(7.8,0.5,'Faktura VAT', border=0, align="C")
        pdf.ln(0.5)

        pdf.set_font('font','',12) 
        pdf.cell(7.8,0.5,'duplikat', border=0, align="R")
        pdf.ln(0.5)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'Numer faktury:', border=0, align="L")
        pdf.set_font('font_bold','',14) 
        pdf.cell(6.2,0.3,numer_faktury+"/2021", border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'Data wystawienia:', border=0, align="L")
        pdf.cell(6.2,0.3,data_wystawienia, border=0, align="L")
        pdf.ln(0.3)

        pdf.cell(1.6,0.3,'Data sprzedaży:', border=0, align="L")
        pdf.cell(6.2,0.3,data_sprzedazy, border=0, align="L")
        pdf.ln(0.3)

        pdf.cell(1.6,0.3,'Miejsce wystawienia:', border=0, align="L")
        pdf.cell(6.2,0.3,miejsce_wystawienia, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'Sprzedawca:', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(2.3,0.3,uzytkownik, border=0, align="L")
        pdf.set_font('font','',12) 
        pdf.cell(0.8,0.3,'Nabywca: ', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(1.6,0.3,nabywca, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(2.3,0.3,ulica_u, border=0, align="L")
        pdf.set_font('','',12) 
        pdf.cell(0.8,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(1.6,0.3,ulica, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(2.3,0.3,kod, border=0, align="L")
        pdf.set_font('font','',12) 
        pdf.cell(0.8,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12) 
        pdf.cell(1.6,0.3,kod_miasto, border=0, align="L")
        pdf.ln(0.3)

        pdf.set_font('font','',12) 
        pdf.cell(1.6,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12)
        pdf.cell(2.3,0.3,'NIP: '+nip, border=0, align="L")
        pdf.set_font('font','',12) 
        pdf.cell(0.8,0.3,'', border=0, align="L")
        pdf.set_font('font_bold','',12)

        if len(vat) == 10:
            pdf.cell(2.3,0.3,'NIP: '+vat, border=0, align="L") 
        elif len(vat) == 11:
            pdf.cell(2.3,0.3,'PESEL: '+vat, border=0, align="L")
        elif len(vat) == 14:
            pdf.cell(2.3,0.3,'REGON: '+vat, border=0, align="L")
        elif len(vat) == 9:
            pdf.cell(2.3,0.3,'Numer firmy: '+vat, border=0, align="L")
        elif len(vat) == 13:
            pdf.cell(2.3,0.3,'VAT EU: '+vat, border=0, align="L")
        else:
            pdf.cell(1.6,0.3,'Osoba fizyczna', border=0, align="L")


        pdf.ln(0.6)

        c.execute("SELECT nazwa, ilosc, printf('%.2f',cena) AS cena, printf('%.2f',stawka) AS stawka, printf('%.2f',ilosc*cena) AS netto, printf('%.2f',(ilosc*cena*stawka)/100) AS vat, printf('%.2f',(ilosc*cena)+((ilosc*cena*stawka)/100)) AS brutto, nazwa_1, ilosc_1, printf('%.2f',cena_1) AS cena_1, printf('%.2f',stawka_1) AS stawka_1, printf('%.2f',ilosc_1*cena_1) AS netto_1, printf('%.2f',(ilosc_1*cena_1*stawka_1)/100) AS vat_1, printf('%.2f',(ilosc_1*cena_1)+((ilosc_1*cena_1*stawka_1)/100)) AS brutto_1, nazwa_2, ilosc_2, printf('%.2f',cena_2) AS cena_2, printf('%.2f',stawka_2) AS stawka_2, printf('%.2f',ilosc_2*cena_2) AS netto_2, printf('%.2f',(ilosc_2*cena_2*stawka_2)/100) AS vat_2, printf('%.2f',(ilosc_2*cena_2)+((ilosc_2*cena_2*stawka_2)/100)) AS brutto_2, nazwa_3, ilosc_3, printf('%.2f',cena_3) AS cena_3, printf('%.2f',stawka_3) AS stawka_3, printf('%.2f',ilosc_3*cena_3) AS netto_3, printf('%.2f',(ilosc_3*cena_3*stawka_3)/100) AS vat_3, printf('%.2f',(ilosc_3*cena_3)+((ilosc_3*cena_3*stawka_3)/100)) AS brutto_3 FROM invoice WHERE id='"+str(id_invoice)+"'")

        #"{:.2f}".format(a)
        
        for i in query:
            nazwa = i[0]
            ilosc = i[1]
            cena = float(i[2])
            stawka = "{:.2f}".format(float(i[3]))
            netto = "{:.2f}".format(float(i[4]))
            vat = "{:.2f}".format(float(i[5]))
            brutto = "{:.2f}".format(float(i[6]))
            nazwa1 = i[7]
            ilosc1 = i[8]
            cena1 = "{:.2f}".format(float(i[9]))
            stawka1 = "{:.2f}".format(float(i[10]))
            nazwa2 = i[14]
            ilosc2 = i[15]
            cena2 = "{:.2f}".format(float(i[16]))
            stawka2 = "{:.2f}".format(float(i[17]))
            nazwa3 = i[21]
            ilosc3 = i[22]
            cena3 = "{:.2f}".format(float(i[23]))
            stawka3 = "{:.2f}".format(float(i[24]))
            
            pdf.set_font('font_bold', '', 12)
            pdf.cell(0.3,0.3,'LP', border=1, align="C")
            pdf.cell(1.8,0.3,'Nazwa', border=1, align="C")
            pdf.cell(0.5,0.3,'Ilość', border=1, align="C")
            pdf.cell(1.0,0.3,'Cena netto', border=1, align="C")
            pdf.cell(1.0,0.3,'Kwota netto', border=1, align="C")
            pdf.cell(1.0,0.3,'Stawka VAT', border=1, align="C")
            pdf.cell(1.0,0.3,'Kwota VAT', border=1, align="C")
            pdf.cell(1.2,0.3,'Wartość brutto', border=1, align="C")

            pdf.set_font('font','',12.0) 
            pdf.ln(0.3)
            pdf.cell(0.3,0.3,'1', border=1, align="C")
            pdf.cell(1.8,0.3,nazwa, border=1, align="C")
            pdf.cell(0.5,0.3,str(ilosc), border=1, align="C")
            pdf.cell(1.0,0.3,str(cena), border=1, align="C")
            pdf.cell(1.0,0.3,str(netto), border=1, align="C")
            pdf.cell(1.0,0.3,str(stawka), border=1, align="C")
            pdf.cell(1.0,0.3,str(vat), border=1, align="C")
            pdf.cell(1.2,0.3,str(brutto), border=1, align="C")
            
            if nazwa1 != "":
                pdf.ln(0.3)
                pdf.cell(0.3,0.3,'2', border=1, align="C")
                pdf.cell(1.8,0.3,nazwa1, border=1, align="C")
                pdf.cell(0.5,0.3,str(ilosc1), border=1, align="C")
                pdf.cell(1.0,0.3,str(cena1), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[11]))), border=1, align="C")
                pdf.cell(1.0,0.3,str(stawka1), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[12]))), border=1, align="C")
                pdf.cell(1.2,0.3,str("{:.2f}".format(float(i[13]))), border=1, align="C")
    
            if nazwa2 != "":
                         
                pdf.ln(0.3)
                pdf.cell(0.3,0.3,'3', border=1, align="C")
                pdf.cell(1.8,0.3,nazwa2, border=1, align="C")
                pdf.cell(0.5,0.3,str(ilosc2), border=1, align="C")
                pdf.cell(1.0,0.3,str(cena2), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[18]))), border=1, align="C")
                pdf.cell(1.0,0.3,str(stawka2), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[19]))), border=1, align="C")
                pdf.cell(1.2,0.3,str("{:.2f}".format(float(i[20]))), border=1, align="C")

            if nazwa3 != "":
                pdf.ln(0.3)
                pdf.cell(0.3,0.3,'4', border=1, align="C")
                pdf.cell(1.8,0.3,nazwa3, border=1, align="C")
                pdf.cell(0.5,0.3,str(ilosc3), border=1, align="C")
                pdf.cell(1.0,0.3,str(cena3), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[25]))), border=1, align="C")
                pdf.cell(1.0,0.3,str(stawka3), border=1, align="C")
                pdf.cell(1.0,0.3,str("{:.2f}".format(float(i[26]))), border=1, align="C")
                x = str("{:.2f}".format(float(i[27])))
                pdf.cell(1.2,0.3,x, border=1, align="C")

        query = c.execute("select printf('%.2f',ilosc*cena+ilosc_1*cena_1+ilosc_2*cena_2+ilosc_3*cena_3) as kwota_netto, printf('%.2f',stawka), printf('%.2f',(ilosc*cena*stawka+ilosc_1*cena_1*stawka_1+ilosc_2*cena_2*stawka_2+ilosc_3*cena_3*stawka_3)/100) as kwota_vat, printf('%.2f',ilosc*cena+ilosc_1*cena_1+ilosc_2*cena_2+ilosc_3*cena_3+(ilosc*cena*stawka+ilosc_1*cena_1*stawka_1+ilosc_2*cena_2*stawka_2+ilosc_3*cena_3*stawka_3)/100) as brutto, payment_date, choice from invoice where id='"+str(id_invoice)+"'")

        for i in query:
            netto = i[0]
            stawka = i[1]
            kwota = i[2]
            brutto = i[3]
            data = i[4]
            wybor = i[5]

            pdf.ln(0.3)
            pdf.cell(0.3,0.3,'', border=0, align="C")
            pdf.cell(1.8,0.3,'', border=0, align="C")
            pdf.cell(0.5,0.3,'', border=0, align="C")
            pdf.cell(1.0,0.3,'w tym:', border=1, align="C")
            pdf.cell(1.0,0.3,str(netto), border=1, align="C")
            pdf.cell(1.0,0.3,str(stawka), border=1, align="C")
            pdf.cell(1.0,0.3,str(kwota), border=1, align="C")
            pdf.cell(1.2,0.3,str(brutto), border=1, align="C")

            pdf.ln(0.3)
            pdf.cell(0.3,0.3,'', border=0, align="C")
            pdf.cell(1.8,0.3,'', border=0, align="C")
            pdf.cell(0.5,0.3,'', border=0, align="C")
            pdf.cell(1.0,0.3,'razem:', border=1, align="C")
            pdf.cell(1.0,0.3,str(netto), border=1, align="C")
            pdf.cell(1.0,0.3,str(stawka), border=1, align="C")
            pdf.cell(1.0,0.3,str(kwota), border=1, align="C")
            pdf.cell(1.2,0.3,str(brutto), border=1, align="C")


        LICZBY = [
                None,
                u'jeden', u'dwa', u'trzy', u'cztery', u'pięć', u'sześć', u'siedem',
                u'osiem', u'dziewięć', u'dziesięć', u'jedenaście', u'dwanaście',
                u'trzynaście', u'czternaście', u'pietnaście', u'szesnaście',
                u'siedemnaście', u'osiemnaście', u'dziewiętnaście',
        ]

        DZIESIATKI = [
                None,
                u'dziesięć', u'dwadzieścia', u'trzydzieści', u'czterdzieści',
                u'pięćdziesiąt', u'sześćdziesiąt', u'siedemdziesiąt', u'osiemdziesiąt',
                u'dziewięćdziesiąt',
        ]

        SETKI = [
                None,
                u'sto', u'dwieście', u'trzysta', u'czterysta', u'pięćset', u'sześćset',
                u'siedemset', u'osiemset', u'dziewięćset',
        ]

        TYSIACE = [
                None,
                (u'tysiąc', u'tysiące', u'tysięcy'),
                (u'milion', u'miliony', u'milionów'),
                (u'miliard', u'miliardy', u'miliardów'),
                (u'bilion', u'biliony', u'bilionów'),
                (u'biliard', u'biliardy', u'biliardów'),
        ]


        def num2words(x, unit=None):
            wynik = []
            if not x:
                return u'zero 0/100'
            y = x % 1
            numer = int(x)
            iteration = 0
            while numer:
                sub_tysiace = numer % 1000
                tysiace = numer // 1000
                if sub_tysiace:
                    reszta = []
                    przedrostek = TYSIACE[iteration]
                    sub_setki = sub_tysiace % 100
                    setki = sub_tysiace // 100
                    sub_dziesiatki = sub_setki % 10
                    dziesiatki = sub_setki // 10
                    if SETKI[setki]:
                        reszta.append(SETKI[setki])
                    if sub_tysiace == 1:
                        if iteration == 0:
                            if LICZBY[sub_tysiace]:
                                reszta.append(LICZBY[sub_tysiace])
                        if przedrostek:
                            reszta.append(przedrostek[0])
                    elif sub_setki < 20:
                        if LICZBY[sub_setki]:
                            reszta.append(LICZBY[sub_setki])
                        if przedrostek:
                            if sub_setki > 1 and sub_setki < 5:
                                reszta.append(przedrostek[1])
                            else:
                                reszta.append(przedrostek[2])
                    else:
                        if DZIESIATKI[dziesiatki]:
                            reszta.append(DZIESIATKI[dziesiatki])
                        if LICZBY[sub_dziesiatki]:
                            reszta.append(LICZBY[sub_dziesiatki])
                        if przedrostek:
                            if sub_dziesiatki > 0 and sub_dziesiatki < 5:
                                if dziesiatki and sub_dziesiatki == 1:
                                    reszta.append(przedrostek[2])
                                else:
                                    reszta.append(przedrostek[1])
                            else:
                                reszta.append(przedrostek[2])
                    wynik = reszta + wynik
                    del reszta
                numer = tysiace
                iteration += 1
            if unit:
                wynik.append(unit)
            wynik.append(u'%d/100 PLN' % int(y * 100))
            wynik = ' '.join(wynik)
            return wynik
        

        query = c.execute("select round(ilosc*cena+ilosc_1*cena_1+ilosc_2*cena_2+ilosc_3*cena_3+(ilosc*cena*stawka+ilosc_1*cena_1*stawka_1+ilosc_2*cena_2*stawka_2+ilosc_3*cena_3*stawka_3)/100,2) as num from invoice where id='"+str(id_invoice)+"'")

        for i in query:
            pdf.ln(0.7)
            pdf.cell(1.5,0.3,'Słownie:', border=0, align="L")
            pdf.cell(6.3,0.3,num2words(i[0]), border=0, align="L")
            
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Sposób zapłaty:', border=0, align="L")
        pdf.cell(6.3,0.3,wybor, border=0, align="L")
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Nazwa banku:', border=0, align="L")
        pdf.cell(6.3,0.3,'Santander Bank Polska S.A.', border=0, align="L")
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Numer konta:', border=0, align="L")
        pdf.cell(6.3,0.3,'70 1410 2006 0000 3200 0926 4671', border=0, align="L")
        pdf.ln(0.3)
        pdf.cell(1.5,0.3,'Termin zapłaty:', border=0, align="L")
        pdf.cell(6.3,0.3,data, border=0, align="L")
        pdf.ln(0.5)

        pdf.cell(3.9,0.3, "Osoba upoważniona do odbioru", border=0, align="C")
        pdf.cell(3.9,0.3, "Osoba upoważniona do wystawienia faktury", border=0, align="C")
        pdf.ln(0.7)
        pdf.cell(3.9,0.3, "..................................................................", border=0, align="C")
        pdf.cell(3.9,0.3, "..................................................................", border=0, align="C")
        pdf.ln(0.9)
        pdf.cell(7.8,0.3, "Pieczęć", border=0, align="C")

        messagebox.showinfo("Sukces", "Plik PDF został utworzony pomyślnie - faktura(duplikat).")
        
        query = c.execute("SELECT * FROM invoice WHERE id='"+str(id_invoice)+"'")
        for i in query:
            nabywca = i[7]
            pdf.output('pdf/'+i[7]+' - duplikat.pdf','F')

            
        
    def update(self, id_invoice, master):
        window = tk.Toplevel()
        window.resizable(0,0)
        
        ttk.Label(window, text="Formularz edytowania faktury o numerze ID = "+str(id_invoice), font=("Calibri", 14, "bold")).pack(pady=20)

        def combo_data():

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute('SELECT nabywca FROM clients ORDER BY nabywca')

            data = []
            for row in c.fetchall():
                data.append(row[0])
            return data
        

        def combo_product():

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute('SELECT name FROM products ORDER BY name')

            data = []
            for row in c.fetchall():
                data.append(row[0])
            return data


        def details(event):

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute("SELECT ulica, miasto_kod, osoba_fizyczna, nip, regon, vat_eu, pesel FROM clients WHERE nabywca='"+event.widget.get()+"' or c_id='"+str(id_invoice)+"'")

            for row in query:
                ulica_entry.config(state = tk.NORMAL)
                ulica_entry.delete(0, tk.END)
                ulica_entry.insert(0, row[0])
                ulica_entry.config(state = "readonly")

                kod_miasto_entry.config(state = tk.NORMAL)
                kod_miasto_entry.delete(0, tk.END)
                kod_miasto_entry.insert(0, row[1])
                kod_miasto_entry.config(state = "readonly")

                if len(row[2]) == 1:
                    osoba_entry.config(state = tk.NORMAL)
                    osoba_entry.delete(0, tk.END)
                    osoba_entry.insert(0, row[2])
                    osoba_entry.config(state = "readonly")
                    osoba_label = ttk.Label(window_frame,text="Osoba fizyczna:", font=("Calibri", 12))
                    osoba_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
                elif len(row[3]) == 10:
                    osoba_entry.config(state = tk.NORMAL)
                    osoba_entry.delete(0, tk.END)
                    osoba_entry.insert(0, row[3])
                    osoba_entry.config(state = "readonly")
                    osoba_label = ttk.Label(window_frame,text="NIP:                   ", font=("Calibri", 12))
                    osoba_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
                elif len(row[4]) == 14:
                    osoba_entry.config(state = tk.NORMAL)
                    osoba_entry.delete(0, tk.END)
                    osoba_entry.insert(0, row[4])
                    osoba_entry.config(state = "readonly")
                    osoba_label = ttk.Label(window_frame,text="REGON:                 ", font=("Calibri", 12))
                    osoba_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
                elif len(row[5]) == 13:
                    osoba_entry.config(state = tk.NORMAL)
                    osoba_entry.delete(0, tk.END)
                    osoba_entry.insert(0, row[5])
                    osoba_entry.config(state = "readonly")
                    osoba_label = ttk.Label(window_frame,text="VAT EU:                 ", font=("Calibri", 12))
                    osoba_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
                elif len(row[6]) == 11:
                    osoba_entry.config(state = tk.NORMAL)
                    osoba_entry.delete(0, tk.END)
                    osoba_entry.insert(0, row[6])
                    osoba_entry.config(state = "readonly")
                    osoba_label = ttk.Label(window_frame,text="PESEL:                 ", font=("Calibri", 12))
                    osoba_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
                    
            c.close()
            con.close()


        def detail_first(event):

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute("SELECT price FROM products WHERE name='"+event.widget.get()+"'")

            for row in query:
                cena_e.config(state = tk.NORMAL)
                cena_e.delete(0, tk.END)
                cena_e.insert(0, row[0])
                cena_e.config(state = "readonly")

            c.close()
            con.close()


        def detail_second(event):

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute("SELECT price FROM products WHERE name='"+event.widget.get()+"'")

            for row in query:
                cena_ee.config(state = tk.NORMAL)
                cena_ee.delete(0, tk.END)
                cena_ee.insert(0, row[0])
                cena_ee.config(state = "readonly")

            c.close()
            con.close()

            
        def detail_third(event):

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute("SELECT price FROM products WHERE name='"+event.widget.get()+"'")

            for row in query:
                cena_eee.config(state = tk.NORMAL)
                cena_eee.delete(0, tk.END)
                cena_eee.insert(0, row[0])
                cena_eee.config(state = "readonly")

            c.close()
            con.close()

            
        def detail_fourth(event):

            con = sqlite3.connect('db/database.db')
            c = con.cursor()
            query = c.execute("SELECT price FROM products WHERE name='"+event.widget.get()+"'")

            for row in query:
                cena_eeee.config(state = tk.NORMAL)
                cena_eeee.delete(0, tk.END)
                cena_eeee.insert(0, row[0])
                cena_eeee.config(state = "readonly")

            c.close()
            con.close()
            

        style = ttk.Style(window)
        style.configure("my.TButton", font=("Calibri", 19, "bold"))

        szczegoly = ttk.Style(window)
        szczegoly.configure("sz.TButton", font=("Calibri", 18))
            
        frame = ttk.LabelFrame(window, text="Dane do faktury")
        frame.pack(padx=10, pady=0, fill="x")

        window.numer = tk.StringVar(window)      
        window.miejsce = tk.StringVar(window)       
        window.sprzedaz = tk.StringVar(window)
        window.wystawienia = tk.StringVar(window)
        window.sposob = tk.StringVar(window)
        window.termin = tk.StringVar(window)

        db=sqlite3.connect('db/database.db')
        c=db.cursor()
        query=c.execute("SELECT number, issue_date, sale_date, place, choice, payment_date FROM invoice WHERE id='"+str(id_invoice)+"';")

        for i in query:
            numer_label = ttk.Label(frame, text="Numer faktury:", font=("Calibri", 12))
            numer_label.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W)
            numer_entry = ttk.Entry(frame, width=27, textvariable=window.numer, font=("Calibri", 12))
            numer_entry.insert(0, i[0])
            numer_entry.grid(padx=5, pady=5, row=0, column=1, sticky=tk.W)

            wystawiona_label = ttk.Label(frame, text="Data wystawienia:", font=("Calibri", 12))
            wystawiona_label.grid(padx=5, pady=5, row=1, column=0, sticky=tk.W)
            wystawiona_entry = DateEntry(frame, width=25, textvariable=window.wystawienia,  font=("Calibri", 12), locale='en_US', date_pattern='dd-mm-y')
            wystawiona_entry.delete(0, "end")
            wystawiona_entry.insert(0, i[1])
            wystawiona_entry.grid(padx=5, pady=5, row=1, column=1, sticky=tk.W)

            sprzedaz_label = ttk.Label(frame, text="Data sprzedaży:", font=("Calibri", 12))
            sprzedaz_label.grid(padx=5, pady=5, row=0, column=2, sticky=tk.W)
            sprzedaz_entry = DateEntry(frame, width=25, textvariable=window.sprzedaz, font=("Calibri", 12), locale='en_US', date_pattern='dd-mm-y')
            sprzedaz_entry.delete(0, "end")
            sprzedaz_entry.insert(0, i[2])
            sprzedaz_entry.grid(padx=5, pady=5, row=0, column=3, sticky=tk.W)

            miejsce_label = ttk.Label(frame, text="Miejsce wystawienia:", font=("Calibri", 12))
            miejsce_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
            miejsce_entry = ttk.Entry(frame, width=27, textvariable=window.miejsce, font=("Calibri", 12))
            miejsce_entry.insert(0, i[3])
            miejsce_entry.grid(padx=5, pady=5, row=1, column=3, sticky=tk.W)

            sposob_label = ttk.Label(frame, text="Sposób zapłaty:", font=("Calibri", 12))
            sposob_label.grid(padx=5, pady=5, row=2, column=0, sticky=tk.W)
                
            sposob_combobox = ttk.Combobox(frame, textvariable=window.sposob, font=("Calibri", 12), width=25)
            sposob_combobox.grid(padx=5, pady=5, row=2, column=1, sticky=tk.W)
            sposob_combobox['values'] = ('Gotówka', ' Przelew') 
            sposob_combobox.insert(0, i[4]) 

            termin_label = ttk.Label(frame, text="Termin zapłaty:", font=("Calibri", 12))
            termin_label.grid(padx=5, pady=5, row=2, column=2, sticky=tk.W)
            termin_entry = DateEntry(frame, width=25, textvariable=window.termin,  font=("Calibri", 12), locale='en_US', date_pattern='dd-mm-y')
            termin_entry.delete(0, "end")
            termin_entry.insert(0, i[5])
            termin_entry.grid(padx=5, pady=5, row=2, column=3, sticky=tk.W)

        window_frame = ttk.LabelFrame(window, text="Klienci")
        window_frame.pack(padx=10, pady=5, fill="x")

        window.nabywca = tk.StringVar(window)
        window.ulica = tk.StringVar(window)
        window.kod_miasto = tk.StringVar(window) 
        window.osoba = tk.StringVar(window)

        query=c.execute("SELECT nabywca, ulica, kod_miasto, vat FROM invoice WHERE id='"+str(id_invoice)+"';")

        for i in query:
            ulica_label = ttk.Label(window_frame, width=17, text="Ulica:", font=("Calibri", 12))
            ulica_label.grid(padx=5, pady=5, row=0, column=2, sticky=tk.W)
            ulica_entry = ttk.Entry(window_frame, width=27, textvariable=window.ulica, font=("Calibri", 12))
            ulica_entry.insert(0, i[1])
            ulica_entry.grid(padx=5, pady=5, row=0, column=3, sticky=tk.W)

            kod_miasto_label = ttk.Label(window_frame,text="Kod/miasto:", font=("Calibri", 12))
            kod_miasto_label.grid(padx=5, pady=5, row=1, column=0, sticky=tk.W)
            kod_miasto_entry = ttk.Entry(window_frame, width=27, textvariable=window.kod_miasto, font=("Calibri", 12))
            kod_miasto_entry.insert(0, i[2])
            kod_miasto_entry.grid(padx=5, pady=5, row=1, column=1, sticky=tk.W)

            osoba_entry = ttk.Entry(window_frame, width=27, textvariable=window.osoba, font=("Calibri", 12))
            osoba_entry.insert(0, i[3])
            osoba_entry.grid(padx=5, pady=5, row=1, column=3, sticky=tk.W)
                    
            nabywca_name = ttk.Label(window_frame, width=15, text="Nabywca:", font=("Calibri", 12))
            nabywca_name.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W)
            combo_nabywca_name = ttk.Combobox(window_frame, width=25, textvariable=window.nabywca, font=("Calibri", 12))
            combo_nabywca_name.grid(padx=5, pady=5, row=0, column=1, sticky=tk.W)
            combo_nabywca_name['values'] = combo_data()
            combo_nabywca_name.bind("<<ComboboxSelected>>", details)
            combo_nabywca_name.insert(0, i[0])

        style = ttk.Style()
        style.configure("font.TButton", font=("Calibri", 12))

        products = ttk.LabelFrame(window, text="Produkty")
        products.pack(padx=10, pady=5, fill="x")
           
        window.nazwa = tk.StringVar(window)
        window.cena = tk.StringVar(window)
        window.ilosc = tk.StringVar(window)
        window.stawka = tk.StringVar(window)

        query=c.execute("SELECT nazwa, ilosc, cena, stawka FROM invoice WHERE id='"+str(id_invoice)+"';")

        for i in query:                  
            nazwa_l = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
            nazwa_l.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W)
            nazwa_c = ttk.Combobox(products, textvariable=window.nazwa, font=("Calibri", 12), width=20)
            nazwa_c.grid(padx=5, pady=5, row=0, column=1, sticky=tk.W)
            nazwa_c['values'] = combo_product()
            nazwa_c.bind("<<ComboboxSelected>>", detail_first)
            nazwa_c.insert(0, i[0])                                    

            style = ttk.Style()
            style.configure("font.TButton", font=("Calibri", 12))

            ilosc_l = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
            ilosc_l.grid(padx=5, pady=5, row=0, column=2, sticky=tk.W)
            ilosc_e = ttk.Entry(products, textvariable=window.ilosc, font=("Calibri", 12), width=7)
            ilosc_e.grid(padx=5, pady=5, row=0, column=3, sticky=tk.W)
            ilosc_e.insert(0, i[1])

            cena_l = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
            cena_l.grid(padx=5, pady=5, row=0, column=4, sticky=tk.W)
            cena_e = ttk.Entry(products, textvariable=window.cena, font=("Calibri", 12), width=13)
            cena_e.grid(padx=5, pady=5, row=0, column=5, sticky=tk.W)
            cena_e.insert(0, i[2])

            stawka_l = ttk.Label(products,text="Stawka VAT:", font=("Calibri", 12))
            stawka_l.grid(padx=5, pady=5, row=0, column=6, sticky=tk.W)
            stawka_combobox = ttk.Combobox(products, textvariable=window.stawka, font=("Calibri", 12), width=5)
            stawka_combobox.grid(padx=5, pady=5, row=0, column=7, sticky=tk.W)
            stawka_combobox['values'] = ('23', '27', '25', '24', '22', '21', '20', '19', '17', '16', '15', '10', '9.5', '9', '8.5', '8', '7.7', '7', '6.5', '5.5', '5', '4', '3', '0') 
            #stawka_combobox.current(0)
            stawka_combobox.insert(0, i[3])


        window.nazwa_1 = tk.StringVar(window)
        window.cena_1 = tk.StringVar(window)
        window.ilosc_1 = tk.StringVar(window)
        window.stawka_1 = tk.StringVar(window)

        query=c.execute("SELECT nazwa_1, ilosc_1, cena_1, stawka_1 FROM invoice WHERE id='"+str(id_invoice)+"';")

        for i in query:
            nazwa_ll = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
            nazwa_ll.grid(padx=5, pady=5, row=1, column=0, sticky=tk.W)
            nazwa_cc = ttk.Combobox(products, textvariable=window.nazwa_1, font=("Calibri", 12), width=20)
            nazwa_cc.grid(padx=5, pady=5, row=1, column=1, sticky=tk.W)
            nazwa_cc['values'] = combo_product()
            nazwa_cc.bind("<<ComboboxSelected>>", detail_second)
            nazwa_cc.insert(0, i[0])

            ilosc_ll = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
            ilosc_ll.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
            ilosc_ee = ttk.Entry(products, textvariable=window.ilosc_1, font=("Calibri", 12), width=7)
            ilosc_ee.grid(padx=5, pady=5, row=1, column=3, sticky=tk.W)
            ilosc_ee.insert(0, i[1])

            cena_ll = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
            cena_ll.grid(padx=5, pady=5, row=1, column=4, sticky=tk.W)
            cena_ee = ttk.Entry(products, textvariable=window.cena_1, font=("Calibri", 12), width=13)
            cena_ee.grid(padx=5, pady=5, row=1, column=5, sticky=tk.W)
            cena_ee.insert(0, i[2])

            stawka_ll = ttk.Label(products,text="Stawka VAT:", font=("Calibri", 12))
            stawka_ll.grid(padx=5, pady=5, row=1, column=6, sticky=tk.W)
            stawka_aa_combobox = ttk.Combobox(products, textvariable=window.stawka_1, font=("Calibri", 12), width=5)
            stawka_aa_combobox.grid(padx=5, pady=5, row=1, column=7, sticky=tk.W)
            stawka_aa_combobox['values'] = ('23', '27', '25', '24', '22', '21', '20', '19', '17', '16', '15', '10', '9.5', '9', '8.5', '8', '7.7', '7', '6.5', '5.5', '5', '4', '3', '0')  
            stawka_aa_combobox.insert(0, i[3])

        window.nazwa_2 = tk.StringVar(window)
        window.cena_2 = tk.StringVar(window)
        window.ilosc_2 = tk.StringVar(window)
        window.stawka_2 = tk.StringVar(window)

        query=c.execute("SELECT nazwa_2, ilosc_2, cena_2, stawka_2 FROM invoice WHERE id='"+str(id_invoice)+"';")

        for i in query:            
            nazwa_lll = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
            nazwa_lll.grid(padx=5, pady=5, row=2, column=0, sticky=tk.W)
            nazwa_ccc = ttk.Combobox(products, textvariable=window.nazwa_2, font=("Calibri", 12), width=20)
            nazwa_ccc.grid(padx=5, pady=5, row=2, column=1, sticky=tk.W)
            nazwa_ccc['values'] = combo_product()
            nazwa_ccc.bind("<<ComboboxSelected>>", detail_third)
            nazwa_ccc.insert(0, i[0])

            ilosc_lll = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
            ilosc_lll.grid(padx=5, pady=5, row=2, column=2, sticky=tk.W)
            ilosc_eee = ttk.Entry(products, textvariable=window.ilosc_2, font=("Calibri", 12), width=7)
            ilosc_eee.grid(padx=5, pady=5, row=2, column=3, sticky=tk.W)
            ilosc_eee.insert(0, i[1])

            cena_lll = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
            cena_lll.grid(padx=5, pady=5, row=2, column=4, sticky=tk.W)
            cena_eee = ttk.Entry(products, textvariable=window.cena_2, font=("Calibri", 12), width=13)
            cena_eee.grid(padx=5, pady=5, row=2, column=5, sticky=tk.W)
            cena_eee.insert(0, i[2])

            stawka_lll = ttk.Label(products,text="Stawka VAT:", font=("Calibri", 12))
            stawka_lll.grid(padx=5, pady=5, row=2, column=6, sticky=tk.W)
            stawka_aaa_combobox = ttk.Combobox(products, textvariable=window.stawka_2, font=("Calibri", 12), width=5)
            stawka_aaa_combobox.grid(padx=5, pady=5, row=2, column=7, sticky=tk.W)
            stawka_aaa_combobox['values'] = ('23', '27', '25', '24', '22', '21', '20', '19', '17', '16', '15', '10', '9.5', '9', '8.5', '8', '7.7', '7', '6.5', '5.5', '5', '4', '3', '0')
            stawka_aaa_combobox.insert(0, i[3])

        window.nazwa_3 = tk.StringVar(window)
        window.cena_3 = tk.StringVar(window)
        window.ilosc_3 = tk.StringVar(window)
        window.stawka_3 = tk.StringVar(window)

        query=c.execute("SELECT nazwa_3, ilosc_3, cena_3, stawka_3 FROM invoice WHERE id='"+str(id_invoice)+"';")
                    
        for i in query:               
            nazwa_llll = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
            nazwa_llll.grid(padx=5, pady=5, row=3, column=0, sticky=tk.W)
            nazwa_cccc = ttk.Combobox(products, textvariable=window.nazwa_3, font=("Calibri", 12), width=20)
            nazwa_cccc.grid(padx=5, pady=5, row=3, column=1, sticky=tk.W)
            nazwa_cccc['values'] = combo_product()
            nazwa_cccc.bind("<<ComboboxSelected>>", detail_fourth)
            nazwa_cccc.insert(0, i[0])

            ilosc_llll = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
            ilosc_llll.grid(padx=5, pady=5, row=3, column=2, sticky=tk.W)
            ilosc_eeee = ttk.Entry(products, textvariable=window.ilosc_3, font=("Calibri", 12), width=7)
            ilosc_eeee.grid(padx=5, pady=5, row=3, column=3, sticky=tk.W)
            ilosc_eeee.insert(0, i[1])

            cena_llll = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
            cena_llll.grid(padx=5, pady=5, row=3, column=4, sticky=tk.W)
            cena_eeee = ttk.Entry(products, textvariable=window.cena_3, font=("Calibri", 12), width=13)
            cena_eeee.grid(padx=5, pady=5, row=3, column=5, sticky=tk.W)
            cena_eeee.insert(0, i[2])

            stawka_llll = ttk.Label(products,text="Stawka VAT:", font=("Calibri", 12))
            stawka_llll.grid(padx=5, pady=5, row=3, column=6, sticky=tk.W)
            stawka_aaaa_combobox = ttk.Combobox(products, textvariable=window.stawka_3, font=("Calibri", 12), width=5)
            stawka_aaaa_combobox.grid(padx=5, pady=5, row=3, column=7, sticky=tk.W)
            stawka_aaaa_combobox['values'] = ('23', '27', '25', '24', '22', '21', '20', '19', '17', '16', '15', '10', '9.5', '9', '8.5', '8', '7.7', '7', '6.5', '5.5', '5', '4', '3', '0')
            stawka_aaaa_combobox.insert(0, i[3])
        

        def updatedetail(id_invoice, master):
            
            numerr = window.numer.get()
            miejscee = window.miejsce.get()
            sprzedazz = window.sprzedaz.get()
            wystawieniaa = window.wystawienia.get()
            sposobb = window.sposob.get()
            terminn = window.termin.get()

            nabywcaa = window.nabywca.get()
            ulicaa = window.ulica.get()
            kod_miastoo = window.kod_miasto.get()
            osobaa = window.osoba.get()

            nazwaa = window.nazwa.get()
            cenaa = window.cena.get()
            iloscc = window.ilosc.get()
            stawkaa = window.stawka.get()

            nazwaa_11 = window.nazwa_1.get()
            cenaa_11 = window.cena_1.get()
            iloscc_11 = window.ilosc_1.get()
            stawkaa_11 = window.stawka_1.get()
    
            nazwaa_22 = window.nazwa_2.get()
            cenaa_22 = window.cena_2.get()
            iloscc_22 = window.ilosc_2.get()
            stawkaa_22 = window.stawka_2.get()        

            nazwaa_33 = window.nazwa_3.get()
            cenaa_33 = window.cena_3.get()
            iloscc_33 = window.ilosc_3.get()
            stawkaa_33 = window.stawka_3.get()
            
            if numerr=="" or miejscee=="" or sprzedazz=="" or wystawieniaa=="" or sposobb=="" or terminn=="" or nabywcaa=="" or ulicaa=="" or kod_miastoo=="" or osobaa=="" or nazwaa=="" or cenaa=="" or iloscc=="" or stawkaa=="":
                messagebox.showerror('Błąd','Wszystkie pola powinny zostać uzupełnione.')
            else:
                db=sqlite3.connect('db/database.db')
                c=db.cursor()
                c.execute("update invoice set number='"+numerr+"',sale_date='"+sprzedazz+"', issue_date='"+wystawieniaa+"', place='"+miejscee+"', choice='"+sposobb+"', payment_date='"+terminn+"', nabywca='"+nabywcaa+"', ulica='"+ulicaa+"', kod_miasto='"+kod_miastoo+"', vat='"+osobaa+"', nazwa='"+nazwaa+"', ilosc='"+iloscc+"', cena='"+cenaa+"', stawka='"+stawkaa+"', nazwa_1='"+nazwaa_11+"', ilosc_1='"+iloscc_11+"', cena_1='"+cenaa_11+"', stawka_1='"+stawkaa_11+"', nazwa_2='"+nazwaa_22+"', ilosc_2='"+iloscc_22+"', cena_2='"+cenaa_22+"', stawka_2='"+stawkaa_22+"',  nazwa_3='"+nazwaa_33+"', ilosc_3='"+iloscc_33+"', cena_3='"+cenaa_33+"', stawka_3='"+stawkaa_33+"' where id='"+str(id_invoice)+"';")
                db.commit()
                db.close()
                window.withdraw()
                messagebox.showinfo('Sukces','Produkt został zaktualizowany.')
                master.switch_frame(Invoice)

        bu = ttk.Style(window)
        bu.configure("bu.TButton", font=("Calibri", 12, "bold"))

        ttk.Button(window, text="EDYTUJ FAKTURĘ", command=lambda: updatedetail(id_invoice, master), style="bu.TButton").pack(pady=10, padx=20, fill="x", ipady=2)

        
    def delete(self, id_invoice, master):
        text=messagebox.askyesnocancel("Usuń","Czy na pewno chcesz usunąć fakture?",icon='warning',default='no')
        if text:
            with sqlite3.connect("db/database.db") as db:
                c = db.cursor()
                c.execute(f"delete from invoice where id = {id_invoice}")
                c.close()
            master.switch_frame(Invoice)
        


### Widok KONTA UŻYTKOWNIKA ###



class Profile(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        master.title("Faktura VAT - panel użytkownika")

        ttk.Label(self, text="Faktura VAT - panel użytkownika", font=("Calibri", 24, "bold")).pack(pady=30)

        bold = ttk.Style(self)
        bold.configure("bold.TButton", font=("Calibri", 14, "bold"))

        normal = ttk.Style(self)
        normal.configure("normal.TButton", font=("Calibri", 12))

        labelframe = ttk.LabelFrame(self, text="Panel użytkownika")
        labelframe.pack(padx=10, pady=10)

        frame = ttk.LabelFrame(self, text="Dane logowania")
        frame.pack(padx=10, pady=10)

        con = sqlite3.connect('db/database.db')
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

            edit_profile_button = ttk.Button(labelframe, text="Edytuj panel użytkownika",command=lambda: self.update(master), width=80, style="normal.TButton")
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
                with sqlite3.connect("db/database.db") as db:
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
            with sqlite3.connect("db/database.db") as db:
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
                        


    def update(self, master):
        window = tk.Toplevel()
        window.resizable(0,0)
        db=sqlite3.connect('db/database.db')
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
                db=sqlite3.connect('db/database.db')
                c=db.cursor()
                c.execute("update profile set nazwa='"+nazwa.get()+"',ulica='"+ulica.get()+"',kod='"+kod.get()+"',miasto='"+miasto.get()+"',nip='"+nip.get()+"',telefon='"+telefon.get()+"' where id=1")
                db.commit()
                db.close()
                window.withdraw()
                messagebox.showinfo('Sukces','Profil użytkownika został zaktualizowany.')
                master.switch_frame(Profile)
        
        normal = ttk.Style(window)
        normal.configure("normal.TButton", font=("Calibri", 12))
        
        button=ttk.Button(window, text="Zaktualizuj", command=updatedetail, style="normal.TButton", width=28)
        button.grid(row=7, column=0, padx=10, pady=10)



### Widok KLIENTÓW ###



class Client(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        master.title("Faktura VAT - klienci")
        
        sf = ScrolledFrame(self, width=800, height=600)
        sf.pack(side="top", expand=1, fill="both")
        
        sf.bind_arrow_keys(self)
        sf.bind_scroll_wheel(self)

        frame = sf.display_widget(tk.Frame)
                
        normal = ttk.Style(frame)
        normal.configure("normal.TButton", font=("Calibri", 14))

        bold = ttk.Style(frame)
        bold.configure("bo.TButton", font=("Calibri", 14, "bold"))

        ttk.Label(frame, text="Faktura VAT - klienci", font=("Calibri", 24, "bold"), anchor="center").grid(pady=20, padx=253, columnspan=6)


        ttk.Button(frame, text="DODAJ NOWEGO KLIENTA", command=lambda: self.okno_zapisz(master), style="normal.TButton").grid(padx=5, pady=10, columnspan=6, sticky="nswe")

        #ttk.Button(frame, text="ODŚWIEŻ", command=lambda: master.switch_frame(Client), style="normal.TButton").grid(padx=5, columnspan=6, sticky="nswe")

        ttk.Button(frame, text="COFNIJ", style="bo.TButton",
                   command=lambda: master.switch_frame(Menu)).grid(pady=0, padx=5, columnspan=6, sticky="nswe")

        ttk.Label(frame, text="TABELA Z KLIENTAMI", font=("Calibri", 14, "bold"), anchor="center").grid(pady=20, padx=0, columnspan=6)

        self.table(frame, master)
        

    def table(self, w, master):  
        limit = 8
        q = "SELECT c_id, nabywca from clients" 
        h = "select count(*) from clients"
        i=0

        normal = ttk.Style(w)
        normal.configure("normaa.TButton", font=("Calibri", 12))

        
        with sqlite3.connect("db/database.db") as db:  
            c = db.cursor()
            c.execute(q)
            r_set = c.fetchall()
            c.execute(h)
            no_rec = c.fetchone()[0]
            c.close()
        l = ["ID",
             "Nazwa"]

        r_set.insert(0, l)  

        for client in r_set:
            for j in range(len(client)):
                e = ttk.Label(w, text=client[j], font=("Calibri", 12))
                e.grid(row=i+4, column=j, padx=10, pady=3)

            if r_set.index(client) != 0:
                f = ttk.Button(w, text='SZCZEGÓŁY', command=lambda d=client[0]: self.detail(d), style="normaa.TButton")
                f.grid(row=i+4, column=j + 1)
                f = ttk.Button(w, text='EDYTUJ', command=lambda d=client[0]: self.update(d, master), style="normaa.TButton")
                f.grid(row=i+4, column=j + 2)
                f = ttk.Button(w, text='USUŃ', command=lambda d=client[0]: self.usun(d, master), style="normaa.TButton")
                f.grid(row=i+4, column=j + 3, pady=3)
            i = i + 1


    def okno_zapisz(self, master):  # Nowe okno do zapisu
        okno = tk.Toplevel(self)
        okno.resizable(0, 0)  
        okno.nabywca = tk.StringVar(okno)
        okno.ulica = tk.StringVar(okno)
        okno.miasto = tk.StringVar(okno)
        okno.kod = tk.StringVar(okno)
        okno.wybor2 = tk.StringVar(okno)
        okno.id = tk.StringVar(okno)

        ttk.Label(okno, text="Formularz dodawania klienta", font=("Calibri", 12, "bold")).pack(padx=0, pady=10)

        frame_napisy = tk.Frame(okno)  # Ramka z napisami pol
        frame_napisy.pack(side="left", fill="both")
        ttk.Label(frame_napisy, text="Nabywca", font=("Calibri", 12)).pack(pady = 6, padx = 5, anchor="w")
        ttk.Label(frame_napisy, text="Ulica", font=("Calibri", 12)).pack(pady = 6, padx = 5, anchor="w")
        ttk.Label(frame_napisy, text="Miasto", font=("Calibri", 12)).pack(pady = 6, padx = 5, anchor="w")
        ttk.Label(frame_napisy, text="Kod", font=("Calibri", 12)).pack(pady = 6, padx = 5, anchor="w")

        menu = ttk.Style(okno)
        menu.configure("menu.TMenubutton", font=("Calibri", 12))

        choices = ("Osoba fizyczna", "NIP", "REGON", "VAT EU", "PESEL", "Numer firmy")
        okno.variable = tk.StringVar(okno)
        okno.variable.set("Osoba fizyczna")
        ttk.OptionMenu(frame_napisy, okno.variable, *choices, command=self.choice, style="menu.TMenubutton").pack(pady = 6, padx = 0, anchor="w")

        frame_entry = tk.Frame(okno)  # Ramka z polami
        frame_entry.pack(side="left", fill="both")
        ttk.Entry(frame_entry, textvariable=okno.nabywca, font=("Calibri", 12), width=25).pack(pady = 5, padx = 5)
        ttk.Entry(frame_entry, textvariable=okno.ulica, font=("Calibri", 12), width=25).pack(pady = 5, padx = 5)
        ttk.Entry(frame_entry, textvariable=okno.miasto, font=("Calibri", 12), width=25).pack(pady = 5, padx = 5)
        ttk.Entry(frame_entry, textvariable=okno.kod, font=("Calibri", 12), width=25).pack(pady = 5, padx = 5)
        self.pole_do_wpisania_wyboru = ttk.Entry(frame_entry, textvariable=okno.wybor2, font=("Calibri", 12), width=25)

        bu = ttk.Style(okno)
        bu.configure("bu.TButton", font=("Calibri", 12))
        
        ttk.Button(frame_napisy, text="ZAPISZ", command=lambda : self.zapisz(okno, master), width=15, style="bu.TButton").pack(side="bottom", pady = 6, padx = 5)
        
            
    def zapisz(self, okno, master):
        nabywca = okno.nabywca.get() if okno.nabywca.get() != "" else "-"

        if okno.nabywca.get()=="" or okno.ulica.get()=="" or okno.kod.get()=="" or okno.miasto.get()=="":
            messagebox.showerror('Błąd', 'Sprawdź, czy wszystkie pola zostały uzupełnione.')
        else:
            if okno.variable.get() == "Osoba fizyczna":
                wybor = "T"
            else:
                wybor = okno.wybor2.get() if okno.wybor2.get() != "" else "-"

            ulica = okno.ulica.get() if okno.ulica.get() != "" else "-"
            miasto = okno.miasto.get() if okno.miasto.get() != "" else "-"
            kod = okno.kod.get() if okno.kod.get() != "" else "-"
            
            text = messagebox.showinfo('Sukces','Rekord dodano prawidłowo.')
            if text:
                query = (f"insert into clients('nabywca', '{okno.variable.get().replace(' ','_')}', 'ulica', 'miasto','kod')values('{nabywca}', '{wybor}', '{ulica}', '{miasto}', '{kod}')")
                with sqlite3.connect("db/database.db") as db:
                    c = db.cursor()
                    c.execute(query)
                    c.close()
                okno.withdraw()
                master.switch_frame(Client)
                

    def usun(self, id_client, master):
        text=messagebox.askyesnocancel("Usuń","Czy na pewno chcesz usunąć klienta?",icon='warning',default='no')
        if text:
            with sqlite3.connect("db/database.db") as db:
                c = db.cursor()
                c.execute(f"delete from clients where c_id = {id_client}")
                c.close()
            master.switch_frame(Client)

    def update(self, id_client, master):  # Nowe okno do update
        window = tk.Toplevel(self)
        window.resizable(0,0)
        with sqlite3.connect("db/database.db") as db:
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
        normal.configure("nor.TButton", font=("Calibri", 12))

        for i in stare_dane:  # Wstawia dane do pol entry
            for j in range(1, len(i)):
                self.e = ttk.Entry(frame_dane, textvariable=lista_kolumn[j-1], font=("Calibri", 12), width=25)
                self.e.insert(-1, i[j])
                self.e.pack(pady=1, padx=5)

            button = ttk.Button(frame_napisy, text="Aktualizuj", command= lambda : self.query_update(window, id_client, master), style="nor.TButton", width=15)
            button.pack(side="bottom", pady=10, padx=10)


    def query_update(self, window, id_client, master):  # Komenda update
        if self.nowy_nabywca.get()=="" or self.nip.get()=="" or self.regon.get()=="" or self.vat_eu.get()=="" or self.pesel.get()=="" or self.numer_firmy.get()=="" or self.osoba_fizyczna.get()=="" or self.nowa_ulica.get()=="" or self.nowe_miasto.get()=="" or self.nowy_kod.get()=="":
            messagebox.showerror('Błąd', 'Sprawdź, czy wszystkie pola zostały uzupełnione.')
        else:
            query = (f"update clients set nabywca = '{self.nowy_nabywca.get()}', nip = '{self.nip.get()}', regon = '{self.regon.get()}', vat_eu = '{self.vat_eu.get()}', pesel = '{self.pesel.get()}', numer_firmy = '{self.numer_firmy.get()}', osoba_fizyczna = '{self.osoba_fizyczna.get()}', ulica = '{self.nowa_ulica.get()}',  miasto = '{self.nowe_miasto.get()}', kod = '{self.nowy_kod.get()}' where c_id = {id_client};")
            with sqlite3.connect("db/database.db") as db:
                c = db.cursor()
                c.execute(query)
                c.close()
                messagebox.showinfo('Sukces','Klient został zaktualizowany.')
            window.destroy()
            master.switch_frame(Client)
            

    def choice(self, v):  # Dodanie pola po wyborze innym niz osoba fizyczna
        if v == "Osoba fizyczna":
            self.pole_do_wpisania_wyboru.pack_forget()
        else:
            self.pole_do_wpisania_wyboru.pack(pady = 7, padx = 5)


    def detail(self, id_client):  # Nowe okno do update
        window = tk.Toplevel(self)
        window.resizable(0,0)

        db=sqlite3.connect('db/database.db')
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
            
            tk.Label(frame, text="Miasto", font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=9, column=0)
            tk.Label(frame, text=i[9], font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=9, column=1)

            tk.Label(frame, text="Kod pocztowy", font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=10, column=0)
            tk.Label(frame, text=i[10], font=("Calibri", 12)).grid(pady=10, padx=10, sticky=tk.W, row=10, column=1)



### Widok PRODUKTÓW ###



class Product(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        master.title("Faktura VAT - produkty")

        sf = ScrolledFrame(self, width=800, height=600)
        sf.pack(side="top", expand=1, fill="both")
        
        sf.bind_arrow_keys(self)
        sf.bind_scroll_wheel(self)

        frame = sf.display_widget(tk.Frame)
                
        normal = ttk.Style(frame)
        normal.configure("normal.TButton", font=("Calibri", 14))

        bold = ttk.Style(frame)
        bold.configure("bo.TButton", font=("Calibri", 14, "bold"))

        ttk.Label(frame, text="Faktura VAT - produkty", font=("Calibri", 24, "bold"), anchor="center").grid(pady=20, padx=235, columnspan=6)


        ttk.Button(frame, text="DODAJ NOWY PRODUKT", command=lambda: self.insert_window(master), style="normal.TButton").grid(padx=5, pady=10, columnspan=6, sticky="nswe")

        #ttk.Button(frame, text="ODŚWIEŻ", command=lambda: master.switch_frame(Product), style="normal.TButton").grid(padx=5, columnspan=6, sticky="nswe")

        ttk.Button(frame, text="COFNIJ", style="bo.TButton",
                   command=lambda: master.switch_frame(Menu)).grid(pady=0, padx=5, columnspan=6, sticky="nswe")

        ttk.Label(frame, text="TABELA Z PRODUKTAMI", font=("Calibri", 14, "bold"), anchor="center").grid(pady=20, padx=0, columnspan=6)

        self.table(frame, master)


    def table(self, w, master):  
        limit = 8
        q = "SELECT id, name, printf('%.2f', price) AS price FROM products;" 
        h = "select count(*) from products"
        i=0

        normal = ttk.Style(w)
        normal.configure("nor.TButton", font=("Calibri", 12))

        
        with sqlite3.connect("db/database.db") as db:  
            c = db.cursor()
            c.execute(q)
            r_set = c.fetchall()
            c.execute(h)
            no_rec = c.fetchone()[0]
            c.close()
        l = ["ID",
             "Nazwa",
             "Cena netto (zł)"]

        r_set.insert(0, l)  

        for product in r_set:
            for j in range(len(product)):
                e = ttk.Label(w, text=product[j], font=("Calibri", 12))
                e.grid(row=i+4, column=j, padx=10, pady=3)

            if r_set.index(product) != 0:
                f = ttk.Button(w, text='EDYTUJ', command=lambda d=product[0]: self.update(d, master), style="nor.TButton")
                f.grid(row=i+4, column=j + 2)
                f = ttk.Button(w, text='USUŃ', command=lambda d=product[0]: self.delete(d, master), style="nor.TButton")
                f.grid(row=i+4, column=j + 3, padx=5, pady=3)
            i = i + 1

        
    def insert_window(self, master):
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

        price_label = ttk.Label(window, text="Cena netto", font=("Calibri", 12), justify=tk.LEFT)
        price_label.grid(row=2, column=0, padx=5, pady=5, sticky = tk.W)
        price_entry = ttk.Entry(window, textvariable=window.price, font=("Calibri", 12), width=30)
        price_entry.grid(row=2, column=1, padx=5, pady=5, sticky = tk.W)

        button = ttk.Button(window, text="Dodaj", command=lambda: self.insert(window, master), style="nor.TButton", width=10)
        button.grid(row=3, column=0, padx=5, pady=5, sticky = tk.W)
        

    def insert(self, window, master):
        name = window.name.get()
        price = window.price.get()

        if price=="" or name=="":
            messagebox.showerror('Błąd', 'Sprawdź, czy wszystkie pola zostały uzupełnione.')
        else:  
            text = messagebox.showinfo('Sukces','Rekord dodano prawidłowo.')
            if text:
                query = (f"insert into products('name', 'price') values ('{name}', '{price}')")
                with sqlite3.connect("db/database.db") as db:
                    c = db.cursor()
                    c.execute(query)
                    c.close()
                window.withdraw()
                master.switch_frame(Product)


    def delete(self, id_product, master):
        text=messagebox.askyesnocancel("Usuń","Czy na pewno chcesz usunąć rekord?",icon='warning',default='no')
        if text:
            with sqlite3.connect("db/database.db") as db:
                c = db.cursor()
                c.execute(f"delete from products where id = {id_product}")
                c.close()
            master.switch_frame(Product)


    def update(self, id_product, master):
        window = tk.Toplevel()
        window.resizable(0, 0)
        db=sqlite3.connect('db/database.db')
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

            cena_label=ttk.Label(window,text="Cena netto", font=("Calibri", 12), justify=tk.LEFT)
            cena_label.grid(row=2, column=0, padx=5, pady=5, sticky = tk.W)
            cena_entry=ttk.Entry(window,textvariable=cena, font=("Calibri", 12), width=30)
            cena_entry.insert(0,i[2])
            cena_entry.grid(row=2, column=1, padx=5, pady=5, sticky = tk.W)


        def updatedetail(id_product):
            if nazwa.get()=="" or cena.get()=="":
                messagebox.showerror('Błąd','Wszystkie pola powinny zostać uzupełnione.')
            else:
                db=sqlite3.connect('db/database.db')
                c=db.cursor()
                c.execute("update products set name='"+nazwa.get()+"',price='"+cena.get()+"' where id='"+str(id_product)+"'")
                db.commit()
                db.close()
                window.withdraw()
                messagebox.showinfo('Sukces','Produkt został zaktualizowany.')
                master.switch_frame(Product)

        normal = ttk.Style(window)
        normal.configure("norm.TButton", font=("Calibri", 12))

        button=ttk.Button(window, text="Zaktualizuj", command=lambda: updatedetail(id_product), style="norm.TButton", width=10)
        button.grid(row=3, column=0, padx=5, pady=5, sticky = tk.W)
        


### KONIEC ###



root = tk.Tk()
root.geometry("800x600")
root.resizable(0,0)
app = Login(root)
root.mainloop()

with open('log/choice.txt','w') as file:
    file.write(str(app.bool.get()))

with open('log/username.txt','w') as file:
    file.write(str(app.username.get()))

with open('log/password.txt','w') as file:
    file.write(str(app.password.get()))



### Twórcy: ####
    
# 1. Radosław Gzyl
# 2. Mateusz Trzebiński
# 3. Maciej Jopek
# 4. Zuzanna Lenczyk-Wąsowska
# 5. Kamil Stefaniuk 
