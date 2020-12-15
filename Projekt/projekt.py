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
        tk.Button(self, text="Konto użytkownika", font=("Calibri", 16, "bold"),
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
        self.connection = sqlite3.connect('database.db')
        self.con = self.connection.cursor()
        tk.Button(self, text="Cofnij",
                  command=lambda: master.switch_frame(Menu)).pack()

        self.show()
        button=tk.Button(self, text="Edytuj",command=self.update).pack()

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
            tk.Label(self, text="Telefon").pack()
        
    def read(self):
        self.con.execute("select * from profile where id=1")
        return self.con.fetchall()

    def update(self):
        window = tk.Toplevel()
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
                             
            nazwa_label=tk.Label(window,text="Nazwa").pack()                
            nazwa_entry=tk.Entry(window,textvariable=nazwa)
            nazwa_entry.insert(0,index[1])
            nazwa_entry.pack()

            ulica_label=tk.Label(window,text="Ulica").pack()
            ulica_entry=tk.Entry(window,textvariable=ulica)
            ulica_entry.insert(0,index[2])
            ulica_entry.pack()

            kod_label=tk.Label(window,text="Kod pocztowy").pack()
            kod_entry=tk.Entry(window,textvariable=kod)
            kod_entry.insert(0,index[3])
            kod_entry.pack()

            miasto_label=tk.Label(window,text="Miasto").pack()
            miasto_entry=tk.Entry(window,textvariable=miasto)
            miasto_entry.insert(0,index[4])
            miasto_entry.pack()

            nip_label=tk.Label(window,text="NIP").pack()
            nip_entry=tk.Entry(window,textvariable=nip)
            nip_entry.insert(0,index[5])
            nip_entry.pack()

            telefon_label=tk.Label(window,text="Telefon").pack()
            telefon_entry=tk.Entry(window,textvariable=telefon)
            telefon_entry.insert(0,index[6])
            telefon_entry.pack()
        
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
        
        button=tk.Button(window, text="Zaktualizuj", command=updatedetail).pack()



### Widok KLIENTÓW ###



class Client(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="TABELA KLIENCI").pack(side="top")
        rama_tabela = tk.Frame(self)
        rama_tabela.pack(side="top", expand="yes")

        self.my_show(rama_tabela, 0)

        tk.Button(self, text="Cofnij", command=lambda: master.switch_frame(Menu)).pack()
        tk.Button(self, text="Dodaj", command=lambda: self.okno_zapisz()).pack(side="bottom", pady=5,padx=5)



    def my_show(self, w, offset):  # Tabelka
        limit = 8
        q = "SELECT * from clients LIMIT " + str(offset) + "," + str(limit)
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
             "NABYWCA",
             "NIP",
             "REGON",
             "VAT EU",
             "PESEL",
             "NUMER FIRMY",
             "OSOBA FIZYCZNA",
             "ULICA",
             "MIASTO/KOD"]

        r_set.insert(0, l)  # Dodanie nazw kolumn

        for client in r_set:
            for j in range(len(client)):
                e = tk.Label(w, text=client[j], width=9, fg='black')
                e.grid(row=i, column=j)

            if r_set.index(client) != 0:
                e = tk.Button(w, text='EDIT', command=lambda d=client[0]: self.update(d))
                e.grid(row=i, column=j + 1)
                f = tk.Button(w, text='DELETE', command=lambda d=client[0]: self.usun(d))
                f.grid(row=i, column=j + 2)
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

        if okno.nabywca.get()=="" or okno.ulica.get()=="" or okno.kod.get()=="" or okno.miasto.get()=="" or okno.wybor2.get()=="":
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
        #tk.Label(self, text="Coś tu prędzej, czy później będzie...").pack(side="top", fill="x", pady=100)
        tk.Button(self, text="Cofnij",
                  command=lambda: master.switch_frame(Menu)).pack(side="top", fill="y", pady=100, padx=100)

        tk.Label(self, text="TABELA Z PRODUKTAMI").pack(side="top")
        frame = tk.Frame(self)
        frame.pack(side="bottom", expand="yes")

        self.table(frame)

        #tk.Button(self, text="Cofnij", command=lambda: master.switch_frame(Menu)).pack()
    

    def table(self, w):  # Tabelka
        limit = 10
        offset = 0
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
             "Cena netto"]

        r_set.insert(0, l)

        for client in r_set:
            for j in range(len(client)):
                e = tk.Label(w, text=client[j], width=9, fg='black')
                e.grid(row=i, column=j)

            if r_set.index(client) != 0:
                e = tk.Button(w, text='EDYTUJ', command=lambda d=client[0]: self.update(d))
                e.grid(row=i, column=j + 1)
                f = tk.Button(w, text='USUŃ', command=lambda d=client[0]: self.usun(d))
                f.grid(row=i, column=j + 2)
            i = i + 1

        while (i < limit):  
            for j in range(10):
                e = tk.Label(w, text=" ", width=9)
                e.grid(row=i, column=j)

            i = i + 1

            
        back = offset - limit  
        next = offset + limit  
        b1 = tk.Button(w, text='Następny >', command=lambda: self.table(w,next))
        b1.grid(row=12, column=3)
        b2 = tk.Button(w, text='< Poprzedni', command=lambda: self.table(w, back))
        b2.grid(row=12, column=1)

        if (no_rec <= next):
            b1["state"] = "disabled"  
        else:
            b1["state"] = "active"

        if (back >= 0):
            b2["state"] = "active"
        else:
            b2["state"] = "disabled"  



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
