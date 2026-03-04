import customtkinter as ctk
from database import get_connection
from datetime import date, timedelta

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FONT_TITLE = ("Consolas", 50, "bold")
FONT_LARGE = ("Consolas", 25, "bold")
FONT_NORMAL = ("Consolas", 20)
FONT_SMALL = ("Consolas", 15)

class MainView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_filter = ctk.StringVar(value="Today")
        self.filter_buttons = {}
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Penny Track", font=FONT_TITLE).pack(pady=20)

        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(pady=10)

        today_btn = ctk.CTkButton(filter_frame, text="Today", width=100,
                                  font=FONT_NORMAL, command=self.filter_today)
        today_btn.pack(side="left", padx=5)
        self.filter_buttons["Today"] = today_btn

        week_btn = ctk.CTkButton(filter_frame, text="This Week", width=100,
                                 font=FONT_NORMAL, command=self.filter_this_week)
        week_btn.pack(side="left", padx=5)
        self.filter_buttons["This Week"] = week_btn

        month_btn = ctk.CTkButton(filter_frame, text="This Month", width=100,
                                  font=FONT_NORMAL, command=self.filter_this_month)
        month_btn.pack(side="left", padx=5)
        self.filter_buttons["This Month"] = month_btn

        year_btn = ctk.CTkButton(filter_frame, text="This Year", width=100,
                                 font=FONT_NORMAL, command=self.filter_this_year)
        year_btn.pack(side="left", padx=5)
        self.filter_buttons["This Year"] = year_btn

        all_btn = ctk.CTkButton(filter_frame, text="All Time", width=100,
                                font=FONT_NORMAL, command=self.filter_all_time)
        all_btn.pack(side="left", padx=5)
        self.filter_buttons["All Time"] = all_btn

        self.update_button_styles("Today")

        self.total_label = ctk.CTkLabel(self, text="Total Expenses: 0.00",
                                        font=FONT_LARGE, text_color="#ff6b6b")
        self.total_label.pack(pady=15)

        ctk.CTkButton(self, text="+ Add Expense", width=200,
                      font=FONT_NORMAL, fg_color="#8BAE66", hover_color="#628141",
                      command=self.open_add_form).pack(pady=10)

        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_transactions()

    def update_button_styles(self, active_filter):
        for label, btn in self.filter_buttons.items():
            if label == active_filter:
                btn.configure(fg_color="#1f6aa5")
            else:
                btn.configure(fg_color="#2b2b2b")

    def filter_today(self):
        self.apply_filter("Today")

    def filter_this_week(self):
        self.apply_filter("This Week")

    def filter_this_month(self):
        self.apply_filter("This Month")

    def filter_this_year(self):
        self.apply_filter("This Year")

    def filter_all_time(self):
        self.apply_filter("All Time")

    def get_date_range(self):
        today = date.today()
        filter_type = self.selected_filter.get()

        if filter_type == "Today":
            start = today
        elif filter_type == "This Week":
            start = today - timedelta(days=7)
        elif filter_type == "This Month":
            start = today.replace(day=1)
        elif filter_type == "This Year":
            start = today.replace(month=1, day=1)
        elif filter_type == "All Time":
            start = date(2000, 1, 1)

        return str(start), str(today)

    def apply_filter(self, filter_name):
        self.selected_filter.set(filter_name)
        self.update_button_styles(filter_name)
        self.load_transactions()

    def load_transactions(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        start, end = self.get_date_range()

        connection = get_connection()
        sql = connection.cursor()

        sql.execute("""SELECT t.id, t.date, c.name, t.amount, t.note
                       FROM transactions t
                       JOIN categories c ON t.category_id = c.id
                       WHERE t.date BETWEEN ? AND ?
                       ORDER BY t.date DESC""", (start, end))
        rows = sql.fetchall()

        sql.execute("""SELECT SUM(t.amount)
                       FROM transactions t
                       WHERE t.date BETWEEN ? AND ?""", (start, end))
        total = sql.fetchone()[0] or 0
        connection.close()

        self.total_label.configure(text=f"Total Expenses: {total:.2f}")

        if not rows:
            ctk.CTkLabel(self.list_frame, text="No expenses found",
                         font=FONT_NORMAL).pack(pady=20)
            return

        for row in rows:
            row_frame = ctk.CTkFrame(self.list_frame, corner_radius=10)
            row_frame.pack(fill="x", pady=5, padx=5)

            transaction_id = row[0]

            ctk.CTkLabel(row_frame, text=row[1], width=120,
                         font=FONT_SMALL).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=row[2], width=150,
                         font=FONT_SMALL).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=f"{row[3]:.2f}", width=100,
                         font=FONT_SMALL).pack(side="left", padx=10)
            ctk.CTkLabel(row_frame, text=row[4] or "", width=200,
                         font=FONT_SMALL).pack(side="left", padx=10)

            delete_button = ctk.CTkButton(row_frame, text="Delete", width=80,
                                          font=FONT_SMALL, fg_color="#ff6b6b",
                                          hover_color="#DA3D20")
            delete_button.configure(command=self.make_delete_command(transaction_id))
            delete_button.pack(side="right", padx=10)

    def make_delete_command(self, transaction_id):
        def delete():
            self.delete_transaction(transaction_id)
        return delete

    def delete_transaction(self, transaction_id):
        connection = get_connection()
        sql = connection.cursor()
        sql.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        connection.commit()
        connection.close()
        self.load_transactions()

    def open_add_form(self):
        form = ctk.CTkToplevel(self)
        form.lift()
        form.focus_force()
        form.attributes("-topmost", True)
        form.title("Add Expense")
        form.geometry("400x450")
        form.resizable(False, False)

        ctk.CTkLabel(form, text="Amount", font=FONT_NORMAL).pack(pady=5)
        amount_entry = ctk.CTkEntry(form, font=FONT_NORMAL)
        amount_entry.pack(pady=5)

        ctk.CTkLabel(form, text="Category", font=FONT_NORMAL).pack(pady=5)
        category_var = ctk.StringVar()
        connection = get_connection()
        sql = connection.cursor()
        sql.execute("SELECT name FROM categories")
        categories = [row[0] for row in sql.fetchall()]
        connection.close()

        category_var.set(categories[0] if categories else "")
        ctk.CTkOptionMenu(form, variable=category_var,
                          values=categories, font=FONT_NORMAL).pack(pady=5)

        ctk.CTkLabel(form, text="Date (YYYY-MM-DD)", font=FONT_NORMAL).pack(pady=5)
        date_entry = ctk.CTkEntry(form, font=FONT_NORMAL)
        date_entry.insert(0, str(date.today()))
        date_entry.pack(pady=5)

        ctk.CTkLabel(form, text="Note (optional)", font=FONT_NORMAL).pack(pady=5)
        note_entry = ctk.CTkEntry(form, font=FONT_NORMAL)
        note_entry.pack(pady=5)

        def save():
            amount = amount_entry.get()
            category_name = category_var.get()
            transaction_date = date_entry.get()
            note = note_entry.get()

            if not amount or not category_name or not transaction_date:
                ctk.CTkLabel(form, text="Please fill all required fields",
                             font=FONT_NORMAL, text_color="red").pack()
                return

            connection = get_connection()
            sql = connection.cursor()
            sql.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            category_id = sql.fetchone()[0]
            sql.execute("""INSERT INTO transactions (amount, category_id, date, note)
                           VALUES (?, ?, ?, ?)""",
                        (float(amount), category_id, transaction_date, note))
            connection.commit()
            connection.close()
            form.destroy()
            self.load_transactions()

        ctk.CTkButton(form, text="Save Expense", width=200,
                      font=FONT_NORMAL, command=save).pack(pady=20)