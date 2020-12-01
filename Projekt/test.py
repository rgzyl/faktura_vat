import tkinter
import tkinter as Tk
import sqlite3
from tkinter.messagebox import showerror, showinfo

with sqlite3.connect('database.db') as db:
    c = db.cursor()

class Main(object):

    def __init__(self, parent): 
        self.root = parent
        self.root.title("Panel logowania do aplikacji")
        self.frame = Tk.Frame(parent)
        self.frame.pack()    
        self.widgets()
     
    def login(self):
        db = sqlite3.connect('database.db')
        c = db.cursor()
        
        #self.username = Tk.StringVar() -> stare
        #self.password = Tk.StringVar() -> stare
        
        c.execute('SELECT * FROM user WHERE username = ? AND password = ?', (self.username.get(), self.password.get()))
        
        if c.fetchall():
            Invoice(self)
        else:
            showerror(title = "error", message = "Podano nieprawidłowy login albo hasło")
        c.close() 

    def hide(self): 
        self.root.withdraw()   

    def show(self):
        self.root.update()
        self.root.deiconify()

    def widgets(self): 

        Tk.Label(text = "Nazwa użytkownika:").pack()
        #Tk.Entry(self.frame, self.username).pack()
        self.username=Tk.Entry(self.frame, textvariable=Tk.StringVar()).pack()
        Tk.Label(text = "Hasło:").pack()
        #Tk.Entry(self.frame).pack()
        self.password=Tk.Entry(self.frame, textvariable=Tk.StringVar()).pack()
        Tk.Button(self.frame, text="Dalej", command=self.login).pack()


class Invoice(Tk.Toplevel):

    def __init__(self, original):
        self.original_frame = original
        Tk.Toplevel.__init__(self)
        self.geometry("400x300")
        self.title("Faktury")
        self.widgets()
    
    def widgets(self):
        btn = Tk.Button(self, text="Zamknij", command=self.onClose)
        btn.pack()
        profile = Tk.Button(self, text="Konto właściciela", command=self.Profile)
        profile.pack()
        product = Tk.Button(self, text="Produkty", command=self.Product)
        product.pack()   
        client = Tk.Button(self, text="Klienci", command=self.Client)
        client.pack()      
    
    def Profile(self):
        self.withdraw()
        Profile(self)

    def Client(self):
        self.withdraw()
        Client(self)

    def Product(self):
        self.withdraw()
        Product(self)
    
    def onClose(self):
        self.destroy()
   

class Client(Tk.Toplevel):

    def __init__(self, original):
        self.original_frame = original
        Tk.Toplevel.__init__(self)
        self.geometry("400x300")
        self.title("Klienci")
        self.widgets()

    def widgets(self):
        btn = Tk.Button(self, text="Cofnij", command=self.onClose)
        btn.pack()

    def onClose(self):
        self.destroy()
        Invoice(self)


class Product(Tk.Toplevel):

    def __init__(self, original):
        self.original_frame = original
        Tk.Toplevel.__init__(self)
        self.geometry("400x300")
        self.title("Produkty")
        self.widgets()

    def widgets(self):
        btn = Tk.Button(self, text="Cofnij", command=self.onClose)
        btn.pack()

    def onClose(self):
        self.destroy()
        Invoice(self)		
  

class Profile(Tk.Toplevel):

    def __init__(self, original):
        self.original_frame = original
        Tk.Toplevel.__init__(self)
        self.geometry("400x300")
        self.title("Profil właściciela")
        self.widgets()

    def widgets(self):
        btn = Tk.Button(self, text="Cofnij", command=self.onClose)
        btn.pack()

    def onClose(self):
        self.destroy()
        Invoice(self)

    
if __name__ == "__main__":
    root = Tk.Tk()
    root.geometry("400x200")
    app = Main(root)
    root.mainloop()


#http://www.blog.pythonlibrary.org/2012/07/26/tkinter-how-to-show-hide-a-window/
