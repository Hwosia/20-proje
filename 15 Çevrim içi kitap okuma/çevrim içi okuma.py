import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class KütüphaneUygulaması:
    def __init__(self, root):
        self.root = root
        self.root.title("Çevrim İçi Kitap okuma sistemi")
        
        # SQLite veritabanı bağlantısı
        self.connection = sqlite3.connect("kutuphane.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS yorumlar (
                id INTEGER PRIMARY KEY,
                yorum TEXT,
                kitap_ad TEXT,
                yazar TEXT
            )
        """)
        self.connection.commit()

        # Kitap sorgulama ve ekleme alanı
        self.kitap_sorgula_frame = ttk.LabelFrame(self.root, text="Kitap Sorgulama ve Ekleme")
        self.kitap_sorgula_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.uye_id = None
        ttk.Label(self.kitap_sorgula_frame, text="Kitap Adı:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.kitap_adı_entry = ttk.Entry(self.kitap_sorgula_frame)
        self.kitap_adı_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.kitap_sorgula_frame, text="Yazar:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.kitap_yazarı_entry = ttk.Entry(self.kitap_sorgula_frame)
        self.kitap_yazarı_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.kitap_sorgula_frame, text="Yayın Evi:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.kitap_yayın_evi_entry = ttk.Entry(self.kitap_sorgula_frame)
        self.kitap_yayın_evi_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")
        self.kitaplar_liste = ttk.Treeview(self.root, columns=("ID", "Ad", "Yazar", "Yayın Evi", "Stok"), show="headings")
        self.kitaplar_liste.heading("ID", text="ID")
        self.kitaplar_liste.heading("Ad", text="Ad")
        self.kitaplar_liste.heading("Yazar", text="Yazar")

        self.yorumlar_liste = ttk.Treeview(self.root, columns=("Yorum", "Yazar"), show="headings")
        self.yorumlar_liste.heading("Yorum", text="Yorum")
        self.yorumlar_liste.heading("Yazar", text="Yazar")
        self.yorumlar_liste.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Yorum yap butonu ekleyelim
        self.yorum_yap_btn = ttk.Button(self.kitap_sorgula_frame, text="Yorum Yap", command=self.yorum_yap)
        self.yorum_yap_btn.grid(row=3, column=3, padx=10, pady=10, sticky="we")
        self.kitaplar_liste.heading("Yayın Evi", text="Yayın Evi")
        self.kitaplar_liste.heading("Stok", text="Stok")
        self.kitaplar_liste.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        ttk.Button(self.kitap_sorgula_frame, text="Sorgula", command=self.kitap_sorgula).grid(row=3, column=0, padx=10, pady=10, sticky="we")
        self.secili_kitap_deger = None
        # Ödünç Geçmişi
        self.odunc_gecmisi_btn = ttk.Button(self.kitap_sorgula_frame, text="Ödünç Geçmişi", command=self.odunc_gecmisi_goster)
        self.odunc_gecmisi_btn.grid(row=3, column=2, padx=10, pady=10, sticky="we")

                # Yorumları silme butonu ekleyelim
        self.yorum_sil_btn = ttk.Button(self.kitap_sorgula_frame, text="Yorumları Sil", command=self.yorumlari_sil)
        self.yorum_sil_btn.grid(row=4, column=3, padx=10, pady=10, sticky="we")
        self.yorumlari_yukle()
        # Üye İşlemleri
        self.uye_frame = ttk.LabelFrame(self.root, text="Üye İşlemleri")
        self.uye_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.uye_giris_btn = ttk.Button(self.uye_frame, text="Üye Girişi", command=self.uye_giris)
        self.uye_giris_btn.grid(row=0, column=0, padx=10, pady=5, sticky="we")

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

        # Grid yöneticisine ağırlık ekleyerek bileşenlerin boyutlarını orantılı olarak büyütme
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Giriş durumu kontrolü için kullanıcı adı değişkeni
        self.kullanici_adi = None
        self.odunc_gecmisi_pencere = None
    def uye_giris(self):
        # Üye giriş penceresi oluşturma
        self.giris_pencere = tk.Toplevel(self.root)
        self.giris_pencere.title("Üye Girişi")

        ttk.Label(self.giris_pencere, text="Kullanıcı Adı:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.kullanici_adi_entry = ttk.Entry(self.giris_pencere)
        self.kullanici_adi_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.giris_pencere, text="Şifre:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.sifre_entry = ttk.Entry(self.giris_pencere, show="*")
        self.sifre_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.giris_pencere, text="Giriş Yap", command=self.uye_giris_onay).grid(row=2, columnspan=2, pady=10)

    def uye_giris_onay(self):
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()

        self.cursor.execute("SELECT * FROM kutuphane_uyeler WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
        uye = self.cursor.fetchone()

        if uye:
            self.kullanici_adi = kullanici_adi
            self.uye_id = uye[0]  # Uye ID'sini saklayalım
            self.hosgeldin_label.config(text="Hoşgeldin, {}".format(kullanici_adi))
            self.kayit_ol_btn.grid_remove()
            self.uye_giris_btn.grid_remove()
            self.bilgileri_guncelle_btn.grid()
            self.cikis_btn.grid()
            messagebox.showinfo("Giriş Başarılı", "Hoş geldiniz, {}!".format(kullanici_adi))
            self.giris_pencere.destroy()
        else:
            messagebox.showerror("Giriş Başarısız", "Kullanıcı adı veya şifre yanlış!")

    def uye_cikis(self):
        self.kullanici_adi = None
        self.hosgeldin_label.config(text="")
        self.uye_giris_btn.grid()
        self.kayit_ol_btn.grid()
        self.bilgileri_guncelle_btn.grid_remove()
        self.cikis_btn.grid_remove()
        messagebox.showinfo("Çıkış Başarılı", "Çıkış yaptınız!")

    def bilgileri_guncelle(self):
        # Kullanıcı bilgilerini güncellemek için bir pencere oluşturma
        self.guncelleme_pencere = tk.Toplevel(self.root)
        self.guncelleme_pencere.title("Bilgileri Güncelle")

        ttk.Label(self.guncelleme_pencere, text="Ad:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.guncelle_ad_entry = ttk.Entry(self.guncelleme_pencere)
        self.guncelle_ad_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.guncelleme_pencere, text="Soyad:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.guncelle_soyad_entry = ttk.Entry(self.guncelleme_pencere)
        self.guncelle_soyad_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.guncelleme_pencere, text="Telefon:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.guncelle_telefon_entry = ttk.Entry(self.guncelleme_pencere)
        self.guncelle_telefon_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.guncelleme_pencere, text="Kullanıcı Adı:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.guncelle_kullanici_adi_entry = ttk.Entry(self.guncelleme_pencere)
        self.guncelle_kullanici_adi_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.guncelleme_pencere, text="Şifre:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.guncelle_sifre_entry = ttk.Entry(self.guncelleme_pencere, show="*")
        self.guncelle_sifre_entry.grid(row=4, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.guncelleme_pencere, text="Güncelle", command=self.bilgileri_guncelle_onay).grid(row=5, columnspan=2, pady=10)

    def bilgileri_guncelle_onay(self):
        ad = self.guncelle_ad_entry.get()
        soyad = self.guncelle_soyad_entry.get()
        telefon = self.guncelle_telefon_entry.get()
        kullanici_adi = self.guncelle_kullanici_adi_entry.get()
        sifre = self.guncelle_sifre_entry.get()

        self.cursor.execute("UPDATE kutuphane_uyeler SET ad=?, soyad=?, telefon=?, kullanici_adi=?, sifre=? WHERE kullanici_adi=?",
                        (ad, soyad, telefon, kullanici_adi, sifre, self.kullanici_adi))
        self.connection.commit()

        self.hosgeldin_label.config(text="Hoşgeldin, {}".format(kullanici_adi))
        messagebox.showinfo("Güncelleme Başarılı", "Bilgiler başarıyla güncellendi!")
        self.guncelleme_pencere.destroy()

    def uye_kayit(self):
        # Üye kayıt penceresi oluşturma
        self.kayit_pencere = tk.Toplevel(self.root)
        self.kayit_pencere.title("Üye Kayıt")

        ttk.Label(self.kayit_pencere, text="Ad:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ad_entry = ttk.Entry(self.kayit_pencere)
        self.ad_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.kayit_pencere, text="Soyad:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.soyad_entry = ttk.Entry(self.kayit_pencere)
        self.soyad_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.kayit_pencere, text="Telefon:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.telefon_entry = ttk.Entry(self.kayit_pencere)
        self.telefon_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.kayit_pencere, text="Kullanıcı Adı:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.kayit_kullanici_adi_entry = ttk.Entry(self.kayit_pencere)
        self.kayit_kullanici_adi_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(self.kayit_pencere, text="Şifre:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.kayit_sifre_entry = ttk.Entry(self.kayit_pencere, show="*")
        self.kayit_sifre_entry.grid(row=4, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.kayit_pencere, text="Kayıt Ol", command=self.uye_kayit_onay).grid(row=5, columnspan=2, pady=10)

    def uye_kayit_onay(self):
        ad = self.ad_entry.get()
        soyad = self.soyad_entry.get()
        telefon = self.telefon_entry.get()
        kullanici_adi = self.kayit_kullanici_adi_entry.get()
        sifre = self.kayit_sifre_entry.get()

        self.cursor.execute("INSERT INTO kutuphane_uyeler (ad, soyad, telefon, kullanici_adi, sifre) VALUES (?, ?, ?, ?, ?)",
                            (ad, soyad, telefon, kullanici_adi, sifre))
        self.connection.commit()
        messagebox.showinfo("Kayıt Başarılı", "Üyelik başarıyla oluşturuldu!")
        self.kayit_pencere.destroy()

    def kitap_sorgula(self):
        kitap_adı = self.kitap_adı_entry.get()
        kitap_yazarı = self.kitap_yazarı_entry.get()
        kitap_yayın_evi = self.kitap_yayın_evi_entry.get()

        sorgu = "SELECT * FROM kutuphane_kitapları WHERE "
        parametreler = []

        if kitap_adı:
            sorgu += "ad LIKE ? AND "
            parametreler.append('%' + kitap_adı + '%')

        if kitap_yazarı:
            sorgu += "yazar LIKE ? AND "
            parametreler.append('%' + kitap_yazarı + '%')

        if kitap_yayın_evi:
            sorgu += "yayin_evi LIKE ? AND "
            parametreler.append('%' + kitap_yayın_evi + '%')

        sorgu = sorgu.rstrip(" AND ")

        self.cursor.execute(sorgu, parametreler)
        kitaplar = self.cursor.fetchall()
        self.odunc_al_btn = ttk.Button(self.kitap_sorgula_frame, text="Ödünç Al", command=self.odunc_al)
        self.odunc_al_btn.grid(row=3, column=1, padx=10, pady=10, sticky="we")

        # Eğer mevcut bir kitaplar_liste varsa, önceki verileri sil
        if hasattr(self, 'kitaplar_liste'):
            for i in self.kitaplar_liste.get_children():
                self.kitaplar_liste.delete(i)
        for kitap in kitaplar:
            self.kitaplar_liste.insert("", "end", values=kitap)
        self.kitaplar_liste.bind("<Double-1>", self.secili_kitap)
    
    def secili_kitap(self, event):
        item = self.kitaplar_liste.selection()[0]
        self.secili_kitap_deger = self.kitaplar_liste.item(item, "values")

    def odunc_al(self):
        if self.uye_id is None:
            messagebox.showerror("Hata", "Ödünç alabilmek için önce üye girişi yapmalısınız!")
            return

        # Ödünç alma işlemi için yeni bir pencere oluşturma
        self.odunc_pencere = tk.Toplevel(self.root)
        self.odunc_pencere.title("Ödünç Alma")

        ttk.Label(self.odunc_pencere, text="Kaç gün ödünç almak istiyorsunuz? (1-10):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.gun_entry = ttk.Entry(self.odunc_pencere)
        self.gun_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.odunc_pencere, text="Tamam", command=self.odunc_onayla).grid(row=1, columnspan=2, pady=10)

    def odunc_onayla(self):
        if self.uye_id is None:
            messagebox.showerror("Hata", "Ödünç alabilmek için üye girişi yapmalısınız!")
            return

        if self.secili_kitap_deger is None:
            messagebox.showerror("Hata", "Lütfen bir kitap seçin!")
            return

        try:
            gun = int(self.gun_entry.get())
            if 1 <= gun <= 10:
                kitap_id = self.secili_kitap_deger[0]
                self.cursor.execute("INSERT INTO odunc (kitap_id, uye_id, gun) VALUES (?, ?, ?)",
                            (kitap_id, self.uye_id, gun))
                self.connection.commit()
                messagebox.showinfo("Ödünç Alma Başarılı", f"{gun} gün ödünç alındı!")

                # Ödünç alınan kitabı ödünç geçmişine ekleyin
                self.odunc_gecmisi_liste.insert("", "end", values=self.secili_kitap_deger + (gun,))
            else:
                messagebox.showerror("Hata", "Lütfen 1-10 arasında bir değer girin!")
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir sayı girin!")

    
    def odunc_gecmisi_goster(self):
        # Ödünç geçmişi göstermek için yeni bir pencere oluşturma
        self.odunc_gecmisi_pencere = tk.Toplevel(self.root)
        self.odunc_gecmisi_pencere.title("Ödünç Geçmişi")

        # Ödünç geçmişi için Treeview oluşturma
        self.odunc_gecmisi_liste = ttk.Treeview(self.odunc_gecmisi_pencere, columns=("ID", "Kitap Adı", "Yazar", "Yayın Evi", "Ödünç Günü"))
        self.odunc_gecmisi_liste.heading("ID", text="ID")
        self.odunc_gecmisi_liste.heading("Kitap Adı", text="Kitap Adı")
        self.odunc_gecmisi_liste.heading("Yazar", text="Yazar")
        self.odunc_gecmisi_liste.heading("Yayın Evi", text="Yayın Evi")
        self.odunc_gecmisi_liste.heading("Ödünç Günü", text="Ödünç Günü")
        self.odunc_gecmisi_liste.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Ödünç geçmişi bilgilerini veritabanından çekme
        self.cursor.execute("""
            SELECT odunc.id, kutuphane_kitapları.ad, kutuphane_kitapları.yazar, kutuphane_kitapları.yayin_evi, odunc.gun
            FROM odunc
            JOIN kutuphane_kitapları ON odunc.kitap_id = kutuphane_kitapları.id
            WHERE odunc.uye_id=?
        """, (self.uye_id,))

        odunc_gecmisi = self.cursor.fetchall()

        # Treeview'e ödünç geçmişi bilgilerini ekleme
        for row in odunc_gecmisi:
            self.odunc_gecmisi_liste.insert("", "end", values=row)

        # İade Et butonu ekleyin
        self.iade_et_btn = ttk.Button(self.odunc_gecmisi_pencere, text="İade Et", command=self.kitap_iade_et)
        self.iade_et_btn.grid(row=1, column=0, padx=10, pady=10)

        # Kitabı Oku butonu ekleyin
        self.kitabi_oku_btn = ttk.Button(self.odunc_gecmisi_pencere, text="Kitabı Oku", command=self.kitabi_oku)
        self.kitabi_oku_btn.grid(row=1, column=1, padx=10, pady=10)

    def kitabi_oku(self):
        selected_item = self.odunc_gecmisi_liste.selection()
        if selected_item:
            # Seçilen kitabın adını al
            kitap_adi = self.odunc_gecmisi_liste.item(selected_item, "values")[1]
            messagebox.showinfo("Kitap Okunuyor", f"{kitap_adi} kitabı okunuyor!")
        else:
            messagebox.showerror("Hata", "Lütfen bir kitap seçin!")


    def kitap_iade_et(self):
        selected_item = self.odunc_gecmisi_liste.selection()[0]
        odunc_id = self.odunc_gecmisi_liste.item(selected_item, "values")[0]

        self.cursor.execute("DELETE FROM odunc WHERE id=?", (odunc_id,))
        self.connection.commit()

        messagebox.showinfo("İade Başarılı", "Kitap iade edildi!")

        # Seçili ödünç işlemini Treeview'den sil
        self.odunc_gecmisi_liste.delete(selected_item)

    def yorum_yap(self):
        if self.secili_kitap_deger is None:
            messagebox.showerror("Hata", "Lütfen bir kitap seçin!")
            return

        # secili_kitap özelliğini tanımlayın ve değerini secili_kitap_deger'e ata
        self.secili_kitap = self.secili_kitap_deger

        # Yorum yapma penceresini oluşturalım
        self.yorum_pencere = tk.Toplevel(self.root)
        self.yorum_pencere.title("Yorum Yap")

        ttk.Label(self.yorum_pencere, text="Kitap:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(self.yorum_pencere, text=self.secili_kitap[1]).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.yorum_pencere, text="Yazar:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(self.yorum_pencere, text=self.secili_kitap[2]).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.yorum_pencere, text="Yorumunuzu Yazın:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.yorum_entry = ttk.Entry(self.yorum_pencere, width=50)
        self.yorum_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        ttk.Button(self.yorum_pencere, text="Onayla", command=self.yorumu_kaydet).grid(row=3, columnspan=2, pady=10)

    def yorumu_kaydet(self):
        yorum = self.yorum_entry.get()
        if yorum and self.secili_kitap_deger:
            # Yorumu veritabanına ekleyin
            self.cursor.execute("INSERT INTO yorumlar (yorum, kitap_ad, yazar) VALUES (?, ?, ?)",
                                (yorum, self.secili_kitap_deger[1], self.secili_kitap_deger[2]))
            self.connection.commit()

            # Yorumu ana sayfadaki yorumlar listesine ekleyin
            self.yorumlar_liste.insert("", "end", values=(yorum, self.secili_kitap_deger[1]))

            # Yorum penceresini kapatın
            self.yorum_pencere.destroy()
        else:
            messagebox.showerror("Hata", "Lütfen bir yorum yazın ve bir kitap seçin!")

    def secili_kitap(self, event):
        # Kitap listesinden seçilen kitabı al
        item = self.kitaplar_liste.selection()[0]
        self.secili_kitap_deger = self.kitaplar_liste.item(item, "values")

    def yorumlari_sil(self):
        if self.uye_id is None:
            messagebox.showerror("Hata", "Yorumları silmek için önce üye girişi yapmalısınız!")
            return
        # Seçili yorumları al
        selected_items = self.yorumlar_liste.selection()

        if selected_items:
            for item in selected_items:
                # Seçili yorumların değerlerini al
                values = self.yorumlar_liste.item(item, "values")

                if values:
                    yorum = values[0]

                    # Yorumu arayüzden sil
                    self.yorumlar_liste.delete(item)

                    # Yorumu veritabanından sil
                    self.cursor.execute("DELETE FROM yorumlar WHERE yorum=?", (yorum,))
                    self.connection.commit()
        else:
            messagebox.showerror("Hata", "Lütfen silinecek bir yorum seçin!")

    def yorumlari_yukle(self):
        # Önce tüm mevcut yorumları temizleyin
        for item in self.yorumlar_liste.get_children():
            self.yorumlar_liste.delete(item)

        # Veritabanından yorumları yükle
        self.cursor.execute("SELECT yorum, kitap_ad FROM yorumlar")
        yorumlar = self.cursor.fetchall()

        for yorum, kitap_ad in yorumlar:
            self.yorumlar_liste.insert("", "end", values=(yorum, kitap_ad))
        

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = KütüphaneUygulaması(root)
    root.mainloop()