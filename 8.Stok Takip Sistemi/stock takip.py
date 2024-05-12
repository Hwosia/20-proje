import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class stockyonetim:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Yönetim Sistemi")

        # SQLite veritabanı bağlantısı
        self.connection = sqlite3.connect("kutuphane.db")
        self.cursor = self.connection.cursor()

        # uyeler tablosunu oluştur
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS uyeler (
                id INTEGER PRIMARY KEY,
                kullanici_adi TEXT NOT NULL,
                sifre TEXT NOT NULL,
                eposta TEXT NOT NULL
            )
        """)
        self.connection.commit()

        # stok tablosunu oluştur
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stok (
                ID INTEGER PRIMARY KEY,
                urun_ismi TEXT NOT NULL,
                yapimci_firma TEXT NOT NULL,
                stok_miktari INTEGER NOT NULL
            )
        """)
        self.connection.commit()

        # Stock sorgulama ve ekleme alanı
        self.stock_sorgula_frame = ttk.LabelFrame(self.root, text="Stock Sorgulama ve Ekleme")
        self.stock_sorgula_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.uye_id = None
        ttk.Label(self.stock_sorgula_frame, text="Ürün İsmi:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.urun_ismi_entry = ttk.Entry(self.stock_sorgula_frame)
        self.urun_ismi_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.stock_sorgula_frame, text="Ürün Sahibi Firma:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.urun_yazari_entry = ttk.Entry(self.stock_sorgula_frame)
        self.urun_yazari_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.stock_sorgula_frame, text="Yeni Stock Miktarı:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.nereden_aliniyor_entry = ttk.Entry(self.stock_sorgula_frame)
        self.nereden_aliniyor_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")
        
        self.urun_liste = ttk.Treeview(self.root, columns=("ID", "Stocklu Ürün", "Ürün Sahibi Firma", "Stok Miktarı"), show="headings")
        self.urun_liste.heading("ID", text="ID")
        self.urun_liste.heading("Stocklu Ürün", text="Stocklu Ürün")
        self.urun_liste.heading("Ürün Sahibi Firma", text="Ürün Sahibi Firma")
        self.urun_liste.heading("Stok Miktarı", text="Stok Miktarı")
        self.urun_liste.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        ttk.Button(self.stock_sorgula_frame, text="Sorgula", command=self.stock_sorgula).grid(row=3, column=0, padx=10, pady=10, sticky="we")
        ttk.Button(self.stock_sorgula_frame, text="Stock Ekle", command=self.stock_ekle_dialog).grid(row=3, column=1, padx=10, pady=10, sticky="we")
        self.secili_urun_deger = None

        # Ödünç Geçmişi
        self.siparis_yonetimi_btn = ttk.Button(self.stock_sorgula_frame, text="Sipariş Yönetimi", command=self.siparis_yonetimi_goster)
        self.siparis_yonetimi_btn.grid(row=3, column=2, padx=10, pady=10, sticky="we")

        # Üye İşlemleri
        self.uye_frame = ttk.LabelFrame(self.root, text="Üye İşlemleri")
        self.uye_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.giris_yap_btn = ttk.Button(self.uye_frame, text="Giriş Yap", command=self.uye_giris)
        self.giris_yap_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="we")

        self.kayit_ol_btn = ttk.Button(self.uye_frame, text="Kayıt Ol", command=self.uye_kayit)
        self.kayit_ol_btn.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        self.hosgeldin_label = ttk.Label(self.uye_frame, text="")
        self.hosgeldin_label.grid(row=2, column=0, padx=10, pady=5, sticky="we")

        self.bilgileri_guncelle_btn = ttk.Button(self.uye_frame, text="Bilgileri Güncelle", command=self.bilgileri_guncelle)
        self.bilgileri_guncelle_btn.grid(row=3, column=0, padx=10, pady=5, sticky="we")
        self.bilgileri_guncelle_btn.grid_remove()

        self.cikis_btn = ttk.Button(self.uye_frame, text="Çıkış", command=self.uye_cikis)
        self.cikis_btn.grid(row=4, column=0, padx=10, pady=5, sticky="we")
        self.cikis_btn.grid_remove()
        self.stock_temizle_btn = ttk.Button(self.stock_sorgula_frame, text="Stock Temizle", command=self.stock_temizle)
        self.stock_temizle_btn.grid(row=3, column=3, padx=10, pady=10, sticky="we")
        # Grid yöneticisine ağırlık ekleyerek bileşenlerin boyutlarını orantılı olarak büyütme
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.anlik_stok_label = ttk.Label(self.root, text="Anlık Stok Miktarı:")
        self.anlik_stok_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.anlik_stok_miktar_label = ttk.Label(self.root, text="")
        self.anlik_stok_miktar_label.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        # Giriş durumu kontrolü için kullanıcı adı değişkeni
        self.kullanici_adi = None
        self.odunc_gecmisi_pencere = None
        # Grid yöneticisine ağırlık ekleyerek bileşenlerin boyutlarını orantılı olarak büyütme
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def stock_sorgula(self):
        if not self.kullanici_adi:
            messagebox.showwarning("Uyarı", "Stock sorgulama işlemi için önce giriş yapmalısınız!")
            return

        # Ürün bilgilerini al
        urun_ismi = self.urun_ismi_entry.get()
        urun_sahibi_firma = self.urun_yazari_entry.get()

        # Eğer her iki alan da boşsa, uyarı ver
        if not urun_ismi and not urun_sahibi_firma:
            messagebox.showwarning("Uyarı", "Lütfen ürün ismi veya ürün sahibi firma alanlarından birine bir değer girin!")
            return

        # Önceki sorgudan kalma verileri temizle
        if hasattr(self, 'urun_liste'):
            self.urun_liste.delete(*self.urun_liste.get_children())

        # Yeni sorguyu yap ve sonuçları göster
        if urun_ismi and not urun_sahibi_firma:
            self.cursor.execute("SELECT * FROM stok WHERE urun_ismi LIKE ?", ('%' + urun_ismi + '%',))
        elif not urun_ismi and urun_sahibi_firma:
            self.cursor.execute("SELECT * FROM stok WHERE yapimci_firma LIKE ?", ('%' + urun_sahibi_firma + '%',))
        else:
            self.cursor.execute("SELECT * FROM stok WHERE urun_ismi LIKE ? OR yapimci_firma LIKE ?", ('%' + urun_ismi + '%', '%' + urun_sahibi_firma + '%',))
        
        urunler = self.cursor.fetchall()

        for urun in urunler:
            self.urun_liste.insert("", "end", values=urun)
    
    def stock_temizle(self):
        if not self.urun_liste.selection():
            messagebox.showwarning("Uyarı", "Lütfen önce bir stok seçiniz.")
            return

        onay = messagebox.askyesno("Onay", "Seçili stok verisini silmek istediğinizden emin misiniz?")
        if onay:
            # Seçili stokun ID'sini al
            secili_stok_id = self.urun_liste.item(self.urun_liste.selection()[0])['values'][0]
            # Veritabanından seçili stoku sil
            self.cursor.execute("DELETE FROM stok WHERE ID=?", (secili_stok_id,))
            self.connection.commit()
            # Ekranı güncelle
            self.stock_sorgula()

    def stock_ekle_dialog(self):
        self.stock_ekle_pencere = tk.Toplevel()
        self.stock_ekle_pencere.title("Stock Ekle")

        ttk.Label(self.stock_ekle_pencere, text="Ürün İsmi:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.yeni_urun_ismi_entry = ttk.Entry(self.stock_ekle_pencere)
        self.yeni_urun_ismi_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.stock_ekle_pencere, text="Ürün Sahibi Firma:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.yeni_urun_yazari_entry = ttk.Entry(self.stock_ekle_pencere)
        self.yeni_urun_yazari_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.stock_ekle_pencere, text="Yeni Stock Miktarı:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.yeni_nereden_aliniyor_entry = ttk.Entry(self.stock_ekle_pencere)
        self.yeni_nereden_aliniyor_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.stock_ekle_pencere, text="Stock Ekle", command=self.stock_ekle).grid(row=3, column=1, padx=10, pady=10, sticky="we")

    def stock_ekle(self):
        yeni_urun_ismi = self.yeni_urun_ismi_entry.get()
        yeni_urun_yazari = self.yeni_urun_yazari_entry.get()
        yeni_stok_miktari = self.yeni_nereden_aliniyor_entry.get()

        if not yeni_urun_ismi or not yeni_urun_yazari or not yeni_stok_miktari:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
            return

        try:
            yeni_stok_miktari = int(yeni_stok_miktari)
        except ValueError:
            messagebox.showwarning("Uyarı", "Stok miktarı sayı olmalıdır!")
            return

        self.cursor.execute("INSERT INTO stok (urun_ismi, yapimci_firma, stok_miktari) VALUES (?, ?, ?)",
                            (yeni_urun_ismi, yeni_urun_yazari, yeni_stok_miktari))
        self.connection.commit()
        messagebox.showinfo("Başarılı", "Yeni stok başarıyla eklendi.")
        # Yeni stok ekledikten sonra pencereyi kapat
        self.stock_ekle_pencere.destroy()
        # Ekranı güncelle
        self.stock_sorgula()

    def uye_giris(self):
        # Kullanıcı girişi için giriş penceresi oluştur
        self.giris_pencere = tk.Toplevel()
        self.giris_pencere.title("Üye Girişi")

        ttk.Label(self.giris_pencere, text="Kullanıcı Adı:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.kullanici_adi_entry = ttk.Entry(self.giris_pencere)
        self.kullanici_adi_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.giris_pencere, text="Şifre:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.sifre_entry = ttk.Entry(self.giris_pencere, show="*")
        self.sifre_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.giris_pencere, text="Giriş Yap", command=self.uye_giris_yap).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def uye_giris_yap(self):
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()

        if not kullanici_adi or not sifre:
            messagebox.showwarning("Uyarı", "Lütfen kullanıcı adı ve şifre alanlarını doldurun!")
            return

        self.cursor.execute("SELECT * FROM uyeler WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
        kullanici = self.cursor.fetchone()

        if kullanici:
            self.kullanici_adi = kullanici_adi
            self.giris_pencere.destroy()
            self.giris_yap_btn.grid_remove()
            self.kayit_ol_btn.grid_remove()
            self.hosgeldin_label.config(text=f"Hoş geldin, {kullanici_adi}!")
            self.hosgeldin_label.grid()
            self.bilgileri_guncelle_btn.grid()
            self.cikis_btn.grid()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı!")

    def uye_kayit(self):
        # Kullanıcı kaydı için kayıt penceresi oluştur
        self.kayit_pencere = tk.Toplevel()
        self.kayit_pencere.title("Üye Kaydı")

        ttk.Label(self.kayit_pencere, text="Kullanıcı Adı:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.yeni_kullanici_adi_entry = ttk.Entry(self.kayit_pencere)
        self.yeni_kullanici_adi_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.kayit_pencere, text="Şifre:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.yeni_sifre_entry = ttk.Entry(self.kayit_pencere, show="*")
        self.yeni_sifre_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.kayit_pencere, text="E-Posta:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.yeni_eposta_entry = ttk.Entry(self.kayit_pencere)
        self.yeni_eposta_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.kayit_pencere, text="Kayıt Ol", command=self.uye_kaydet).grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def uye_kaydet(self):
        yeni_kullanici_adi = self.yeni_kullanici_adi_entry.get()
        yeni_sifre = self.yeni_sifre_entry.get()
        yeni_eposta = self.yeni_eposta_entry.get()

        if not yeni_kullanici_adi or not yeni_sifre or not yeni_eposta:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
            return

        self.cursor.execute("INSERT INTO uyeler (kullanici_adi, sifre, eposta) VALUES (?, ?, ?)",
                            (yeni_kullanici_adi, yeni_sifre, yeni_eposta))
        self.connection.commit()
        messagebox.showinfo("Başarılı", "Üye kaydı başarıyla oluşturuldu.")
        # Kayıt penceresini kapat
        self.kayit_pencere.destroy()

    def bilgileri_guncelle(self):
        # Kullanıcı bilgilerini güncellemek için güncelleme penceresi oluştur
        self.guncelleme_pencere = tk.Toplevel()
        self.guncelleme_pencere.title("Bilgileri Güncelle")

        ttk.Label(self.guncelleme_pencere, text="Yeni Kullanıcı Adı:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.yeni_kullanici_adi_entry = ttk.Entry(self.guncelleme_pencere)
        self.yeni_kullanici_adi_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.guncelleme_pencere, text="Yeni Şifre:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.yeni_sifre_entry = ttk.Entry(self.guncelleme_pencere, show="*")
        self.yeni_sifre_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.guncelleme_pencere, text="Yeni E-Posta:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.yeni_eposta_entry = ttk.Entry(self.guncelleme_pencere)
        self.yeni_eposta_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.guncelleme_pencere, text="Bilgileri Güncelle", command=self.bilgileri_kaydet).grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def bilgileri_kaydet(self):
        yeni_kullanici_adi = self.yeni_kullanici_adi_entry.get()
        yeni_sifre = self.yeni_sifre_entry.get()
        yeni_eposta = self.yeni_eposta_entry.get()

        if not yeni_kullanici_adi and not yeni_sifre and not yeni_eposta:
            messagebox.showwarning("Uyarı", "En az bir alanı doldurun!")
            return

        if yeni_kullanici_adi:
            self.cursor.execute("UPDATE uyeler SET kullanici_adi=? WHERE kullanici_adi=?", (yeni_kullanici_adi, self.kullanici_adi))
            self.kullanici_adi = yeni_kullanici_adi
            messagebox.showinfo("Başarılı", "Kullanıcı adı başarıyla güncellendi.")

        if yeni_sifre:
            self.cursor.execute("UPDATE uyeler SET sifre=? WHERE kullanici_adi=?", (yeni_sifre, self.kullanici_adi))
            messagebox.showinfo("Başarılı", "Şifre başarıyla güncellendi.")

        if yeni_eposta:
            self.cursor.execute("UPDATE uyeler SET eposta=? WHERE kullanici_adi=?", (yeni_eposta, self.kullanici_adi))
            messagebox.showinfo("Başarılı", "E-Posta başarıyla güncellendi.")

        self.connection.commit()
        # Güncelleme penceresini kapat
        self.guncelleme_pencere.destroy()

    def uye_cikis(self):
        self.kullanici_adi = None
        self.hosgeldin_label.grid_remove()
        self.bilgileri_guncelle_btn.grid_remove()
        self.cikis_btn.grid_remove()
        self.giris_yap_btn.grid()
        self.kayit_ol_btn.grid()

    def siparis_yonetimi_goster(self):
        # Sipariş yönetim penceresini oluştur
        self.siparis_yonetimi_pencere = tk.Toplevel()
        self.siparis_yonetimi_pencere.title("Sipariş Yönetimi")

        # Sipariş seçimi için ListBox ve Scrollbar
        ttk.Label(self.siparis_yonetimi_pencere, text="Ürün Seçiniz:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.urun_listesi = tk.Listbox(self.siparis_yonetimi_pencere)
        self.urun_listesi.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        scrollbar = tk.Scrollbar(self.siparis_yonetimi_pencere, orient=tk.VERTICAL, command=self.urun_listesi.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.urun_listesi.config(yscrollcommand=scrollbar.set)

        # Mevcut stok verilerini getir ve ListBox'a ekle
        self.cursor.execute("SELECT urun_ismi FROM stok")
        stok_urunleri = self.cursor.fetchall()
        for urun in stok_urunleri:
            self.urun_listesi.insert(tk.END, urun[0])

        
        ttk.Button(self.siparis_yonetimi_pencere, text="Ekstra Stok Siparişi Ekle", command=self.ekstra_stok_siparisi_ekle).grid(row=2, column=1, padx=10, pady=10, sticky="we")



    def siparis_miktarini_belirle(self, urun_ismi):
        # Sipariş miktarını belirlemek için bir pencere oluştur
        self.siparis_miktar_pencere = tk.Toplevel()
        self.siparis_miktar_pencere.title("Sipariş Miktarını Belirle")

        ttk.Label(self.siparis_miktar_pencere, text=f"{urun_ismi} için sipariş miktarını giriniz:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.siparis_miktar_entry = ttk.Entry(self.siparis_miktar_pencere)
        self.siparis_miktar_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.siparis_miktar_pencere, text="Onayla", command=lambda: self.siparis_gonder(urun_ismi)).grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def siparis_gonder(self, urun_ismi, miktar):
        if not miktar:
            messagebox.showwarning("Uyarı", "Lütfen sipariş miktarını girin!")
            return

        try:
            miktar = int(miktar)
        except ValueError:
            messagebox.showwarning("Uyarı", "Sipariş miktarı sayı olmalıdır!")
            return

        self.siparis_miktar_pencere.destroy()

        # Seçili ürünün mevcut stok miktarını al
        mevcut_stok_miktari = self.stok_miktarini_al(urun_ismi)

        if miktar <= mevcut_stok_miktari:
            yeni_stok_miktari = mevcut_stok_miktari - miktar
            self.stok_miktari_guncelle(urun_ismi, yeni_stok_miktari)
            messagebox.showinfo("Sipariş Gönderildi", f"{miktar} adet {urun_ismi} siparişi başarıyla gönderildi.")
            self.gonderilen_siparisler_paneli.insert(tk.END, f"{miktar} adet {urun_ismi}\n")
        else:
            messagebox.showwarning("Stok Yetersiz", f"Stokta yeterli miktarda {urun_ismi} bulunmamaktadır.")

    def stok_miktari_guncelle(self, urun_ismi, yeni_stok_miktari):
        self.cursor.execute("UPDATE stok SET stok_miktari=? WHERE urun_ismi=?", (yeni_stok_miktari, urun_ismi))
        self.connection.commit()
        self.anlik_stok_miktar_label.config(text=f"Anlık Stok Miktarı: {yeni_stok_miktari}")


    def ekstra_stok_siparisi_ekle(self):
        # Seçilen ürünü al
        secili_urun = self.urun_listesi.get(tk.ACTIVE)
        
        # Ekstra stok siparişi için miktar girişi iste
        self.ekstra_stok_siparisi_pencere = tk.Toplevel()
        self.ekstra_stok_siparisi_pencere.title("Ekstra Stok Siparişi Ekle")

        ttk.Label(self.ekstra_stok_siparisi_pencere, text=f"{secili_urun} için ekstra stok miktarını giriniz:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ekstra_stok_miktar_entry = ttk.Entry(self.ekstra_stok_siparisi_pencere)
        self.ekstra_stok_miktar_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.ekstra_stok_siparisi_pencere, text="Sipariş Ver", command=lambda: self.ekstra_stok_siparisi_ver(secili_urun)).grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def ekstra_stok_siparisi_ver(self, urun_ismi):
        ekstra_stok_miktar = self.ekstra_stok_miktar_entry.get()

        if not ekstra_stok_miktar:
            messagebox.showwarning("Uyarı", "Lütfen miktarı girin!")
            return

        try:
            ekstra_stok_miktar = int(ekstra_stok_miktar)
        except ValueError:
            messagebox.showwarning("Uyarı", "Miktar bir sayı olmalıdır!")
            return

        # Sipariş verildiğini bildir
        messagebox.showinfo("Başarılı", "Sipariş verildi.")

        # Seçilen ürünün mevcut stok miktarını al
        stok_miktari = self.stok_miktarini_al(urun_ismi)
        if stok_miktari is not None:
            stok_miktari = int(stok_miktari)
        else:
            messagebox.showerror("Hata", "Stok miktarı belirlenemedi.")
            return

        # Seçilen ürünün stok miktarını arttır
        yeni_stok_miktari = stok_miktari + ekstra_stok_miktar
        self.cursor.execute("UPDATE stok SET stok_miktari=? WHERE urun_ismi=?", (yeni_stok_miktari, urun_ismi))
        self.connection.commit()

        # Tekrar Sorgula butonuna basıldığında güncel stok miktarını göster
        self.anlik_stok_label.config(text=f"Mevcut Stok: {yeni_stok_miktari}")
    
        # Başarı mesajı göster
        messagebox.showinfo("Başarılı", f"{ekstra_stok_miktar} adet {urun_ismi} stoklarına eklenmiştir.")
        self.ekstra_stok_siparisi_pencere.destroy()


    def stok_miktarini_al(self, urun_ismi):
        self.cursor.execute("SELECT stok_miktari FROM stok WHERE urun_ismi=?", (urun_ismi,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
# Uygulamayı başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = stockyonetim(root)
    root.mainloop()
