import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import tix
import sqlite3



### Panel logowania ###



class Login(tk.Tk):
            
    def __init__(self, *args, **kwargs):        
        tk.Tk.__init__(self, *args, **kwargs)

        title = tk.Label(self, text="Faktura VAT", font=("Calibri", 24, 'bold'))
        title.pack(padx=100, pady=100)

        labelframe = tk.LabelFrame(self, text="Panel logowania", padx=10, pady=10, font=("Calibri", 12))  
        labelframe.pack()

        self.username = tk.StringVar()
        self.password = tk.StringVar()
     
        username_label = tk.Label(labelframe, text="Nazwa użytkownika: ", width=20, font=("Calibri", 12))
        username_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        username_entry = tk.Entry(labelframe, textvariable=self.username, width=25, font=("Calibri", 12))
        username_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.username.set("admin")
        
        password_label = tk.Label(labelframe, text="Hasło: ", width=20, font=("Calibri", 12))
        password_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        password_entry = tk.Entry(labelframe, textvariable=self.password, show="*", width=25, font=("Calibri", 12))
        password_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.password.set("1234")
        
        login_button = tk.Button(labelframe, text="Zaloguj się", command= self.login, width=20, font=("Calibri", 12))
        login_button.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        data = tk.Label(self, text="Autorzy: Radosław Gzyl, Mateusz Trzebiński, Maciej Jopek, Kamil Stefaniuk, Zuzanna Lenczyk-Wąsowska", font=("Calibri", 8, ""))
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


        tk.Label(self, text="Faktura VAT", font=("Calibri", 24, "bold")).pack(pady=10)
        tk.Button(self, text="Panel użytkownika", font=("Calibri", 16, "bold"),
                  command=lambda: master.switch_frame(Profile)).pack(side=tk.LEFT)
        tk.Button(self, text="Klienci", font=("Calibri", 16, "bold"),
                  command=lambda: master.switch_frame(Client)).pack(side=tk.LEFT)
        tk.Button(self, text='Produkty', font=("Calibri", 16, "bold"),
                  command=lambda: master.switch_frame(Product)).pack(side=tk.LEFT)
        tk.Button(self, text="Zamknij", font=("Calibri", 16, "bold"),
                  command=lambda: master.close()).pack(side=tk.LEFT)



### Widok KONTA UŻYTKOWNIKA ###



class Profile(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)            

        tk.Label(self, text="Faktura VAT - panel użytkownika", font=("Calibri", 24, "bold")).pack(pady=20)
        
        labelframe = tk.LabelFrame(self, text="Panel użytkownika", font=("Calibri", 12, "bold"))
        labelframe.pack(padx=10, pady=10)

        frame = tk.LabelFrame(self, text="Dane logowania", font=("Calibri", 12, 'bold'))
        frame.pack(padx=10, pady=10)

        con = sqlite3.connect('database.db')
        c = con.cursor()
        query = c.execute('SELECT * FROM profile WHERE id=1')
        
        for dat in query:           
            nazwa_opis = tk.Label(labelframe, text="Nazwa firmy", font=("Calibri", 12))
            nazwa_opis.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            nazwa = tk.Label(labelframe, text=dat[1], font=("Calibri", 12))
            nazwa.grid(row=0, column=1, padx=10, pady=5)
            
            ulica_opis = tk.Label(labelframe, text="Adres siedziby", font=("Calibri", 12))
            ulica_opis.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
            ulica = tk.Label(labelframe, text=dat[2], font=("Calibri", 12))
            ulica.grid(row=1, column=1, padx=10, pady=5)
            
            kod_opis = tk.Label(labelframe, text="Kod pocztowy/miasto", font=("Calibri", 12))
            kod_opis.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
            kod = tk.Label(labelframe, text=dat[3]+" "+dat[4], font=("Calibri", 12))
            kod.grid(row=2, column=1, padx=10, pady=5)
            
            telefon_opis = tk.Label(labelframe, text="Telefon kontaktowy", font=("Calibri", 12))
            telefon_opis.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
            telefon = tk.Label(labelframe, text="+48 "+dat[6], font=("Calibri", 12))
            telefon.grid(row=3, column=1, padx=10, pady=5)
            
            nip_opis = tk.Label(labelframe, text="Numer identyfikacji podatkowej", font=("Calibri", 12))
            nip_opis.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
            nip = tk.Label(labelframe, text=dat[5], font=("Calibri", 12))
            nip.grid(row=4, column=1, padx=10, pady=5)

            edit_profile_button = tk.Button(labelframe, text="Edytuj panel użytkownika",command=self.update, font=('Calibri', 12), width=90)
            edit_profile_button.grid(row=5, columnspan=2, padx=15, pady=15)
        
        edit_login_button = tk.Button(frame, text="Zaktualizuj/zmień nazwe użytkownika",command=self.login, font=('Calibri', 12), width=90)
        edit_login_button.grid(padx=15, pady=10)

        edit_password_button = tk.Button(frame, text="Zaktualizuj/zmień hasło",command=self.password, font=('Calibri', 12), width=90)
        edit_password_button.grid(padx=15, pady=10)

        button = tk.Button(self, text="Cofnij", font=('Calibri', 12, 'bold'), bg="grey",
            command=lambda: master.switch_frame(Menu))
        button.pack(fill="x", padx=5, pady=20, side=tk.BOTTOM)
            
        
    def password(self):
        window = tk.Toplevel()
        window.resizable(0,0)

        old_password = tk.StringVar()
        password = tk.StringVar()
        re_password = tk.StringVar()
        
        title=tk.Label(window, text="Formularz zmiany hasła w panelu użytkownika", font=("Calibri", 12, "bold"))
        title.grid(row=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

        password_label=tk.Label(window, text="Podaj obecne hasło", font=("Calibri", 12))
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        password_entry=tk.Entry(window, textvariable=old_password, font=("Calibri", 12), width=30, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        new_password_label=tk.Label(window, text="Podaj nowe hasło", font=("Calibri", 12))
        new_password_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        new_password_entry=tk.Entry(window, textvariable=password, font=("Calibri", 12), width=30, show="*")
        new_password_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        re_new_password_label=tk.Label(window, text="Powtórz nowe hasło", font=("Calibri", 12))
        re_new_password_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        re_new_password_entry=tk.Entry(window, textvariable=re_password, font=("Calibri", 12), width=30, show="*")
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
                        

        button = tk.Button(window, text="Zaktualizuj", font=("Calibri",12), width=18, command=password_update)
        button.grid(row=4, column=0, padx=10, pady=10)


    def login(self):
        window = tk.Toplevel()
        window.resizable(0,0)

        window.old_login = tk.StringVar()
        window.login = tk.StringVar()
        window.re_login = tk.StringVar()
        
        title=tk.Label(window, text="Formularz zmiany nazwy użytkownika w panelu użytkownika", font=("Calibri", 12, "bold"))
        title.grid(row=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

        login_label=tk.Label(window, text="Podaj obecną nazwę użytkownika", font=("Calibri", 12))
        login_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        login_entry=tk.Entry(window, textvariable=window.old_login, font=("Calibri", 12), width=40)
        login_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        new_login_label=tk.Label(window, text="Podaj nową nazwę użytkownika", font=("Calibri", 12))
        new_login_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        new_login_entry=tk.Entry(window, textvariable=window.login, font=("Calibri", 12), width=40)
        new_login_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        re_new_login_label=tk.Label(window, text="Powtórz nowa nazwę użytkownika", font=("Calibri", 12))
        re_new_login_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        re_new_login_entry=tk.Entry(window, textvariable=window.re_login, font=("Calibri", 12), width=40)
        re_new_login_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        button = tk.Button(window, text="Zaktualizuj", font=("Calibri",12), width=26, command=lambda: self.login_update(window))
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

            title = tk.Label(window, text="Formularz edytowania danych panelu użytkownika", font=("Calibri", 12, "bold"))
            title.grid(row=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
                             
            nazwa_label=tk.Label(window,text="Nazwa firmy", font=("Calibri", 12))
            nazwa_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)                
            nazwa_entry=tk.Entry(window,textvariable=nazwa, font=("Calibri", 12), width=35)
            nazwa_entry.insert(0,index[1])
            nazwa_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

            ulica_label=tk.Label(window,text="Adres siedziby", font=("Calibri", 12))
            ulica_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
            ulica_entry=tk.Entry(window,textvariable=ulica, font=("Calibri", 12), width=35)
            ulica_entry.insert(0,index[2])
            ulica_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

            kod_label=tk.Label(window,text="Kod pocztowy", font=("Calibri", 12))
            kod_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
            kod_entry=tk.Entry(window,textvariable=kod, font=("Calibri", 12), width=35)
            kod_entry.insert(0,index[3])
            kod_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

            miasto_label=tk.Label(window,text="Miasto", font=("Calibri", 12))
            miasto_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
            miasto_entry=tk.Entry(window,textvariable=miasto, font=("Calibri", 12), width=35)
            miasto_entry.insert(0,index[4])
            miasto_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

            telefon_label=tk.Label(window,text="Telefon kontaktowy", font=("Calibri", 12))
            telefon_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
            telefon_entry=tk.Entry(window,textvariable=telefon, font=("Calibri", 12), width=35)
            telefon_entry.insert(0,index[6])
            telefon_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

            nip_label=tk.Label(window,text="Numer identyfikacji podatkowej", font=("Calibri", 12))
            nip_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
            nip_entry=tk.Entry(window,textvariable=nip, font=("Calibri", 12), width=35)
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
                messagebox.showinfo('Sukces','Profil właściciela został zaktualizowany.')
        
        button=tk.Button(window, text="Zaktualizuj", command=updatedetail, font=("Calibri", 12), width=28)
        button.grid(row=7, column=0, padx=10, pady=10)



### Widok KLIENTÓW ###



class Client(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="TABELA KLIENCI").pack(side="top")
        rama_tabela = tk.Frame(self)
        self.my_show(rama_tabela, 0)
        rama_tabela.pack(side="top", expand="yes")
        
        tk.Button(self, text="Cofnij", command=lambda: master.switch_frame(Menu)).pack()
        tk.Button(self, text="Dodaj", command=lambda: self.okno_zapisz()).pack(side="bottom", pady=5,padx=5)



    def my_show(self, w, offset):  # Tabelka
        limit = 8
        q = "SELECT C_ID, Nabywca from clients LIMIT " + str(offset) + "," + str(limit)
        h = "select count(*) from clients"
        i=0
        with sqlite3.connect("database.db") as db:  # Wypisanie recordow
            c = db.cursor()
            c.execute(q)
            r_set = c.fetchall()
            c.execute(h)
            no_rec = c.fetchone()[0]
            c.close()
        l = ["ID",
             "NABYWCA"]

        r_set.insert(0, l)  # Dodanie nazw kolumn

        for client in r_set:
            for j in range(len(client)):
                e = tk.Label(w, text=client[j], width=9, fg='black')
                e.grid(row=i, column=j)

            if r_set.index(client) != 0:
                e = tk.Button(w, text='DETAIL')
                e.grid(row=i, column=j + 1)
                f = tk.Button(w, text='DELETE', command=lambda d=client[0]: self.update(d))
                f.grid(row=i, column=j + 2)
                f = tk.Button(w, text='DELETE', command=lambda d=client[0]: self.usun(d))
                f.grid(row=i, column=j + 3)
            i = i + 1

        while (i < limit):  # required to blank the balance rows if they are less
            for j in range(10):
                e = tk.Label(w, text=" ", width=9)
                e.grid(row=i, column=j)

            i = i + 1

            # Show buttons
        back = offset - limit  # This value is used by Previous button
        next = offset + limit  # This value is used by Next button
        b1 = tk.Button(w, text='Next >', command=lambda: self.my_show(w,next))
        b1.grid(row=12, column=10)
        b2 = tk.Button(w, text='< Prev', command=lambda: self.my_show(w, back))
        b2.grid(row=12, column=1)

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
        
            text = messagebox.showinfo('Sukces','Rekord dodano prawidłowo.')
            if text:
                query = (f"insert into clients('nabywca', '{okno.variable.get().replace(' ','_')}', 'ulica', 'miasto_kod')values('{nabywca}', '{wybor}', '{ulica}', '{kod_miasto}')")
                with sqlite3.connect("database.db") as db:
                    c = db.cursor()
                    c.execute(query)
                    c.close()
                okno.withdraw()


    def usun(self, id_client):
        text=messagebox.askyesnocancel("Usuń","Czy na pewno chcesz usunąć rekord?",icon='warning',default='no')
        if text:
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

        tk.Label(self, text="Faktura VAT - produkty", font=("Calibri", 24, "bold")).pack(pady=10)

        tk.Button(self, text="COFNIJ", font=("Calibri", 14, "bold"), bg="grey",
                  command=lambda: master.switch_frame(Menu)).pack(side="bottom", fill="x", pady=10, padx=10)

        tk.Button(self, text="DODAJ NOWY PRODUKT", command=self.insert_window, font=("Calibri", 14, "bold")).pack(padx=20, pady=0, side="top", fill='x')
        tk.Button(self, text="ODŚWIEŻ TABELĘ", command=lambda: master.switch_frame(Product), font=("Calibri", 14)).pack(padx=20, pady=15, side="top", fill='x')

        tk.Label(self, text="TABELA Z PRODUKTAMI", font=("Calibri", 14, "bold")).pack(side="top")
        frame = tk.Frame(self)
        self.table(frame, 0)
        frame.pack()

        
    def insert_window(self):
        window = tk.Toplevel(self)
        window.resizable(0, 0)  
        window.name = tk.StringVar(window)
        window.price = tk.StringVar(window)

        title= tk.Label(window, text="Formularz dodawania nowego produktu:", font=("Calibri", 12), justify=tk.LEFT)
        title.grid(row=0, columnspan=2, padx=5, pady=5, sticky = tk.W)

        name_label = tk.Label(window, text="Nazwa", font=("Calibri", 12), justify=tk.LEFT)
        name_label.grid(row=1, column=0, padx=5, pady=5, sticky = tk.W)
        name_entry = tk.Entry(window, textvariable=window.name, font=("Calibri", 12), width=30)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky = tk.W)

        price_label = tk.Label(window, text="Cena brutto", font=("Calibri", 12), justify=tk.LEFT)
        price_label.grid(row=2, column=0, padx=5, pady=5, sticky = tk.W)
        price_entry = tk.Entry(window, textvariable=window.price, font=("Calibri", 12), width=30)
        price_entry.grid(row=2, column=1, padx=5, pady=5, sticky = tk.W)

        button = tk.Button(window, text="Dodaj", command=lambda: self.insert(window), font=("Calibri", 12), width=10)
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

        for product in r_set:
            for j in range(len(product)):
                e = tk.Label(w, text=product[j], width=12, fg='black', font=("Calibri", 12))
                e.grid(row=i, column=j)

            if r_set.index(product) != 0:
                e = tk.Button(w, text='Edytuj', command=lambda d=product[0]: self.update(d), font=("Calibri", 12))
                e.grid(row=i, column=j + 1)
                f = tk.Button(w, text='Usuń', command=lambda d=product[0]: self.delete(d), font=("Calibri", 12))
                f.grid(row=i, column=j + 2)
            i = i + 1

        while (i < limit): 
            for j in range(10):
                e = tk.Label(w, text=" ", width=12)
                e.grid(row=i, column=j)

            i = i + 1

        back = offset - limit  
        next = offset + limit  
        b1 = tk.Button(w, text='Następny >', command=lambda: self.table(w, next), font=("Calibri", 12))
        b1.grid(row=12, column=3, pady=10)
        b2 = tk.Button(w, text='< Poprzedni', command=lambda: self.table(w, back), font=("Calibri", 12))
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

        title= tk.Label(window, text="Formularz edycji produktu:", font=("Calibri", 12), justify=tk.LEFT)
        title.grid(row=0, columnspan=2, padx=5, pady=5, sticky = tk.W)

        for i in query:
            nazwa=tk.StringVar()
            cena=tk.StringVar()
                             
            nazwa_label=tk.Label(window,text="Nazwa", font=("Calibri", 12), justify=tk.LEFT)
            nazwa_label.grid(row=1, column=0, padx=5, pady=5, sticky = tk.W)
            nazwa_entry=tk.Entry(window,textvariable=nazwa, font=("Calibri", 12), width=30)
            nazwa_entry.insert(0,i[1])
            nazwa_entry.grid(row=1, column=1, padx=5, pady=5, sticky = tk.W)

            cena_label=tk.Label(window,text="Cena brutto", font=("Calibri", 12), justify=tk.LEFT)
            cena_label.grid(row=2, column=0, padx=5, pady=5, sticky = tk.W)
            cena_entry=tk.Entry(window,textvariable=cena, font=("Calibri", 12), width=30)
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

        button=tk.Button(window, text="Zaktualizuj", command=lambda: updatedetail(id_product), font=("Calibri", 12), width=10)
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
