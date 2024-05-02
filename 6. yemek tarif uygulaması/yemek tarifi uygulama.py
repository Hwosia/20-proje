import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class YemekUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Yemek Tarifi Uygulaması")

        # SQLite veritabanı bağlantısı
        self.connection = sqlite3.connect("yemekler.db")
        self.cursor = self.connection.cursor()

        # Üye İşlemleri
        self.giris_cerceve = ttk.LabelFrame(self.root, text="Üye İşlemleri")
        self.giris_cerceve.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.kullanici_adi_lbl = ttk.Label(self.giris_cerceve, text="Kullanıcı Adı:")
        self.kullanici_adi_lbl.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.kullanici_adi_entry = ttk.Entry(self.giris_cerceve)
        self.kullanici_adi_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        self.sifre_lbl = ttk.Label(self.giris_cerceve, text="Şifre:")
        self.sifre_lbl.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.sifre_entry = ttk.Entry(self.giris_cerceve, show="*")
        self.sifre_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        self.giris_btn = ttk.Button(self.giris_cerceve, text="Giriş Yap", command=self.uye_giris)
        self.giris_btn.grid(row=2, column=0, padx=10, pady=5, sticky="we")

        self.kayit_btn = ttk.Button(self.giris_cerceve, text="Kayıt Ol", command=self.kayit_ol)
        self.kayit_btn.grid(row=2, column=1, padx=10, pady=5, sticky="we")
        
        self.cikis_btn = ttk.Button(self.giris_cerceve, text="Çıkış Yap", command=self.cikis_yap, state=tk.DISABLED)
        self.cikis_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.hosgeldiniz_lbl = ttk.Label(self.giris_cerceve, text="")
        self.hosgeldiniz_lbl.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        # Yemek sorgulama ve ekleme alanı
        self.yemek_sorgula_frame = ttk.LabelFrame(self.root, text="Yemek Sorgulama ve Ekleme")
        self.yemek_sorgula_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

         # Ekle butonunun genişliğini küçültelim
        self.ekle_btn = ttk.Button(self.yemek_sorgula_frame, text="Ekle", command=self.yemek_ekle)
        self.ekle_btn.grid(row=3, column=1, padx=5, pady=10, sticky="we")
        
        # Sorgula butonunu önceye alalım
        ttk.Button(self.yemek_sorgula_frame, text="Sorgula", command=self.yemek_sorgula).grid(row=3, column=0, padx=10, pady=10, sticky="we")
        
        # Malzemeleri Görüntüle Butonu

        self.goruntule_btn = ttk.Button(self.yemek_sorgula_frame, text="Malzeme ve Tarifi Görüntüle", command=self.malzeme_tarif_goruntule, state=tk.DISABLED)
        self.goruntule_btn.grid(row=4, column=1, padx=10, pady=10, sticky="we")


        # Diğer bileşenler
        self.yemek_adı_lbl = ttk.Label(self.yemek_sorgula_frame, text="Yemek Adı:")
        self.yemek_adı_lbl.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.yemek_adı_entry = ttk.Entry(self.yemek_sorgula_frame)
        self.yemek_adı_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        self.malzemeler_lbl = ttk.Label(self.yemek_sorgula_frame, text="Malzemeler:")
        self.malzemeler_lbl.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.malzemeler_entry = ttk.Entry(self.yemek_sorgula_frame)
        self.malzemeler_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        self.tarif_lbl = ttk.Label(self.yemek_sorgula_frame, text="Tarif:")
        self.tarif_lbl.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.tarif_entry = ttk.Entry(self.yemek_sorgula_frame)
        self.tarif_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        self.yemekler_liste = ttk.Treeview(self.root, columns=("ID", "Yemek", "Malzemeler", "Tarif"), show="headings")
        self.yemekler_liste.heading("ID", text="ID")
        self.yemekler_liste.heading("Yemek", text="Yemek")
        self.yemekler_liste.heading("Malzemeler", text="Malzemeler")
        self.yemekler_liste.heading("Tarif", text="Tarif")
        self.yemekler_liste.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Grid yöneticisine ağırlık ekleyerek bileşenlerin boyutlarını orantılı olarak büyütme
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Giriş durumu kontrolü için kullanıcı adı değişkeni
        self.kullanici_adi = None

        # Yemek veritabanı oluşturma
        self.yemek_veritabani_olustur()

    def yemek_veritabani_olustur(self):
        # Yemekler tablosunu oluşturma
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS yemekler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
                malzemeler TEXT NOT NULL,
                tarif TEXT NOT NULL,
                degerlendirme INTEGER,
                yorum TEXT
            )
        """)
    
        # Uyeler tablosunu oluşturma
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS uyeler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT UNIQUE NOT NULL,
                sifre TEXT NOT NULL
            )
        """)
    
        self.connection.commit()

    def kayit_ol(self):
        self.kayit_pencere = tk.Toplevel(self.root)
        self.kayit_pencere.title("Kayıt Ol")
        
        ttk.Label(self.kayit_pencere, text="İsim:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.isim_entry = ttk.Entry(self.kayit_pencere)
        self.isim_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.kayit_pencere, text="Soyisim:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.soyisim_entry = ttk.Entry(self.kayit_pencere)
        self.soyisim_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.kayit_pencere, text="Kullanıcı Adı:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.kayit_kullanici_adi_entry = ttk.Entry(self.kayit_pencere)
        self.kayit_kullanici_adi_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.kayit_pencere, text="Şifre:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.kayit_sifre_entry = ttk.Entry(self.kayit_pencere, show="*")
        self.kayit_sifre_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.kayit_pencere, text="Kayıt Ol", command=self.uye_kayit).grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def uye_kayit(self):
        isim = self.isim_entry.get()
        soyisim = self.soyisim_entry.get()
        kullanici_adi = self.kayit_kullanici_adi_entry.get()
        sifre = self.kayit_sifre_entry.get()

        self.cursor.execute("INSERT INTO uyeler (kullanici_adi, sifre) VALUES (?, ?)", (kullanici_adi, sifre))
        self.connection.commit()
        
        messagebox.showinfo("Başarılı", "Kayıt işlemi başarıyla tamamlandı! Lütfen giriş yapınız.")
        self.kayit_pencere.destroy()

    def uye_giris(self):
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()

        self.cursor.execute("SELECT * FROM uyeler WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
        uye = self.cursor.fetchone()

        if uye:
            self.kullanici_adi = kullanici_adi
            self.hosgeldiniz_lbl.config(text=f"Hoş geldiniz, {kullanici_adi}!")
            self.giris_btn.grid_remove()
            self.kayit_btn.grid_remove()
            self.cikis_btn.config(state=tk.NORMAL)
            self.kullanici_adi_lbl.grid_remove()
            self.kullanici_adi_entry.grid_remove()
            self.sifre_lbl.grid_remove()
            self.sifre_entry.grid_remove()
        
            # Malzeme ve Tarifi Görüntüleme butonunu aktif hale getir
            self.goruntule_btn.config(state=tk.NORMAL if self.kullanici_adi else tk.DISABLED)
        
            # Tüm yemekleri listeye ekle
            self.yemek_sorgula()

        else:
            messagebox.showerror("Giriş Başarısız", "Kullanıcı adı veya şifre yanlış!")

    def malzeme_tarif_goruntule(self):
        secilen = self.yemekler_liste.selection()

        if not secilen:
            messagebox.showwarning("Uyarı", "Lütfen bir tarif seçin.")
            return

        tarif_id = self.yemekler_liste.item(secilen)['values'][0]
        
        self.cursor.execute("SELECT * FROM yemekler WHERE id=?", (tarif_id,))
        yemek = self.cursor.fetchone()

        self.tarif_goruntule_pencere = tk.Toplevel(self.root)
        self.tarif_goruntule_pencere.title("Tarif Görüntüle")

        ttk.Label(self.tarif_goruntule_pencere, text="Malzemeler:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(self.tarif_goruntule_pencere, text=yemek[2]).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.tarif_goruntule_pencere, text="Tarif:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(self.tarif_goruntule_pencere, text=yemek[3]).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(self.tarif_goruntule_pencere, text="Tarifi Sil", command=self.tarif_sil).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")
    
    def tarif_sil(self):
        secilen = self.yemekler_liste.selection()
        
        if not secilen:
            messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz bir tarifi seçin.")
            return
        
        tarif_id = self.yemekler_liste.item(secilen)['values'][0]
        
        self.cursor.execute("DELETE FROM yemekler WHERE id=?", (tarif_id,))
        self.connection.commit()
        
        messagebox.showinfo("Başarılı", "Tarif başarıyla silindi!")
        
        self.yemek_sorgula()
    
    def yemek_ekle(self):
        if not self.kullanici_adi:
            messagebox.showerror("Hata", "Yemek eklemek için önce giriş yapmalısınız!")
            return

        ad = self.yemek_adı_entry.get()
        malzemeler = self.malzemeler_entry.get()
        tarif = self.tarif_entry.get()

        if not ad or not malzemeler or not tarif:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return

        self.cursor.execute("INSERT INTO yemekler (ad, malzemeler, tarif) VALUES (?, ?, ?)", (ad, malzemeler, tarif))
        self.connection.commit()

        messagebox.showinfo("Başarılı", "Yemek başarıyla eklendi!")

        # Yemek listesini güncelle
        self.yemek_sorgula()



    def yemek_sorgula(self):
        ad = self.yemek_adı_entry.get()
        malzemeler = self.malzemeler_entry.get()
        tarif = self.tarif_entry.get()

        sorgu = "SELECT * FROM yemekler"
        parametreler = []

        if ad:
            sorgu += " WHERE ad LIKE ?"
            parametreler.append('%' + ad + '%')

        if malzemeler:
            if not ad:
                sorgu += " WHERE malzemeler LIKE ?"
            else:
                sorgu += " AND malzemeler LIKE ?"
            parametreler.append('%' + malzemeler + '%')

        if tarif:
            if not ad and not malzemeler:
                sorgu += " WHERE tarif LIKE ?"
            else:
                sorgu += " AND tarif LIKE ?"
            parametreler.append('%' + tarif + '%')

        self.cursor.execute(sorgu, parametreler)
        yemekler = self.cursor.fetchall()

        self.yemekler_liste.delete(*self.yemekler_liste.get_children())

        for yemek in yemekler:
            self.yemekler_liste.insert("", "end", values=yemek)
    

    def cikis_yap(self):
        self.kullanici_adi = None
        self.hosgeldiniz_lbl.config(text="")
        self.giris_btn.grid()
        self.kayit_btn.grid()
        self.cikis_btn.config(state=tk.DISABLED)
        self.kullanici_adi_lbl.grid()
        self.kullanici_adi_entry.grid()
        self.sifre_lbl.grid()
        self.sifre_entry.grid()
       # Malzeme ve Tarifi Görüntüle Butonunu Pasif Hale Getir
        self.goruntule_btn.config(state=tk.DISABLED)

 

# Ana kod
if __name__ == "__main__":
    root = tk.Tk()
    uygulama = YemekUygulamasi(root)
    root.mainloop()
