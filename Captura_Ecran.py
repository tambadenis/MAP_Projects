import tkinter as tk
from tkinter import messagebox
import pyautogui

# Funcția pentru captură de ecran
def captura_ecran():
    # Preluăm numele fișierului introdus
    file_name = entry.get().strip()
    if not file_name:
        messagebox.showerror("Eroare", "Introduceți un nume valid pentru fișier!")
        return
    
    try:
        # Realizăm captura de ecran și salvăm
        screenshot = pyautogui.screenshot()
        file_name += ".png"
        screenshot.save(file_name)
        messagebox.showinfo("Succes", f"Captura a fost salvată ca {file_name}!")
    except Exception as e:
        messagebox.showerror("Eroare", f"A apărut o problemă: {e}")

# Interfața GUI
root = tk.Tk()
root.title("Captură de Ecran")
root.geometry("400x200")

# Etichetă pentru instrucțiuni
label = tk.Label(root, text="Introduceți numele fișierului:")
label.pack(pady=5)

# Câmp text pentru numele fișierului
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Buton pentru a face captura
button = tk.Button(root, text="Capturează Ecranul", command=captura_ecran)
button.pack(pady=10)

# Forțăm actualizarea ferestrei
root.update()

# Rularea aplicației
root.mainloop()