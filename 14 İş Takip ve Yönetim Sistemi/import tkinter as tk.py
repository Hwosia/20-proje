import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import simpledialog
import random
conn = sqlite3.connect('randevular.db')
cursor = conn.cursor()

class RandevuUygulamasi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("İş Takip Uygulaması")
        cursor.execute('''CREATE TABLE IF NOT EXISTS projeler (id INTEGER PRIMARY KEY AUTOINCREMENT, proje_zamani TEXT)''')
        conn.commit()

        # Combobox özelliklerini tanımlayalım
        self.gun_combobox = None
        self.zaman_combobox = None

        # Combobox için seçenekler
        self.gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
        self.zamanlar = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
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
        self.zaman_combobox = ttk.Combobox(self.kayit_tab, values=self.zamanlar)
        self.gun_combobox = ttk.Combobox(self.kayit_tab, values=self.gunler)
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
        self.zaman_combobox = ttk.Combobox(self.giris_tab, values=self.zamanlar)
        self.gun_combobox = ttk.Combobox(self.giris_tab, values=self.gunler)
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

        cursor.execute("INSERT INTO hastalar (isim, kimlik, sifre) VALUES (?, ?, ?)", (isim, kimlik, sifre))
        conn.commit()

        messagebox.showinfo("Başarılı", "Kayıt başarıyla oluşturuldu. Şimdi giriş yapabilirsiniz.")

        self.tabControl.select(self.giris_tab)

        self.isim_entry.delete(0, tk.END)
        self.kimlik_entry.delete(0, tk.END)
        self.sifre_entry.delete(0, tk.END)

    def giris(self):
        kimlik = self.giris_kimlik_entry.get()
        sifre = self.giris_sifre_entry.get()

        cursor.execute("SELECT * FROM hastalar WHERE kimlik = ? AND sifre = ?", (kimlik, sifre))
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
        self.tabControl.add(self.randevu_tab, text="İş Takip ve Yönetim Sistemi")

        self.randevu_tab_label = ttk.Label(self.randevu_tab, text="İş Takip İşlemleri")
        self.randevu_tab_label.grid(row=0, column=0, padx=10, pady=10)

        self.proje_olustur_button = ttk.Button(self.randevu_tab, text="Proje Oluştur", command=self.proje_olustur)
        self.proje_olustur_button.grid(row=1, column=0, padx=10, pady=5)

        self.proje_iptal_button = ttk.Button(self.randevu_tab, text="Proje İptal Et", command=self.proje_iptal)
        self.proje_iptal_button.grid(row=2, column=0, padx=10, pady=5)

        self.gorevli_ata_button = ttk.Button(self.randevu_tab, text="Görevli Ata", command=self.gorevli_ata)
        self.gorevli_ata_button.grid(row=3, column=0, padx=10, pady=5)

        self.ilerleme_takip_button = ttk.Button(self.randevu_tab, text="İlerleme Takip", command=self.ilerleme_takip)
        self.ilerleme_takip_button.grid(row=4, column=0, padx=10, pady=5)


        self.cikis_button = ttk.Button(self.randevu_tab, text="Çıkış", command=self.cikis)
        self.cikis_button.grid(row=6, column=0, padx=10, pady=5)

        self.randevu_listbox = tk.Listbox(self.randevu_tab, width=70, height=15)
        self.randevu_listbox.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")

        # Oran tablosu için Treeview widget'ını oluşturalım

        
        # Proje bilgisini göster
        self.proje_tamamla()
        self.randevulari_goster()

    def proje_olustur(self):
        self.proje_olustur_pencere = tk.Toplevel(self)
        self.proje_olustur_pencere.title("Proje Oluştur")

        self.gun_label = ttk.Label(self.proje_olustur_pencere, text="Proje Günü Seçin:")
        self.gun_label.grid(row=0, column=0, padx=10, pady=5)

        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
        self.gun_combobox = ttk.Combobox(self.proje_olustur_pencere, values=gunler)
        self.gun_combobox.grid(row=0, column=1, padx=10, pady=5)

        self.zaman_label = ttk.Label(self.proje_olustur_pencere, text="Proje Saati Seçin:")
        self.zaman_label.grid(row=1, column=0, padx=10, pady=5)

        zamanlar = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
        self.zaman_combobox = ttk.Combobox(self.proje_olustur_pencere, values=zamanlar)
        self.zaman_combobox.grid(row=1, column=1, padx=10, pady=5)

        self.tamamla_button = ttk.Button(self.proje_olustur_pencere, text="Tamamla", command=self.proje_tamamla)
        self.tamamla_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def proje_tamamla(self):
        # Proje bilgilerini al
        gun = self.gun_combobox.get()
        saat = self.zaman_combobox.get()
        proje_zamani = f"Proje Günü: {gun}, Saati: {saat}"

        # Proje bilgisini `self.randevu_listbox` widget'ının içine ekleyelim
        self.randevu_listbox.insert(tk.END, proje_zamani)

        # Projeyi veritabanına kaydet
        cursor.execute("INSERT INTO projeler (proje_zamani) VALUES (?)", (proje_zamani,))
        conn.commit()

    def randevulari_goster(self):
        # Projeleri temizle
        self.randevu_listbox.delete(0, tk.END)

        # Veritabanından projeleri al
        cursor.execute("SELECT * FROM projeler")
        projeler = cursor.fetchall()

        # Her projeyi listbox'a ekle
        for proje in projeler:
            self.randevu_listbox.insert(tk.END, proje[1])

    def proje_iptal(self):
        # Seçilen projenin kimliğini al
        secilen_proje_indexi = self.randevu_listbox.curselection()
        if secilen_proje_indexi:
            secilen_proje_indexi = secilen_proje_indexi[0]
            secilen_proje = self.randevu_listbox.get(secilen_proje_indexi)

            # Veritabanından projeyi sil
            cursor.execute("DELETE FROM projeler WHERE proje_zamani = ?", (secilen_proje,))
            conn.commit()

            # Proje listesini güncelle
            self.randevulari_goster()
        else:
            messagebox.showerror("Hata", "Lütfen bir proje seçin.")

    def gorevli_ata(self):
        # Seçilen projenin index'ini al
        secilen_proje_indexi = self.randevu_listbox.curselection()
        if secilen_proje_indexi:
            secilen_proje_indexi = secilen_proje_indexi[0]
            secilen_proje = self.randevu_listbox.get(secilen_proje_indexi)

            # Görevli atanacak kişinin ismini kullanıcıdan al
            gorevli_isim = simpledialog.askstring("Görevli Atama", f"{secilen_proje} için görevli atanacak kişinin ismini girin:")

            # Seçilen projenin yanına görevli bilgisini ekleyerek listbox'ta güncelle
            self.randevu_listbox.delete(secilen_proje_indexi)
            self.randevu_listbox.insert(secilen_proje_indexi, f"{secilen_proje} - Görevli: {gorevli_isim}")
        else:
            messagebox.showerror("Hata", "Lütfen bir proje seçin.")

    def ilerleme_takip(self):
        # Yeni bir pencere oluştur
        ilerleme_pencere = tk.Toplevel(self)
        ilerleme_pencere.title("İlerleme Takip")

        # Oran tablosu için Treeview widget'ını oluşturalım
        oran_tablosu = ttk.Treeview(ilerleme_pencere, columns=("Proje", "Durum"), show="headings")
        oran_tablosu.heading("Proje", text="Proje")
        oran_tablosu.heading("Durum", text="Durum")
        oran_tablosu.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Proje ve tamamlanma oranı örnek verileri (örneğin tamamlanma oranı rastgele)
        projeler = ["Proje 1"]
        for proje in projeler:
            tamamlanma_orani = random.randint(0, 100)
            oran_tablosu.insert("", "end", values=(proje, f"%{tamamlanma_orani} tamamlandı"))


    def cikis(self):
        self.destroy()

if __name__ == "__main__":
    cursor.execute('''CREATE TABLE IF NOT EXISTS hastalar (isim TEXT, kimlik TEXT PRIMARY KEY, sifre TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS randevular (id INTEGER PRIMARY KEY AUTOINCREMENT, kimlik TEXT, uzmanlik TEXT, doktor TEXT, zaman TEXT)''')
    conn.commit()

    app = RandevuUygulamasi()
    app.mainloop()
