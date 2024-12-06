# Importă biblioteca pyautogui pentru automatizarea interacțiunii cu mouse-ul și tastatura
import pyautogui

# Importă tkinter pentru a crea interfața grafică (GUI)
import tkinter as tk

# Importă threading pentru rularea proceselor pe un fir separat
import threading

# Importă biblioteca time pentru a introduce pauze între clicuri
import time

# Importă messagebox din tkinter pentru afișarea mesajelor pop-up
from tkinter import messagebox

# Definim clasa AutoClicker care gestionează logica aplicației și GUI-ul
class AutoClicker:
    def __init__(self, root):
        """
        Constructorul clasei AutoClicker.
        Inițializează fereastra principală, variabilele și elementele GUI.
        """
        # Referința către fereastra principală a aplicației
        self.root = root
        
        # Setează titlul ferestrei
        self.root.title("Clicker Automat")
        
        # Variabilă pentru a urmări starea aplicației (dacă rulează sau nu)
        self.running = False
        
        # Variabilă pentru a stoca poziția unde vor fi executate clicurile
        self.click_position = None

        # Adaugă un label pentru descrierea frecvenței clicurilor
        tk.Label(root, text="Frecvență Click-uri (secunde):").pack(pady=5)
        
        # Creează o intrare pentru utilizator unde poate introduce frecvența clicurilor
        self.frequency_entry = tk.Entry(root)
        self.frequency_entry.pack(pady=5)

        # Creează un buton pentru a seta poziția mouse-ului unde vor avea loc clicurile
        self.set_position_button = tk.Button(root, text="Setează Poziția", command=self.set_position)
        self.set_position_button.pack(pady=5)
        
        # Creează un label care afișează poziția setată de utilizator
        self.position_label = tk.Label(root, text="Poziție nespecificată")
        self.position_label.pack(pady=5)

        # Creează un buton pentru a începe executarea clicurilor automate
        self.start_button = tk.Button(root, text="Start", command=self.start_clicking)
        self.start_button.pack(pady=5)
        
        # Creează un buton pentru a opri clicurile automate, inițial dezactivat
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_clicking, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

    def set_position(self):
        """
        Funcție pentru a seta poziția unde vor avea loc clicurile automate.
        """
        # Ascunde temporar fereastra principală pentru a nu obstrucționa utilizatorul
        self.root.withdraw()
        
        # Afișează un mesaj informativ utilizatorului
        messagebox.showinfo("Setare Poziție", "Mutați mouse-ul pe poziția dorită și apăsați ENTER.")
        
        # Așteaptă 2 secunde pentru ca utilizatorul să mute mouse-ul
        time.sleep(2)
        
        # Salvează poziția curentă a mouse-ului
        self.click_position = pyautogui.position()
        
        # Reafișează fereastra principală
        self.root.deiconify()
        
        # Actualizează labelul pentru a afișa poziția selectată
        self.position_label.config(text=f"Poziție: {self.click_position}")

    def start_clicking(self):
        """
        Funcție pentru a începe clicurile automate.
        Verifică dacă datele introduse sunt valide.
        """
        try:
            # Încearcă să convertești frecvența introdusă de utilizator într-un număr real
            self.frequency = float(self.frequency_entry.get())
            
            # Verifică dacă frecvența este mai mare decât zero
            if self.frequency <= 0:
                raise ValueError
        except ValueError:
            # Afișează un mesaj de eroare dacă frecvența este invalidă
            tk.messagebox.showerror("Eroare", "Introduceți o frecvență validă!")
            return

        # Verifică dacă poziția mouse-ului a fost setată
        if not self.click_position:
            # Afișează un mesaj de eroare dacă poziția nu este setată
            tk.messagebox.showerror("Eroare", "Setați mai întâi o poziție de click!")
            return

        # Setează aplicația ca fiind în stare de rulare
        self.running = True
        
        # Dezactivează butonul Start și activează butonul Stop
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Rulează funcția de clicuri automate pe un fir separat
        threading.Thread(target=self.perform_clicks).start()

    def stop_clicking(self):
        """
        Funcție pentru a opri clicurile automate.
        """
        # Setează aplicația ca fiind oprită
        self.running = False
        
        # Reactivare butonul Start și dezactivează butonul Stop
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def perform_clicks(self):
        """
        Funcție care execută clicurile automate la intervale regulate.
        Rulează pe un fir de execuție separat.
        """
        # Continuă să facă clicuri cât timp aplicația este în stare de rulare
        while self.running:
            # Execută un clic la poziția setată
            pyautogui.click(self.click_position)
            
            # Așteaptă frecvența specificată înainte de următorul clic
            time.sleep(self.frequency)

# Creează fereastra principală a aplicației
root = tk.Tk()

# Creează o instanță a clasei AutoClicker
app = AutoClicker(root)

# Rulează bucla principală a aplicației (pentru interacțiunea cu GUI-ul)
root.mainloop()