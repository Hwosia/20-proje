import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random

conn = sqlite3.connect('sporcular.db')
cursor = conn.cursor()

spor_isinma_hareketleri = {
    "Futbol": [
        "Koşu",
        "Koşu ters",
        "Yüksek diz kaldırma",
        "Kısa pas",
        "Topla koşu",
        "Koşu sırasında germe"
        # Diğer ısınma hareketleri eklenebilir
    ],
    "Basketbol": [
        "Koşu",
        "Top sektirme",
        "Top pas",
        "Hareketli şutlar",
        "Yerden top alma",
        "Denge hareketleri"
        # Diğer ısınma hareketleri eklenebilir
    ],
    # Diğer sporlar için de aynı şekilde ısınma hareketleri listesi eklenebilir
}

class SporRandevuUygulamasi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spor Randevu Uygulaması")

        self.create_widgets()

        self.create_giris_tab()  # Giriş sekmesini oluştur

    def create_widgets(self):
        self.tabControl = ttk.Notebook(self)

        self.kayit_tab = ttk.Frame(self.tabControl)
        self.giris_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.kayit_tab, text="Kayıt Ol")
        self.tabControl.add(self.giris_tab, text="Giriş Yap")

        self.tabControl.pack(expand=1, fill="both")

        self.create_kayit_tab()

    def create_kayit_tab(self):
        self.kayit_tab_label = ttk.Label(self.kayit_tab, text="Kayıt Ol")
        self.kayit_tab_label.grid(row=0, column=0, padx=10, pady=10)

        self.isim_label = ttk.Label(self.kayit_tab, text="İsim Soyisim:")
        self.isim_label.grid(row=1, column=0, padx=10, pady=5)
        self.isim_entry = ttk.Entry(self.kayit_tab)
        self.isim_entry.grid(row=1, column=1, padx=10, pady=5)

        self.kimlik_label = ttk.Label(self.kayit_tab, text="Kimlik Numarası:")
        self.kimlik_label.grid(row=2, column=0, padx=10, pady=5)
        self.kimlik_entry = ttk.Entry(self.kayit_tab)
        self.kimlik_entry.grid(row=2, column=1, padx=10, pady=5)

        self.sifre_label = ttk.Label(self.kayit_tab, text="Şifre:")
        self.sifre_label.grid(row=3, column=0, padx=10, pady=5)
        self.sifre_entry = ttk.Entry(self.kayit_tab, show="*")
        self.sifre_entry.grid(row=3, column=1, padx=10, pady=5)

        self.kayit_button = ttk.Button(self.kayit_tab, text="Kayıt Ol", command=self.kayit_ol)
        self.kayit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def create_giris_tab(self):
        self.giris_tab_label = ttk.Label(self.giris_tab, text="Giriş Yap")
        self.giris_tab_label.grid(row=0, column=0, padx=10, pady=10)

        self.giris_kimlik_label = ttk.Label(self.giris_tab, text="Kimlik Numarası:")
        self.giris_kimlik_label.grid(row=1, column=0, padx=10, pady=5)
        self.giris_kimlik_entry = ttk.Entry(self.giris_tab)
        self.giris_kimlik_entry.grid(row=1, column=1, padx=10, pady=5)

        self.giris_sifre_label = ttk.Label(self.giris_tab, text="Şifre:")
        self.giris_sifre_label.grid(row=2, column=0, padx=10, pady=5)
        self.giris_sifre_entry = ttk.Entry(self.giris_tab, show="*")
        self.giris_sifre_entry.grid(row=2, column=1, padx=10, pady=5)

        self.giris_button = ttk.Button(self.giris_tab, text="Giriş Yap", command=self.giris)
        self.giris_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)


    def kayit_ol(self):
        isim = self.isim_entry.get()
        kimlik = self.kimlik_entry.get()
        sifre = self.sifre_entry.get()

        cursor.execute("INSERT INTO sporcular (isim, kimlik, sifre) VALUES (?, ?, ?)", (isim, kimlik, sifre))
        conn.commit()

        messagebox.showinfo("Başarılı", "Kayıt başarıyla oluşturuldu. Şimdi giriş yapabilirsiniz.")

        self.tabControl.select(self.giris_tab)

        self.isim_entry.delete(0, tk.END)
        self.kimlik_entry.delete(0, tk.END)
        self.sifre_entry.delete(0, tk.END)

    def giris(self):
        kimlik = self.giris_kimlik_entry.get()
        sifre = self.giris_sifre_entry.get()

        cursor.execute("SELECT * FROM sporcular WHERE kimlik = ? AND sifre = ?", (kimlik, sifre))
        kullanici = cursor.fetchone()

        if kullanici:
            self.create_randevu_tab()
            self.tabControl.forget(self.kayit_tab)
            self.tabControl.forget(self.giris_tab)
            self.tabControl.select(self.randevu_tab)
        else:
            messagebox.showerror("Hata", "Geçersiz kimlik numarası veya şifre")

    def create_randevu_tab(self):
        self.randevu_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.randevu_tab, text="Spor Randevuları")

        self.randevu_tab_label = ttk.Label(self.randevu_tab, text="Spor Randevu İşlemleri")
        self.randevu_tab_label.grid(row=0, column=0, padx=10, pady=10)

        self.randevu_al_button = ttk.Button(self.randevu_tab, text="Randevu Al", command=self.randevu_al)
        self.randevu_al_button.grid(row=1, column=0, padx=10, pady=5)

        self.randevu_iptal_button = ttk.Button(self.randevu_tab, text="Randevu İptal Et", command=self.randevu_iptal)
        self.randevu_iptal_button.grid(row=2, column=0, padx=10, pady=5)

        self.ilerleme_takip_button = ttk.Button(self.randevu_tab, text="İlerleme Takip", command=self.ilerleme_takip)
        self.ilerleme_takip_button.grid(row=3, column=0, padx=10, pady=5)  # İlerleme Takip butonu eklendi

        self.rapor_gecmisi_button = ttk.Button(self.randevu_tab, text="Rapor Geçmişi", command=self.rapor_gecmisi_goster)
        self.rapor_gecmisi_button.grid(row=4, column=0, padx=10, pady=5)
        

        self.cikis_button = ttk.Button(self.randevu_tab, text="Çıkış", command=self.cikis)
        self.cikis_button.grid(row=6, column=0, padx=10, pady=5)

        self.randevu_listbox = tk.Listbox(self.randevu_tab, width=70, height=15)
        self.randevu_listbox.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

    # Kullanıcının mevcut randevularını göster
        self.randevulari_goster()



    def randevu_al(self):
        self.uzmanlik_seci = tk.StringVar()  # Kullanıcının seçtiği spor dalını tutacak değişken
        self.randevu_al_pencere = tk.Toplevel(self)
        self.randevu_al_pencere.title("Spor Randevu Al")

        self.uzmanlik_label = ttk.Label(self.randevu_al_pencere, text="Spor Seçin:")
        self.uzmanlik_label.grid(row=0, column=0, padx=10, pady=5)

        self.uzmanlik_combobox = ttk.Combobox(self.randevu_al_pencere, values=list(spor_isinma_hareketleri.keys()), textvariable=self.uzmanlik_seci)
        self.uzmanlik_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.uzmanlik_combobox.bind("<<ComboboxSelected>>", self.antrenorleri_getir)  # Spor seçildiğinde antrenörleri getir

        self.doktor_label = ttk.Label(self.randevu_al_pencere, text="Antrenör Seçin:")
        self.doktor_label.grid(row=1, column=0, padx=10, pady=5)

        self.doktor_combobox = ttk.Combobox(self.randevu_al_pencere)
        self.doktor_combobox.grid(row=1, column=1, padx=10, pady=5)

        self.boy_label = ttk.Label(self.randevu_al_pencere, text="Boy (cm):")
        self.boy_label.grid(row=2, column=0, padx=10, pady=5)
        self.boy_entry = ttk.Entry(self.randevu_al_pencere)
        self.boy_entry.grid(row=2, column=1, padx=10, pady=5)

        self.kilo_label = ttk.Label(self.randevu_al_pencere, text="Kilo (kg):")
        self.kilo_label.grid(row=3, column=0, padx=10, pady=5)
        self.kilo_entry = ttk.Entry(self.randevu_al_pencere)
        self.kilo_entry.grid(row=3, column=1, padx=10, pady=5)

        self.gun_label = ttk.Label(self.randevu_al_pencere, text="Gün Seçin:")
        self.gun_label.grid(row=4, column=0, padx=10, pady=5)

        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
        self.gun_combobox = ttk.Combobox(self.randevu_al_pencere, values=gunler)
        self.gun_combobox.grid(row=4, column=1, padx=10, pady=5)

        self.zaman_label = ttk.Label(self.randevu_al_pencere, text="Zaman:")
        self.zaman_label.grid(row=5, column=0, padx=10, pady=5)

        zamanlar = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
        self.zaman_combobox = ttk.Combobox(self.randevu_al_pencere, values=zamanlar)
        self.zaman_combobox.grid(row=5, column=1, padx=10, pady=5)

        self.randevu_olustur_button = ttk.Button(self.randevu_al_pencere, text="Randevu Al", command=self.randevu_tamamla)
        self.randevu_olustur_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def antrenorleri_getir(self, *args):
        uzmanlik = self.uzmanlik_seci.get()  # Kullanıcının seçtiği spor dalını al

        antrenorler = {
            "Futbol": ["Ali Kaya", "Ayşe Yılmaz", "Mehmet Demir"],
            "Basketbol": ["Selim Yıldız", "Fatma Karadağ", "Burak Tekin"],
            "Voleybol": ["Elif Öztürk", "Hakan Kaya", "Seda Özdemir"],
            "Yüzme": ["İsmail Yılmaz", "Nihan Yıldız", "Emre Demir"],
            "Fitness": ["Sevgi Kaya", "Cem Demir", "Zeynep Yılmaz"]
        }

        self.doktor_combobox['values'] = antrenorler.get(uzmanlik, [])

    def randevu_tamamla(self):
        kimlik = self.giris_kimlik_entry.get()
        uzmanlik = self.uzmanlik_combobox.get()
        doktor = self.doktor_combobox.get()
        gun = self.gun_combobox.get()
        zaman = self.zaman_combobox.get()

        tarih = f"{gun} {zaman}"

        cursor.execute("SELECT * FROM spor_randevulari WHERE doktor = ? AND zaman = ?", (doktor, tarih))
        varmi = cursor.fetchone()

        if varmi:
            messagebox.showerror("Hata", "Seçilen antrenör ve zaman diliminde randevu bulunmaktadır. Lütfen farklı bir zaman dilimi seçiniz.")
            return

        cursor.execute("INSERT INTO spor_randevulari (kimlik, uzmanlik, doktor, zaman) VALUES (?, ?, ?, ?)", (kimlik, uzmanlik, doktor, tarih))
        conn.commit()

        messagebox.showinfo("Başarılı", "Randevunuz alınmıştır.")

        self.uzmanlik_combobox.set('')
        self.doktor_combobox.set('')
        self.gun_combobox.set('')
        self.zaman_combobox.set('')

        self.randevulari_goster()

    def randevu_iptal(self):
        selected_index = self.randevu_listbox.curselection()

        if not selected_index:
            messagebox.showerror("Hata", "Lütfen iptal etmek istediğiniz randevuyu seçin.")
            return

        selected_id = self.randevu_listbox.get(selected_index[0]).split(",")[0].split(":")[1].strip()

        cursor.execute("DELETE FROM spor_randevulari WHERE id = ?", (selected_id,))
        conn.commit()

        messagebox.showinfo("Başarılı", "Randevunuz iptal edilmiştir.")

        self.randevulari_goster()

    def randevulari_goster(self):
        kimlik = self.giris_kimlik_entry.get()
        
        cursor.execute("SELECT id, uzmanlik, doktor, zaman FROM spor_randevulari WHERE kimlik = ?", (kimlik,))
        randevular = cursor.fetchall()
        
        self.randevu_listbox.delete(0, tk.END)
        
        for randevu in randevular:
            randevu_str = f"ID: {randevu[0]}, Uzmanlık: {randevu[1]}, Doktor: {randevu[2]}, Zaman: {randevu[3]}"
            self.randevu_listbox.insert(tk.END, randevu_str)

    def ilerleme_takip_goster(self, spor, hareket_setleri):
        self.ilerleme_takip_pencere = tk.Toplevel(self)
        self.ilerleme_takip_pencere.title("İlerleme Takip")

        spor_label = ttk.Label(self.ilerleme_takip_pencere, text=f"{spor} İlerleme Takip")
        spor_label.grid(row=0, column=0, padx=10, pady=10)

        for i, hareket_seti in enumerate(hareket_setleri, start=1):
            set_label = ttk.Label(self.ilerleme_takip_pencere, text=f"Hareket Seti {i}: {', '.join(hareket_seti)}")
            set_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        rapor_button = ttk.Button(self.ilerleme_takip_pencere, text="Rapor Çıkar", command=lambda: self.rapor_cikar(spor, hareket_setleri))
        rapor_button.grid(row=i+1, column=0, padx=10, pady=10)

    def spor_ısınma_hareketleri(self, spor):
        spor_isinma_hareketleri = {
            "Futbol": [
                "Koşu",
                "Koşu ters",
                "Yüksek diz kaldırma",
                "Kısa pas",
                "Topla koşu",
                "Koşu sırasında germe"
                # Diğer ısınma hareketleri eklenebilir
            ],
            "Basketbol": [
                "Koşu",
                "Top sektirme",
                "Top pas",
                "Hareketli şutlar",
                "Yerden top alma",
                "Denge hareketleri"
                # Diğer ısınma hareketleri eklenebilir
            ],
            # Diğer sporlar için de aynı şekilde ısınma hareketleri listesi eklenebilir
        }

        return spor_isinma_hareketleri.get(spor, [])

    def ilerleme_takip(self):
        selected_index = self.randevu_listbox.curselection()

        if not selected_index:
            messagebox.showerror("Hata", "Lütfen takip etmek istediğiniz randevuyu seçin.")
            return

        selected_id = self.randevu_listbox.get(selected_index[0]).split(",")[0].split(":")[1].strip()

        cursor.execute("SELECT uzmanlik FROM spor_randevulari WHERE id = ?", (selected_id,))
        spor = cursor.fetchone()[0]

        hareket_setleri = [random.sample(self.spor_ısınma_hareketleri(spor), 3) for _ in range(3)]

        self.ilerleme_takip_goster(spor, hareket_setleri)
        
    def rapor_cikar(self, spor, hareket_setleri):
        self.rapor_cikar_pencere = tk.Toplevel(self)
        self.rapor_cikar_pencere.title("Spor Raporu")

        kilo_label = ttk.Label(self.rapor_cikar_pencere, text="Güncel Kilo (kg):")
        kilo_label.grid(row=0, column=0, padx=10, pady=5)
        self.guncel_kilo = ttk.Entry(self.rapor_cikar_pencere)
        self.guncel_kilo.grid(row=0, column=1, padx=10, pady=5)

        boy_label = ttk.Label(self.rapor_cikar_pencere, text="Güncel Boy (cm):")
        boy_label.grid(row=1, column=0, padx=10, pady=5)
        self.guncel_boy = ttk.Entry(self.rapor_cikar_pencere)
        self.guncel_boy.grid(row=1, column=1, padx=10, pady=5)

        rapor_button = ttk.Button(self.rapor_cikar_pencere, text="Rapor Çıkar", command=lambda: self.rapor_olustur(spor, hareket_setleri))
        rapor_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # selected_id'yi al
        selected_index = self.randevu_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Hata", "Lütfen takip etmek istediğiniz randevuyu seçin.")
            return

        self.selected_id = self.randevu_listbox.get(selected_index[0]).split(",")[0].split(":")[1].strip()

    def rapor_olustur(self, spor, hareket_setleri):
        kimlik = self.giris_kimlik_entry.get()

        # Veritabanından randevu bilgilerini al
        cursor.execute("SELECT uzmanlik, doktor, zaman FROM spor_randevulari WHERE id = ?", (self.selected_id,))
        randevu = cursor.fetchone()

        # Randevu bilgisini yazdır
        print(randevu)

        # Kullanıcının girdiği güncel kilo ve boy bilgilerini al
        guncel_kilo_str = self.guncel_kilo.get()
        guncel_boy_str = self.guncel_boy.get()

        if not guncel_kilo_str or not guncel_boy_str:
            messagebox.showerror("Hata", "Lütfen güncel kilo ve boy bilgilerini giriniz.")
            return

        # Güncel kilo ve boy bilgilerini float'a çevir
        guncel_kilo = float(guncel_kilo_str)
        guncel_boy = float(guncel_boy_str)

        # Raporu oluştur
        rapor = f"Spor: {spor}\n"
        rapor += "Girdiği Bilgiler:\n"
        if randevu:
            uzmanlik, doktor, zaman = randevu
            rapor += f"Spor: {uzmanlik}, Hoca: {doktor}, Zaman: {zaman}\n"
        
        # Yapılan hareketleri rapora ekle
        rapor += "Yapılan Hareketler:\n"
        for i, hareket_seti in enumerate(hareket_setleri, start=1):
            rapor += f"Hareket Seti {i}: {', '.join(hareket_seti)}\n"

        # Güncel kilo ve boyu rapora ekle
        rapor += f"Güncel Kilo: {guncel_kilo:.2f} kg\n"
        rapor += f"Güncel Boy: {guncel_boy:.2f} cm\n"

        # Oluşturulan raporu veritabanına kaydet
        cursor.execute("INSERT INTO spor_raporlari (kimlik, rapor) VALUES (?, ?)", (kimlik, rapor))
        conn.commit()

        # Oluşturulan raporu ekrana yazdır
        rapor_text = tk.Text(self.rapor_cikar_pencere, width=50, height=15)
        rapor_text.insert(tk.END, rapor)
        rapor_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.rapor_cikar_pencere.destroy()

    def rapor_gecmisi_goster(self):
        kimlik = self.giris_kimlik_entry.get()
        
        cursor.execute("SELECT * FROM spor_raporlari WHERE kimlik = ?", (kimlik,))
        raporlar = cursor.fetchall()
        
        rapor_gecmisi_pencere = tk.Toplevel(self)
        rapor_gecmisi_pencere.title("Rapor Geçmişi")

        rapor_listbox = tk.Listbox(rapor_gecmisi_pencere, width=70, height=15)
        rapor_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        for rapor in raporlar:
            rapor_str = f"ID: {rapor[0]}, Spor: {rapor[1]}, Bilgiler: {rapor[2]}"
            rapor_listbox.insert(tk.END, rapor_str)

        goruntule_button = ttk.Button(rapor_gecmisi_pencere, text="Geçmişi Görüntüle", command=lambda: self.gecmisi_goruntule(kimlik, rapor_listbox))
        goruntule_button.grid(row=1, column=0, padx=10, pady=5)

        temizle_button = ttk.Button(rapor_gecmisi_pencere, text="Geçmişi Temizle", command=lambda: self.gecmisi_temizle(kimlik, rapor_listbox))
        temizle_button.grid(row=2, column=0, padx=10, pady=5)


    def gecmisi_goruntule(self, kimlik, rapor_listbox):
        # Seçilen raporun indeksini al
        selected_index = rapor_listbox.curselection()

        # Eğer bir rapor seçilmediyse, hata mesajı göster
        if not selected_index:
            messagebox.showerror("Hata", "Lütfen bir rapor seçin.")
            return

        # Seçilen raporun veritabanındaki ID'sini al
        selected_id = rapor_listbox.get(selected_index[0]).split(",")[0].split(":")[1].strip()

        # Veritabanından seçilen raporu al
        cursor.execute("SELECT rapor FROM spor_raporlari WHERE id = ?", (selected_id,))
        secilen_rapor = cursor.fetchone()

        # Eğer rapor bulunamadıysa, hata mesajı göster
        if not secilen_rapor:
            messagebox.showerror("Hata", "Seçilen rapor bulunamadı.")
            return

        # Raporu bir pencerede göster
        rapor_goruntule_pencere = tk.Toplevel(self)
        rapor_goruntule_pencere.title("Rapor Görüntüle")

        # Raporu bir etikette göster
        rapor_etiket = tk.Label(rapor_goruntule_pencere, text=secilen_rapor[0])
        rapor_etiket.pack(padx=10, pady=10, fill="both", expand=True)

    def gecmisi_temizle(self, kimlik, rapor_listbox):
        # Kullanıcının tüm raporlarını veritabanından sil
        cursor.execute("DELETE FROM spor_raporlari WHERE kimlik = ?", (kimlik,))
        conn.commit()

        # Liste kutusunu temizle
        rapor_listbox.delete(0, tk.END)

        # Bilgi mesajı göster
        messagebox.showinfo("Başarılı", "Geçmiş başarıyla temizlendi.")

    def gecmisi_guncelle(self, kimlik, rapor_listbox):
        # Seçilen raporun indeksini al
        selected_index = rapor_listbox.curselection()

        # Eğer bir rapor seçilmediyse, hata mesajı göster
        if not selected_index:
            messagebox.showerror("Hata", "Lütfen bir rapor seçin.")
            return

        # Seçilen raporun veritabanındaki ID'sini al
        selected_id = rapor_listbox.get(selected_index[0]).split(",")[0].split(":")[1].strip()

        # Veritabanından seçilen raporu al
        cursor.execute("SELECT rapor FROM spor_raporlari WHERE id = ?", (selected_id,))
        secilen_rapor = cursor.fetchone()

        # Eğer rapor bulunamadıysa, hata mesajı göster
        if not secilen_rapor:
            messagebox.showerror("Hata", "Seçilen rapor bulunamadı.")
            return

        # Raporu bir pencerede göster
        guncelle_pencere = tk.Toplevel(self)
        guncelle_pencere.title("Rapor Güncelle")

        # Raporu bir metin kutusunda göster
        rapor_metin = tk.Text(guncelle_pencere, width=50, height=15)
        rapor_metin.insert(tk.END, secilen_rapor[0])
        rapor_metin.pack(padx=10, pady=10, fill="both", expand=True)

        # Güncelleme butonunu oluştur
        guncelle_button = ttk.Button(guncelle_pencere, text="Raporu Güncelle", command=lambda: self.raporu_guncelle(kimlik, selected_id, rapor_metin.get("1.0", tk.END)))
        guncelle_button.pack(padx=10, pady=10)

    def raporu_guncelle(self, kimlik, rapor_id, yeni_rapor):
        # Seçilen raporu güncelle
        cursor.execute("UPDATE spor_raporlari SET rapor = ? WHERE id = ?", (yeni_rapor, rapor_id))
        conn.commit()

        # Bilgi mesajı göster
        messagebox.showinfo("Başarılı", "Rapor başarıyla güncellendi.")

        # Geçmişin güncel halini göstermek için rapor geçmişi penceresini güncelle
        self.rapor_gecmisi_goster()

    def cikis(self):
        self.destroy()

if __name__ == "__main__":
    uygulama = SporRandevuUygulamasi()
    uygulama.mainloop()
