import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
# Örnek tarihi olaylar ve hikayeleri
tarihi_olaylar = {
    "Apollo 11 Ay Görevi": {"Hikaye": "Apollo 11, 16-24 Temmuz 1969 tarihleri arasında gerçekleşen uzay göreviydi. "
                                    "Neil Armstrong, Buzz Aldrin ve Michael Collins, Ay'a gitmek üzere görevlendirilen "
                                    "astronotlardı. 20 Temmuz 1969'da Apollo 11, Ay'a inen ilk insanlı uzay aracı oldu.",
                             "Kişiler": ["Neil Armstrong - İlk insanlı ay yürüyüşünün kumandanı",
                                         "Buzz Aldrin - Apollo 11 astronotu",
                                         "Michael Collins - Apollo 11 komuta modülü pilotu"]},
    "Fransız Devrimi": {"Hikaye": "Fransız Devrimi, 1789'da Fransa'da başlayan siyasi ve toplumsal bir dönüşümdü. "
                                   "Devrim, mutlakiyetçilik ve soyluların ayrıcalıklarına karşı halkın öfkesi sonucu patlak verdi. "
                                   "Fransız Devrimi, halkın eşitlik, özgürlük ve kardeşlik talepleriyle ortaya çıktı.",
                        "Kişiler": ["Napolyon Bonaparte - Fransa'nın imparatoru",
                                    "Jean-Jacques Rousseau - Aydınlanma Çağı filozofu",
                                    "Marie Antoinette - Fransa kraliçesi"]},
    "İkinci Dünya Savaşı": {"Hikaye": "İkinci Dünya Savaşı, 1939-1945 yılları arasında dünyanın dört bir yanındaki "
                                       "ülkeler arasında gerçekleşen büyük ölçekli bir savaştı. Milyonlarca asker ve sivil öldü, "
                                       "büyük ekonomik hasarlar meydana geldi ve tarih boyunca en yıkıcı çatışmalardan biri oldu.",
                             "Kişiler": ["Winston Churchill - Birleşik Krallık başbakanı",
                                         "Adolf Hitler - Nazi Almanyası lideri",
                                         "Franklin D. Roosevelt - ABD başkanı"]}
}

class TarihOlaylariUygulamasi:
    def __init__(self, master):
        self.master = master
        master.title("Tarihi Olaylar ve Hikayeler")

        self.layout = ttk.Frame(master, padding="20")
        self.layout.pack()

        self.event_label = ttk.Label(self.layout, text="Olay Seçin:")
        self.event_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.event_combo = ttk.Combobox(self.layout, values=list(tarihi_olaylar.keys()))
        self.event_combo.current(0)
        self.event_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.show_story_button = ttk.Button(self.layout, text="Hikayeyi Görüntüle", command=self.show_story)
        self.show_story_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        self.story_text = scrolledtext.ScrolledText(self.layout, width=40, height=10)
        self.story_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.person_label = ttk.Label(self.layout, text="Kişi Seçin:")
        self.person_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.person_combo = ttk.Combobox(self.layout)
        self.person_combo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.person_info_text = scrolledtext.ScrolledText(self.layout, width=40, height=3)
        self.person_info_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.extra_info_text = scrolledtext.ScrolledText(self.layout, width=40, height=5)
        self.extra_info_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.add_event_button = ttk.Button(self.layout, text="Olay Ekle", command=self.add_event)
        self.add_event_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    def show_story(self):
        selected_event = self.event_combo.get()
        story = tarihi_olaylar[selected_event]["Hikaye"]
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(tk.END, story)
        self.load_people(selected_event)
        self.show_extra_info(selected_event)  # Ek bilgileri göster

    def load_people(self, selected_event):
        people = tarihi_olaylar[selected_event]["Kişiler"]
        self.person_combo["values"] = people
        self.person_combo.current(0 if people else -1)

    def show_person(self, selected_person):
        selected_event = self.event_combo.get()
        people_info = tarihi_olaylar[selected_event]["Kişiler"]
        for info in people_info:
            if selected_person.split(' - ')[0] in info:
                self.person_info_text.delete(1.0, tk.END)
                self.person_info_text.insert(tk.END, info)
                break

    def show_extra_info(self, selected_event):
        extra_info = tarihi_olaylar[selected_event]
        formatted_info = "\n".join(["{}: {}".format(key, value) for key, value in extra_info.items()])
        self.extra_info_text.delete(1.0, tk.END)
        self.extra_info_text.insert(tk.END, formatted_info)

    def add_event(self):
        self.add_event_window = AddEventWindow(self.master, self)

class AddEventWindow:
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent
        self.add_event_window = tk.Toplevel(master)
        self.add_event_window.title("Olay Ekle")

        self.layout = ttk.Frame(self.add_event_window, padding="20")
        self.layout.pack()

        self.event_name_label = ttk.Label(self.layout, text="Olay Adı:")
        self.event_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.event_name_input = ttk.Entry(self.layout)
        self.event_name_input.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.event_desc_label = ttk.Label(self.layout, text="Olay Açıklaması:")
        self.event_desc_label.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.event_desc_input = scrolledtext.ScrolledText(self.layout, width=30, height=5)
        self.event_desc_input.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.people_label = ttk.Label(self.layout, text="Kişiler:")
        self.people_label.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.people_input = scrolledtext.ScrolledText(self.layout, width=30, height=5)
        self.people_input.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.add_button = ttk.Button(self.layout, text="Olay Ekle", command=self.add_event)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="e")

    def add_event(self):
        event_name = self.event_name_input.get()
        event_desc = self.event_desc_input.get("1.0", tk.END)
        people = self.people_input.get("1.0", tk.END).splitlines()
        if event_name and event_desc.strip():
            tarihi_olaylar[event_name] = {"Hikaye": event_desc, "Kişiler": people}
            self.parent.event_combo["values"] = list(tarihi_olaylar.keys())
            self.parent.event_combo.current(len(tarihi_olaylar) - 1)
            self.add_event_window.destroy()
        else:
            messagebox.showwarning("Uyarı", "Lütfen olay adı ve açıklaması girin.")

def main():
    root = tk.Tk()
    app = TarihOlaylariUygulamasi(root)
    root.mainloop()

if __name__ == "__main__":
    main()