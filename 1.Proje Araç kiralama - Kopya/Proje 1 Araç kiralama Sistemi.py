import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import random
conn = sqlite3.connect('arac_kiralama.db')
cursor = conn.cursor()

class AracKiralamaUygulamasi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Araç Kiralama Sistemi")
        self.create_widgets()

    def create_widgets(self):
        self.tabControl = ttk.Notebook(self)

        self.kayit_tab = ttk.Frame(self.tabControl)
        self.giris_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.kayit_tab, text="Kayıt Ol")
        self.tabControl.add(self.giris_tab, text="Giriş Yap")

        self.tabControl.pack(expand=1, fill="both")

        self.create_kayit_tab()
        self.create_giris_tab()

    def create_kayit_tab(self):
        self.kayit_tab_label = ttk.Label(self.kayit_tab, text="Kayıt Ol")
        self.kayit_tab_label.grid(row=0, column=0, padx=10, pady=10)

        self.isim_label = ttk.Label(self.kayit_tab, text="İsim Soyisim:")
        self.isim_label.grid(row=1, column=0, padx=10, pady=5)
        self.isim_entry = ttk.Entry(self.kayit_tab)
        self.isim_entry.grid(row=1, column=1, padx=10, pady=5)

        self.tc_label = ttk.Label(self.kayit_tab, text="TC Kimlik No:")
        self.tc_label.grid(row=2, column=0, padx=10, pady=5)
        self.tc_entry = ttk.Entry(self.kayit_tab)
        self.tc_entry.grid(row=2, column=1, padx=10, pady=5)

        self.telefon_label = ttk.Label(self.kayit_tab, text="Telefon Numarası:")
        self.telefon_label.grid(row=3, column=0, padx=10, pady=5)
        self.telefon_entry = ttk.Entry(self.kayit_tab)
        self.telefon_entry.grid(row=3, column=1, padx=10, pady=5)

        self.sifre_label = ttk.Label(self.kayit_tab, text="Şifre:")
        self.sifre_label.grid(row=4, column=0, padx=10, pady=5)
        self.sifre_entry = ttk.Entry(self.kayit_tab, show="*")
        self.sifre_entry.grid(row=4, column=1, padx=10, pady=5)

        self.kayit_button = ttk.Button(self.kayit_tab, text="Kayıt Ol", command=self.kayit_ol)
        self.kayit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def create_giris_tab(self):
        self.giris_tab_label = ttk.Label(self.giris_tab, text="Giriş Yap")
        self.giris_tab_label.grid(row=0, column=0, padx=10, pady=10)

        self.giris_tc_label = ttk.Label(self.giris_tab, text="TC Kimlik No:")
        self.giris_tc_label.grid(row=1, column=0, padx=10, pady=5)
        self.giris_tc_entry = ttk.Entry(self.giris_tab)
        self.giris_tc_entry.grid(row=1, column=1, padx=10, pady=5)

        self.giris_sifre_label = ttk.Label(self.giris_tab, text="Şifre:")
        self.giris_sifre_label.grid(row=2, column=0, padx=10, pady=5)
        self.giris_sifre_entry = ttk.Entry(self.giris_tab, show="*")
        self.giris_sifre_entry.grid(row=2, column=1, padx=10, pady=5)

        self.giris_button = ttk.Button(self.giris_tab, text="Giriş Yap", command=self.giris)
        self.giris_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def kayit_ol(self):
        isim = self.isim_entry.get()
        tc = self.tc_entry.get()
        telefon = self.telefon_entry.get()
        sifre = self.sifre_entry.get()

        cursor.execute("INSERT INTO musteriler (isim, tc, telefon, sifre) VALUES (?, ?, ?, ?)", (isim, tc, telefon, sifre))
        conn.commit()

        messagebox.showinfo("Başarılı", "Kayıt başarıyla oluşturuldu. Şimdi giriş yapabilirsiniz.")

        self.tabControl.select(self.giris_tab)

        self.isim_entry.delete(0, tk.END)
        self.tc_entry.delete(0, tk.END)
        self.telefon_entry.delete(0, tk.END)
        self.sifre_entry.delete(0, tk.END)

    def giris(self):
        tc = self.giris_tc_entry.get()
        sifre = self.giris_sifre_entry.get()

        cursor.execute("SELECT * FROM musteriler WHERE tc = ? AND sifre = ?", (tc, sifre))
        kullanici = cursor.fetchone()

        if kullanici:
            self.create_kiralama_tab()
            self.tabControl.forget(self.kayit_tab)
            self.tabControl.forget(self.giris_tab)
            self.tabControl.select(self.kiralama_tab)
        else:
            messagebox.showerror("Hata", "Geçersiz TC kimlik numarası veya şifre")

    def create_kiralama_tab(self):
        self.kiralama_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.kiralama_tab, text="Kiralama İşlemleri")

        self.kiralama_tab_label = ttk.Label(self.kiralama_tab, text="Kiralama İşlemleri")
        self.kiralama_tab_label.grid(row=0, column=0, padx=10, pady=10)

        self.kiralama_al_button = ttk.Button(self.kiralama_tab, text="Araç Kirala", command=self.arac_kirala)
        self.kiralama_al_button.grid(row=1, column=0, padx=10, pady=5)

        self.musteri_bilgileri_button = ttk.Button(self.kiralama_tab, text="Müşteri Bilgileri", command=self.musteri_bilgileri_guncelle)
        self.musteri_bilgileri_button.grid(row=2, column=0, padx=10, pady=5)

        self.kiralama_iptal_button = ttk.Button(self.kiralama_tab, text="Kiralama İptal Et", command=self.arac_iptal)
        self.kiralama_iptal_button.grid(row=3, column=0, padx=10, pady=5)

        self.cikis_button = ttk.Button(self.kiralama_tab, text="Çıkış", command=self.cikis)
        self.cikis_button.grid(row=4, column=0, padx=10, pady=5, sticky=tk.NE)

        self.kiralanan_araclar_listbox = tk.Listbox(self.kiralama_tab, width=70, height=15)
        self.kiralanan_araclar_listbox.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")


        # Bakiye bölümü
        self.bakiye = random.randint(0, 50000)
    
        # Bakiye yazısı
        self.bakiye_label = ttk.Label(self.kiralama_tab, text=f"Bakiye: ${self.bakiye}")
        self.bakiye_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Bakiye Yükle butonu
        self.bakiye_yukle_button = ttk.Button(self.kiralama_tab, text="Bakiye Yükle", command=self.bakiye_yukle)
        self.bakiye_yukle_button.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.kiralanan_araclari_goster()    

    def bakiye_yukle(self):
        yeni_bakiye_miktarı = random.randint(50, 2000)
        self.bakiye += yeni_bakiye_miktarı
        self.bakiye_label.config(text=f"Bakiye: ${self.bakiye}")
        messagebox.showinfo("Başarılı", f"Bakiyenize ${yeni_bakiye_miktarı} yüklendi.")
    
    def arac_kirala(self):
        self.arac_kirala_pencere = tk.Toplevel(self)
        self.arac_kirala_pencere.title("Araç Kiralama")

        self.arac_turu_label = ttk.Label(self.arac_kirala_pencere, text="Araç Türü Seçin:")
        self.arac_turu_label.grid(row=0, column=0, padx=10, pady=5)

        self.arac_turu_combobox = ttk.Combobox(self.arac_kirala_pencere, values=["Sedan", "Hatchback", "SUV", "Minivan", "Kamyonet"])
        self.arac_turu_combobox.grid(row=0, column=1, padx=10, pady=5)

        self.arac_marka_label = ttk.Label(self.arac_kirala_pencere, text="Araç Markası:")
        self.arac_marka_label.grid(row=1, column=0, padx=10, pady=5)

        self.arac_marka_combobox = ttk.Combobox(self.arac_kirala_pencere, values=["Audi", "BMW", "Mercedes-Benz", "Toyota", "Honda", "Ford", "Volkswagen", "Nissan", "Hyundai", "Renault"])
        self.arac_marka_combobox.grid(row=1, column=1, padx=10, pady=5)

        self.arac_yil_label = ttk.Label(self.arac_kirala_pencere, text="Araç Yılı (2000-2024):")
        self.arac_yil_label.grid(row=2, column=0, padx=10, pady=5)
        self.arac_yil_entry = ttk.Entry(self.arac_kirala_pencere)
        self.arac_yil_entry.grid(row=2, column=1, padx=10, pady=5)

        self.fiyat_getir_button = ttk.Button(self.arac_kirala_pencere, text="Fiyat Getir", command=self.fiyat_getir)
        self.fiyat_getir_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def fiyat_getir(self):
        # Araç yılı kontrolü
        yil = self.arac_yil_entry.get()
        if not (yil.isdigit() and 2000 <= int(yil) <= 2024):
            messagebox.showerror("Hata", "Lütfen geçerli bir araç yılı girin (2000-2024 aralığında).")
            return

        # Rastgele fiyat oluştur
        fiyatlar = [random.randint(200, 500), random.randint(300, 600), random.randint(400, 700)]
        self.arac_fiyat_combobox = ttk.Combobox(self.arac_kirala_pencere, values=fiyatlar)
        self.arac_fiyat_combobox.grid(row=4, column=1, padx=10, pady=5)

        self.arac_fiyat_label = ttk.Label(self.arac_kirala_pencere, text="Günlük Fiyat:")
        self.arac_fiyat_label.grid(row=4, column=0, padx=10, pady=5)

        self.arac_kirala_button = ttk.Button(self.arac_kirala_pencere, text="Kiralama Tamamla", command=self.kiralama_tamamla)
        self.arac_kirala_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
    
    def bilgileri_kaydet(self):
        yeni_isim = self.isim_entry.get()
        yeni_tc = self.tc_entry.get()
        yeni_telefon = self.telefon_entry.get()
        yeni_sifre = self.sifre_entry.get()

        eski_tc = self.giris_tc_entry.get()

        cursor.execute("UPDATE musteriler SET isim=?, tc=?, telefon=?, sifre=? WHERE tc=?", (yeni_isim, yeni_tc, yeni_telefon, yeni_sifre, eski_tc))
        conn.commit()

        messagebox.showinfo("Başarılı", "Bilgiler başarıyla güncellendi.")
    
    def musteri_bilgileri_guncelle(self):
        self.musteri_guncelle_pencere = tk.Toplevel(self)
        self.musteri_guncelle_pencere.title("Müşteri Bilgileri Güncelle")

        # Mevcut müşteri bilgilerini al
        tc = self.giris_tc_entry.get()
        cursor.execute("SELECT * FROM musteriler WHERE tc = ?", (tc,))
        musteri = cursor.fetchone()

        # Label ve Entry'ler oluştur
        self.isim_label = ttk.Label(self.musteri_guncelle_pencere, text="İsim Soyisim:")
        self.isim_label.grid(row=0, column=0, padx=10, pady=5)
        self.isim_entry = ttk.Entry(self.musteri_guncelle_pencere)
        self.isim_entry.insert(0, musteri[0])
        self.isim_entry.grid(row=0, column=1, padx=10, pady=5)

        self.tc_label = ttk.Label(self.musteri_guncelle_pencere, text="TC Kimlik No:")
        self.tc_label.grid(row=1, column=0, padx=10, pady=5)
        self.tc_entry = ttk.Entry(self.musteri_guncelle_pencere)
        self.tc_entry.insert(0, musteri[1])
        self.tc_entry.grid(row=1, column=1, padx=10, pady=5)

        self.telefon_label = ttk.Label(self.musteri_guncelle_pencere, text="Telefon Numarası:")
        self.telefon_label.grid(row=2, column=0, padx=10, pady=5)
        self.telefon_entry = ttk.Entry(self.musteri_guncelle_pencere)
        self.telefon_entry.insert(0, musteri[2])
        self.telefon_entry.grid(row=2, column=1, padx=10, pady=5)

        self.sifre_label = ttk.Label(self.musteri_guncelle_pencere, text="Şifre:")
        self.sifre_label.grid(row=3, column=0, padx=10, pady=5)
        self.sifre_entry = ttk.Entry(self.musteri_guncelle_pencere, show="*")
        self.sifre_entry.insert(0, musteri[3])
        self.sifre_entry.grid(row=3, column=1, padx=10, pady=5)

        self.kaydet_button = ttk.Button(self.musteri_guncelle_pencere, text="Kaydet", command=self.musteri_bilgileri_kaydet)
        self.kaydet_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
    
    def musteri_bilgileri_kaydet(self):
        yeni_isim = self.isim_entry.get()
        yeni_tc = self.tc_entry.get()
        yeni_telefon = self.telefon_entry.get()
        yeni_sifre = self.sifre_entry.get()

        # Güncelleme işlemi
        cursor.execute("UPDATE musteriler SET isim=?, telefon=?, sifre=? WHERE tc=?", (yeni_isim, yeni_telefon, yeni_sifre, yeni_tc))
        conn.commit()

        # Girdi alanlarını temizle
        self.isim_entry.delete(0, tk.END)
        self.tc_entry.delete(0, tk.END)
        self.telefon_entry.delete(0, tk.END)
        self.sifre_entry.delete(0, tk.END)

        messagebox.showinfo("Başarılı", "Müşteri bilgileri güncellendi.")

    def arac_tamamla(self):
        tc = self.giris_tc_entry.get()
        arac_turu = self.arac_turu_combobox.get()
        marka = self.arac_marka_combobox.get()
        yil = self.arac_yil_entry.get()

        # Araç yılı kontrolü
        if not (yil.isdigit() and 2000 <= int(yil) <= 2024):
            messagebox.showerror("Hata", "Lütfen geçerli bir araç yılı girin (2000-2024 aralığında).")
            return

        # Rastgele fiyat oluştur
        fiyatlar = [random.randint(200, 500), random.randint(300, 600), random.randint(400, 700)]
        self.arac_fiyat_combobox = ttk.Combobox(self.arac_kirala_pencere, values=fiyatlar)
        self.arac_fiyat_combobox.grid(row=3, column=1, padx=10, pady=5)

        self.arac_fiyat_label = ttk.Label(self.arac_kirala_pencere, text="Günlük Fiyat:")
        self.arac_fiyat_label.grid(row=3, column=0, padx=10, pady=5)

        self.arac_kirala_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def kiralama_tamamla(self):
        tc = self.giris_tc_entry.get()
        arac_turu = self.arac_turu_combobox.get()
        marka = self.arac_marka_combobox.get()
        yil = self.arac_yil_entry.get()
        fiyat = self.arac_fiyat_combobox.get()

        # Fiyat kontrolü
        if not fiyat.isdigit():
            messagebox.showerror("Hata", "Lütfen geçerli bir fiyat seçin.")
            return

        fiyat = int(fiyat)

        onay = messagebox.askyesno("Onay", f"{arac_turu} - {marka} - {yil} aracını günlük ${fiyat} fiyatına kiralamak istiyor musunuz?")
    
        if onay:
            # Bakiye kontrolü
            if self.bakiye < fiyat:
                messagebox.showerror("Hata", "Yetersiz bakiye. Lütfen bakiye yükleyin.")
                return

            # Bakiyeden ücreti düşme ve yeni bakiye güncelleme
            self.bakiye -= fiyat
            self.bakiye_label.config(text=f"Bakiye: ${self.bakiye}")

            cursor.execute("INSERT INTO kiralanmis_araclar (tc, arac_turu, marka, yil, fiyat) VALUES (?, ?, ?, ?, ?)",
                    (tc, arac_turu, marka, yil, fiyat))
            conn.commit()

            messagebox.showinfo("Başarılı", "Araç kiralama işlemi tamamlandı.")
            self.kiralanan_araclari_goster()



    def arac_iptal(self):
        selected_index = self.kiralanan_araclar_listbox.curselection()

        if not selected_index:
            messagebox.showerror("Hata", "Lütfen iptal etmek istediğiniz aracı seçin.")
            return

        selected_id = self.kiralanan_araclar_listbox.get(selected_index[0]).split(",")[0].split(":")[1].strip()

        # Seçilen aracın fiyatını al
        cursor.execute("SELECT fiyat FROM kiralanmis_araclar WHERE id = ?", (selected_id,))
        fiyat = cursor.fetchone()[0]

        # Bakiyeyi güncelle
        self.bakiye += fiyat
        self.bakiye_label.config(text=f"Bakiye: ${self.bakiye}")

        # Seçilen aracı veritabanından sil
        cursor.execute("DELETE FROM kiralanmis_araclar WHERE id = ?", (selected_id,))
        conn.commit()

        messagebox.showinfo("Başarılı", "Kiralama işlemi iptal edildi.")

        self.kiralanan_araclari_goster()

    def kiralanan_araclari_goster(self):
        tc = self.giris_tc_entry.get()

        cursor.execute("SELECT id, arac_turu, marka, yil FROM kiralanmis_araclar WHERE tc = ?", (tc,))
        kiralanan_araclar = cursor.fetchall()

        self.kiralanan_araclar_listbox.delete(0, tk.END)

        for arac in kiralanan_araclar:
            arac_str = f"ID: {arac[0]}, Tür: {arac[1]}, Marka: {arac[2]}, Yıl: {arac[3]}"
            self.kiralanan_araclar_listbox.insert(tk.END, arac_str)
    

    def cikis(self):
        self.destroy()
    


if __name__ == "__main__":
    cursor.execute('''CREATE TABLE IF NOT EXISTS musteriler (isim TEXT, tc TEXT PRIMARY KEY, telefon TEXT, sifre TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS kiralanmis_araclar (id INTEGER PRIMARY KEY AUTOINCREMENT, tc TEXT, arac_turu TEXT, marka TEXT, yil INTEGER)''')
    conn.commit()

    app = AracKiralamaUygulamasi()
    app.mainloop()