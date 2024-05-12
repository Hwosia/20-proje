import tkinter as tk
from tkinter import ttk, messagebox

class RestaurantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YEMEKSEPETİ.COM")
        self.geometry("1440x500")

        self.menu_items = {
            "Hamburger": {"fiyat": 120, "stok": 15},
            "Pizza": {"fiyat": 200, "stok": 20},
            "Sosisli": {"fiyat": 75, "stok": 12},
            "Köfte": {"fiyat": 90, "stok": 18},
            "Makarna": {"fiyat": 50, "stok": 25},
            "Tavuk Şiş": {"fiyat": 150, "stok": 10},
            "Çıtır Tavuk": {"fiyat": 80, "stok": 14},
            "Salata": {"fiyat": 30, "stok": 30},
            "Pilav": {"fiyat": 40, "stok": 22},
            "Kumpir": {"fiyat": 70, "stok": 16},
        }

        self.drink_items = {
            "Kola": {"fiyat": 5, "stok": 20},
            "Limonata": {"fiyat": 4, "stok": 25},
            "Meyve Suyu": {"fiyat": 6, "stok": 18},
            "Çay": {"fiyat": 3, "stok": 30},
            "Kahve": {"fiyat": 7, "stok": 15},
        }

        self.selected_items = []
        self.menu_items_entry = {}  # Yemekler için entry widget'ları
        self.drink_items_entry = {}  # İçecekler için entry widget'ları
        self.layout = ttk.Frame(self)
        self.layout.grid(row=0, column=0, sticky="nsew")

        # Hoşgeldiniz mesajı
        welcome_label = ttk.Label(self, text="YEMEKSEPETİ.COM'un İNANILMAZ FIRSATLARINA HOŞGELDİNİZ!",
                                  font=("Arial", 20, "bold"))
        welcome_label.place(relx=0.5, rely=0.5, anchor="center")


        self.welcome_label = ttk.Label(self.layout, text="MAYIS AYINA ÖZEL ÜCRETSİZ KARGO!", font=("Arial", 16, "bold"))
        self.welcome_label.place(relx=0.5, rely=0.5, anchor="center")

        self.food_button = ttk.Button(self.layout, text="Yemekler", style="Accent.TButton", command=self.show_foods)
        self.food_button.grid(row=2, column=0, pady=5, padx=100, sticky="ew")

        self.drink_button = ttk.Button(self.layout, text="İçecekler", style="Accent.TButton", command=self.show_drinks)
        self.drink_button.grid(row=3, column=0, pady=5, padx=100, sticky="ew")

        self.order_button = ttk.Button(self.layout, text="Sipariş Ver", style="Order.TButton", command=self.place_order)
        self.order_button.grid(row=4, column=0, pady=5, padx=100, sticky="ew")

        self.history_button = ttk.Button(self.layout, text="Sipariş Geçmişi", style="Accent.TButton", command=self.show_order_history)
        self.history_button.grid(row=5, column=0, pady=5, padx=100, sticky="ew")

        self.stock_button = ttk.Button(self.layout, text="Stock Ekle", style="Accent.TButton", command=self.add_stock)
        self.stock_button.grid(row=6, column=0, pady=5, padx=100, sticky="ew")

        style = ttk.Style()
        style.configure("Accent.TButton", background="#4CAF50", foreground="black")
        style.configure("Order.TButton", background="#f44336", foreground="black")

        self.order_history_frame = ttk.Frame(self)
        self.order_history_frame.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")

        self.order_history_table = ttk.Treeview(self.order_history_frame, columns=("name", "surname", "phone", "address", "payment", "total_price", "items"), show="headings")
        self.order_history_table.heading("name", text="Ad")
        self.order_history_table.heading("surname", text="Soyad")
        self.order_history_table.heading("phone", text="Telefon Numarası")
        self.order_history_table.heading("address", text="Adres")
        self.order_history_table.heading("payment", text="Ödeme Tipi")
        self.order_history_table.heading("total_price", text="Toplam Tutar")
        self.order_history_table.heading("items", text="Alınan Ürünler")
        self.order_history_table.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.order_history_frame, orient="vertical", command=self.order_history_table.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.order_history_table.configure(yscrollcommand=self.scrollbar.set)

    def populate_menu(self, items, layout):
        row = 0
        col = 0
        for item in items:
            button = ttk.Button(layout, text=item, command=lambda item=item: self.add_item(item))
            button.grid(row=row, column=col)

            quantity_label = ttk.Label(layout, text="Stok: {}".format(items[item]["stok"]))
            quantity_label.grid(row=row, column=col + 1)

            col += 2
            if col >= 4:
                col = 0
                row += 1

    def add_item(self, item):
        dialog = tk.Toplevel(self)
        dialog.title("Adet Seçin")

        label = ttk.Label(dialog, text="Kaç adet {} istiyorsunuz?".format(item))
        label.pack()

        line_edit = ttk.Entry(dialog)
        line_edit.pack()

        add_button = ttk.Button(dialog, text="Ekle", command=lambda: self.add_to_selected(item, line_edit.get(), dialog))
        add_button.pack()

        remove_button = ttk.Button(dialog, text="Çıkar", command=lambda: self.remove_from_selected(item, line_edit.get(), dialog))
        remove_button.pack()

    def add_to_selected(self, item, quantity, dialog):
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
            self.selected_items.append({"item": item, "quantity": quantity})
            if item in self.menu_items:
                self.menu_items[item]["stok"] -= quantity
                messagebox.showinfo("Başarılı", "{} adet {} seçildi.".format(quantity, item))
            elif item in self.drink_items:
                self.drink_items[item]["stok"] -= quantity
                messagebox.showinfo("Başarılı", "{} adet {} seçildi.".format(quantity, item))
            dialog.destroy()
        except ValueError:
            messagebox.showwarning("Hata", "Geçerli bir sayı girin.")

    def remove_from_selected(self, item, quantity, dialog):
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
            for i, selected_item in enumerate(self.selected_items):
                if selected_item["item"] == item:
                    if selected_item["quantity"] >= quantity:
                        selected_item["quantity"] -= quantity
                        if selected_item["quantity"] == 0:
                            del self.selected_items[i]
                        if item in self.menu_items:
                            self.menu_items[item]["stok"] += quantity
                        elif item in self.drink_items:
                            self.drink_items[item]["stok"] += quantity
                        messagebox.showinfo("Başarılı", "{} adet {} çıkartıldı.".format(quantity, item))
                    else:
                        messagebox.showwarning("Uyarı", "Seçili {} kadar ürün yok.".format(item))
            dialog.destroy()
        except ValueError:
            messagebox.showwarning("Hata", "Geçerli bir sayı girin.")

    def place_order(self):
        total_price = sum(self.get_item_price(item["item"]) * item["quantity"] for item in self.selected_items)
        order_text = "Siparişiniz:\n\n"
        for item in self.selected_items:
            order_text += "{} x{} - Toplam: {} TL\n".format(item["item"], item["quantity"], self.get_item_price(item["item"]) * item["quantity"])
        order_text += "\nToplam Tutar: {} TL".format(total_price)

        confirmation = messagebox.askquestion("Sipariş Onayı", order_text)

        if confirmation == 'yes':
            self.get_customer_info(total_price)

    def get_item_price(self, item_name):
        if item_name in self.menu_items:
            return self.menu_items[item_name]["fiyat"]
        elif item_name in self.drink_items:
            return self.drink_items[item_name]["fiyat"]
        return 0

    def get_customer_info(self, total_price):
        customer_info = {}

        def process_order():
            nonlocal customer_info
            name = name_input.get()
            surname = surname_input.get()
            phone_number = phone_input.get()
            address = address_input.get()
            payment = payment_input.get()

            if len(phone_number) != 11 or not phone_number.startswith("05"):
                messagebox.showwarning("Hata", "Geçerli bir telefon numarası girin.")
                return

            customer_info = {
                "name": name,
                "surname": surname,
                "phone": phone_number,
                "address": address,
                "payment": payment,
                "total_price": total_price,
                "items": self.selected_items
            }
            self.process_order(customer_info)
            dialog.destroy()

        dialog = tk.Toplevel(self)
        dialog.title("Müşteri Bilgileri")

        name_label = ttk.Label(dialog, text="Ad:")
        name_label.grid(row=0, column=0)
        name_input = ttk.Entry(dialog)
        name_input.grid(row=0, column=1)

        surname_label = ttk.Label(dialog, text="Soyad:")
        surname_label.grid(row=1, column=0)
        surname_input = ttk.Entry(dialog)
        surname_input.grid(row=1, column=1)

        phone_label = ttk.Label(dialog, text="Telefon Numarası:")
        phone_label.grid(row=2, column=0)
        phone_input = ttk.Entry(dialog)
        phone_input.grid(row=2, column=1)

        address_label = ttk.Label(dialog, text="Adres:")
        address_label.grid(row=3, column=0)
        address_input = ttk.Entry(dialog)
        address_input.grid(row=3, column=1)

        payment_label = ttk.Label(dialog, text="Ödeme Tipi:")
        payment_label.grid(row=4, column=0)
        payment_input = ttk.Entry(dialog)
        payment_input.grid(row=4, column=1)

        confirm_button = ttk.Button(dialog, text="Onayla", command=process_order)
        confirm_button.grid(row=5, columnspan=2)

    def process_order(self, customer_info):
        self.selected_items = []  # Sipariş geçmişine eklendiğinde seçili ürünleri temizle
        self.order_history_table.insert("", "end", values=(customer_info["name"], customer_info["surname"], customer_info["phone"], customer_info["address"], customer_info["payment"], customer_info["total_price"], self.format_items(customer_info["items"])))
        order_text = "Siparişiniz:\n\n"
        for item in customer_info["items"]:
            order_text += "{} x{} - Toplam: {} TL\n".format(item["item"], item["quantity"], self.get_item_price(item["item"]) * item["quantity"])
        order_text += "\nToplam Tutar: {} TL\n\n".format(customer_info["total_price"])
        order_text += "Müşteri Bilgileri:\n"
        order_text += "Ad: {}\n".format(customer_info["name"])
        order_text += "Soyad: {}\n".format(customer_info["surname"])
        order_text += "Telefon Numarası: {}\n".format(customer_info["phone"])
        order_text += "Adres: {}\n".format(customer_info["address"])
        order_text += "Ödeme Tipi: {}\n".format(customer_info["payment"])

        print("Sipariş Bilgileri:", order_text)
        messagebox.showinfo("Sipariş Tamamlandı", "Siparişiniz alınmıştır. Teşekkür ederiz!")

    def format_items(self, items):
        formatted_items = ""
        for item in items:
            formatted_items += "{} x{}, ".format(item["item"], item["quantity"])
        return formatted_items.rstrip(", ")

    def show_drinks(self):
        dialog = tk.Toplevel(self)
        dialog.title("İçecekler")
        layout = ttk.Frame(dialog)
        layout.pack()
        self.populate_menu(self.drink_items, layout)

    def show_foods(self):
        dialog = tk.Toplevel(self)
        dialog.title("Yemekler")
        layout = ttk.Frame(dialog)
        layout.pack()
        self.populate_menu(self.menu_items, layout)

    def show_order_history(self):
        self.order_history_frame.tkraise()

    def add_stock(self):
        dialog = tk.Toplevel(self)
        dialog.title("Stok Ekle")

        menu_items_label = ttk.Label(dialog, text="Yemekler")
        menu_items_label.grid(row=0, column=0, padx=5, pady=5)

        row = 1
        for item in self.menu_items:
            label = ttk.Label(dialog, text=item)
            label.grid(row=row, column=0, padx=5, pady=5)
            entry = ttk.Entry(dialog)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.menu_items_entry[item] = entry
            row += 1

        drink_items_label = ttk.Label(dialog, text="İçecekler")
        drink_items_label.grid(row=0, column=2, padx=5, pady=5)

        row = 1
        for item in self.drink_items:
            label = ttk.Label(dialog, text=item)
            label.grid(row=row, column=2, padx=5, pady=5)
            entry = ttk.Entry(dialog)
            entry.grid(row=row, column=3, padx=5, pady=5)
            self.drink_items_entry[item] = entry
            row += 1

        confirm_button = ttk.Button(dialog, text="Onayla", command=self.update_stock)
        confirm_button.grid(row=row, columnspan=4, padx=5, pady=5)

    def update_stock(self):
        for item in self.menu_items:
            if self.menu_items_entry[item].get():
                try:
                    quantity = int(self.menu_items_entry[item].get())
                    self.menu_items[item]["stok"] += quantity
                except ValueError:
                    messagebox.showwarning("Hata", "Geçerli bir sayı girin.")

        for item in self.drink_items:
            if self.drink_items_entry[item].get():
                try:
                    quantity = int(self.drink_items_entry[item].get())
                    self.drink_items[item]["stok"] += quantity
                except ValueError:
                    messagebox.showwarning("Hata", "Geçerli bir sayı girin.")

        messagebox.showinfo("Başarılı", "Stoklar güncellendi.")

if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()
