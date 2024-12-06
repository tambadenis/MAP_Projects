# Importă biblioteca pyautogui pentru capturi de ecran automate
import pyautogui

# Importă tkinter pentru interfața grafică a utilizatorului (GUI)
import tkinter as tk

# Importă funcționalitatea pentru deschiderea ferestrelor de dialog
from tkinter import filedialog

# Importă biblioteca os pentru gestionarea căilor și operațiunilor pe fișiere
import os

# Importă biblioteca threading pentru a rula procese pe un fir de execuție separat
import threading

# Importă biblioteca time pentru a introduce pauze între capturile de ecran
import time

# Definim o clasă care va gestiona logica aplicației și elementele GUI
class ScreenshotManager:
    def __init__(self, root):
        """
        Constructorul clasei ScreenshotManager.
        Inițializează interfața grafică și variabilele necesare.
        """
        # Referința către fereastra principală a aplicației
        self.root = root
        
        # Setează titlul ferestrei
        self.root.title("Manager de Screenshots")
        
        # Variabilă pentru a urmări starea aplicației (dacă rulează sau nu)
        self.running = False

        # Adaugă un label pentru descrierea intervalului de timp
        tk.Label(root, text="Interval de timp (secunde):").pack(pady=5)
        
        # Creează o intrare pentru utilizator, unde se poate introduce intervalul
        self.interval_entry = tk.Entry(root)
        self.interval_entry.pack(pady=5)
        
        # Creează un buton pentru a deschide dialogul de alegere a folderului
        tk.Button(root, text="Alege Folder", command=self.choose_folder).pack(pady=5)
        
        # Creează un label care arată calea folderului ales
        self.folder_label = tk.Label(root, text="Folder nespecificat")
        self.folder_label.pack(pady=5)
        
        # Creează un buton pentru a începe capturile de ecran
        self.start_button = tk.Button(root, text="Start", command=self.start_screenshots)
        self.start_button.pack(pady=5)
        
        # Creează un buton pentru a opri capturile de ecran, inițial dezactivat
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_screenshots, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

    def choose_folder(self):
        """
        Funcție pentru alegerea folderului unde vor fi salvate capturile de ecran.
        Deschide un dialog de selecție a folderului.
        """
        # Deschide dialogul de selecție a folderului
        self.folder_path = filedialog.askdirectory()
        
        # Dacă un folder a fost ales, actualizează labelul pentru a arăta calea
        if self.folder_path:
            self.folder_label.config(text=f"Folder: {self.folder_path}")
        else:
            # Dacă nu a fost selectat niciun folder, afișează un mesaj implicit
            self.folder_label.config(text="Folder nespecificat")

    def start_screenshots(self):
        """
        Funcție pentru a începe capturile automate de ecran.
        Verifică dacă datele introduse de utilizator sunt valide.
        """
        try:
            # Încearcă să convertești intervalul introdus de utilizator într-un număr întreg
            self.interval = int(self.interval_entry.get())
            
            # Verifică dacă intervalul este mai mare decât zero
            if self.interval <= 0:
                raise ValueError
        except ValueError:
            # Afișează un mesaj de eroare dacă intervalul este invalid
            tk.messagebox.showerror("Eroare", "Introduceți un interval valid!")
            return

        # Verifică dacă a fost ales un folder
        if not hasattr(self, 'folder_path') or not self.folder_path:
            # Afișează un mesaj de eroare dacă folderul lipsește
            tk.messagebox.showerror("Eroare", "Alegeți un folder pentru salvare!")
            return

        # Setează aplicația ca fiind în stare de rulare
        self.running = True
        
        # Dezactivează butonul Start și activează butonul Stop
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Rulează funcția de capturi de ecran pe un fir separat
        threading.Thread(target=self.capture_screenshots).start()

    def stop_screenshots(self):
        """
        Funcție pentru a opri capturile automate de ecran.
        """
        # Oprește capturile de ecran
        self.running = False
        
        # Reactivare butonul Start și dezactivează butonul Stop
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def capture_screenshots(self):
        """
        Funcție care efectuează capturile de ecran și le salvează în folderul selectat.
        Rulează pe un fir de execuție separat.
        """
        # Contor pentru a număra capturile de ecran
        count = 1
        
        # Continuă să facă capturi de ecran cât timp aplicația este în stare de rulare
        while self.running:
            # Realizează o captură de ecran folosind pyautogui
            screenshot = pyautogui.screenshot()
            
            # Salvează captura de ecran în folderul selectat, cu un nume unic
            screenshot.save(os.path.join(self.folder_path, f"screenshot_{count}.png"))
            
            # Crește contorul pentru următoarea captură
            count += 1
            
            # Așteaptă intervalul specificat înainte de următoarea captură
            time.sleep(self.interval)

# Creează fereastra principală a aplicației
root = tk.Tk()

# Creează o instanță a clasei ScreenshotManager
app = ScreenshotManager(root)

# Rulează bucla principală a aplicației (pentru interacțiunea cu GUI-ul)
root.mainloop()