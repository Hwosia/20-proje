import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import simpledialog
import random
conn = sqlite3.connect('online_kurs.db')
cursor = conn.cursor()

class KursUygulamasi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Kurs Uygulaması")

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

        self.email_label = ttk.Label(self.kayit_tab, text="E-posta:")
        self.email_label.grid(row=2, column=0, padx=10, pady=5)
        self.email_entry = ttk.Entry(self.kayit_tab)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        self.sifre_label = ttk.Label(self.kayit_tab, text="Şifre:")
        self.sifre_label.grid(row=3, column=0, padx=10, pady=5)
        self.sifre_entry = ttk.Entry(self.kayit_tab, show="*")
        self.sifre_entry.grid(row=3, column=1, padx=10, pady=5)

        self.kayit_button = ttk.Button(self.kayit_tab, text="Kayıt Ol", command=self.kayit_ol)
        self.kayit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def create_giris_tab(self):
        self.giris_tab_label = ttk.Label(self.giris_tab, text="Giriş Yap")
        self.giris_tab_label.grid(row=0, column=0, padx=10, pady=10)

        self.giris_email_label = ttk.Label(self.giris_tab, text="E-posta:")
        self.giris_email_label.grid(row=1, column=0, padx=10, pady=5)
        self.giris_email_entry = ttk.Entry(self.giris_tab)
        self.giris_email_entry.grid(row=1, column=1, padx=10, pady=5)

        self.giris_sifre_label = ttk.Label(self.giris_tab, text="Şifre:")
        self.giris_sifre_label.grid(row=2, column=0, padx=10, pady=5)
        self.giris_sifre_entry = ttk.Entry(self.giris_tab, show="*")
        self.giris_sifre_entry.grid(row=2, column=1, padx=10, pady=5)

        self.giris_button = ttk.Button(self.giris_tab, text="Giriş Yap", command=self.giris)
        self.giris_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def kayit_ol(self):
        isim = self.isim_entry.get()
        email = self.email_entry.get()
        sifre = self.sifre_entry.get()

        # E-posta adresinin daha önce kaydedilip kaydedilmediğini kontrol et
        cursor.execute("SELECT * FROM kullanicilar WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Hata", "Bu e-posta adresi zaten kayıtlıdır. Lütfen başka bir e-posta adresi kullanın.")
            return

        cursor.execute("INSERT INTO kullanicilar (isim, email, sifre) VALUES (?, ?, ?)", (isim, email, sifre))
        conn.commit()

        messagebox.showinfo("Başarılı", "Kayıt başarıyla oluşturuldu. Şimdi giriş yapabilirsiniz.")

        self.tabControl.select(self.giris_tab)

        self.isim_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.sifre_entry.delete(0, tk.END)

    def giris(self):
        email = self.giris_email_entry.get()
        sifre = self.giris_sifre_entry.get()

        cursor.execute("SELECT * FROM kullanicilar WHERE email = ? AND sifre = ?", (email, sifre))
        kullanici = cursor.fetchone()

        if kullanici:
            self.create_kurs_tab()  # Kurslar sekmesini oluştur
            self.tabControl.forget(self.kayit_tab)  # Kayıt sekmesini kaldır
            self.tabControl.forget(self.giris_tab)  # Giriş sekmesini kaldır
            self.tabControl.select(self.kurs_tab)  # Kurslar sekmesini seç
        else:
            messagebox.showerror("Hata", "Geçersiz e-posta veya şifre")

    def create_kurs_tab(self):
        self.kurs_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.kurs_tab, text="Kurslar")

        self.kurs_tab_label = ttk.Label(self.kurs_tab, text="Kurs İşlemleri")
        self.kurs_tab_label.grid(row=0, column=0, padx=10, pady=10)

        self.profil_button = ttk.Button(self.kurs_tab, text="Profil", command=self.goster_profil)
        self.profil_button.grid(row=0, column=1, padx=10, pady=10)

        self.kurs_al_button = ttk.Button(self.kurs_tab, text="Kurs Al", command=self.kurs_al)
        self.kurs_al_button.grid(row=1, column=0, padx=10, pady=5)

        self.kurs_listbox = tk.Listbox(self.kurs_tab, width=70, height=15)
        self.kurs_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.iade_et_button = ttk.Button(self.kurs_tab, text="İade Et", command=self.iade_et)
        self.iade_et_button.grid(row=3, column=0, padx=10, pady=5)

        self.kursu_izle_button = ttk.Button(self.kurs_tab, text="Kursu İzle", command=self.kursu_izle)
        self.kursu_izle_button.grid(row=3, column=1, padx=10, pady=5)

        self.cikis_button = ttk.Button(self.kurs_tab, text="Çıkış", command=self.cikis)
        self.cikis_button.grid(row=1, column=1, padx=10, pady=5)

        # Kullanıcının mevcut kurslarını göster
        self.kurslari_goster()

    def goster_profil(self):
        # Kullanıcıya bir soru sor
        cevap = messagebox.askquestion("Profil Bilgileri", "Bilgilerinizi güncellemek ister misiniz?", icon='question')

        if cevap == 'yes':  # Eğer 'Evet' seçeneği seçilirse
            self.guncelle_profil()  # Profil bilgilerini güncelleme fonksiyonunu çağır
        else:
            # Profil bilgilerini gösterme işlemleri
            email = self.giris_email_entry.get()
            cursor.execute("SELECT isim, email FROM kullanicilar WHERE email = ?", (email,))
            kullanici = cursor.fetchone()

            if kullanici:
                isim, email = kullanici
                messagebox.showinfo("Profil Bilgileri", f"İsim: {isim}\nE-posta: {email}")
            else:
                messagebox.showerror("Hata", "Profil bilgileri alınamadı.")

    def guncelle_profil(self):
        # Yeni ad, soyad, e-posta ve şifre bilgilerini al
        yeni_isim = simpledialog.askstring("Bilgi Güncelleme", "Yeni İsim Soyisim:")
        yeni_email = simpledialog.askstring("Bilgi Güncelleme", "Yeni E-posta:")
        yeni_sifre = simpledialog.askstring("Bilgi Güncelleme", "Yeni Şifre:", show='*')

        # Eğer tüm bilgiler sağlanmışsa güncelleme işlemlerini yap
        if yeni_isim and yeni_email and yeni_sifre:
            eski_email = self.giris_email_entry.get()
        
            cursor.execute("UPDATE kullanicilar SET isim = ?, email = ?, sifre = ? WHERE email = ?", (yeni_isim, yeni_email, yeni_sifre, eski_email))
            conn.commit()
        
            messagebox.showinfo("Başarılı", "Profil bilgileriniz başarıyla güncellendi.")
        else:
            messagebox.showerror("Hata", "Tüm bilgileri eksiksiz giriniz.")

    def kurs_al(self):
        self.kurs_al_pencere = tk.Toplevel(self)
        self.kurs_al_pencere.title("Kursları Göster")

        self.kurs_listbox_al = tk.Listbox(self.kurs_al_pencere, width=50, height=10)
        self.kurs_listbox_al.grid(row=0, column=0, padx=10, pady=10)

        self.kurs_al_button = ttk.Button(self.kurs_al_pencere, text="Kursu Al", command=self.kursu_al)
        self.kurs_al_button.grid(row=1, column=0, padx=5, pady=5)

        self.icerik_button = ttk.Button(self.kurs_al_pencere, text="İçerik", command=self.kurs_icerik_goster)
        self.icerik_button.grid(row=1, column=1, padx=5, pady=5)

        self.kurslari_goster_al()

    def kurslari_goster_al(self):
        kurslar = [
            ("Python", "Python programlama diline giriş."),
            ("JavaScript", "JavaScript ile web geliştirme."),
            ("Java", "Java programlama diline temel yaklaşım."),
            ("C++", "C++ programlama diline detaylı bakış."),
            ("SQL", "SQL veritabanı yönetimi.")
        ]

        self.kurs_listbox_al.delete(0, tk.END)

        for index, (baslik, _) in enumerate(kurslar):
            kurs_str = f"{baslik}"
            self.kurs_listbox_al.insert(tk.END, kurs_str)

    def kurs_icerik_goster(self):
        selected_index = self.kurs_listbox_al.curselection()

        if not selected_index:
            messagebox.showerror("Hata", "Lütfen bir kurs seçin.")
            return

        selected_title = self.kurs_listbox_al.get(selected_index[0])

        kurs_bilgileri = {
            "Python": {
                "icerik": "Python programlama diline giriş. Python'un temel konseptleri ve kullanım alanları.",
                "egitmenler": ["Ahmet Yılmaz", "Ayşe Kaya", "Mehmet Demir"],
                "neden_alinmali": "Python, öğrenmesi kolay, okunabilir ve geniş kütüphane desteğine sahip bir programlama dilidir. Web geliştirme, veri analizi, yapay zeka ve daha birçok alanda kullanılır."
            },
            "JavaScript": {
                "icerik": "JavaScript programlama diline giriş. JavaScript'in temel yapıları ve web geliştirme için kullanımı.",
                "egitmenler": ["Fatma Özcan", "Mustafa Altın", "Zeynep Aktaş"],
                "neden_alinmali": "JavaScript, web geliştirme için temel bir dildir. Dinamik web siteleri ve web uygulamaları geliştirmek için yaygın olarak kullanılır."
            },
            "C++": {
                "icerik": "C++ programlama diline detaylı bakış. C++'ın temel yapıları ve kullanımı.",
                "egitmenler": ["Ali Can", "Elif Kaya", "Berkay Yıldız"],
                "neden_alinmali": "C++, performans odaklı uygulamalar ve sistem programlama için kullanılan güçlü bir programlama dilidir. Oyun geliştirme, sistem programlama ve daha birçok alanda tercih edilir."
            },
            "SQL": {
                "icerik": "SQL veritabanı yönetimi. SQL sorguları ve veritabanı işlemleri.",
                "egitmenler": ["Gizem Yılmaz", "Hasan Ak", "Leyla Demir"],
                "neden_alinmali": "SQL, veri tabanı yönetimi ve sorgulama için temel bir dil olarak kabul edilir. Veri tabanı işlemleri ve sorgulamaları için esansiyeldir."
            },
            "Java": {
                "icerik": "Java programlama diline temel yaklaşım. Nesne yönelimli programlama ve Java'nın özellikleri.",
                "egitmenler": ["Hüseyin Yıldız", "Seda Ay", "Tolga Demir"],
                "neden_alinmali": "Java, geniş kütüphane desteği ve platform bağımsızlığı ile popüler bir programlama dilidir. Büyük ölçekli uygulamalar ve mobil uygulamalar için idealdir."
            }
        }

        bilgiler = kurs_bilgileri.get(selected_title)

        if bilgiler:
            icerik = f"Içerik:\n{bilgiler['icerik']}\n\nEğitmen: {random.choice(bilgiler['egitmenler'])}\n\nNeden Alınmalı:\n{bilgiler['neden_alinmali']}"
            messagebox.showinfo(selected_title, icerik)
        else:
            messagebox.showerror("Hata", "Kurs bilgileri bulunamadı.")


    def kursu_al(self):
        selected_index = self.kurs_listbox_al.curselection()

        if not selected_index:
            messagebox.showerror("Hata", "Lütfen bir kurs seçin.")
            return

        selected_title = self.kurs_listbox_al.get(selected_index[0])

        # Kursu "Kurslar" sekmesine ekleyin
        self.kurs_listbox.insert(tk.END, selected_title)

        messagebox.showinfo("Başarılı", f"{selected_title} kursunu satın aldınız.")

    def iade_et(self):
        selected_index = self.kurs_listbox.curselection()

        if not selected_index:
            messagebox.showerror("Hata", "Lütfen bir kurs seçin.")
            return

        selected_title = self.kurs_listbox.get(selected_index[0])

    # Kursu veritabanından silme (Burada kursun id'sini veya başlığını kullanabilirsiniz)
    # Örneğin:
    # cursor.execute("DELETE FROM kurslar WHERE baslik = ?", (selected_title,))
    # conn.commit()

        self.kurs_listbox.delete(selected_index)

        messagebox.showinfo("Başarılı", "Kurs iade edildi.")

    def kursu_izle(self):
        selected_index = self.kurs_listbox.curselection()

        if not selected_index:
            messagebox.showerror("Hata", "Lütfen bir kurs seçin.")
            return

        selected_title = self.kurs_listbox.get(selected_index[0])

        # Kursu izleme ekranı aç
        self.kurs_izle_ekrani(selected_title)

    def kurs_izle_ekrani(self, kurs_adi):
        # Burada kurs izleme ekranını oluşturabilirsiniz.
        # Şu an için sadece bir mesaj kutusu gösteriyoruz.
        messagebox.showinfo("Kurs İzle", f"{kurs_adi} kursunun video içeriğini izlemek için video yükleniyor lütfen bekleyiniz...")

    def goruntule(self):
        selected_index = self.kurs_listbox_al.curselection()

        if not selected_index:
            messagebox.showerror("Hata", "Lütfen bir kurs seçin.")
            return

        selected_title = self.kurs_listbox_al.get(selected_index[0]).split(",")[1].split(":")[1].strip()

        # Örnek olarak kurs içeriği metinleri belirttik.
        # Gerçek içerikleri veritabanından çekebilirsiniz.
        kurs_icerikleri = {
            "Python": "Python programlama diline giriş.",
            "JavaScript": "JavaScript ile web geliştirme.",
            "Java": "Java programlama diline temel yaklaşım.",
            "C++": "C++ programlama diline detaylı bakış.",
            "SQL": "SQL veritabanı yönetimi."
        }

        kurs_icerik = kurs_icerikleri.get(selected_title)

        if kurs_icerik:
            # İçeriği bir messagebox ile gösterme
            messagebox.showinfo(selected_title, kurs_icerik)
            # Kullanıcı bu kursu aldı olarak işaretleniyor
            # (Bu kısmı gerçek veritabanı işlemleri ile değiştirebilirsiniz.)
            self.kurs_listbox_al.delete(selected_index[0])
        else:
            messagebox.showerror("Hata", "Kurs içeriği bulunamadı.")


    def gecmisi_goster(self):
        email = self.giris_email_entry.get()
        
        cursor.execute("SELECT id, baslik, yazar FROM kurslar WHERE email = ?", (email,))
        kurslar = cursor.fetchall()
        
        self.kurs_listbox.delete(0, tk.END)
        
        for kurs in kurslar:
            kurs_str = f"ID: {kurs[0]}, Başlık: {kurs[1]}, Yazar: {kurs[2]}"
            self.kurs_listbox.insert(tk.END, kurs_str)

    def kurslari_goster(self):
        cursor.execute("SELECT id, baslik, yazar FROM kurslar")
        kurslar = cursor.fetchall()

        self.kurs_listbox.delete(0, tk.END)

        for kurs in kurslar:
            kurs_str = f"ID: {kurs[0]}, Başlık: {kurs[1]}, Yazar: {kurs[2]}"
            self.kurs_listbox.insert(tk.END, kurs_str)

    def icerik_goster(self):
        selected_index = self.kurs_listbox_al.curselection()

        if not selected_index:
            messagebox.showerror("Hata", "Lütfen bir kurs seçin.")
            return

        selected_title = self.kurs_listbox_al.get(selected_index[0])

        # Seçilen kurs başlığını kurs_icerik_goster fonksiyonuna argüman olarak gönder
        self.kurs_icerik_goster(selected_title)

    def cikis(self):
        self.tabControl.forget(self.kurs_tab)  # Kurslar sekmesini kaldır
        self.create_widgets()

if __name__ == "__main__":
    cursor.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (isim TEXT, email TEXT PRIMARY KEY, sifre TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS kurslar (id INTEGER PRIMARY KEY AUTOINCREMENT, baslik TEXT, yazar TEXT, alindi_mi INTEGER DEFAULT 0)''')
    conn.commit()

    app = KursUygulamasi()
    app.mainloop()