from tkinter import *
import random
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

class SimpleBill:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Info")
        self.root.geometry("1100x680+50+30")

        self.entries = []

        Label(root, text="Billing Info", font=("arial", 24, "bold"),
              bg="#d1e7ff", fg="#003366").pack(fill=X, pady=(0, 10))

        cust_frame = LabelFrame(root, text="Customer", font=("arial", 14, "bold"), bg="#f0f8ff")
        cust_frame.pack(fill=X, padx=15, pady=5)

        Label(cust_frame, text="Name:", font=("arial", 13), bg="#f0f8ff").grid(row=0, column=0, padx=15, pady=12, sticky=W)
        self.name_entry = Entry(cust_frame, font=("arial", 13), width=40)
        self.name_entry.grid(row=0, column=1, pady=12, padx=10, sticky=W)

        self.bill_no = random.randint(100000, 999999)
        Label(cust_frame, text=f"Bill No: {self.bill_no}", font=("arial", 13, "bold"),
              bg="#f0f8ff", fg="#c62828").grid(row=0, column=2, padx=50, pady=12, sticky=E)

        items_frame = LabelFrame(root, text="Add Items (Name - Qty - Price)", font=("arial", 14, "bold"), bg="#e8f5e9")
        items_frame.pack(fill=BOTH, expand=True, padx=15, pady=5)

        Label(items_frame, text="item name", font=("arial", 11), bg="#e8f5e9").grid(row=0, column=0, padx=15, pady=6, sticky=W)
        Label(items_frame, text="quantity", font=("arial", 11), bg="#e8f5e9").grid(row=0, column=1, padx=15, pady=6)
        Label(items_frame, text="price", font=("arial", 11), bg="#e8f5e9").grid(row=0, column=2, padx=15, pady=6)

        self.items_container = Frame(items_frame, bg="#e8f5e9")
        self.items_container.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        self.add_item_row()

        btn_frame = Frame(root, bg="#ffffff")
        btn_frame.pack(fill=X, pady=12)

        Button(btn_frame, text="+ Add Item", font=("arial", 11, "bold"), bg="#388e3c", fg="white",
               command=self.add_item_row, width=12).pack(side=LEFT, padx=30)

        Button(btn_frame, text="Show Bill", font=("arial", 11, "bold"), bg="#1565c0", fg="white",
               command=self.show_bill, width=12).pack(side=LEFT, padx=20)

        Button(btn_frame, text="Save as PDF", font=("arial", 11, "bold"), bg="#8e24aa", fg="white",
               command=self.save_pdf, width=12).pack(side=LEFT, padx=20)

        Button(btn_frame, text="Clear All", font=("arial", 11, "bold"), bg="#c62828", fg="white",
               command=self.clear_all, width=12).pack(side=LEFT, padx=20)

        Button(btn_frame, text="Exit", font=("arial", 11, "bold"), bg="#455a64", fg="white",
               command=root.destroy, width=12).pack(side=LEFT, padx=20)

        bill_frame = LabelFrame(root, text="Receipt", font=("arial", 13, "bold"), bg="#fff8e1")
        bill_frame.pack(fill=BOTH, expand=True, padx=15, pady=(0, 10))

        self.bill_text = Text(bill_frame, font=("consolas", 12), height=15, bg="#fffdf7", relief="flat")
        self.bill_text.pack(fill=BOTH, expand=True, padx=8, pady=8)

        self.welcome_text()

        self.name_entry.bind("<KeyRelease>", lambda e: self.welcome_text())

    def add_item_row(self):
        row_frame = Frame(self.items_container, bg="#e8f5e9")
        row_frame.pack(fill=X, pady=5)

        name = Entry(row_frame, font=("arial", 12), width=42)
        name.pack(side=LEFT, padx=12)

        qty = Entry(row_frame, font=("arial", 12), width=10, justify="center")
        qty.pack(side=LEFT, padx=12)
        qty.insert(0, "1")

        price = Entry(row_frame, font=("arial", 12), width=12, justify="right")
        price.pack(side=LEFT, padx=12)
        price.insert(0, "0.00")

        Button(row_frame, text="X", font=("arial", 10, "bold"), bg="#e53935", fg="white",
               width=3, command=lambda f=row_frame: (f.destroy(), self.entries.remove((name, qty, price)))).pack(side=RIGHT, padx=10)

        self.entries.append((name, qty, price))

    def get_current_date(self):
        return datetime.now().strftime("%d/%m/%Y")

    def welcome_text(self):
        self.bill_text.delete("1.0", END)
        self.bill_text.insert(END, "          Billing Info\n\n")
        self.bill_text.insert(END, f"Bill No:   {self.bill_no}\n")
        self.bill_text.insert(END, f"Date:      {self.get_current_date()}\n")
        self.bill_text.insert(END, f"Customer:  {self.name_entry.get().strip() or '–'}\n")
        self.bill_text.insert(END, "\n" + "═" * 60 + "\n")

    def show_bill(self):
        self.welcome_text()

        total = 0.0
        has_items = False

        # Header row – clearly above items
        self.bill_text.insert(END, f"{'Item Description':<40} {'Qty':>6}   {'Price':>8}   {'Amount':>10}\n")
        self.bill_text.insert(END, "─" * 70 + "\n")

        for name_entry, qty_entry, price_entry in self.entries:
            name = name_entry.get().strip()
            if not name:
                continue
            try:
                qty = float(qty_entry.get() or 0)
                price = float(price_entry.get() or 0)
                if qty <= 0 or price <= 0:
                    continue
                amount = qty * price
                total += amount
                has_items = True

                self.bill_text.insert(END, f"{name:<40} {int(qty):>6}   {price:>8.2f}   {amount:>10.2f}\n")
            except ValueError:
                pass

        if not has_items:
            self.bill_text.insert(END, "No valid items entered\n")
            return

        self.bill_text.insert(END, "─" * 70 + "\n")
        self.bill_text.insert(END, f"{'TOTAL':<54} {total:>10.2f}\n")
        self.bill_text.insert(END, "═" * 70 + "\n\n")
        self.bill_text.insert(END, "          Thank you for your purchase\n\n")
        self.bill_text.insert(END, "          Billing System est. 2026")

    def save_pdf(self):
        if not any(e.get().strip() for e, _, _ in self.entries):
            messagebox.showwarning("Nothing to save", "Add some items first")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Bill as PDF"
        )
        if not file_path:
            return

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y = height - 80

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, y, "Billing Info")
        y -= 35

        c.setFont("Helvetica", 12)
        c.drawString(70, y, f"Bill No:   {self.bill_no}")
        y -= 20
        c.drawString(70, y, f"Date:      {self.get_current_date()}")
        y -= 20
        c.drawString(70, y, f"Customer:  {self.name_entry.get().strip() or '–'}")
        y -= 40

        c.line(60, y, width - 60, y)
        y -= 25

        c.drawString(70, y, "Item Description")
        c.drawRightString(380, y, "Qty")
        c.drawRightString(450, y, "Price")
        c.drawRightString(530, y, "Amount")
        y -= 15
        c.line(60, y, width - 60, y)
        y -= 25

        total = 0.0
        for name_entry, qty_entry, price_entry in self.entries:
            name = name_entry.get().strip()
            if not name:
                continue
            try:
                qty = float(qty_entry.get() or 0)
                price = float(price_entry.get() or 0)
                if qty <= 0 or price <= 0:
                    continue
                amount = qty * price
                total += amount

                c.drawString(70, y, name[:50])
                c.drawRightString(380, y, f"{qty:.0f}")
                c.drawRightString(450, y, f"{price:.2f}")
                c.drawRightString(530, y, f"{amount:.2f}")
                y -= 22
            except:
                pass

        c.line(60, y, width - 60, y)
        y -= 25

        c.setFont("Helvetica-Bold", 12)
        c.drawString(340, y, "TOTAL")
        c.drawRightString(530, y, f"{total:.2f}")
        y -= 50

        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, y, "Thank you for your purchase")
        y -= 20
        c.drawCentredString(width / 2, y, "Billing System est. 2026")

        c.save()
        messagebox.showinfo("Saved", f"Bill saved:\n{file_path}")

    def clear_all(self):
        if not messagebox.askyesno("Clear", "Clear everything?"):
            return

        for widget in self.items_container.winfo_children():
            widget.destroy()

        self.entries.clear()
        self.add_item_row()

        self.name_entry.delete(0, END)
        self.bill_no = random.randint(100000, 999999)

        self.welcome_text()


if __name__ == "__main__":
    root = Tk()
    app = SimpleBill(root)
    root.mainloop()