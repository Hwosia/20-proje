import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import sqlite3

class SeyahatUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Seyahat Planlama Uygulaması")
        self.root.geometry("1200x500")
        
        # Veritabanı bağlantısı
        self.baglanti = sqlite3.connect("seyahatler.db")
        self.cursor = self.baglanti.cursor()
        
        # Tabloyu oluşturma
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS seyahatler (
                                    id INTEGER PRIMARY KEY,
                                    ad TEXT,
                                    tarih TEXT,
                                    taşıma TEXT,
                                    konaklama TEXT  -- Konaklama sütunu eklendi
                                    )""")
        self.baglanti.commit()

        # Veritabanı güncelleme
        self.baglanti.commit()
        
        # Başlık etiketi
        self.baslik_label = tk.Label(root, text="Seyahat Planlama", font=("Helvetica", 16, "bold"), pady=10)
        self.baslik_label.grid(row=0, column=0, columnspan=2)
        
        # Tur listesi
        self.tur_listesi = ttk.Treeview(root, columns=("Ad", "Tarih", "Fiyat"))
        self.tur_listesi.heading("#0", text="ID")
        self.tur_listesi.heading("Ad", text="Tur Adı")
        self.tur_listesi.heading("Tarih", text="Tarih")
        self.tur_listesi.heading("Fiyat", text="Fiyat")
        
        # Örnek turlar ekleme
        turlar = [
            ("Şehir Turu", "15.05.2024", "100 TL"),
            ("Doğa Turu", "20.05.2024", "150 TL"),
            ("Tarih Turu", "25.05.2024", "120 TL"),
            ("Deniz Turu", "30.05.2024", "200 TL"),
            ("Dağ Turu", "05.06.2024", "180 TL"),
            ("Kültür Turu", "10.06.2024", "160 TL"),
            ("Eğlence Turu", "15.06.2024", "250 TL"),
            ("Yemek Turu", "20.06.2024", "90 TL"),
            ("Macera Turu", "25.06.2024", "300 TL"),
            ("Spa Turu", "30.06.2024", "220 TL"),
            ("Sağlık Turu", "05.07.2024", "280 TL"),
            ("Alışveriş Turu", "10.07.2024", "130 TL"),
            ("Gezi Turu", "15.07.2024", "170 TL"),
            ("Spor Turu", "20.07.2024", "190 TL")
        ]
        
        for i, (ad, tarih, fiyat) in enumerate(turlar, 1):
            self.tur_listesi.insert("", "end", text=str(i), values=(ad, tarih, fiyat))
        
        self.tur_listesi.grid(row=1, column=0, padx=10, pady=10)
        
        # Taşıma seçenekleri
        self.taşıma_label = tk.Label(root, text="Taşıma Seçenekleri:", font=("Helvetica", 12))
        self.taşıma_label.grid(row=2, column=0, pady=(0,5), sticky="w")
        
        self.taşıma_seçimleri = ttk.Combobox(root, values=["Otobüs", "Tren", "Uçak", "Özel Araç"], font=("Helvetica", 10))
        self.taşıma_seçimleri.grid(row=3, column=0, padx=10, pady=(0,10), sticky="w")

        
        # Seyahat planlama düğmesi
        self.planla_düğmesi = tk.Button(root, text="Seyahat Planla", command=self.seyahat_planla, font=("Helvetica", 12), bg="green", fg="white")
        self.planla_düğmesi.grid(row=4, column=0, padx=10, pady=10)
        
        # Kayıtlı Seyahatler
        self.kayıtlı_seyahatler_frame = tk.Frame(root)
        self.kayıtlı_seyahatler_frame.grid(row=1, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        
        self.kayıtlı_seyahatler_label = tk.Label(self.kayıtlı_seyahatler_frame, text="Kayıtlı Seyahatler", font=("Helvetica", 14, "bold"))
        self.kayıtlı_seyahatler_label.pack(pady=10)
                # Konaklama seçenekleri
        self.konaklama_label = tk.Label(root, text="Konaklama Seçenekleri:", font=("Helvetica", 12))
        self.konaklama_label.grid(row=4, column=0, pady=(0,5), sticky="w")
        
        self.konaklama_seçimleri = ttk.Combobox(root, values=["Otel", "Pansiyon", "Ev Kiralama", "Kamp"], font=("Helvetica", 10))
        self.konaklama_seçimleri.grid(row=5, column=0, padx=10, pady=(0,10), sticky="w")
        
        # Örnek kayıtlı seyahatler
        self.ornek_kayıtlı_seyahatler = self.seyahatleri_getir()
        
        for seyahat in self.ornek_kayıtlı_seyahatler:
            self.seyahat_ekle(seyahat)
        
    def seyahat_ekle(self, seyahat):
        ad, tarih, taşıma, konaklama = seyahat  # Tuple'ı dört değerle açıyoruz
        seyahat_frame = tk.Frame(self.kayıtlı_seyahatler_frame)
        seyahat_frame.pack(fill="x", padx=5, pady=5)
        
        seyahat_etiket = tk.Label(seyahat_frame, text=f"{ad} - {tarih} ({taşıma}) - {konaklama}", font=("Helvetica", 10))
        seyahat_etiket.pack(side="left", padx=5)
        
        iptal_düğmesi = tk.Button(seyahat_frame, text="İptal Et", command=lambda: self.seyahat_iptal(ad, tarih, taşıma), font=("Helvetica", 10), bg="red", fg="white")
        iptal_düğmesi.pack(side="left", padx=5)
        
        incele_düğmesi = tk.Button(seyahat_frame, text="İncele", command=lambda a=ad, t=tarih, tr=taşıma, k=konaklama: self.seyahati_incele(a, t, tr, k), font=("Helvetica", 10), bg="blue", fg="white")

        incele_düğmesi.pack(side="left", padx=5)

    def seyahati_incele(self, ad, tarih, taşıma, konaklama):
        inceleme_mesajı = f"Tur Adı: {ad}\nTarih: {tarih}\nTaşıma: {taşıma}\nKonaklama: {konaklama}"
        tkinter.messagebox.showinfo("Tur İnceleme", inceleme_mesajı)
        
    def seyahat_planla(self):
        if not self.tur_listesi.selection():
            tkinter.messagebox.showwarning("Uyarı", "Lütfen bir tur seçiniz.")
            return
        
        secilen_tur = self.tur_listesi.selection()[0]  # Seçilen turun indeksi
        secilen_taşıma = self.taşıma_seçimleri.get()
        secilen_konaklama = self.konaklama_seçimleri.get()
        print("Seçilen Tur:", secilen_tur)
        print("Seçilen Taşıma:", secilen_taşıma)
        print("Seçilen Konaklama:", secilen_konaklama)
        
        # Örnek olarak seyahat ekleyelim
        secilen_tur_info = self.tur_listesi.item(secilen_tur)
        tur_adı = secilen_tur_info["values"][0]
        tur_tarihi = secilen_tur_info["values"][1]
        self.seyahat_ekle((tur_adı, tur_tarihi, secilen_taşıma, secilen_konaklama))  # Burada 4 değer gönderiliyor.
        
        # Seyahati veritabanına ekleyelim
        self.cursor.execute("INSERT INTO seyahatler (ad, tarih, taşıma, konaklama) VALUES (?, ?, ?, ?)", (tur_adı, tur_tarihi, secilen_taşıma, secilen_konaklama))
        self.baglanti.commit()
    
    def seyahat_iptal(self, ad, tarih, taşıma):
        for widget in self.kayıtlı_seyahatler_frame.winfo_children():
            children = widget.winfo_children()
            if children:  # Eğer widget'ın içinde başka widget'lar varsa
                info = children[0].cget("text")
                if f"{ad} - {tarih} ({taşıma})" in info:
                    widget.destroy()
                    break
        self.cursor.execute("DELETE FROM seyahatler WHERE ad=? AND tarih=? AND taşıma=?", (ad, tarih, taşıma))
        self.baglanti.commit()
        
    
    def seyahatleri_getir(self):
        self.cursor.execute("SELECT ad, tarih, taşıma, konaklama FROM seyahatler")
        return self.cursor.fetchall()
        
    def __del__(self):
        self.baglanti.close()

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = SeyahatUygulamasi(root)
    root.mainloop()