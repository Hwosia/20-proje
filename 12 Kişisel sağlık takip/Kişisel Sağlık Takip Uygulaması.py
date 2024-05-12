import tkinter as tk
from tkinter import ttk, messagebox

class Kullanici:
    def __init__(self, adi, soyadi, yas, cinsiyet, telefon_no):
        self.adi = adi
        self.soyadi = soyadi
        self.yas = yas
        self.cinsiyet = cinsiyet
        self.telefon_no = telefon_no
        self.sikayet = ""

class SaglikBilgileri:
    def __init__(self, boy, kilo, kan_grubu, seker_durumu, tansiyon_durumu):
        self.boy = boy
        self.kilo = kilo
        self.kan_grubu = kan_grubu
        self.seker_durumu = seker_durumu
        self.tansiyon_durumu = tansiyon_durumu

class Egzersiz:
    def __init__(self, seviye1, seviye2, seviye3):
        self.seviye1 = seviye1
        self.seviye2 = seviye2
        self.seviye3 = seviye3


class Arayuz:
    def __init__(self, root):
        self.root = root
        self.root.title("Kişisel Sağlık Takip Uygulaması")
        self.root.geometry("400x300")

        self.tab_control = ttk.Notebook(root)

        self.kullanici_tab = ttk.Frame(self.tab_control)
        self.saglik_tab = ttk.Frame(self.tab_control)
        self.egzersiz_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.kullanici_tab, text="Kullanıcı")
        self.tab_control.add(self.saglik_tab, text="Sağlık Bilgileri")
        self.tab_control.add(self.egzersiz_tab, text="Egzersiz")

        self.kullanici_arayuz_olustur()
        self.saglik_arayuz_olustur()
        self.egzersiz_arayuz_olustur()

        self.tab_control.pack(expand=1, fill="both")

    def kullanici_arayuz_olustur(self):
        frame = ttk.LabelFrame(self.kullanici_tab, text="Kullanıcı Bilgileri", relief="groove")

        self.adi_label = ttk.Label(frame, text="Kullanıcı Adı:")
        self.adi_input = ttk.Entry(frame)
        self.soyadi_label = ttk.Label(frame, text="Kullanıcı Soyadı:")
        self.soyadi_input = ttk.Entry(frame)
        self.yas_label = ttk.Label(frame, text="Yaş:")
        self.yas_input = ttk.Entry(frame)
        self.cinsiyet_label = ttk.Label(frame, text="Cinsiyet:")
        self.cinsiyet_combo = ttk.Combobox(frame, values=["Kadın", "Erkek"])
        self.sikayet_label = ttk.Label(frame, text="Şikayet:")
        self.sikayet_combo = ttk.Combobox(frame, values=["Baş Bölgesi", "Boyun Bölgesi", "Kol Bölgesi", "Göğüs Bölgesi", "Bacak Bölgesi"])
        self.telefon_no_label = ttk.Label(frame, text="Telefon No:")
        self.telefon_no_input = ttk.Entry(frame)

        self.adi_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.adi_input.grid(row=0, column=1, padx=5, pady=2)
        self.soyadi_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.soyadi_input.grid(row=1, column=1, padx=5, pady=2)
        self.yas_label.grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.yas_input.grid(row=2, column=1, padx=5, pady=2)
        self.cinsiyet_label.grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.cinsiyet_combo.grid(row=3, column=1, padx=5, pady=2)
        self.sikayet_label.grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.sikayet_combo.grid(row=4, column=1, padx=5, pady=2)
        self.telefon_no_label.grid(row=5, column=0, padx=5, pady=2, sticky="w")
        self.telefon_no_input.grid(row=5, column=1, padx=5, pady=2)

        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ekle_button = ttk.Button(self.kullanici_tab, text="Ekle", command=self.kullanici_ekle)
        ekle_button.pack(pady=5)

    def saglik_arayuz_olustur(self):
        frame = ttk.LabelFrame(self.saglik_tab, text="Sağlık Bilgileri", relief="groove")

        self.boy_label = ttk.Label(frame, text="Boy (cm):")
        self.boy_input = ttk.Entry(frame)
        self.kilo_label = ttk.Label(frame, text="Kilo (kg):")
        self.kilo_input = ttk.Entry(frame)
        self.kan_grubu_label = ttk.Label(frame, text="Kan Grubu:")
        self.kan_grubu_input = ttk.Entry(frame)
        self.seker_durumu_label = ttk.Label(frame, text="Şeker Durumu:")
        self.seker_durumu_input = ttk.Entry(frame)
        self.tansiyon_durumu_label = ttk.Label(frame, text="Tansiyon Durumu:")
        self.tansiyon_durumu_input = ttk.Entry(frame)

        self.boy_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.boy_input.grid(row=0, column=1, padx=5, pady=2)
        self.kilo_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.kilo_input.grid(row=1, column=1, padx=5, pady=2)
        self.kan_grubu_label.grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.kan_grubu_input.grid(row=2, column=1, padx=5, pady=2)
        self.seker_durumu_label.grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.seker_durumu_input.grid(row=3, column=1, padx=5, pady=2)
        self.tansiyon_durumu_label.grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.tansiyon_durumu_input.grid(row=4, column=1, padx=5, pady=2)

        frame.pack(padx=10, pady=10, fill="both", expand=True)

        guncelle_button = ttk.Button(self.saglik_tab, text="Güncelle", command=self.egzersiz_sekmeye_git)
        guncelle_button.pack(pady=5)

    def egzersiz_arayuz_olustur(self):
        frame = ttk.LabelFrame(self.egzersiz_tab, text="Egzersiz Seviyeleri", relief="groove")

        self.seviye1_checkbox = ttk.Checkbutton(frame, text="Seviye 1")
        self.seviye2_checkbox = ttk.Checkbutton(frame, text="Seviye 2")
        self.seviye3_checkbox = ttk.Checkbutton(frame, text="Seviye 3")
        
        self.seviye1_checkbox.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.seviye2_checkbox.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.seviye3_checkbox.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        frame.pack(padx=10, pady=10, fill="both", expand=True)

        basla_button = ttk.Button(self.egzersiz_tab, text="Başla", command=self.egzersiz_basla)
        basla_button.pack(pady=5)

    def kullanici_ekle(self):
        self.tab_control.select(1)  
        self.kullanici = Kullanici(
            self.adi_input.get(),
            self.soyadi_input.get(),
            self.yas_input.get(),
            self.cinsiyet_combo.get(),
            self.telefon_no_input.get(),
        )
        self.kullanici.sikayet = self.sikayet_combo.get()

    def egzersiz_sekmeye_git(self):
        self.tab_control.select(2)

    def egzersiz_basla(self):
        sikayet = self.kullanici.sikayet
        egzersiz_onerisi = ""

        if "Baş Bölgesi" in sikayet:
            egzersiz_onerisi = "Baş ağrıları için şakaklara yuvarlak çizerek masaj yapabilirsiniz."
            messagebox.showinfo("Egzersiz Önerisi", egzersiz_onerisi)
        elif "Boyun Bölgesi" in sikayet:
            egzersiz_onerisi = "Kafanızı öne arkaya sağa sola yavaşça çevirerek hafif bir egzersiz yapabilirsiniz.. Sonrasında sıcak bir bezle boyun bölgesini sararak ağrıyı azaltabilirsiniz."
            messagebox.showinfo("Egzersiz Önerisi", egzersiz_onerisi)
        elif "Kol Bölgesi" in sikayet:
            egzersiz_onerisi = "Kollarınızı 2 kgluk Dumbell kullanarak güçlendirebilirsiniz. Plates lastiği kullanarak kollarınızı esnetebilirsiniz."
            messagebox.showinfo("Egzersiz Önerisi", egzersiz_onerisi)
        elif "Göğüs Bölgesi" in sikayet:
            egzersiz_onerisi = "Göğüs ağrısı veya daralması için: Kobra gerinmesi yapabilirsiniz. Bu göğüs bölgesindeki kasları gerecek ve ciğerlerinize daha fazla oksijen gitmesine sebep olacaktır."
            messagebox.showinfo("Egzersiz Önerisi", egzersiz_onerisi)
        elif "Bacak Bölgesi" in sikayet:
            egzersiz_onerisi = "Bacak ağrıları için, bacak esnetme yapabilirsiniz. Bir bacağınız önde, diğeri arkadayken, öndeki bacağınızı oturur şekilde kırarken arkadaki bacağı dümdüz tutarak diz arkası kaslarını esnetirsiniz."
            messagebox.showinfo("Egzersiz Önerisi", egzersiz_onerisi)
        else:
            egzersiz_onerisi = "Genel olarak vücudu güçlendirecek egzersizler yapabilirsiniz."
            messagebox.showinfo("Egzersiz Önerisi", egzersiz_onerisi)


if __name__ == "__main__":
    root = tk.Tk()
    arayuz = Arayuz(root)
    root.mainloop()
