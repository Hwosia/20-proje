import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime

class Film:
    def __init__(self, ad, yonetmen, tur):
        self.ad = ad
        self.yonetmen = yonetmen
        self.tur = tur
        self.izleme_durumu = 0

class Kullanici:
    def __init__(self, kullanici_adi, sifre):
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre
        self.izleme_gecmisi = []

class FilmServisi(tk.Tk):
    def __init__(self):
        super().__init__()

        self.veritabani_baglantisi_olustur()
        self.kullanici = Kullanici("kullanici", "sifre")
        self.izleme_listeleri = []  
        self.filmler = []  

        self.init_ui()
        self.izleme_listelerini_yukle()

    def veritabani_baglantisi_olustur(self):
        self.baglanti = sqlite3.connect("film_veritabani.db")
        self.cur = self.baglanti.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS filmler (ad TEXT, yonetmen TEXT, tur TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS izleme_listeleri (id INTEGER PRIMARY KEY AUTOINCREMENT, tarih TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS izleme_listesi_filmler (liste_id INTEGER, film_ad TEXT)")

    def init_ui(self):
        self.title("Film ve Dizi İzleme Servisi")
        self.geometry("600x400")

        label_baslik = ttk.Label(self, text="Film ve Dizi İzleme Servisi", font=("Arial", 20, "bold"))
        label_baslik.pack(pady=10)

        self.alt_widget = tk.Frame(self)
        self.alt_widget.pack(pady=10)

        button_film_ekle = ttk.Button(self.alt_widget, text="Film Ekle", command=self.film_ekle_dialog_ac)
        button_film_ekle.pack(side=tk.LEFT)

        button_filmleri_listele = ttk.Button(self.alt_widget, text="Filmleri Listele", command=self.filmleri_listele)
        button_filmleri_listele.pack(side=tk.LEFT, padx=10)

        button_izleme_listesi_olustur = ttk.Button(self.alt_widget, text="İzleme Listesi Oluştur", command=self.izleme_listesi_olustur)
        button_izleme_listesi_olustur.pack(side=tk.LEFT)

        button_izleme_gecmisi = ttk.Button(self.alt_widget, text="İzleme Geçmişi", command=self.izleme_gecmisi_goster)
        button_izleme_gecmisi.pack(side=tk.LEFT, padx=10)

        self.text_bilgi = tk.Text(self, height=10, width=50)
        self.text_bilgi.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text_bilgi.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_bilgi.config(yscrollcommand=scrollbar.set)

    def film_ekle_dialog_ac(self):
        dialog = tk.Toplevel(self)
        dialog.title("Film Ekle")

        label_film_ad = ttk.Label(dialog, text="Film Adı:")
        label_film_ad.grid(row=0, column=0)
        self.entry_film_ad = ttk.Entry(dialog)
        self.entry_film_ad.grid(row=0, column=1)

        label_yonetmen = ttk.Label(dialog, text="Yönetmen:")
        label_yonetmen.grid(row=1, column=0)
        self.entry_yonetmen = ttk.Entry(dialog)
        self.entry_yonetmen.grid(row=1, column=1)

        label_tur = ttk.Label(dialog, text="Tür:")
        label_tur.grid(row=2, column=0)
        self.combo_box_tur = ttk.Combobox(dialog, values=["Aksiyon", "Komedi", "Fantezi", "Korku", "Aşk", "Bilim Kurgu", "Western", "Müzikal"])
        self.combo_box_tur.grid(row=2, column=1)

        button_kaydet = ttk.Button(dialog, text="Kaydet", command=self.film_ekle)
        button_kaydet.grid(row=3, columnspan=2)

    def film_ekle(self):
        film_ad = self.entry_film_ad.get()
        yonetmen = self.entry_yonetmen.get()
        tur = self.combo_box_tur.get()

        self.cur.execute("INSERT INTO filmler VALUES (?, ?, ?)", (film_ad, yonetmen, tur))
        self.baglanti.commit()

        self.text_bilgi.insert(tk.END, f"Eklenen Film:\nAd: {film_ad}\nYönetmen: {yonetmen}\nTür: {tur}\n\n")
        messagebox.showinfo("Başarılı", "Film başarıyla eklendi.")

    def filmleri_listele(self):
        dialog = tk.Toplevel(self)
        dialog.title("Filmleri Listele")
        dialog.geometry("400x300")

        self.cur.execute("SELECT * FROM filmler")
        self.filmler = self.cur.fetchall()  

        listbox_filmler = tk.Listbox(dialog)
        for film in self.filmler:  
            listbox_filmler.insert(tk.END, film[0] + " - " + film[1] + " - " + film[2])
        listbox_filmler.pack(fill=tk.BOTH, expand=True)

        listbox_filmler.bind("<Double-Button-1>", self.izlemeye_basla)

    def izlemeye_basla(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            film_ad = event.widget.get(index).split(" - ")[0]
            for film in self.filmler:  
                if film[0] == film_ad:
                    progress = simpledialog.askinteger("İlerleme Durumu", "İzleme Durumu:")
                    film.izleme_durumu = progress
                    messagebox.showinfo("Başarılı", "İzleme durumu kaydedildi.")

    def izleme_listesi_olustur(self):
        dialog = tk.Toplevel(self)
        dialog.title("İzleme Listesi Oluştur")
        dialog.geometry("400x300")

        self.cur.execute("SELECT * FROM filmler")
        self.filmler = self.cur.fetchall()  

        listbox_filmler = tk.Listbox(dialog, selectmode=tk.MULTIPLE)
        for film in self.filmler:  
            listbox_filmler.insert(tk.END, film[0] + " - " + film[1] + " - " + film[2])
        listbox_filmler.pack(fill=tk.BOTH, expand=True)

        button_olustur = ttk.Button(dialog, text="Oluştur", command=lambda: self.izleme_listesi_kaydet(listbox_filmler.curselection()))
        button_olustur.pack()

    def izleme_listesi_kaydet(self, selection):
        izleme_listesi = []
        for index in selection:
            film_ad = self.filmler[index][0]  
            for film in self.filmler:  
                if film[0] == film_ad:
                    izleme_listesi.append(Film(film[0], film[1], film[2]))
        self.cur.execute("INSERT INTO izleme_listeleri (tarih) VALUES (?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
        liste_id = self.cur.lastrowid
        self.izleme_listeleri.append(izleme_listesi)  
        for film in izleme_listesi:
            self.cur.execute("INSERT INTO izleme_listesi_filmler VALUES (?, ?)", (liste_id, film.ad))
        self.baglanti.commit()
        self.izleme_listelerini_yukle()
        messagebox.showinfo("Başarılı", "İzleme listesi oluşturuldu.")

    def izleme_listelerini_yukle(self):
        self.izleme_listeleri.clear()
        self.cur.execute("SELECT * FROM izleme_listeleri")
        for izleme_listesi in self.cur.fetchall():
            self.izleme_listeleri.append(izleme_listesi[0])

    def izleme_gecmisi_goster(self):
        dialog = tk.Toplevel(self)
        dialog.title("İzleme Geçmişi")
        dialog.geometry("400x300")

        listbox_izleme_listeleri = tk.Listbox(dialog)
        for izleme_listesi_id in self.izleme_listeleri:
            listbox_izleme_listeleri.insert(tk.END, f"İzleme Listesi {izleme_listesi_id}")

        def izleme_listesi_sil():
            selection = listbox_izleme_listeleri.curselection()
            if selection:
                index = selection[0]
                izleme_listesi = listbox_izleme_listeleri.get(index)
                izleme_listesi_id = int(izleme_listesi.split()[2])
                if izleme_listesi_id in self.izleme_listeleri:
                    self.cur.execute("DELETE FROM izleme_listeleri WHERE id=?", (izleme_listesi_id,))
                    self.cur.execute("DELETE FROM izleme_listesi_filmler WHERE liste_id=?", (izleme_listesi_id,))
                    self.baglanti.commit()
                    self.izleme_listeleri.remove(izleme_listesi_id)
                    listbox_izleme_listeleri.delete(index)

        button_sil = ttk.Button(dialog, text="Sil", command=izleme_listesi_sil)
        button_sil.pack()

        listbox_izleme_listeleri.pack(fill=tk.BOTH, expand=True)

        def izleme_listesi_goster(event=None):
            selection = listbox_izleme_listeleri.curselection()
            if selection:
                index = selection[0]
                izleme_listesi_id = listbox_izleme_listeleri.get(index).split()[2]
                self.cur.execute("SELECT * FROM izleme_listesi_filmler WHERE liste_id=?", (izleme_listesi_id,))
                filmler = self.cur.fetchall()
                if filmler:
                    dialog_izleme_listesi = tk.Toplevel(self)
                    dialog_izleme_listesi.title(f"İzleme Listesi {izleme_listesi_id}")
                    dialog_izleme_listesi.geometry("400x300")
                    listbox_filmler = tk.Listbox(dialog_izleme_listesi)
                    for film in filmler:
                        listbox_filmler.insert(tk.END, film[1])
                    listbox_filmler.pack(fill=tk.BOTH, expand=True)

                    def izle():
                        selection = listbox_filmler.curselection()
                        if selection:
                            index = selection[0]
                            film_ad = listbox_filmler.get(index)
                            messagebox.showinfo("İzle", f"Şu anda \"{film_ad}\" filmi izleniyor.")

                    button_izle = ttk.Button(dialog_izleme_listesi, text="İzle", command=izle)
                    button_izle.pack()

                    # Çift tıklama olayı için fonksiyon bağlama
                    listbox_filmler.bind("<Double-Button-1>", lambda event: izle())

        listbox_izleme_listeleri.bind("<Double-Button-1>", izleme_listesi_goster)


    def __del__(self):
        self.baglanti.close()

if __name__ == "__main__":
    film_servisi = FilmServisi()
    film_servisi.mainloop()
