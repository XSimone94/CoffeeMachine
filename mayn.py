import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

# Menu e risorse
MENU = {
    "espresso": {"ingredienti": {"acqua": 50, "caffè": 10}, "costo": 1.5},
    "latte": {"ingredienti": {"acqua": 200, "latte": 150, "caffè": 24}, "costo": 2.5},
    "cappuccino": {"ingredienti": {"acqua": 250, "latte": 100, "caffè": 24}, "costo": 3.0},
}

profitto = 0
risorse = {"acqua": 300, "latte": 200, "caffè": 100}
saldo = 0.0


# Funzioni principali
def risorse_sufficienti(ingredienti_ordine):
    for elemento in ingredienti_ordine:
        if ingredienti_ordine[elemento] > risorse[elemento]:
            messagebox.showerror("Errore", f"Non c'è abbastanza {elemento}.")
            return False
    return True


def transazione_avvenuta(costo_bevanda):
    global saldo, profitto
    if saldo >= costo_bevanda:
        saldo -= costo_bevanda
        profitto += costo_bevanda
        messagebox.showinfo("Pagamento", f"Pagamento avvenuto! Saldo rimanente: €{saldo:.2f}")
        return True
    else:
        messagebox.showerror("Errore", "Saldo insufficiente.")
        return False


def prepara_caffè(nome_bevanda, ingredienti_ordine, costo_bevanda):
    global risorse
    for elemento in ingredienti_ordine:
        risorse[elemento] -= ingredienti_ordine[elemento]
    messagebox.showinfo("Pronto!", f"Ecco il tuo {nome_bevanda} per €{costo_bevanda:.2f}! ☕")


def ordina_bevanda(nome_bevanda):
    bevanda = MENU[nome_bevanda]
    costo_bevanda = bevanda["costo"]
    if risorse_sufficienti(bevanda["ingredienti"]):
        risposta = messagebox.askyesno(
            "Conferma Ordine",
            f"Vuoi ordinare un {nome_bevanda} per €{costo_bevanda:.2f}?"
        )
        if risposta and transazione_avvenuta(costo_bevanda):
            prepara_caffè(nome_bevanda, bevanda["ingredienti"], costo_bevanda)


def mostra_saldo():
    messagebox.showinfo("Saldo", f"Saldo attuale: €{saldo:.2f}")


def ricarica_saldo():
    global saldo
    importo = simpledialog.askfloat("Ricarica", "Inserisci l'importo da ricaricare (€):")
    if importo and importo > 0:
        saldo += importo
        messagebox.showinfo("Ricarica", f"Hai ricaricato €{importo:.2f}. Saldo attuale: €{saldo:.2f}")


def mostra_rapporto():
    rapporto = (
        f"Acqua: {risorse['acqua']}ml\n"
        f"Latte: {risorse['latte']}ml\n"
        f"Caffè: {risorse['caffè']}g\n"
        f"Profitto: €{profitto:.2f}"
    )
    messagebox.showinfo("Rapporto", rapporto)


# === Interfaccia grafica === #
app = tk.Tk()
app.title("Macchina del Caffè")
app.geometry("400x500")

# Caricamento immagine sfondo
background_image_path = "C:/Users/Simone/OneDrive/Desktop/Coffee-APPeal_QR-Code.jpg"

try:
    bg_image = Image.open(background_image_path)
    bg_image = bg_image.resize((400, 500), Image.Resampling.LANCZOS)
    background = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(app, width=400, height=500)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background, anchor="nw")
except Exception as e:
    print(f"[Errore immagine di sfondo]: {e}")
    canvas = tk.Canvas(app, width=400, height=500, bg="white")
    canvas.pack(fill="both", expand=True)

# Testo iniziale
canvas.create_text(200, 50, text="Scegli la tua bevanda:", font=("Aptos", 12), fill="white")

# Pulsanti
buttons = [
    ("☕ Espresso", lambda: ordina_bevanda("espresso")),
    ("🥛 Latte", lambda: ordina_bevanda("latte")),
    ("🧋 Cappuccino", lambda: ordina_bevanda("cappuccino")),
    ("💳 Controlla Saldo", mostra_saldo),
    ("➕ Ricarica Saldo", ricarica_saldo),
    ("📊 Mostra Rapporto", mostra_rapporto),
    ("❌ Spegni", app.quit),
]

y_position = 100
for text, command in buttons:
    button = tk.Button(app, text=text, command=command)
    canvas.create_window(200, y_position, window=button, width=200, height=30)
    y_position += 50

# Avvia l'interfaccia
app.mainloop()