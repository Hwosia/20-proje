import tkinter as tk
from tkinter import ttk, simpledialog
import json

class Oyun:
    def __init__(self, adi, turu, platformu, yildiz=0, yorum=""):
        self.adi = adi
        self.turu = turu
        self.platformu = platformu
        self.yorum = yorum
        self.yildiz = yildiz

class Koleksiyon:
    def __init__(self):
        self.oyunlar = []

    def oyun_ekle(self, oyun):
        self.oyunlar.append(oyun)

class Oyuncu:
    def __init__(self, adi):
        self.adi = adi
        self.koleksiyon = Koleksiyon()
        self.favori_oyunlar = []

    def oyun_ekle(self, oyun):
        self.koleksiyon.oyun_ekle(oyun)

    def yildiz_ver(self, oyun, yildiz):
        oyun.yildiz = yildiz
        self.sirala_favori_oyunlar()

    def sirala_favori_oyunlar(self):
        self.favori_oyunlar = sorted(self.koleksiyon.oyunlar, key=lambda oyun: oyun.yildiz, reverse=True)

class YorumEkleDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Yorum Ekle")

        self.yorum_edit = tk.Text(self, height=5, width=30)
        self.yorum_edit.grid(row=0, column=0, padx=10, pady=10)

        ok_button = ttk.Button(self, text="Tamam", command=self.on_ok_button_click)
        ok_button.grid(row=1, column=0, padx=10, pady=10)

    def on_ok_button_click(self):
        self.yorum = self.yorum_edit.get("1.0", "end-1c")
        self.destroy()

class FavoriOyunlarDialog(tk.Toplevel):
    def __init__(self, oyuncu, parent):
        super().__init__(parent)
        self.title("Favori Oyunlar")

        self.browser = tk.Text(self, height=10, width=50)
        self.browser.grid(row=0, column=0, padx=10, pady=10)
        self.browser.insert(tk.END, "\n".join("{} ({}) - {} - Yıldız: {}".format(oyun.adi, oyun.turu, oyun.platformu, oyun.yildiz) for oyun in oyuncu.favori_oyunlar))

class YorumlarDialog(tk.Toplevel):
    def __init__(self, oyuncu, parent):
        super().__init__(parent)
        self.title("Oyun Yorumları")

        self.browser = tk.Text(self, height=10, width=50)
        self.browser.grid(row=0, column=0, padx=10, pady=10)
        self.browser.insert(tk.END, "\n\n".join("{}\nYorum: {}\n".format(oyun.adi, oyun.yorum) for oyun in oyuncu.koleksiyon.oyunlar if oyun.yorum))

class AnaPencere(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Oyun Koleksiyonu Yönetimi")
        self.geometry("800x600")
        self.configure(background="#f0f0f0")

        self.label = tk.Label(self, text="Oyun Koleksiyonu Yönetimi", font=("Helvetica", 16), bg="#f0f0f0")
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(self, bg="#f0f0f0")
        self.button_frame.pack()

        self.button = ttk.Button(self.button_frame, text="Oyun Ekle", command=self.oyun_ekle)
        self.button.grid(row=0, column=0, padx=10, pady=5)

        self.favori_button = ttk.Button(self.button_frame, text="Favori Oyunlarım", command=self.show_favori_oyunlar)
        self.favori_button.grid(row=0, column=1, padx=10, pady=5)

        self.yorumlar_button = ttk.Button(self.button_frame, text="Oyun Yorumları", command=self.show_yorumlar)
        self.yorumlar_button.grid(row=0, column=2, padx=10, pady=5)

        self.canvas = tk.Canvas(self, bg="#f0f0f0")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.game_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.canvas.create_window((0, 0), window=self.game_frame, anchor="nw")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.game_widgets = []

        self.oyuncu = Oyuncu("Ahmet")
        self.load_data()

    def load_data(self):
        try:
            with open("oyunlar.json", "r") as file:
                data = json.load(file)
                for oyun_data in data:
                    oyun = Oyun(**oyun_data)
                    self.oyuncu.oyun_ekle(oyun)
                    self.update_game_widgets()
        except FileNotFoundError:
            pass

    def save_data(self):
        with open("oyunlar.json", "w") as file:
            data = [{"adi": oyun.adi, "turu": oyun.turu, "platformu": oyun.platformu, "yildiz": oyun.yildiz, "yorum": oyun.yorum} for oyun in self.oyuncu.koleksiyon.oyunlar]
            json.dump(data, file)

    def update_game_widgets(self):
        for widget in self.game_widgets:
            widget.destroy()
        self.game_widgets = []

        for index, oyun in enumerate(self.oyuncu.koleksiyon.oyunlar):
            frame = tk.Frame(self.game_frame, bg="#f0f0f0")
            frame.grid(row=index, column=0, sticky="ew")
            self.game_widgets.append(frame)

            label = tk.Label(frame, text="{} ({}) - {} - Yıldız: {}".format(oyun.adi, oyun.turu, oyun.platformu, oyun.yildiz), bg="#f0f0f0")
            label.grid(row=0, column=0, padx=10, pady=5)
            self.game_widgets.append(label)

            yildiz_slider = ttk.Scale(frame, from_=0, to=5, orient=tk.HORIZONTAL)
            yildiz_slider.set(oyun.yildiz)
            yildiz_slider.grid(row=0, column=1, padx=10, pady=5)
            yildiz_slider.bind("<ButtonRelease-1>", lambda event, oyun=oyun, yildiz_slider=yildiz_slider: self.yildiz_ver(oyun, yildiz_slider.get()))
            self.game_widgets.append(yildiz_slider)

            yorum_button = ttk.Button(frame, text="Yorum Ekle", command=lambda oyun=oyun: self.yorum_ekle(oyun))
            yorum_button.grid(row=0, column=2, padx=10, pady=5)
            self.game_widgets.append(yorum_button)

    def oyun_ekle(self):
        oyun_adi = simpledialog.askstring("Oyun Ekle", "Oyun adı:")
        if oyun_adi:
            oyun_turu = simpledialog.askstring("Oyun Ekle", "Oyun türü:")
            if oyun_turu:
                oyun_platformu = simpledialog.askstring("Oyun Ekle", "Oyun platformu:")
                if oyun_platformu:
                    oyun = Oyun(oyun_adi, oyun_turu, oyun_platformu)
                    self.oyuncu.oyun_ekle(oyun)
                    self.update_game_widgets()
                    self.save_data()

    def yildiz_ver(self, oyun, yildiz):
        self.oyuncu.yildiz_ver(oyun, yildiz)
        self.save_data()

    def yorum_ekle(self, oyun):
        dialog = YorumEkleDialog(self)
        self.wait_window(dialog)
        if hasattr(dialog, "yorum"):
            oyun.yorum = dialog.yorum
            self.update_game_widgets()
            self.save_data()

    def show_favori_oyunlar(self):
        dialog = FavoriOyunlarDialog(self.oyuncu, self)
        dialog.grab_set()

    def show_yorumlar(self):
        dialog = YorumlarDialog(self.oyuncu, self)
        dialog.grab_set()

if __name__ == "__main__":
    app = AnaPencere()
    app.mainloop()
