import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import tix as tx
import sqlite3
from tkscrolledframe import ScrolledFrame
from tkcalendar import *



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
        

        def combo_data():

            con = sqlite3.connect('database.db')
            c = con.cursor()
            query = c.execute('SELECT nabywca FROM clients ORDER BY nabywca')

            data = []
            for row in c.fetchall():
                data.append(row[0])
            return data
        

        def combo_product():

            con = sqlite3.connect('database.db')
            c = con.cursor()
            query = c.execute('SELECT name FROM products ORDER BY name')

            data = []
            for row in c.fetchall():
                data.append(row[0])
            return data


        def details(event):

            con = sqlite3.connect('database.db')
            c = con.cursor()
            query = c.execute("SELECT ulica, miasto_kod, osoba_fizyczna, nip, regon, vat_eu, pesel FROM clients WHERE nabywca='"+event.widget.get()+"'")

            for row in query:
                ulica_entry.config(state = tk.NORMAL)
                ulica_entry.delete(0, tk.END)
                ulica_entry.insert(0, row[0])
                ulica_entry.config(state = "readonly")

                kod_miasto_entry.config(state = tk.NORMAL)
                kod_miasto_entry.delete(0, tk.END)
                kod_miasto_entry.insert(0, row[1])
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

            con = sqlite3.connect('database.db')
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

            con = sqlite3.connect('database.db')
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

            con = sqlite3.connect('database.db')
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

            con = sqlite3.connect('database.db')
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
        
        przycisk = ttk.Button(menu, text="Zamknij", command=lambda: master.close(), style="my.TButton")
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

        numer_label = ttk.Label(frame, text="Numer faktury", font=("Calibri", 12))
        numer_label.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W)
        numer_entry = ttk.Entry(frame, width=27, textvariable=self.numer, font=("Calibri", 12))
        numer_entry.grid(padx=5, pady=5, row=0, column=1, sticky=tk.W)

        wystawiona_label = ttk.Label(frame, text="Data wystawienia", font=("Calibri", 12))
        wystawiona_label.grid(padx=5, pady=5, row=1, column=0, sticky=tk.W)
        wystawiona_entry = DateEntry(frame, width=25, textvariable=self.wystawienia,  font=("Calibri", 12), locale='en_US', date_pattern='dd-mm-y')  
        wystawiona_entry.grid(padx=5, pady=5, row=1, column=1, sticky=tk.W)

        sprzedaz_label = ttk.Label(frame, text="Data sprzedaży", font=("Calibri", 12))
        sprzedaz_label.grid(padx=5, pady=5, row=0, column=2, sticky=tk.W)
        sprzedaz_entry = DateEntry(frame, width=25, textvariable=self.sprzedaz, font=("Calibri", 12), locale='en_US', date_pattern='dd-mm-y')
        sprzedaz_entry.grid(padx=5, pady=5, row=0, column=3, sticky=tk.W)

        miejsce_label = ttk.Label(frame, text="Miejsce wystawienia", font=("Calibri", 12))
        miejsce_label.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
        miejsce_entry = ttk.Entry(frame, width=27, textvariable=self.miejsce, font=("Calibri", 12))
        miejsce_entry.insert(0, "Wrocław")
        miejsce_entry.grid(padx=5, pady=5, row=1, column=3, sticky=tk.W)

        sposob_label = ttk.Label(frame, text="Sposób zapłaty", font=("Calibri", 12))
        sposob_label.grid(padx=5, pady=5, row=2, column=0, sticky=tk.W)
            
        sposob_combobox = ttk.Combobox(frame, textvariable=self.sposob, font=("Calibri", 12), width=25)
        sposob_combobox.grid(padx=5, pady=5, row=2, column=1, sticky=tk.W)
        sposob_combobox['values'] = ('Gotówka', ' Przelew') 
        sposob_combobox.current(0) 

        termin_label = ttk.Label(frame, text="Termin zapłaty", font=("Calibri", 12))
        termin_label.grid(padx=5, pady=5, row=2, column=2, sticky=tk.W)
        termin_entry = DateEntry(frame, width=25, textvariable=self.termin,  font=("Calibri", 12), locale='en_US', date_pattern='dd-mm-y')  
        termin_entry.grid(padx=5, pady=5, row=2, column=3, sticky=tk.W)

        window = ttk.LabelFrame(self, text="Klienci")
        window.pack(padx=10, pady=5, fill="x")

        self.nabywca = tk.StringVar(self)
        self.ulica = tk.StringVar(self)
        self.kod_miasto = tk.StringVar(self) 
        self.osoba = tk.StringVar(self)

            
        ulica_label = ttk.Label(window, width=18, text="Ulica:", font=("Calibri", 12))
        ulica_label.grid(padx=5, pady=5, row=0, column=2, sticky=tk.W)
        ulica_entry = ttk.Entry(window, width=27 ,state="readonly", textvariable=self.ulica, font=("Calibri", 12))
        ulica_entry.grid(padx=5, pady=5, row=0, column=3, sticky=tk.W)

        kod_miasto_label = ttk.Label(window,text="Kod/miasto:", font=("Calibri", 12))
        kod_miasto_label.grid(padx=5, pady=5, row=1, column=0, sticky=tk.W)
        kod_miasto_entry = ttk.Entry(window, width=27, state="readonly", textvariable=self.kod_miasto, font=("Calibri", 12))
        kod_miasto_entry.grid(padx=5, pady=5, row=1, column=1, sticky=tk.W)

        osoba_entry = ttk.Entry(window, width=27, state="readonly", textvariable=self.osoba, font=("Calibri", 12))
        osoba_entry.grid(padx=5, pady=5, row=1, column=3, sticky=tk.W)
                    
        nabywca_name = ttk.Label(window, width=14, text="Nabywca:", font=("Calibri", 12))
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
                    
        nazwa_l = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
        nazwa_l.grid(padx=5, pady=5, row=0, column=0, sticky=tk.W)
        nazwa_c = ttk.Combobox(products, textvariable=self.nazwa, font=("Calibri", 12))
        nazwa_c.grid(padx=5, pady=5, row=0, column=1, sticky=tk.W)
        nazwa_c['values'] = combo_product()
        nazwa_c.bind("<<ComboboxSelected>>", detail_first)

        style = ttk.Style()
        style.configure("font.TButton", font=("Calibri", 12))

        ilosc_l = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
        ilosc_l.grid(padx=5, pady=5, row=0, column=2, sticky=tk.W)
        ilosc_e = ttk.Entry(products, textvariable=self.ilosc, font=("Calibri", 12))
        ilosc_e.grid(padx=5, pady=5, row=0, column=3, sticky=tk.W)

        cena_l = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
        cena_l.grid(padx=5, pady=5, row=0, column=4, sticky=tk.W)
        cena_e = ttk.Entry(products,state="readonly", textvariable=self.cena, font=("Calibri", 12))
        cena_e.grid(padx=5, pady=5, row=0, column=5, sticky=tk.W)

        self.nazwa_1 = tk.StringVar(self)
        self.cena_1 = tk.StringVar(self)
        self.ilosc_1 = tk.StringVar(self)
                    
        nazwa_ll = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
        nazwa_ll.grid(padx=5, pady=5, row=1, column=0, sticky=tk.W)
        nazwa_cc = ttk.Combobox(products, textvariable=self.nazwa_1, font=("Calibri", 12))
        nazwa_cc.grid(padx=5, pady=5, row=1, column=1, sticky=tk.W)
        nazwa_cc['values'] = combo_product()
        nazwa_cc.bind("<<ComboboxSelected>>", detail_second)

        ilosc_ll = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
        ilosc_ll.grid(padx=5, pady=5, row=1, column=2, sticky=tk.W)
        ilosc_ee = ttk.Entry(products, textvariable=self.ilosc_1, font=("Calibri", 12))
        ilosc_ee.grid(padx=5, pady=5, row=1, column=3, sticky=tk.W)

        cena_ll = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
        cena_ll.grid(padx=5, pady=5, row=1, column=4, sticky=tk.W)
        cena_ee = ttk.Entry(products,state="readonly", textvariable=self.cena_1, font=("Calibri", 12))
        cena_ee.grid(padx=5, pady=5, row=1, column=5, sticky=tk.W)

        self.nazwa_2 = tk.StringVar(self)
        self.cena_2 = tk.StringVar(self)
        self.ilosc_2 = tk.StringVar(self)
                    
        nazwa_lll = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
        nazwa_lll.grid(padx=5, pady=5, row=2, column=0, sticky=tk.W)
        nazwa_ccc = ttk.Combobox(products, textvariable=self.nazwa_2, font=("Calibri", 12))
        nazwa_ccc.grid(padx=5, pady=5, row=2, column=1, sticky=tk.W)
        nazwa_ccc['values'] = combo_product()
        nazwa_ccc.bind("<<ComboboxSelected>>", detail_third)

        ilosc_lll = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
        ilosc_lll.grid(padx=5, pady=5, row=2, column=2, sticky=tk.W)
        ilosc_eee = ttk.Entry(products, textvariable=self.ilosc_2, font=("Calibri", 12))
        ilosc_eee.grid(padx=5, pady=5, row=2, column=3, sticky=tk.W)

        cena_lll = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
        cena_lll.grid(padx=5, pady=5, row=2, column=4, sticky=tk.W)
        cena_eee = ttk.Entry(products,state="readonly", textvariable=self.cena_2, font=("Calibri", 12))
        cena_eee.grid(padx=5, pady=5, row=2, column=5, sticky=tk.W)

        self.nazwa_3 = tk.StringVar(self)
        self.cena_3 = tk.StringVar(self)
        self.ilosc_3 = tk.StringVar(self)
                    
        nazwa_llll = ttk.Label(products, text="Nazwa:", font=("Calibri", 12))
        nazwa_llll.grid(padx=5, pady=5, row=3, column=0, sticky=tk.W)
        nazwa_cccc = ttk.Combobox(products, textvariable=self.nazwa_3, font=("Calibri", 12))
        nazwa_cccc.grid(padx=5, pady=5, row=3, column=1, sticky=tk.W)
        nazwa_cccc['values'] = combo_product()
        nazwa_cccc.bind("<<ComboboxSelected>>", detail_fourth)

        ilosc_llll = ttk.Label(products,text="Ilość:", font=("Calibri", 12))
        ilosc_llll.grid(padx=5, pady=5, row=3, column=2, sticky=tk.W)
        ilosc_eeee = ttk.Entry(products, textvariable=self.ilosc_3, font=("Calibri", 12))
        ilosc_eeee.grid(padx=5, pady=5, row=3, column=3, sticky=tk.W)

        cena_llll = ttk.Label(products,text="Cena netto:", font=("Calibri", 12))
        cena_llll.grid(padx=5, pady=5, row=3, column=4, sticky=tk.W)
        cena_eeee = ttk.Entry(products,state="readonly", textvariable=self.cena_3, font=("Calibri", 12))
        cena_eeee.grid(padx=5, pady=5, row=3, column=5, sticky=tk.W)

        ins = ttk.Style(self)
        ins.configure("ins.TButton", font=("Calibri", 12, "bold"))
        
        ttk.Button(self, text="DODAJ", command = lambda: self.insert(master), style="ins.TButton").pack(side=tk.RIGHT, ipady=2, padx=10)


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

        nazwa_11 = self.nazwa_1.get()
        cena_11 = self.cena_1.get()
        ilosc_11 = self.ilosc_1.get()
            
        nazwa_22 = self.nazwa_2.get()
        cena_22 = self.cena_2.get()
        ilosc_22 = self.ilosc_2.get()

        nazwa_33 = self.nazwa_3.get()
        cena_33 = self.cena_3.get()
        ilosc_33 = self.ilosc_3.get()
          
        if numerr=="" or miejscee=="" or nabywcaa=="" or nazwaa=="" or iloscc=="":
            messagebox.showerror('Błąd','Wszystkie pola powinny zostać uzupełnione.')
        else:
            text = messagebox.showinfo('Sukces','Faktura została dodana.')
            if text:
                query = (f"insert into invoice('number', 'sale_date', 'issue_date', 'place', 'choice', 'payment_date', 'nabywca', 'ulica', 'kod_miasto', 'vat', 'nazwa', 'ilosc', 'cena', 'nazwa_1', 'ilosc_1', 'cena_1', 'nazwa_2', 'ilosc_2', 'cena_2', 'nazwa_3', 'ilosc_3', 'cena_3') values ('{numerr}', '{miejscee}', '{sprzedazz}', '{wystawieniaa}', '{sposobb}', '{terminn}', '{nabywcaa}', '{ulicaa}', '{kod_miastoo}', '{osobaa}','{nazwaa}', '{iloscc}', '{cenaa}', '{nazwa_11}', '{ilosc_11}', '{cena_11}', '{nazwa_22}', '{ilosc_22}', '{cena_22}', '{nazwa_33}', '{ilosc_33}', '{cena_33}')")
                with sqlite3.connect("database.db") as db:
                    c = db.cursor()
                    c.execute(query)
                    c.close()
                master.switch_frame(Menu)


                  
### Widok FAKTURY ###



class Invoice(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        sf = ScrolledFrame(self, width=800, height=600)
        sf.pack(side="top", expand=1, fill="both")
        
        sf.bind_arrow_keys(self)
        sf.bind_scroll_wheel(self)

        frame = sf.display_widget(tk.Frame)
                
        normal = ttk.Style(frame)
        normal.configure("normal.TButton", font=("Calibri", 14))

        bold = ttk.Style(frame)
        bold.configure("bo.TButton", font=("Calibri", 14, "bold"))

        ttk.Label(frame, text="Faktura VAT - szczegóły", font=("Calibri", 24, "bold"), anchor="center").grid(pady=20, padx=232, columnspan=6)

        ttk.Button(frame, text="ODŚWIEŻ", command=lambda: master.switch_frame(Invoice), style="normal.TButton").grid(padx=5, columnspan=6, sticky="nswe")

        ttk.Label(frame, text="TABELA Z FAKTURAMI", font=("Calibri", 14, "bold"), anchor="center").grid(pady=20, padx=0, columnspan=6)

        self.table(frame)

        ttk.Button(frame, text="COFNIJ", style="bo.TButton",
                   command=lambda: master.switch_frame(Menu)).grid(pady=10, padx=5, columnspan=6, sticky="nswe")


    def table(self, w):  
        limit = 8
        q = "SELECT id, number, nabywca from invoice" 
        h = "select count(*) from invoice"
        i=0

        normal = ttk.Style(w)
        normal.configure("normaa.TButton", font=("Calibri", 12))

        
        with sqlite3.connect("database.db") as db:  
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
                f = ttk.Button(w, text='EDYTUJ', command=lambda d=invoice[0]: self.update(d), style="normaa.TButton")
                f.grid(row=i+4, column=j + 2)
                f = ttk.Button(w, text='USUŃ', command=lambda d=invoice[0]: self.delete(d), style="normaa.TButton")
                f.grid(row=i+4, column=j + 3, pady=3)
            i = i + 1


    def detail(self, id_invoice):
        window = tk.TopLevel(self)
        window.resizable(0,0)


    def update(self, id_invoice):
        window = tk.TopLevel(self)
        window.resizable(0,0)


    def delete(self, id_invoice):
        text=messagebox.askyesnocancel("Usuń","Czy na pewno chcesz usunąć fakture?",icon='warning',default='no')
        if text:
            with sqlite3.connect("database.db") as db:
                c = db.cursor()
                c.execute(f"delete from invoice where id = {id_invoice}")
                c.close()

            

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
                        


    def update(self, master):
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
                master.switch_frame(Profile)
        
        normal = ttk.Style(window)
        normal.configure("normal.TButton", font=("Calibri", 12))
        
        button=ttk.Button(window, text="Zaktualizuj", command=updatedetail, style="normal.TButton", width=28)
        button.grid(row=7, column=0, padx=10, pady=10)



### Widok KLIENTÓW ###



class Client(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
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


        ttk.Button(frame, text="DODAJ NOWEGO KLIENTA", command=self.okno_zapisz, style="normal.TButton").grid(padx=5, pady=10, columnspan=6, sticky="nswe")

        ttk.Button(frame, text="ODŚWIEŻ", command=lambda: master.switch_frame(Client), style="normal.TButton").grid(padx=5, columnspan=6, sticky="nswe")

        ttk.Label(frame, text="TABELA Z KLIENTAMI", font=("Calibri", 14, "bold"), anchor="center").grid(pady=20, padx=0, columnspan=6)

        self.table(frame)

        ttk.Button(frame, text="COFNIJ", style="bo.TButton",
                   command=lambda: master.switch_frame(Menu)).grid(pady=10, padx=5, columnspan=6, sticky="nswe")

    def table(self, w):  
        limit = 8
        q = "SELECT c_id, nabywca from clients" 
        h = "select count(*) from clients"
        i=0

        normal = ttk.Style(w)
        normal.configure("normaa.TButton", font=("Calibri", 12))

        
        with sqlite3.connect("database.db") as db:  
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
                f = ttk.Button(w, text='EDYTUJ', command=lambda d=client[0]: self.update(d), style="normaa.TButton")
                f.grid(row=i+4, column=j + 2)
                f = ttk.Button(w, text='USUŃ', command=lambda d=client[0]: self.usun(d), style="normaa.TButton")
                f.grid(row=i+4, column=j + 3, pady=3)
            i = i + 1


    def okno_zapisz(self):  # Nowe okno do zapisu
        okno = tk.Toplevel(self)
        okno.resizable(0, 0)  
        okno.nabywca = tk.StringVar(okno)
        okno.ulica = tk.StringVar(okno)
        okno.miasto = tk.StringVar(okno)
        okno.kod = tk.StringVar(okno)
        okno.wybor2 = tk.StringVar(okno)
        okno.id = tk.StringVar(okno)

        frame_napisy = tk.Frame(okno)  # Ramka z napisami pol
        frame_napisy.pack(side="left", fill="both")
        tk.Label(frame_napisy, text="Nabywca").pack(pady = 5, padx = 5)
        tk.Label(frame_napisy, text="Ulica").pack(pady = 5, padx = 5)
        tk.Label(frame_napisy, text="Miasto").pack(pady = 5, padx = 5)
        tk.Label(frame_napisy, text="Kod").pack(pady = 5, padx = 5)

        choices = ("NIP", "REGON", "VAT EU", "PESEL", "Numer firmy", "Osoba fizyczna")
        okno.variable = tk.StringVar(okno)
        okno.variable.set("Osoba fizyczna")
        tk.OptionMenu(frame_napisy, okno.variable, *choices, command=self.choice).pack(pady = 5, padx = 5)

        frame_entry = tk.Frame(okno)  # Ramka z polami
        frame_entry.pack(side="left", fill="both")
        tk.Entry(frame_entry, textvariable=okno.nabywca).pack(pady = 5, padx = 5)
        tk.Entry(frame_entry, textvariable=okno.ulica).pack(pady = 8, padx = 5)
        tk.Entry(frame_entry, textvariable=okno.miasto).pack(pady = 4, padx = 5)
        tk.Entry(frame_entry, textvariable=okno.kod).pack(pady = 9, padx = 5)
        self.pole_do_wpisania_wyboru = tk.Entry(frame_entry, textvariable=okno.wybor2)


        tk.Button(okno, text="ZAPISZ", command=lambda : self.zapisz(okno) ).pack(side="bottom", pady = 5, padx = 5)
        
            
    def zapisz(self, okno):
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
        
            text = messagebox.showinfo('Sukces','Rekord dodano prawidłowo.')
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
        normal.configure("nor.TButton", font=("Calibri", 12))

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

            button = ttk.Button(frame_napisy, text="Aktualizuj", command= lambda : self.query_update(id_client), style="nor.TButton", width=15)
            button.pack(side="bottom", pady=10, padx=10)


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





### Widok PRODUKTÓW ###



class Product(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

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


        ttk.Button(frame, text="DODAJ NOWY PRODUKT", command=self.insert_window, style="normal.TButton").grid(padx=5, pady=10, columnspan=6, sticky="nswe")

        ttk.Button(frame, text="ODŚWIEŻ", command=lambda: master.switch_frame(Product), style="normal.TButton").grid(padx=5, columnspan=6, sticky="nswe")

        ttk.Label(frame, text="TABELA Z PRODUKTAMI", font=("Calibri", 14, "bold"), anchor="center").grid(pady=20, padx=0, columnspan=6)

        self.table(frame)

        ttk.Button(frame, text="COFNIJ", style="bo.TButton",
                   command=lambda: master.switch_frame(Menu)).grid(pady=10, padx=5, columnspan=6, sticky="nswe")

    def table(self, w):  
        limit = 8
        q = "SELECT * from products" 
        h = "select count(*) from products"
        i=0

        normal = ttk.Style(w)
        normal.configure("nor.TButton", font=("Calibri", 12))

        
        with sqlite3.connect("database.db") as db:  
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
                f = ttk.Button(w, text='EDYTUJ', command=lambda d=product[0]: self.update(d), style="nor.TButton")
                f.grid(row=i+4, column=j + 2)
                f = ttk.Button(w, text='USUŃ', command=lambda d=product[0]: self.delete(d), style="nor.TButton")
                f.grid(row=i+4, column=j + 3, padx=5, pady=3)
            i = i + 1

        
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

        price_label = ttk.Label(window, text="Cena netto", font=("Calibri", 12), justify=tk.LEFT)
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

            cena_label=ttk.Label(window,text="Cena netto", font=("Calibri", 12), justify=tk.LEFT)
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
