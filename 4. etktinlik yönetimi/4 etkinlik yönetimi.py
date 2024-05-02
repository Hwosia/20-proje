import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import sqlite3

class Event:
    def __init__(self, id, name, location, date):
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.participants = {}

    def add_participant(self, first_name, last_name, phone):
        full_name = f"{first_name} {last_name}"
        self.participants[full_name] = {"phone": phone, "ticket": False
                                        }

    def get_details(self):
        return f"Etkinlik Adı: {self.name}\nYeri: {self.location}\nTarihi: {self.date}"

class EventManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                event_id INTEGER,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                ticket BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (event_id) REFERENCES events(id)
            )
        """)
        self.conn.commit()

    def add_event(self, name, location, date):
        try:
            event_date = datetime.strptime(date, "%d.%m.%Y")
            if event_date < datetime.now():
                raise ValueError("Geçmiş bir tarih girdiniz.")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir tarih girin.")
            return None

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO events (name, location, date) VALUES (?, ?, ?)", (name, location, date))
        self.conn.commit()

        event_id = cursor.lastrowid
        return Event(event_id, name, location, date)

    def delete_event(self, event_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM events WHERE id=?", (event_id,))
        cursor.execute("DELETE FROM participants WHERE event_id=?", (event_id,))
        self.conn.commit()

    def get_events(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, location, date FROM events")
        events = []
        for row in cursor.fetchall():
            event = Event(*row)
            events.append(event)
        return events

    def add_participant(self, event_id, first_name, last_name, phone):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO participants (event_id, first_name, last_name, phone) VALUES (?, ?, ?, ?)", (event_id, first_name, last_name, phone))
        self.conn.commit()

    def get_participants(self, event_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT first_name, last_name, phone, ticket FROM participants WHERE event_id=?", (event_id,))
        participants = {}
        for row in cursor.fetchall():
            full_name = f"{row[0]} {row[1]}"
            participants[full_name] = {"phone": row[2], "ticket": row[3]}
        return participants

    def mark_ticket(self, event_id, first_name, last_name):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE participants SET ticket=TRUE WHERE event_id=? AND first_name=? AND last_name=?", (event_id, first_name, last_name))
        self.conn.commit()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Etkinlik Yönetimi")

        self.event_manager = EventManager("events.db")

        self.label = tk.Label(root, text="Hoşgeldiniz!")
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.show_button = tk.Button(root, text="Etkinlik Detayları", command=self.show_event_details)
        self.show_button.grid(row=1, column=0, padx=10, pady=5)

        self.add_button = tk.Button(root, text="Etkinlik Ekle", command=self.add_event)
        self.add_button.grid(row=1, column=1, padx=10, pady=5)

        self.event_listbox = tk.Listbox(root)
        self.event_listbox.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky=tk.NSEW)

        # Sayfa boyutlandırma ayarları
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.load_events()

    def add_event(self):
        name = simpledialog.askstring("Etkinlik Ekle", "Etkinlik adını giriniz:")
        location = simpledialog.askstring("Etkinlik Ekle", "Etkinlik yerini giriniz:")
        date = simpledialog.askstring("Etkinlik Ekle", "Etkinlik tarihini giriniz (örn. 18.04.2024):")

        if name and location and date:
            event = self.event_manager.add_event(name, location, date)
            if event:
                self.event_listbox.insert(tk.END, event.name)

    def show_event_details(self):
        selected_index = self.event_listbox.curselection()
        
        if selected_index:
            index = selected_index[0]
            details_window = EventDetailsWindow(self.root, self.event_manager, index, self.update_event_list)
        else:
            messagebox.showwarning("Hata", "Lütfen bir etkinlik seçin.")

    def load_events(self):
        self.event_listbox.delete(0, tk.END)
        for event in self.event_manager.get_events():
            self.event_listbox.insert(tk.END, event.name)

    def update_event_list(self):
        self.load_events()

class EventDetailsWindow:
    def __init__(self, parent, event_manager, index, update_callback):
        self.parent = parent
        self.event_manager = event_manager
        self.index = index
        self.update_callback = update_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Etkinlik Detayları")

        self.label = tk.Label(self.window, text=self.event_manager.get_events()[self.index].get_details())
        self.label.grid(row=0, column=0, columnspan=4, pady=20)

        self.delete_button = tk.Button(self.window, text="Etkinliği Sil", command=self.delete_event)
        self.delete_button.grid(row=0, column=3, padx=10, pady=5)

        self.participant_label = tk.Label(self.window, text="Katılımcılar:")
        self.participant_label.grid(row=1, column=0, padx=10)

        self.participant_listbox = tk.Listbox(self.window, width=50)
        self.participant_listbox.grid(row=1, column=1, padx=10, pady=10, sticky=tk.NSEW)

        self.add_participant_button = tk.Button(self.window, text="Katılımcı Ekle", command=self.add_participant)
        self.add_participant_button.grid(row=2, column=0, padx=10, pady=5)

        self.ticket_button = tk.Button(self.window, text="Bilet Kes", command=self.mark_ticket)
        self.ticket_button.grid(row=2, column=1, padx=10, pady=5)

        self.status_label = tk.Label(self.window, text="", fg="red")
        self.status_label.grid(row=3, column=1, pady=10, sticky=tk.W)

        self.update_participant_list()

    def delete_event(self):
        if messagebox.askyesno("Etkinlik Sil", "Etkinliği silmek istediğinizden emin misiniz?"):
            self.event_manager.delete_event(self.event_manager.get_events()[self.index].id)
            self.update_callback()
            self.window.destroy()

    def update_participant_list(self):
        self.participant_listbox.delete(0, tk.END)
        for participant, info in self.event_manager.get_participants(self.event_manager.get_events()[self.index].id).items():
            ticket_status = "Bilet Kesildi" if info["ticket"] else "Bilet Kesilmedi"
            self.participant_listbox.insert(tk.END, f"{participant} - {info['phone']} - {ticket_status}")

    def add_participant(self):
        first_name = simpledialog.askstring("Katılımcı Ekle", "Adınızı giriniz:")
        last_name = simpledialog.askstring("Katılımcı Ekle", "Soyadınızı giriniz:")
        phone = simpledialog.askstring("Katılımcı Ekle", "Telefon numaranızı giriniz:")

        if first_name and last_name and phone:
            self.event_manager.add_participant(self.event_manager.get_events()[self.index].id, first_name, last_name, phone)
            self.update_participant_list()
            self.status_label.config(text="Katılımcı başarıyla eklendi.", fg="green")

    def mark_ticket(self):
        selected_participant_index = self.participant_listbox.curselection()
        
        if selected_participant_index:
            participant_index = selected_participant_index[0]
            participant_info = self.participant_listbox.get(participant_index)
            participant_name = participant_info.split(" - ")[0]
            first_name, last_name = participant_name.split()
            
            self.event_manager.mark_ticket(self.event_manager.get_events()[self.index].id, first_name, last_name)
            self.update_participant_list()
            self.status_label.config(text="Bilet kesildi.", fg="green")
        else:
            self.status_label.config(text="Bilet daha kesilmedi. Para bekleniyor.", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
