import tkinter as tk
from tkinter import messagebox
import math

# Box information
boxes = {
    1: {
        "name": "Small Box",
        "dimensions": (30, 20, 15),
        "max_weight": 5,
        "price_per_kg": 50,
        "base_price":100 # เพิ่ม base price
    },
    2: {
        "name": "Medium Box",
        "dimensions": (40, 30, 20),
        "max_weight": 10,
        "price_per_kg": 40,
        "base_price": 150
    },
    3: {
        "name": "Large Box",
        "dimensions": (60, 40, 30),
        "max_weight": 20,
        "price_per_kg": 30,
        "base_price": 200
    },
    4: {
        "name": "Extra Large Box",
        "dimensions": (80, 60, 50),
        "max_weight": 30,
        "price_per_kg": 25,
        "base_price": 300
    },
}
# Dictionary for province GPS coordinates (Lat, Long)
province_coords = {
    "Chiang Mai": (18.787747, 98.993128),
    "Khon Kaen": (16.441935, 102.835992),
    "Nakhon Ratchasima": (14.979900, 102.097769),
    "Songkhla": (7.189343, 100.595171),
    "Phuket": (7.880447, 98.392540),
    "Bangkok": (13.756331, 100.501762)
}

def calculate_price_and_weight(box_info, weight):
    if weight > box_info["max_weight"]:
        return None, "Weight exceeds the box limit"

    total_price = weight * box_info["price_per_kg"] + box_info["base_price"]  # เพิ่มราคาฐาน
    return total_price, weight


def add_delivery_time(start_time, delivery_time):
    start_hour, start_minute = map(int, start_time.split(':'))
    delivery_hour, delivery_minute = map(int, delivery_time.split(':'))

    total_minutes = (start_hour * 60 + start_minute) + (delivery_hour * 60 + delivery_minute)
    new_hour = (total_minutes // 60) % 24
    new_minute = total_minutes % 60

    return f"{new_hour:02d}:{new_minute:02d}"


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


class DeliveryApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Logistic Calculator")
        self.geometry("500x600")
        self.configure(bg="#99FFCC")  # เปลี่ยนสีพื้นหลังเป็น #99FFCC

        title_font = ("Arial", 16, "bold")
        label_font = ("Arial", 12)
        button_font = ("Arial", 12, "bold")

        # Title
        tk.Label(self,
                 text="Logistic Calculator",
                 font=title_font,
                 bg="#99FFCC",
                 fg="#333").pack(pady=20)

        # Weight entry section
        tk.Label(self,
                 text="Please enter the package weight (kg):",
                 font=label_font,
                 bg="#99FFCC",
                 fg="#333").pack(pady=10)
        self.weight_entry = tk.Entry(self, font=label_font)
        self.weight_entry.pack()

        # Calculate suitable box button
        tk.Button(self,
                  text="Select Box",
                  font=button_font,
                  bg="#4CAF50",
                  fg="white",
                  command=self.select_box).pack(pady=20)

        # Suitable box display section
        self.box_label = tk.Label(self,
                                  text="",
                                  font=label_font,
                                  bg="#99FFCC",
                                  fg="#333")
        self.box_label.pack(pady=10)

        # Delivery start time entry section
        tk.Label(self,
                 text="Enter the delivery start time (HH:MM):",
                 font=label_font,
                 bg="#99FFCC",
                 fg="#333").pack(pady=10)
        self.time_entry = tk.Entry(self, font=label_font)
        self.time_entry.pack()

        # Province selection
        tk.Label(self,
                 text="Select Destination Province:",
                 font=label_font,
                 bg="#99FFCC",
                 fg="#333").pack(pady=10)
        self.provinces = [
            "Chiang Mai", "Khon Kaen", "Nakhon Ratchasima", "Songkhla",
            "Phuket", "Bangkok"
        ]
        self.delivery_times = [
            "8:00", "6:00", "4:00", "10:00", "12:00", "2:00"
        ]  # Approx delivery times in hours from Bangkok
        self.province_var = tk.StringVar(value=self.provinces[0])
        tk.OptionMenu(self, self.province_var, *self.provinces).pack()

        # Calculate delivery time button
        tk.Button(self,
                  text="Calculate Delivery Time",
                  font=button_font,
                  bg="#2196F3",
                  fg="white",
                  command=self.calculate_time).pack(pady=20)

        # Delivery time display section
        self.time_label = tk.Label(self,
                                   text="",
                                   font=label_font,
                                   bg="#99FFCC",
                                   fg="#333")
        self.time_label.pack(pady=10)

        # Confirm button
        tk.Button(self,
                  text="Confirm Delivery",
                  font=button_font,
                  bg="#FF5722",
                  fg="white",
                  command=self.confirm_delivery).pack(pady=20)

        # Confirmation display section
        self.confirm_label = tk.Label(self,
                                      text="",
                                      font=label_font,
                                      bg="#99FFCC",
                                      fg="#333")
        self.confirm_label.pack(pady=10)

    def select_box(self):
        try:
            weight = float(self.weight_entry.get())
            suitable_boxes = [
                box_id for box_id, box_info in boxes.items()
                if weight <= box_info["max_weight"]
            ]

            if not suitable_boxes:
                messagebox.showerror("Error",
                                     "No suitable box for this weight")
                return

            self.box_choice = suitable_boxes[0]
            selected_box = boxes[self.box_choice]

            total_price, _ = calculate_price_and_weight(selected_box, weight)
            self.box_label.config(
                text=
                f"Selected Box: {selected_box['name']} (Size: {selected_box['dimensions'][0]}x{selected_box['dimensions'][1]}x{selected_box['dimensions'][2]} cm)\nTotal Price: {total_price:.2f} Baht"
            )

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid weight")

    def calculate_time(self):
        start_time = self.time_entry.get()

        if not hasattr(self, 'box_choice'):
            messagebox.showerror("Error", "Please select a box first")
            return

        try:
            selected_province = self.province_var.get()
            delivery_index = self.provinces.index(selected_province)
            delivery_time = self.delivery_times[delivery_index]
            estimated_arrival = add_delivery_time(start_time, delivery_time)
            self.time_label.config(
                text=
                f"Estimated Arrival Time in {selected_province}: {estimated_arrival}"
            )
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid time")

    def confirm_delivery(self):
        if not hasattr(self, 'box_choice'):
            messagebox.showerror("Error", "Please select a box first")
            return

        weight = self.weight_entry.get()
        selected_province = self.province_var.get()
        start_time = self.time_entry.get()

        if weight and selected_province and start_time:
            selected_box = boxes[self.box_choice]
            distance = haversine_distance(province_coords["Bangkok"][0], province_coords["Bangkok"][1],
                                          province_coords[selected_province][0], province_coords[selected_province][1])
            self.confirm_label.config(
                text=f"Delivery confirmed!\nPackage: {selected_box['name']}\nWeight: {weight} kg\nDistance: {distance:.2f} km\nProvince: {selected_province}\nStart Time: {start_time}"
            )
        else:
            messagebox.showerror("Error", "Please complete all fields")       


if __name__ == "__main__":
    app = DeliveryApp()
    app.mainloop()





    
    