import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('randevular.db')
cursor = conn.cursor()

class RandevuUygulamasi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Randevu Uygulaması")

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
        self.tabControl.add(self.randevu_tab, text="Randevu")

        self.randevu_tab_label = ttk.Label(self.randevu_tab, text="Randevu İşlemleri")
        self.randevu_tab_label.grid(row=0, column=0, padx=10, pady=10)

        self.randevu_al_button = ttk.Button(self.randevu_tab, text="Randevu Al", command=self.randevu_al)
        self.randevu_al_button.grid(row=1, column=0, padx=10, pady=5)

        self.randevu_iptal_button = ttk.Button(self.randevu_tab, text="Randevu İptal Et", command=self.randevu_iptal)
        self.randevu_iptal_button.grid(row=2, column=0, padx=10, pady=5)

        self.cikis_button = ttk.Button(self.randevu_tab, text="Çıkış", command=self.cikis)
        self.cikis_button.grid(row=3, column=0, padx=10, pady=5)

        self.randevu_listbox = tk.Listbox(self.randevu_tab, width=70, height=15)
        self.randevu_listbox.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        # Kullanıcının mevcut randevularını göster
        self.randevulari_goster()

    def randevu_al(self):
        self.randevu_al_pencere = tk.Toplevel(self)
        self.randevu_al_pencere.title("Randevu Al")

        self.uzmanlik_label = ttk.Label(self.randevu_al_pencere, text="Uzmanlık Alanı Seçin:")
        self.uzmanlik_label.grid(row=0, column=0, padx=10, pady=5)

        self.uzmanlik_combobox = ttk.Combobox(self.randevu_al_pencere, values=[
            "Dahiliye", "Cerrahi", "Göz Hastalıkları", "Kulak Burun Boğaz", "Ortopedi", "Kardiyoloji",
            "Dermatoloji", "Nöroloji", "Radyoloji", "Üroloji"])
        self.uzmanlik_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.uzmanlik_combobox.bind("<<ComboboxSelected>>", self.doktorlari_getir)

        self.doktor_label = ttk.Label(self.randevu_al_pencere, text="Doktor Seçin:")
        self.doktor_label.grid(row=1, column=0, padx=10, pady=5)

        self.doktor_combobox = ttk.Combobox(self.randevu_al_pencere)
        self.doktor_combobox.grid(row=1, column=1, padx=10, pady=5)

        self.gun_label = ttk.Label(self.randevu_al_pencere, text="Gün Seçin:")
        self.gun_label.grid(row=2, column=0, padx=10, pady=5)

        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
        self.gun_combobox = ttk.Combobox(self.randevu_al_pencere, values=gunler)
        self.gun_combobox.grid(row=2, column=1, padx=10, pady=5)

        self.zaman_label = ttk.Label(self.randevu_al_pencere, text="Zaman:")
        self.zaman_label.grid(row=3, column=0, padx=10, pady=5)

        zamanlar = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
        self.zaman_combobox = ttk.Combobox(self.randevu_al_pencere, values=zamanlar)
        self.zaman_combobox.grid(row=3, column=1, padx=10, pady=5)

        self.randevu_olustur_button = ttk.Button(self.randevu_al_pencere, text="Randevu Tamamla", command=self.randevu_tamamla)
        self.randevu_olustur_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def doktorlari_getir(self, *args):
        uzmanlik = self.uzmanlik_combobox.get()
        
        doktorlar = {
            "Dahiliye": ["Dr. Ahmet", "Dr. Ayşe", "Dr. Mehmet"],
            "Cerrahi": ["Dr. Selim", "Dr. Fatma", "Dr. Burak"],
            "Göz Hastalıkları": ["Dr. Elif", "Dr. Hakan", "Dr. Seda"],
            "Kulak Burun Boğaz": ["Dr. İsmail", "Dr. Nihan", "Dr. Emre"],
            "Ortopedi": ["Dr. Sevgi", "Dr. Cem", "Dr. Zeynep"],
            "Kardiyoloji": ["Dr. Ali", "Dr. Selma", "Dr. Ercan"],
            "Dermatoloji": ["Dr. Ceren", "Dr. Cihan", "Dr. Serkan"],
            "Nöroloji": ["Dr. Barış", "Dr. Şebnem", "Dr. Oğuz"],
            "Radyoloji": ["Dr. Ebru", "Dr. Emir", "Dr. Ela"],
            "Üroloji": ["Dr. Feride", "Dr. Ahu", "Dr. Turgut"]
        }

        self.doktor_combobox['values'] = doktorlar.get(uzmanlik, [])

    def randevu_tamamla(self):
        kimlik = self.giris_kimlik_entry.get()
        uzmanlik = self.uzmanlik_combobox.get()
        doktor = self.doktor_combobox.get()
        gun = self.gun_combobox.get()
        zaman = self.zaman_combobox.get()

        tarih = f"{gun} {zaman}"

        cursor.execute("SELECT * FROM randevular WHERE doktor = ? AND zaman = ?", (doktor, tarih))
        varmi = cursor.fetchone()

        if varmi:
            messagebox.showerror("Hata", "Seçilen doktor ve zaman diliminde randevu bulunmaktadır. Lütfen farklı bir zaman dilimi seçiniz.")
            return

        cursor.execute("INSERT INTO randevular (kimlik, uzmanlik, doktor, zaman) VALUES (?, ?, ?, ?)", (kimlik, uzmanlik, doktor, tarih))
        conn.commit()

        messagebox.showinfo("Başarılı", "Randevunuz tamamlandı.")

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

        cursor.execute("DELETE FROM randevular WHERE id = ?", (selected_id,))
        conn.commit()

        messagebox.showinfo("Başarılı", "Randevunuz iptal edilmiştir.")

        self.randevulari_goster()

    def randevulari_goster(self):
        kimlik = self.giris_kimlik_entry.get()
        
        cursor.execute("SELECT id, uzmanlik, doktor, zaman FROM randevular WHERE kimlik = ?", (kimlik,))
        randevular = cursor.fetchall()
        
        self.randevu_listbox.delete(0, tk.END)
        
        for randevu in randevular:
            randevu_str = f"ID: {randevu[0]}, Uzmanlık: {randevu[1]}, Doktor: {randevu[2]}, Zaman: {randevu[3]}"
            self.randevu_listbox.insert(tk.END, randevu_str)

    def cikis(self):
        self.destroy()

if __name__ == "__main__":
    cursor.execute('''CREATE TABLE IF NOT EXISTS hastalar (isim TEXT, kimlik TEXT PRIMARY KEY, sifre TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS randevular (id INTEGER PRIMARY KEY AUTOINCREMENT, kimlik TEXT, uzmanlik TEXT, doktor TEXT, zaman TEXT)''')
    conn.commit()

    app = RandevuUygulamasi()
    app.mainloop()
