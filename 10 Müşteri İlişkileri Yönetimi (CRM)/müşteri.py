import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sqlite3

class Musteri:
    def __init__(self, adi, soyadi, tc, telno, urun_id, urun_adı, tarih=datetime.now().strftime("%d/%m/%Y %H:%M:%S")):
        self.adi = adi
        self.soyadi = soyadi
        self.tc = tc
        self.telno = telno
        self.urunler = []
        self.urun_id = urun_id
        self.urun_adı = urun_adı
        self.tarih = tarih

    def urun_ekle(self, urun):
        self.urunler.append(urun)

    def urunleri_listele(self):
        return self.urunler

class MusteriYonetimi(tk.Tk):
    def __init__(self):
        super().__init__()

        self.musteri_listesi = []
        self.destek_talepleri = []

        # Veritabanı bağlantısı ve imleç oluşturma
        self.connection = sqlite3.connect("musteri_veritabani.db")
        self.cursor = self.connection.cursor()

        # Tabloları oluşturma
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS musteriler (
                id INTEGER PRIMARY KEY,
                adi TEXT NOT NULL,
                soyadi TEXT NOT NULL,
                tc TEXT NOT NULL,
                telno TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS satislar (
                id INTEGER PRIMARY KEY,
                musteri_id INTEGER,
                urun_id INTEGER,
                urun_adı TEXT NOT NULL,
                tarih TEXT NOT NULL,
                FOREIGN KEY(musteri_id) REFERENCES musteriler(id)
            )
        """)

        # Değişiklikleri kaydet
        self.connection.commit()

        self.init_ui()

    def __del__(self):
        # Bağlantıyı kapat
        self.connection.close()

    def init_ui(self):
        self.title("Müşteri İlişkileri Yönetimi")
        self.geometry("400x300")

        self.tab_widget = ttk.Notebook(self)
        self.tab_widget.pack(fill="both", expand=True)

        self.tab_musteri = ttk.Frame(self.tab_widget)
        self.tab_widget.add(self.tab_musteri, text="Müşteri Ekle")
        # Müşteri ekle sekmesini aktif hale getir
        self.tab_widget.select(self.tab_musteri)

        ttk.Label(self.tab_musteri, text="Müşteri Adı:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.lineedit_adi = ttk.Entry(self.tab_musteri)
        self.lineedit_adi.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(self.tab_musteri, text="Müşteri Soyadı:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.lineedit_soyadi = ttk.Entry(self.tab_musteri)
        self.lineedit_soyadi.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(self.tab_musteri, text="Müşteri TcNo:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.lineedit_tc = ttk.Entry(self.tab_musteri)
        self.lineedit_tc.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        
        ttk.Label(self.tab_musteri, text="Müşteri TelNo:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.lineedit_telno = ttk.Entry(self.tab_musteri)
        self.lineedit_telno.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(self.tab_musteri, text="Ürün ID:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.lineedit_urun_id = ttk.Entry(self.tab_musteri)
        self.lineedit_urun_id.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(self.tab_musteri, text="Satın Alınan Ürünler:").grid(row=5, column=0, padx=5, pady=2, sticky="w")
        self.plaintext_urunler = tk.Text(self.tab_musteri, height=4, width=30)
        self.plaintext_urunler.grid(row=5, column=1, padx=5, pady=2, sticky="ew")

        self.button_musteri_ekle = ttk.Button(self.tab_musteri, text="Müşteri Ekle", command=self.musteri_ekle)
        self.button_musteri_ekle.grid(row=6, columnspan=2, pady=10)
        
        self.tab_satis = ttk.Frame(self.tab_widget)
        self.tab_widget.add(self.tab_satis, text="Satış Takibi")
        # Satış takibi sekmesine geçiş yapıldığında pencere boyutunu ayarla
        self.tab_widget.bind("<<NotebookTabChanged>>", self.set_tab_size)

        self.table_satis = ttk.Treeview(self.tab_satis, columns=("Ürün ID", "Müşteri Adı", "Ürün Adı", "Tarih"))
        self.table_satis.heading("#0", text="Index")
        self.table_satis.heading("Ürün ID", text="Ürün ID")
        self.table_satis.heading("Müşteri Adı", text="Müşteri Adı")
        self.table_satis.heading("Ürün Adı", text="Ürün Adı")
        self.table_satis.heading("Tarih", text="Tarih")
        self.table_satis.pack(fill="both", expand=True)
        self.table_satis.bind("<Triple-1>", self.delete_selected_sale) 
        self.tab_destek = ttk.Frame(self.tab_widget)
        self.tab_widget.add(self.tab_destek, text="Destek Talepleri")

        ttk.Label(self.tab_destek, text="Gelen Talepler:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.listbox_gelen_talepler = tk.Listbox(self.tab_destek, height=8)  # Height artırıldı
        self.listbox_gelen_talepler.grid(row=0, column=1, padx=10, pady=5)

        self.button_talep_detay = ttk.Button(self.tab_destek, text="Talep Detayı", command=self.talep_detay)
        self.button_talep_detay.grid(row=1, column=0, padx=10, pady=5)

        self.button_talep_iptal = ttk.Button(self.tab_destek, text="Talebi İptal Et", command=self.talep_iptal)
        self.button_talep_iptal.grid(row=1, column=1, padx=10, pady=5)

    def musteri_ekle(self):
        adi = self.lineedit_adi.get()
        soyadi = self.lineedit_soyadi.get()
        tc = self.lineedit_tc.get()
        telno = self.lineedit_telno.get()
        urun_id = self.lineedit_urun_id.get()
        urunler = self.plaintext_urunler.get("1.0", tk.END).strip().split("\n")

        # Tüm bilgilerin girilip girilmediğini kontrol et
        if adi and soyadi and tc and telno and urun_id and urunler:
            # Müşteriyi veritabanına ekle
            self.cursor.execute("INSERT INTO musteriler (adi, soyadi, tc, telno) VALUES (?, ?, ?, ?)", (adi, soyadi, tc, telno))
            musteri_id = self.cursor.lastrowid

            # Satın alınan ürünleri veritabanına ekle
            for urun_adı in urunler:
                self.cursor.execute("INSERT INTO satislar (musteri_id, urun_id, urun_adı, tarih) VALUES (?, ?, ?, ?)", (musteri_id, urun_id, urun_adı, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

            self.connection.commit()
            messagebox.showinfo("Başarılı", "Müşteri başarıyla eklendi.")
            self.update_satis_takibi()
            # Bilgi girişlerini temizle
            self.lineedit_adi.delete(0, tk.END)
            self.lineedit_soyadi.delete(0, tk.END)
            self.lineedit_tc.delete(0, tk.END)
            self.lineedit_telno.delete(0, tk.END)
            self.lineedit_urun_id.delete(0, tk.END)
            self.plaintext_urunler.delete(1.0, tk.END)
        else:
            messagebox.showwarning("Uyarı", "Lütfen tüm müşteri bilgilerini eksiksiz girin.")

    def update_satis_takibi(self):
        self.table_satis.delete(*self.table_satis.get_children())
        self.cursor.execute("SELECT satislar.urun_id, musteriler.adi, satislar.urun_adı, satislar.tarih FROM satislar INNER JOIN musteriler ON satislar.musteri_id = musteriler.id")
        satislar = self.cursor.fetchall()
        for index, satis in enumerate(satislar, start=1):
            self.table_satis.insert("", "end", text=index, values=satis)

    def talep_detay(self):
        selected_index = self.listbox_gelen_talepler.curselection()
        if selected_index:
            selected_talep = self.destek_talepleri[selected_index[0]]
            messagebox.showinfo("Talep Detayı", f"Talep:\n\n{selected_talep}")
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir talep seçin.")

    def talep_iptal(self):
        selected_index = self.listbox_gelen_talepler.curselection()
        if selected_index:
            self.destek_talepleri.pop(selected_index[0])
            self.update_gelen_talepler()
            messagebox.showinfo("Başarılı", "Talep başarıyla iptal edildi.")
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir talep seçin.")

    def update_gelen_talepler(self):
        self.listbox_gelen_talepler.delete(0, tk.END)
        for talep in self.destek_talepleri:
            self.listbox_gelen_talepler.insert(tk.END, f"{talep}")

    def set_tab_size(self, event):
        # Satış takibi sekmesine geçildiğinde pencere boyutunu ayarla
        current_tab = event.widget.index("current")
        if current_tab == 1:  # "Satış Takibi" sekmesinin indeksi
            self.geometry("1000x400")
        else:
            self.geometry("400x300")

    def delete_selected_sale(self, event):
        # Seçilen satışın indeksini al
        selected_item = self.table_satis.selection()[0]
        # İlgili satışın bilgilerini al
        urun_id = self.table_satis.item(selected_item, "values")[0]
        musteri_adi = self.table_satis.item(selected_item, "values")[1]
        urun_adi = self.table_satis.item(selected_item, "values")[2]
        tarih = self.table_satis.item(selected_item, "values")[3]
        # Onay iste
        result = messagebox.askquestion("Satış Sil", f"{musteri_adi} adlı müşterinin {urun_adi} ürününün {tarih} tarihli satışını silmek istediğinizden emin misiniz?")
        # Kullanıcı onaylarsa, ilgili satışı veritabanından sil
        if result == "yes":
            self.cursor.execute("DELETE FROM satislar WHERE urun_id=?", (urun_id,))
            self.connection.commit()
            # Satış takibi sekmesini güncelle
            self.update_satis_takibi()
            messagebox.showinfo("Başarılı", "Satış başarıyla silindi.")


if __name__ == "__main__":
    app = MusteriYonetimi()
    app.mainloop()
