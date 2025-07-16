import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from abc import ABC, abstractmethod
import pandas as pd
import random

# ---------------- Abstract Class & Subclasses ---------------- #
class Vehicle(ABC):
    def __init__(self, name, reg_no, owner):
        self.name = name
        self.reg_no = reg_no
        self.owner = owner

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def fuelEfficiency(self):
        pass

class Car(Vehicle):
    def start(self):
        return f"{self.name} (Car) started."

    def stop(self):
        return f"{self.name} (Car) stopped."

    def fuelEfficiency(self):
        return round(random.uniform(12, 18), 2)  # km/l

class Bike(Vehicle):
    def start(self):
        return f"{self.name} (Bike) started."

    def stop(self):
        return f"{self.name} (Bike) stopped."

    def fuelEfficiency(self):
        return round(random.uniform(35, 60), 2)  # km/l

class Truck(Vehicle):
    def start(self):
        return f"{self.name} (Truck) started."

    def stop(self):
        return f"{self.name} (Truck) stopped."

    def fuelEfficiency(self):
        return round(random.uniform(4, 8), 2)  # km/l

# ---------------- Tkinter GUI ---------------- #
class FastAndFuriousGarage:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast and Furious Garage")
        self.root.geometry("1200x800")
        self.root.configure(bg="#000000")

        self.vehicles = []  # List of Vehicle objects
        self.service_records = []
        self.current_service = None

        self.create_header()
        main_frame = tk.Frame(root, bg="#000000")
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)

        self.create_vehicle_tab()
        self.create_records_tab()
        self.create_status_bar()

    def create_header(self):
        header = tk.Frame(self.root, bg="#000000", height=80)
        header.pack(fill='x')
        tk.Label(header, text="FAST & FURIOUS GARAGE", font=('Arial', 28, 'bold'), bg="#000000", fg="#FF0000").pack(side='left', padx=20)
        tk.Button(header, text="Export Records", command=self.export_records, bg="#FF0000", fg="white").pack(side='right', padx=20)

    def create_vehicle_tab(self):
        vehicle_tab = ttk.Frame(self.notebook)
        self.notebook.add(vehicle_tab, text="Vehicle Management")

        form_frame = tk.LabelFrame(vehicle_tab, text="Register New Vehicle", padx=10, pady=10)
        form_frame.pack(side='left', fill='y', padx=10, pady=10)

        tk.Label(form_frame, text="Type:").grid(row=0, column=0, sticky='e')
        self.vehicle_type = ttk.Combobox(form_frame, values=["Car", "Bike", "Truck"])
        self.vehicle_type.grid(row=0, column=1)
        self.vehicle_type.set("Car")

        tk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky='e')
        self.vehicle_name = tk.Entry(form_frame)
        self.vehicle_name.grid(row=1, column=1)

        tk.Label(form_frame, text="License:").grid(row=2, column=0, sticky='e')
        self.reg_no = tk.Entry(form_frame)
        self.reg_no.grid(row=2, column=1)

        tk.Label(form_frame, text="Owner:").grid(row=3, column=0, sticky='e')
        self.owner_name = tk.Entry(form_frame)
        self.owner_name.grid(row=3, column=1)

        tk.Button(form_frame, text="Add Vehicle", command=self.add_vehicle, bg="#FF0000", fg="white").grid(row=4, column=1, pady=10)

        # Service Queue
        queue_frame = tk.LabelFrame(vehicle_tab, text="Service Queue")
        queue_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        self.vehicle_tree = ttk.Treeview(queue_frame, columns=("ID", "Type", "Name", "License", "Owner", "Status"), show='headings')
        for col in ("ID", "Type", "Name", "License", "Owner", "Status"):
            self.vehicle_tree.heading(col, text=col)
        self.vehicle_tree.pack(fill='both', expand=True)

        control_frame = tk.Frame(queue_frame)
        control_frame.pack(fill='x')
        self.start_btn = tk.Button(control_frame, text="Start Service", command=self.start_service, bg="#2ecc71", fg="white")
        self.start_btn.pack(side='left', padx=5)
        self.stop_btn = tk.Button(control_frame, text="Complete Service", command=self.stop_service, bg="#e74c3c", fg="white", state=tk.DISABLED)
        self.stop_btn.pack(side='left', padx=5)
        tk.Button(control_frame, text="Check Fuel Efficiency", command=self.check_fuel_efficiency, bg="#f39c12", fg="white").pack(side='left', padx=5)

    def create_records_tab(self):
        records_tab = ttk.Frame(self.notebook)
        self.notebook.add(records_tab, text="Service Records")
        self.records_tree = ttk.Treeview(records_tab, columns=("ID", "Vehicle", "License", "Start", "End", "Duration", "Fuel Efficiency"), show='headings')
        for col in ("ID", "Vehicle", "License", "Start", "End", "Duration", "Fuel Efficiency"):
            self.records_tree.heading(col, text=col)
        self.records_tree.pack(fill='both', expand=True)

    def create_status_bar(self):
        self.status_label = tk.Label(self.root, text="Ready", bg="#FF0000", fg="white")
        self.status_label.pack(fill='x', side='bottom')

    def add_vehicle(self):
        vtype = self.vehicle_type.get()
        name = self.vehicle_name.get().strip()
        reg_no = self.reg_no.get().strip()
        owner = self.owner_name.get().strip()
        if not all([vtype, name, reg_no, owner]):
            messagebox.showerror("Error", "All fields required")
            return

        # Create Vehicle Object
        if vtype == "Car":
            vehicle = Car(name, reg_no, owner)
        elif vtype == "Bike":
            vehicle = Bike(name, reg_no, owner)
        else:
            vehicle = Truck(name, reg_no, owner)

        vehicle.id = f"V{len(self.vehicles)+1:03d}"
        vehicle.status = "Waiting"
        vehicle.added_on = datetime.now().strftime("%Y-%m-%d %H:%M")

        self.vehicles.append(vehicle)
        self.vehicle_tree.insert("", "end", values=(vehicle.id, vtype, name, reg_no, owner, "Waiting"))

        self.vehicle_name.delete(0, tk.END)
        self.reg_no.delete(0, tk.END)
        self.owner_name.delete(0, tk.END)
        self.update_status(f"Vehicle {vehicle.id} added.")

    def start_service(self):
        selected = self.vehicle_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a vehicle")
            return
        item = self.vehicle_tree.item(selected)['values']
        vid = item[0]

        for v in self.vehicles:
            if v.id == vid:
                self.current_service = {
                    "id": f"S{len(self.service_records)+1:03d}",
                    "vehicle": v,
                    "start": datetime.now(),
                    "end": None,
                    "duration": None,
                    "fuel_efficiency": None
                }
                break

        self.vehicle_tree.item(selected, values=(item[0], item[1], item[2], item[3], item[4], "In Service"))
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.update_status(f"Service started for {item[2]}")

    def stop_service(self):
        if not self.current_service:
            return
        self.current_service["end"] = datetime.now()
        duration = self.current_service["end"] - self.current_service["start"]
        self.current_service["duration"] = str(duration).split(".")[0]
        self.service_records.append(self.current_service)

        self.current_service = None
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_records_display()
        self.update_status("Service completed.")

    def check_fuel_efficiency(self):
        if not self.current_service:
            messagebox.showinfo("Info", "No vehicle in service")
            return
        v = self.current_service["vehicle"]
        efficiency = v.fuelEfficiency()
        self.current_service["fuel_efficiency"] = f"{efficiency} km/l"
        self.update_records_display()
        self.update_status(f"Fuel efficiency: {efficiency} km/l")

    def update_records_display(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        for record in self.service_records:
            v = record["vehicle"]
            self.records_tree.insert("", "end", values=(
                record["id"],
                f"{v.__class__.__name__} - {v.name}",
                v.reg_no,
                record["start"].strftime("%Y-%m-%d %H:%M:%S"),
                record["end"].strftime("%Y-%m-%d %H:%M:%S"),
                record["duration"],
                record["fuel_efficiency"] or "N/A"
            ))
        if self.current_service:
            v = self.current_service["vehicle"]
            self.records_tree.insert("", "end", values=(
                self.current_service["id"],
                f"{v.__class__.__name__} - {v.name}",
                v.reg_no,
                self.current_service["start"].strftime("%Y-%m-%d %H:%M:%S"),
                "In Progress",
                "N/A",
                self.current_service["fuel_efficiency"] or "Not Checked"
            ), tags=('current',))
            self.records_tree.tag_configure('current', background='#fffacd')

    def export_records(self):
        if not self.service_records:
            messagebox.showerror("Error", "No records to export")
            return
        data = {"ID": [], "Vehicle": [], "License": [], "Start": [], "End": [], "Duration": [], "Fuel Efficiency": []}
        for record in self.service_records:
            v = record["vehicle"]
            data["ID"].append(record["id"])
            data["Vehicle"].append(f"{v.__class__.__name__} - {v.name}")
            data["License"].append(v.reg_no)
            data["Start"].append(record["start"].strftime("%Y-%m-%d %H:%M:%S"))
            data["End"].append(record["end"].strftime("%Y-%m-%d %H:%M:%S"))
            data["Duration"].append(record["duration"])
            data["Fuel Efficiency"].append(record["fuel_efficiency"] or "N/A")
        df = pd.DataFrame(data)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")])
        if file_path:
            if file_path.endswith('.csv'):
                df.to_csv(file_path, index=False)
            else:
                df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Exported successfully!")

    def update_status(self, msg):
        self.status_label.config(text=msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = FastAndFuriousGarage(root)
    root.mainloop()
