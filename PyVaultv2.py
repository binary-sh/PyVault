######## Import der benötigten Datenbanken und Dateien ########
import threading
import pyodbc
import easygui
import time
import csv
import tkinter as tk
from tkinter import Button
from tkinter import HORIZONTAL
from tkinter import ttk
from tkinter import messagebox
from tkinter import Frame
from PIL import Image
from PIL import ImageTk
from SQL import Logindata

################ Startseite ################  
class Startseite(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x400")
        self.title("PyVault")
        self.minsize(width = 800, height = 400)
        self.config(bg = "black")
        self.option_add("*Background", "black")
        self.option_add("*Foreground", "green")
        self.create_gui()
        
# Erstellung der GUI-Elemente   
    def create_gui(self):
# Menüleiste erstellen & Menü hinzufügen
        menuleiste = tk.Menu(self)
        datei_menu = tk.Menu(menuleiste, tearoff = 0)
        help_menu = tk.Menu(menuleiste, tearoff = 0)
        menuleiste.add_cascade(label = "Datei", menu = datei_menu)
        menuleiste.add_cascade(label = "Hilfe", menu = help_menu)
        self.config(menu = menuleiste, bg = "black")
        
# Menüpunkte erstellen und hinzufügen
        datei_menu.add_command(label = "Admin - Login", command = self.admin_login)
        datei_menu.add_separator()
        datei_menu.add_command(label = "Beenden", command = self.quit)
        help_menu.add_command(label = "Info", command = self.info_dialog)

# Pfad für das Logo
        path = "PyVault - Tkinter/Images/Logo_PyVault.png"
        self.image = Image.open(path)
        self.photo = ImageTk.PhotoImage(self.image)
        
# Erstellung der Labels
        self.Labelwelcome = tk.Label(self,
                                      text = "Willkommen beim PyVault!",
                                      image = self.photo,
                                      compound = "top",
                                      background = "black",
                                      foreground = "green",
                                      font = ("TkMenuFont", 18))
        
# Erstellung der Buttons
        self.Button_login = tk.Button(self,
                                       text = "Anmelden",
                                       command = self.zur_anmeldung,
                                       bg = "black",
                                       fg = "green")
        
        self.Button_register = tk.Button(self,
                                          text = "Registrieren",
                                          command = self.zur_registrierung,
                                          bg = "black",
                                          fg = "green")
        
# Platzierung der Elemente
        self.Labelwelcome.place(relx = 0.25, rely = 0.15, width = 400, height = 200)
        self.Button_login.place(relx = 0.235, rely = 0.75, width = 100, height = 50)
        self.Button_register.place(relx = 0.635, rely = 0.75, width = 100, height = 50)
        
    def zur_anmeldung(self):
        Anmeldefenster(self)
        
    def zur_registrierung(self):
        Registrierungsfenster(self)
        
    def admin_login(self):
        anmeldefenster_admin = Anmeldung_Admin(self)
        anmeldefenster_admin.mainloop()
         
# Messagebox erzeugen und einbinden
    def info_dialog(self):
        m_text = "************************\n" \
                 "Autoren:\n\n" \
                 "Michael Thies\n" \
                 "            &\n" \
                 "Masseo Winterstetter\n\n" \
                 "Date: 11.06.2023\n\n" \
                 "Version: 1.0.0\n" \
                 "************************"
        messagebox.showinfo(message = m_text, title = "Programminformationen")
        
################ Login - Admin ################
class Anmeldung_Admin(tk.Tk):
    def __init__(self, Startseite):
        super().__init__()
        self.geometry("400x200")
        self.title("PyVault - LogIn Administratorenbereich")
        self.minsize(width = 400, height = 200)
        self.resizable(width = False, height = False)
        self.config(bg = "black")
        self.option_add("*Background", "black")
        self.option_add("*Foreground", "green")
        self.startseite = Startseite
        self.anmeldung_erfolgt=False
        self.create_gui()
        
######## Erstellung der GUI ########
# Erstellung der GUI-Elemente        
    def create_gui(self):
 #Labels einfügen
        self.LabelUser = tk.Label(self,
                                  text = "Username:",
                                  background = "black",
                                  foreground = "green",
                                  font = ("TkMenuFont", 12))

        self.LabelPW = tk.Label(self,
                                text = "Password:",
                                background = "black",
                                foreground = "green",
                                font = ("TkMenuFont", 12))
# Entry-Felder einfügen    
        self.User_A = tk.StringVar()
        self.UsernameEingabe = tk.Entry(self,
                                        textvariable = self.User_A,
                                        bd = 1,
                                        width = 20)

        self.PWD_A = tk.StringVar()
        self.PasswordEingabe = tk.Entry(self,
                                        textvariable = self.PWD_A,
                                        bd = 1,
                                        width = 20)
        
# Buttons einfügen
        self.Button_login = Button(self,
                                   text = "LogIn",
                                   command = self.ALogin,
                                   bg = "black",
                                   fg = "green")
        
        self.Button_abort = Button(self,
                                   text = "Abbruch",
                                   command = self.destroy,
                                   bg = "black",
                                   fg = "green")

# Platzierung der Elemente
        self.LabelUser.place(relx = 0.25,rely = 0.05, width = 200, height = 50)
        self.UsernameEingabe.place(relx = 0.35, rely = 0.25)
        self.LabelPW.place(relx = 0.25, rely = 0.35, width = 200, height = 50)
        self.PasswordEingabe.place(relx = 0.35, rely = 0.55)
        self.Button_login.place(relx = 0.15, rely = 0.75, width = 100, height = 25)
        self.Button_abort.place(relx = 0.6, rely = 0.75, width = 100, height = 25)

######## Erstellung der Programmfunktionen ########
# Definition der Funktionen
    def ALogin(self):
        username = str(self.User_A.get())
        password = str(self.PWD_A.get())
        if username == "":
            if password == "":
                self.login_success()
            else:
                self.login_failure()
        else:
            self.user_not_found()
        
    def login_success(self):
        self.anmeldung_erfolgt=True
        if self.anmeldung_erfolgt:
            startseite.destroy()
            self.destroy()
            Adminbereich()
    
    def login_failure(self):
        Falsches_Passwort()

    def user_not_found(self):
        Unbekannter_Benutzer()

################ LogIn ################  
class Anmeldefenster(tk.Tk):
    def __init__(self, Startseite):
        super().__init__()
        self.geometry("400x200")
        self.title("PyVault - LogIn")
        self. minsize(width = 400, height = 200)
        self.resizable(width = False, height = False)
        self.config(bg = "black")
        self.option_add("*Background", "black")
        self.option_add("*Foreground", "green")
        self.startseite = Startseite
        self.anmeldung_erfolgt = False
        self.create_gui()
        
######## Erstellung der GUI ########
# Erstellung der GUI-Elemente  
    def create_gui(self):
# Labels einfügen
        self.LabelUser = tk.Label(self,
                                   text = "Benutzer:",
                                   background = "black",
                                   foreground = "green",
                                   font = ("TkMenuFont", 12))
        
        self.LabelPW = tk.Label(self,
                                 text = "Passwort:",
                                 background = "black",
                                 foreground = "green",
                                 font = ("TkMenuFont", 12))
        
# Entry - Felder einfügen
        self.User_V = tk.StringVar()
        self.UserE = tk.Entry(self,
                               bg = "black",
                               fg = "green",
                               textvariable = self.User_V,
                               bd = 1,
                               width = 20)
        
        self.Pwd_V = tk.StringVar()
        self.PwdE = tk.Entry(self,
                              bg = "black",
                              fg = "green",
                              textvariable = self.Pwd_V,
                              show = "*",
                              bd = 1,
                              width = 20)
        
# Buttons einfügen
        self.Button_login = tk.Button(self,
                                       text = "LogIn",
                                       command = self.BLogin,
                                       bg = "black",
                                       fg = "green")
        
        self.Button_abort = tk.Button(self,
                                       text = "Abbruch",
                                       command = self.destroy,
                                       bg = "black",
                                       fg = "green")
        
# Platzierung der Elemente
        self.LabelUser.place(relx = 0.25, rely = 0.05, width = 200, height = 50)
        self.UserE.place(relx = 0.35, rely = 0.25)
        self.LabelPW.place(relx = 0.25, rely = 0.35, width = 200, height = 50)
        self.PwdE.place(relx = 0.35, rely = 0.55)
        self.Button_login.place(relx = 0.15, rely = 0.75, width = 100, height = 25)
        self.Button_abort.place(relx = 0.6, rely = 0.75, width = 100, height = 25)

######## Erstellung der Programmfunktionen ########
# Definition der Funktionen
    def BLogin(self):
        username = str(self.User_V.get())
        password = str(self.Pwd_V.get())
        if username == "":
            if password == "":
                self.login_success()
            else:
                self.password_not_recognised()
        else:
            self.user_not_found()
            
    def login_success(self):
        self.anmeldung_erfolgt=True
        if self.anmeldung_erfolgt:
            startseite.destroy()
            self.destroy()
            connect_to_database()
            Hauptfenster()        
            
    def user_not_found(self):
        Unbekannter_Benutzer()
    
    def password_not_recognised(self):
        Falsches_Passwort()

################ Unbekanntes Passwort ################
class Falsches_Passwort(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("200x100")
        self.title("Falsches Passwort")
        self.resizable(width = False, height = False)
        self.configure(bg = "black")
        
        self.LabelPW = tk.Label(self,
                         text = "Passwort ist nicht korrekt!",
                         bg = "black",
                         fg = "green")
        
        self.ButtonPW = Button(self,
                        text = "Close",
                        command = self.Close,
                        bg = "black",
                        fg = "green")
        
# Platzierung der Elemente
        self.LabelPW.place(x = 25, y = 15, width = 150, height = 50)
        self.ButtonPW.place(x = 75, y = 75, width = 50, height = 20)
        
    def Close(self):
        self.destroy()

################ Unbekannter Benutzer ################   
class Unbekannter_Benutzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("200x100")
        self.title("Benutzer unbekannt")
        self.resizable(width = False, height = False)
        self.configure(bg = "black")
        self.LabelUser = tk.Label(self,
                                text = "Benutzer existiert nicht!",
                                bg = "black",
                                fg = "green")
        
        self.ButtonUser = Button(self,
                               text = "OK",
                               command = self.Close,
                               bg = "black",
                               fg = "green")
        
# Platzierung der Elemente
        self.LabelUser.place(x = 25, y = 15, width = 150, height = 50)
        self.ButtonUser.place(x = 75, y = 75, width = 50, height = 20)
        
    def Close(self):
        self.destroy()
            
################ Registry ################  
class Registrierungsfenster(tk.Tk):
    def __init__(self, Startseite):
        super().__init__()
        self.geometry("400x200")
        self.title("Registrieren")
        self.resizable(width = False, height = False)
        self.config(bg = "black")
        self.Startseite = Startseite
        
# Erstellung der GUI-Elemente
        self.create_gui()
        
    def create_gui(self):
# Erstellung der Labels
        self.LabelR = tk.Label(self,
                               text = " Um ein Benutzerkonto anzulegen wenden\n"
                                      "Sie sich an Ihrem Systemadministrator!",
                               bg = "black",
                               fg = "green",
                               font = ("TkMenuFont", 12))
        
# Erstellung des Button
        self.CloseR = tk.Button(self,
                                 text = "Close",
                                 command = self.close,
                                 bg = "black",
                                 fg = "green")
        
# Platzierung der Elemente
        self.LabelR.place(x = 50, y = 25, width = 300, height = 100)
        self.CloseR.place(x = 150, y = 150, width = 100, height = 25)
        
    def close(self):
        self.destroy()

################ Ladenbalken ################
def connect_to_database():
    class DatabaseConnector(tk.Tk):
        def __init__(self):
            super().__init__()
            self.geometry("400x200")
            self.title("Verbindung zum SQL-Server")
            self.resizable(width = False, height = False)
            self.config(bg = "black")
            self.protocol("WM_DELETE_WINDOW", self.on_close)  # Hinzufügen eines Protokolls, um das Hauptfenster zu schließen

# Definition der Variablen
            self.text_variable_C = tk.StringVar()
            self.text_variable_P = tk.StringVar()
            self.text_variable_C.set("Verbindung wird aufgebaut...")           

# Auslesen der Dateien zur Verbindung mit dem Server
            self.server = Logindata.Server[0]
            self.database = Logindata.Database[0]
            self.user = Logindata.User[0]
            self.pw = Logindata.Passwort[0]

# Erstellung der GUI-Elemente
            self.create_gui()

# Erstellung der Label
        def create_gui(self):
            self.label_connect = tk.Label(self,
                                          textvariable = self.text_variable_C,
                                          bg = "black",
                                          fg = "green",
                                          font = ("TkMenuFont", 12))

            self.progress_bar = ttk.Progressbar(self,
                                                orient = HORIZONTAL,
                                                length = 300,
                                                mode = 'indeterminate')

            self.label_progress = tk.Label(self,
                                           textvariable = self.text_variable_P,
                                           bg = "black",
                                           fg = "green",
                                           font = ("TkMenuFont", 10))

            self.button_close = Button(self,
                                       text = "Close",
                                       command = self.destroy,
                                       bg = "black",
                                       fg = "green")

# Platzierung der Elemente
            self.label_connect.place(x = 90, y = 50, width = 220, height = 20)
            self.progress_bar.place(x = 50, y = 75, width = 300, height = 15)
            self.label_progress.place(x = 100, y = 100, width = 200, height = 40)
            self.button_close.place(x = 162.5, y = 150, width = 75, height = 25)

# Verbindung zur Datenbank
## Auslesen der Dateien zur Verbindung mit dem Server
        def start(self):
            self.progress_bar.start(10)
            threading.Thread(target = self.connection).start()

        def connection(self):
            time.sleep(1)
            cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';ENCRYPT=yes;TrustServerCertificate=yes;UID=' + self.user + ';PWD=' + self.pw)
            cursor = cnxn.cursor()
## Überprüfen, ob die Verbindung erfolgreich war
            if not cnxn:
                print("Verbindung zur Datenbank konnte nicht hergestellt werden.")
                self.text_variable_C.set("Verbindungsaufbau fehlgeschlagen!")
            else:
                print("Verbindung zur Datenbank hergestellt.")
                self.text_variable_P.set(("Verbunden mit ") + self.database)
                self.text_variable_C.set("Verbindungsaufbau erfolgreich!")
                time.sleep(1)
                self.on_close()
                
        def on_close(self):
            self.progress_bar.stop()
            self.destroy()

# Erzeugung der Anwendung und Start
    app = DatabaseConnector()
    app.start()
    app.mainloop()

################ Abminbereich von PyVault ################
class Adminbereich(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyVault - Adminbereich")
        self.geometry("800x400")
        self.minsize(width = 800, height = 400)
        self.config(bg = "black")
        self.option_add("*Background", "black")
        self.option_add("*Foreground", "green")
        self.create_gui()

######## Erstellen der GUI ########
    def create_gui(self):
# Menüleiste erstellen & Menü hinzufügen
        menuleiste = tk.Menu(self)
        datei_menu = tk.Menu(menuleiste, tearoff = 0)
        help_menu = tk.Menu(menuleiste, tearoff = 0)
        menuleiste.add_cascade(label = "Datei", menu = datei_menu)
        menuleiste.add_cascade(label = "Help", menu = help_menu)
        self.config(menu = menuleiste, bg = "black")

# Menüpunkte erstellen und hinzufügen
        datei_menu.add_command(label = "Abmelden", command = self.logOut)
        datei_menu.add_separator() # Trennlinie im Drop-down-Menü
        datei_menu.add_command(label = "Quit", command = self.quit)
        help_menu.add_cascade(label = "Info", command = self.info_dialog)
        
# Pfad für das Logo
        path = "PyVault - Tkinter/Images/Logo_PyVault.png"
        self.image = Image.open(path).resize((100,40))
        self.photo = ImageTk.PhotoImage(self.image)
        
# Labels & Entry - Felder einfügen
        self.LabelHead = tk.Label(self,
                                  text = "   PyVault - Adminbereich",
                                  image = self.photo,
                                  compound = "left",
                                  bg = "black",
                                  fg = "green",
                                  font = ("TkMenuFont", 11))
        
        self.Bau = tk.Label(self,
                            text = "Diese Seite befindet sich noch im Bau! \n\
                            Sobald diese Seite fertiggestellt ist können \n\
                            Sie hier Ihre Nutzer verwalten.",
                            bg = "black",
                            fg = "green",
                            font = ("TkMenuFont", 14))
        
# Platzierung der Elemente
        self.LabelHead.place(relx = 0, rely = 0, width = 300, height = 50)
        self.Bau.place(x = 0, y = 150, width = 500, height = 100)
        
# Definition der Funktionen
    def info_dialog(self):
        Startseite.info_dialog(self) # type: ignore
    
    def logOut(self):
        self.destroy()
        Startseite()

################ Hauptfenster des Programms ################  
class Hauptfenster(tk.Tk):
# Initialisierung der globalen Variablen
    def __init__(self):
        super().__init__()
        self.geometry("1400x600")
        self.title("PyVault")
        self.minsize(width = 1200, height = 600)
        self.resizable(width = False, height = False)
        self.config(bg = "black")
        self.option_add("*Background", "black")
        self.option_add("*Foreground", "green")
        self.create_gui()
        
# Anpassen der TTK-Widgets
        style = ttk.Style()
        style.configure('Custom.TCombobox', fieldbackground = 'black', background = 'black', foreground = 'green')

######## Erstellen der GUI ########
    def create_gui(self):
# Menüleiste erstellen & Menü hinzufügen
        menuleiste = tk.Menu(self)
        datei_menu = tk.Menu(menuleiste, tearoff = 0)
        help_menu = tk.Menu(menuleiste, tearoff = 0)
        menuleiste.add_cascade(label = "Datei", menu = datei_menu)
        menuleiste.add_cascade(label = "Help", menu = help_menu)
        self.config(menu = menuleiste, bg = "black")

# Menüpunkte erstellen und hinzufügen
        datei_menu.add_command(label = "Admin - Login", command = self.admin_login)
        datei_menu.add_separator()
        datei_menu.add_command(label = "LogOut", command = self.logOut)
        datei_menu.add_separator()
        datei_menu.add_command(label = "Quit", command = self.quit)

        help_menu.add_command(label = "Info", command = self.info_dialog)
        help_menu.add_separator()
        help_menu.add_command(label = "Anleitung")
        
# Pfad für das Logo
      # Pfad für das Logo
        path = "PyVault - Tkinter/Images/Logo_PyVault.png"
        image = Image.open(path).resize((100,40))
        try:
            photo = ImageTk.PhotoImage(image)
        except tk.TclError:
            photo = None
        
# Ertsellung des Frames für das Logo
        Frame_logo = Frame(master = self, bg = "black")

# Erstellung der Label
        self.LabelHead = tk.Label(Frame_logo,
                                text = "PyVault",
                                image = photo, # type: ignore
                                compound = "left",
                                bg = "black",
                                fg = "green",
                                font = ("TkMenuFont", 16))

        self.LabelTabelle = tk.Label(self,
                                   text = "Tabelle anzeigen:",
                                   bg = "black",
                                   fg = "green",
                                   font = ("TkMenuFont", 11))

        self.LabelFilter = tk.Label(self,
                                  text = "Filter:",
                                  bg = "black",
                                  fg = "green",
                                  font = ("TkMenuFont", 11))

        self.Labellöschen = tk.Label(self,
                                   text = "Löschen:",
                                   bg = "black",
                                   fg = "green",
                                   font = ("TkMenuFont", 11))

# Erstellung der Button
        self.AnzeigeDatensatz = tk.Button(self,
                                        text = "Anzeigen",
                                        command = self.handle_table_selection,
                                        font = ("TkMenuFont", 11))

        self.CSV_einlesen = tk.Button(self,
                                    text = "CSV-Datei importieren",
                                    command = self.csv_import, # type: ignore
                                    font = ("TkMenuFont", 11))

        self.Datensatzhinzufuegen = tk.Button(self,
                                            text = "Datensatz hinzufügen",
                                            command = self.Dhinzufuegen,
                                            font = ("TkMenuFont", 11))

        self.Datensatzlöschen = tk.Button(self,
                                        text = "Datensatz löschen",
                                        command = self.delete_record,
                                        font = ("TkMenuFont", 11))

        self.DatensatzFiltern = tk.Button(self,
                                        text = "Filtern",
                                        command = self.apply_filter, # type: ignore
                                        font = ("TkMenuFont", 11))

        self.CloseButton = tk.Button(self,
                                   text = "Beenden",
                                   command = self.End,
                                   font = ("TkMenuFont", 11))

        self.Datensatz_aendern = tk.Button(self,
                                           text = "Datensatz ändern",
                                           command = self.Daktualisieren,
                                           font = ("TkMenuFont", 11))

# Erstellen der Auswahlfelder
        self.DropdownT = ttk.Combobox(self,
                                    style = 'Custom.TCombobox')
        self.DropdownT['values'] = ('Geraete', 'Hardware', 'MAC_Adressen', 'Peripheriegeraete', 'Geraeteperipherie', 'Installierte_Software', 'Software')
        self.DropdownT.current(0)
        self.DropdownT.bind("<<ComboboxSelected>>", self.handle_table_selection)

        self.DropdownF = ttk.Combobox(self,
                                    style = 'Custom.TCombobox')

        self.DropdownD = ttk.Combobox(self,
                                    state = "readonly")
                        
# Erstellung des Ausgabe-Felds
        self.ausgabe = tk.Text(self,
                             bg = "black")

# Platzierung der Elemente
        Frame_logo.place(x=0, y=15, width=350, height=70)
        self.LabelHead.place(x = 0, y = 15, width = 300, height = 50)
        self.AnzeigeDatensatz.place(x = 870, y = 250, width = 100, height = 30)
        self.ausgabe.place(x = 50, y = 100, width = 800, height = 460)
        self.CSV_einlesen.place(x = 1000, y = 250, width = 175, height = 30)
        self.Datensatzhinzufuegen.place(x = 1205, y = 250, width = 175, height = 30)
        self.Datensatzlöschen.place(x = 870, y = 300, width = 175, height = 30)
        self.DatensatzFiltern.place(x = 1075, y = 300, width = 100, height = 30)
        self.Datensatz_aendern.place(x = 870, y = 350, width = 175, height = 30)
        self.CloseButton.place(x = 1250, y = 525, width = 100, height = 30)
        self.LabelTabelle.place(x = 870, y = 100, width = 150, height = 20)
        self.DropdownT.place(x = 870, y = 130, width = 150, height = 30)
        self.LabelFilter.place(x = 1050, y = 100, width = 150, height = 20)
        self.DropdownF.place(x = 1050, y = 130, width = 150, height = 30)
        self.Labellöschen.place(x = 1225, y = 100, width = 150, height = 20)
        self.DropdownD.place(x = 1225, y = 130, width = 150, height = 30)


######## Verbindung der Datenbank ########
# Auslesen der Dateien zur Verbindung mit dem Server
        server = Logindata.Server[0]
        database = Logindata.Database[0]
        user = Logindata.User[0]
        pw = Logindata.Passwort[0]

# Verbindung zur Datenbank aufbauen
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;TrustServerCertificate=yes;UID='+user+';PWD='+ pw)
        self.cursor = self.cnxn.cursor()
        self.connection_string = self.cnxn
        
######## Erstellen der Programmfunktionen ########
# Definition der Funktionen der Menüleiste
    def logOut(self):
        self.destroy()
        Startseite()
        
## Definition des Buttons zum Beenden der Anwendung
    def End(self):
        self.cnxn.close()
        self.destroy()
       
## Hier kommt die Verbindung zum Admin-LogIn hin
    def admin_login(self):
        Anmeldung_Admin(Startseite)
         
## Messagebox erzeugen und einbinden
    def info_dialog(self):
        Startseite.info_dialog(self) #type: ignore
        
# Definition der Button-Funktionen
    def csv_import(self):
# Importieren der CSV-Datei
        fileupload = easygui.fileopenbox(title='Wähle die .CSV Datei aus.', default='*', filetypes=["*.csv"])
    
        with open(fileupload, 'r') as csvfile: # type: ignore
            reader = csv.DictReader(csvfile)
# Spaltennamen der CSV-Datei abrufen
            columns = reader.fieldnames
# Durchsuchen aller Tabellen in der Datenbank nach den passenden Spalten und Einfügen der Daten
            tables = self.get_all_tables(self.cursor)
            for table in tables:
                missing_columns = set(columns) - set(self.get_table_columns(self.cursor, table)) # type: ignore
                
                if missing_columns:
                    print(f"Fehlende Spalten in Tabelle '{table}': {', '.join(missing_columns)}")
                    continue
# Einfügen der Daten in die aktuelle Tabelle
                for row in reader:
                    self.insert_data(self.cursor, table, row) 
                    
            self.cnxn.commit()
            self.cnxn.close()
            
# Funktion, um alle Tabellen in der Datenbank abzurufen
    def get_all_tables(self, cursor):
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
        tables = cursor.fetchall()
        return [table[0] for table in tables]
        git 
# Funktion, um die Spalten einer bestimmten Tabelle abzurufen
    def get_table_columns(self, cursor, table):
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table}'")
        columns = cursor.fetchall()
        return [column[0] for column in columns]
        
# Funktion, um die Daten in eine bestimmte Tabelle einzufügen
    def insert_data(self, cursor, table, row):
        query = f"INSERT INTO {table} (GeraeteID, Bezeichnung, Modell, Typ) VALUES (?,?,?,?)"
        cursor.execute(query, row['GeraeteID'], row['Bezeichnung'], row['Modell'], row['Typ'])

# Definition der Suchfunktion     
    def search_records(self):
        search_table = input("Bitte geben Sie den Namen der Tabelle ein: ")
        search_column = input("Bitte geben Sie den Namen der Spalte ein (optional): ")
        search_value = input("Bitte geben Sie den Suchwert ein (optional): ")
        
        self.db_search.search_records(search_table, search_column, search_value)
        
        hauptfenster = Hauptfenster()
        hauptfenster.search_records()
        
## Definition der Funktion zum manuellen einfügen neuer Datensätze
    def Dhinzufuegen(self):
        Entry_Datensatz() # type: ignore
        
## Definition der Funktion zum ändern bestehender Datensätze
    def Daktualisieren(self):
        Change_Datensatz() # type: ignore
    
###### Erstellung der Funktionen zur Nutzung der Datenbank ######
# Funktion zum Handhaben der Tabellenauswahl
    def handle_table_selection(self, *args):
        selected_table = self.DropdownT.get()
        self.update_record_dropdown(selected_table)  # Aktualisiere Dropdown-Menü für Datensätze
        self.execute_query(selected_table)  # Führe die Abfrage für die ausgewählte Tabelle aus
    
# Funktion zum Ausführen der Abfrage basierend auf der ausgewählten Tabelle
    def execute_query(self, selected_table):
        query = f"SELECT * FROM {selected_table}"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
# Formatierung der Ergebnisse in tabellarischer Form
        columns = [column[0] for column in self.cursor.description]
        ausgabe = "\t".join(columns) + "\n"
        ausgabe += "\n".join([("\t".join(map(str, row))) for row in results])
        
        self.ausgabe.delete('1.0', tk.END)  # Textfeld leeren
        self.ausgabe.insert(tk.END, ausgabe)  # Ergebnisse im Textfeld anzeigen        
    
# Funktion zum Aktualisieren des Datensatz-Dropdown-Menüs basierend auf der ausgewählten Tabelle
    def update_record_dropdown(self, selected_table):
        if selected_table == "Geraete":
            query_u = "SELECT GeraeteID FROM Geraete"
        elif selected_table == "Hardware":
            query_u = "SELECT HaID FROM Hardware"
        elif selected_table == "MAC_Adressen":
            query_u = "SELECT SNr FROM [MAC_Adressen]"
        elif selected_table == "Peripheriegeraete":
            query_u = "SELECT PID FROM Peripheriegeraete"
        elif selected_table == "Geraeteperipherie":
            query_u = "SELECT GeraeteID FROM Geraeteperipherie"
        elif selected_table == "Installierte_Software":
            query_u = "SELECT GeraeteID FROM Installierte_Software"
        elif selected_table == "Software":
            query_u = "SELECT Herausgeber FROM Software"
        
        query = query_u #type: ignore
        self.cursor.execute(query)
        records = [str(record[0]) for record in self.cursor.fetchall()]
        self.DropdownD['values'] = records

#### Definition zur Filterung der Ergebnisse ####
# Funktion zum Handhaben der Filterauswahl
    def apply_filter(self):
        selected_table = self.DropdownT.get()
        selected_filter = self.DropdownF.get()

        query = ""
        filter_values = ()
    
        if selected_table == "Geraete":
            query = "SELECT * FROM Geraete WHERE Bezeichnung = ? OR GeraeteID = ?"
            filter_values = (selected_filter, selected_filter)
        elif selected_table == "Hardware":
            query = "SELECT * FROM Hardware WHERE Modell = ? OR Hersteller = ?"
            filter_values = (selected_filter, selected_filter)
        elif selected_table == "MAC_Adressen":
            query = "SELECT * FROM MAC_Adressen WHERE LAN = ? OR WLAN = ? OR Bluetooth = ?"
            filter_values = (selected_filter, selected_filter, selected_filter)
        elif selected_table == "Peripheriegeraete":
            query = "SELECT * FROM Peripheriegeraete WHERE Bezeichnung = ? OR Modell = ? OR Typ = ?"
            filter_values = (selected_filter, selected_filter, selected_filter)
        elif selected_table == "Geraeteperipherie":
            query = "SELECT * FROM Geraeteperipherie WHERE GeraeteID = ? OR PID = ?"
            filter_values = (selected_filter, selected_filter)
        elif selected_table == "Installierte_Software":
            query = "SELECT * FROM Installierte_Software WHERE GeraeteID = ? OR SoID = ?"
            filter_values = (selected_filter, selected_filter)
        elif selected_table == "Software":
            query = "SELECT * FROM Software WHERE Herausgeber = ? OR Bezeichnung = ? OR Version = ?"
            filter_values = (selected_filter, selected_filter, selected_filter)

        self.cursor.execute(query, filter_values)
        results = self.cursor.fetchall()

# Formatierung der Ergebnisse in tabellarischer Form
        columns = [column[0] for column in self.cursor.description]
        ausgabe = "\t".join(columns) + "\n"
        ausgabe += "\n".join([("\t".join(map(str, row))) for row in results])

        self.ausgabe.delete('1.0', tk.END) # Textfeld leeren
        self.ausgabe.insert(tk.END, ausgabe) # Ergebnisse im Textfeld anzeigen

    
# Funktion zum Löschen eines Datensatzes
    def delete_record(self):
        selected_table = self.DropdownT.get()
        selected_record = self.DropdownD.get()
        query = ""
        if not selected_record:
            return
        
        if selected_table == "Geraete":
            query = "DELETE FROM Geraete WHERE GeraeteID = ?"
        elif selected_table == "Hardware":
            query = "DELETE FROM Hardware WHERE HaID = ?"
        elif selected_table == "MAC_Adressen":
            query = "DELETE FROM [MAC_Adressen] WHERE SNr = ?"
        elif selected_table == "Peripheriegeraete":
            query = "DELETE FROM Peripheriegeraete WHERE PID = ?"
        elif selected_table == "Geraeteperipherie":
            query = "DELETE FROM Geraeteperipherie WHERE GeraeteID = ?"
        elif selected_table == "Installierte_Software":
            query = "DELETE FROM Installierte_Software WHERE GeraeteID = ?"
        elif selected_table == "Software":
            query = "DELETE FROM Software WHERE Herausgeber = ?"
        self.cursor.execute(query, selected_record)
        self.cnxn.commit()
        
# Aktualisiere die Ergebnisse nach dem Löschen des Datensatzes
        self.execute_query(selected_table)
        
# Instanz der PyVaultDBSearch-Klasse erstellen
        self.db_search = PyVaultDBSearch(self.connection_string)
        self.entry_datensatz = Entry_Datensatz(self.connection_string)
        self.change_datensatz = Change_Datensatz(self.connection_string)
        
# Erzeugung der Hauptanwendung und Start
        self.mainloop()

################ Datensatz hinzufügen - Frame ################ 
class Entry_Datensatz(tk.Tk):
    def __init__(self, connection_string):
        super().__init__()
        self.connection_string = connection_string
        self.title("Datensatz")
        self.geometry("800x400")
        self.resizable(width=False, height=False)
        self.configure(bg="black")
        self.option_add("*Background", "black")
        self.option_add("*Foreground", "green")
        
        # Anpassen der TTK-Widgets 
        style = ttk.Style()
        style.configure('Custom.TCombobox', fieldbackground='black', background='black', foreground='green')
        
        # Auswahlfeld für die Tabellen & die GUI generieren
        self.PyVault = tk.Label(self,
                                text="PyVault - Datensatz einfügen",
                                bg="black",
                                fg="green",
                                font=("TkMenuFond", 14))
        self.PyVault.place(x=10, y=10, width=300, height=30)
        
        self.label = tk.Label(self,
                              text="Auswahlmenü",
                              bg="black",
                              fg="green",
                              font=("TkMenuFont", 12))
        self.label.place(x=50, y=60, width=150, height=30)
        
        self.options = ['Geraete', 'Hardware', 'MAC_Adressen', 'Peripheriegeraete', 'Software']
        self.selected_option = tk.StringVar()
        self.dropdown = tk.OptionMenu(self,
                                      self.selected_option,
                                      *self.options,
                                      command=self.create_entry_fields)
        self.dropdown.place(x=250, y=60, width=150, height=30)
        
    def create_entry_fields(self, selected_table):
        self.clear_entry_fields()
        
        self.PyVault = tk.Label(self,
                                text="PyVault - Datensatz einfügen",
                                bg="black",
                                fg="green",
                                font=("TkMenuFond", 14))
        self.PyVault.place(x=10, y=10, width=300, height=30)
        
        self.label = tk.Label(self,
                              text="Auswahlmenü",
                              bg="black",
                              fg="green",
                              font=("TkMenuFont", 12))
        self.label.place(x=50, y=60, width=150, height=30)
        
        # Verbindung zur Datenbank herstellen
        with pyodbc.connect(self.connection_string) as connection:
            cursor = connection.cursor()
            
            # Spaltennamen abrufen
            cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{selected_table}'")
            columns = [column[0] for column in cursor.fetchall()]
            
            # Entry-Felder für die Spalten erzeugen
            self.entry_fields = []
            label_y = 0.32
            entry_y = 0.32
            label_spacing = 0.08  # Vertikaler Abstand zwischen den Labels
            
            for column in columns:
                label = tk.Label(self,
                                 text=column,
                                 bg="black",
                                 fg="green",
                                 font=("TkMenuFont", 12))
                label.place(relx=0.1, rely=label_y, height=20, anchor=tk.W)
                label_y += label_spacing
                
                entry = tk.Entry(self,
                                 font=("TkMenuFont", 11))
                entry.place(relx=0.5, rely=entry_y, width=400, height=20, anchor=tk.CENTER)
                entry_y += label_spacing
                
                self.entry_fields.append((column, entry))
            
            save_button = tk.Button(self,
                                    text="Speichern",
                                    command=self.save_data)
            save_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        
    def save_data(self):
        # Verbindung zur Datenbank herstellen
        with pyodbc.connect(self.connection_string) as connection:
            cursor = connection.cursor()
            
            # Daten in die entsprechende Tabelle speichern
            for column, entry in self.entry_fields:
                value = entry.get()
                
                # Anpassen des SQL-Insert-Statements basierend auf der Tabellenstruktur
                sql = f"INSERT INTO {self.selected_option.get()} ({column}) VALUES (?)"
                cursor.execute(sql, value)
            
            connection.commit()
        
    def clear_entry_fields(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.destroy()

################ Datensatz verändern - Frame ################ 
class Change_Datensatz(tk.Tk):
    def __init__(self, connection_string):
        super().__init__()
        self.connection_string = connection_string
        self.title("Datensatz")
        self.geometry("800x400")
        self.resizable(width=False, height=False)
        self.configure(bg="black")
        self.option_add("*Background", "black")
        self.option_add("*Foreground", "green")

# Anpassen der TTK-Widgets
        style = ttk.Style()
        style.configure('Custom.TCombobox', fieldbackground='black', background='black', foreground='green')

# Auswahlfeld für die Tabellen & die GUI generieren
        self.PyVault = tk.Label(self,
                                text="PyVault - Datensatz aktualisieren",
                                bg="black",
                                fg="green",
                                font=("TkMenuFond", 14))
        self.PyVault.place(x=10, y=10, width=300, height=30)

        self.label = tk.Label(self,
                              text="Auswahlmenü",
                              bg="black",
                              fg="green",
                              font=("TkMenuFont", 12))
        self.label.place(x=50, y=60, width=150, height=30)

        self.options = ['Geraete', 'Hardware', 'MAC_Adressen', 'Peripheriegeraete', 'Software']
        self.selected_option = tk.StringVar()
        self.dropdown = tk.OptionMenu(self,
                                      self.selected_option,
                                      *self.options,
                                      command=self.create_entry_fields)
        self.dropdown.place(x=210, y=60, width=150, height=30)

        self.record_selection_label = tk.Label(self,
                                               text="Datensatz auswählen",
                                               bg="black",
                                               fg="green",
                                               font=("TkMenuFont", 12))
        self.record_selection_label.place(x=400, y=75, width=150, height=30, anchor=tk.W)

        self.record_selection = tk.StringVar()
        self.record_dropdown = tk.OptionMenu(self,
                                             self.record_selection,'')
        self.record_dropdown.place(x=600, y=75, width=150, height=30, anchor=tk.W)

        self.record_selection.trace('w', self.load_selected_record)

    def create_entry_fields(self, selected_table):
        self.clear_entry_fields()

        self.PyVault = tk.Label(self,
                                text="PyVault - Datensatz aktualisieren",
                                bg="black",
                                fg="green",
                                font=("TkMenuFond", 14))
        self.PyVault.place(x=10, y=10, width=300, height=30)

        self.label = tk.Label(self,
                              text="Auswahlmenü",
                              bg="black",
                              fg="green",
                              font=("TkMenuFont", 12))
        self.label.place(x=50, y=60, width=150, height=30)

        self.record_selection_label = tk.Label(self,
                                               text="Datensatz auswählen",
                                               bg="black",
                                               fg="green",
                                               font=("TkMenuFont", 12))
        self.record_selection_label.place(x=400, y=75, width=150, height=30, anchor=tk.W)

# Verbindung zur Datenbank herstellen
        with pyodbc.connect(self.connection_string) as connection:
            cursor = connection.cursor()

# Spaltennamen abrufen
            cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{selected_table}'")
            columns = [column[0] for column in cursor.fetchall()]

# Entry-Felder für die Spalten erzeugen
            self.entry_fields = []
            label_y = 0.32
            entry_y = 0.32
            label_spacing = 0.08  # Vertikaler Abstand zwischen den Labels

            for column in columns:
                label = tk.Label(self,
                                 text=column,
                                 bg="black",
                                 fg="green",
                                 font=("TkMenuFont", 12))
                label.place(relx=0.1, rely=label_y, height=20, anchor=tk.W)
                label_y += label_spacing

                entry = tk.Entry(self,
                                 font=("TkMenuFont", 11))
                entry.place(relx=0.5, rely=entry_y, width=400, height=20, anchor=tk.CENTER)
                entry_y += label_spacing

                self.entry_fields.append((column, entry))

            save_button = tk.Button(self,
                                    text="Speichern",
                                    command=self.save_data)
            save_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

            self.populate_record_dropdown(cursor, selected_table)

    def populate_record_dropdown(self, cursor, selected_table):
# Datensätze abrufen
        cursor.execute(f"SELECT * FROM {selected_table}")
        records = cursor.fetchall()

# Dropdown-Menü für Datensätze aktualisieren
        self.record_dropdown['menu'].delete(0, 'end')
        self.record_selection.set('')  # Auswahl zurücksetzen

        for record in records:
            record_text = ', '.join(str(value) for value in record)
            self.record_dropdown['menu'].add_command(
                label=record_text,
                command=tk._setit(self.record_selection, record_text)
            )

    def load_selected_record(self, *args):
        selected_record = self.record_selection.get()
        if selected_record:
            values = selected_record.split(', ')
            for entry_field, value in zip(self.entry_fields, values):
                _, entry = entry_field
                entry.delete(0, 'end')
                entry.insert('end', value)

    def save_data(self):
# Verbindung zur Datenbank herstellen
        with pyodbc.connect(self.connection_string) as connection:
            cursor = connection.cursor()

            # Daten in die entsprechende Tabelle speichern
            for column, entry in self.entry_fields:
                value = entry.get()

                # Anpassen des SQL-Update-Statements basierend auf der Tabellenstruktur
                sql = f"UPDATE {self.selected_option.get()} SET {column}=?"
                cursor.execute(sql, value)

            connection.commit()

    def clear_entry_fields(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Entry) or isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.destroy()
                
################ Suchfunktion ################
class PyVaultDBSearch:
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    def search_records(self, search_table, search_column=None, search_value=None):
        query = f"SELECT * FROM {search_table}"
        
        if search_column and search_value:
            query += f" WHERE {search_column} = ?"
        
        try:
            with pyodbc.connect(self.connection_string) as connection:
                cursor = connection.cursor()
                
                if search_column and search_value:
                    cursor.execute(query, search_value)
                else:
                    cursor.execute(query)
                
                records = cursor.fetchall()
                
                if len(records) == 0:
                    print("Keine Datensätze gefunden.")
                else:
                    for record in records:
                        print(record)
        except pyodbc.Error as e:
            print(f"Fehler bei der Verbindung zur Datenbank: {str(e)}")


if __name__ == "__main__":
    startseite=Startseite()
    startseite.mainloop()
