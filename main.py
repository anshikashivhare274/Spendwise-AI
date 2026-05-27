import customtkinter as ctk
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

from datetime import datetime

# ---------------- APP SETUP ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("1100x820")
app.title("SpendWise AI")
app.resizable(True, True)
app.configure(fg_color="#BAD797")

# ---------------- DATABASE ----------------

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    amount REAL,
    category TEXT,
    month TEXT
)
""")
conn.commit()

# ---------------- TITLE ----------------

title = ctk.CTkLabel(
    app,
    text="💸 SpendWise AI",
    font=("Poppins", 32, "bold"),
    text_color="#4a0010"
)
title.pack(pady=10)

subtitle = ctk.CTkLabel(
    app,
    text="Smart Personal Finance & Expense Tracker",
    font=("Poppins", 16),
    text_color="#6b0f1a"
)
subtitle.pack(pady=2)

# ---------------- MAIN FRAME ----------------

main_frame = ctk.CTkFrame(
    app,
    width=1060,
    height=740,
    corner_radius=20,
    fg_color="#BAD797"
)
main_frame.pack(pady=10)
main_frame.pack_propagate(False)

# ---------------- LEFT PANEL ----------------

left_panel = ctk.CTkFrame(
    main_frame,
    width=420,
    height=720,
    corner_radius=15,
    fg_color="#4a0010",
    border_width=1,
    border_color="#6b0f1a"
)
left_panel.pack(side="left", padx=20, pady=10)
left_panel.pack_propagate(False)

# ---------------- RIGHT PANEL ----------------

right_panel = ctk.CTkFrame(
    main_frame,
    width=560,
    height=720,
    corner_radius=15,
    fg_color="#4a0010",
    border_width=1,
    border_color="#6b0f1a"
)
right_panel.pack(side="left", padx=20, pady=10)
right_panel.pack_propagate(False)

# ---------------- LEFT PANEL CONTENT ----------------

section_title = ctk.CTkLabel(
    left_panel,
    text="Add Expense",
    font=("Poppins", 22, "bold"),
    text_color="#BAD797"
)
section_title.pack(pady=14)

budget_entry = ctk.CTkEntry(
    left_panel,
    placeholder_text="Set Monthly Budget",
    width=300,
    height=42,
    corner_radius=10,
    fg_color="#BAD797",
    border_color="#6b0f1a",
    border_width=2,
    text_color="#2a0d14",
    placeholder_text_color="#5a7a40"
)
budget_entry.pack(pady=6)

expense_name = ctk.CTkEntry(
    left_panel,
    placeholder_text="Expense Name",
    width=300,
    height=42,
    corner_radius=10,
    fg_color="#BAD797",
    border_color="#6b0f1a",
    border_width=2,
    text_color="#2a0d14",
    placeholder_text_color="#5a7a40"
)
expense_name.pack(pady=6)

amount_entry = ctk.CTkEntry(
    left_panel,
    placeholder_text="Amount",
    width=300,
    height=42,
    corner_radius=10,
    fg_color="#BAD797",
    border_color="#6b0f1a",
    border_width=2,
    text_color="#2a0d14",
    placeholder_text_color="#5a7a40"
)
amount_entry.pack(pady=6)

categories = ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]

category_menu = ctk.CTkOptionMenu(
    left_panel,
    values=categories,
    width=300,
    height=42,
    corner_radius=10,
    fg_color="#4a0010",
    text_color="#f5f0e8",
    button_color="#6b0f1a",
    button_hover_color="#8b1a2a",
    dropdown_fg_color="#BAD797",
    dropdown_hover_color="#d4eabc",
    dropdown_text_color="#2a0d14"
)
category_menu.pack(pady=6)

add_btn = ctk.CTkButton(
    left_panel,
    text="➕ Add Expense",
    width=300,
    height=44,
    font=("Poppins", 16, "bold"),
    fg_color="#6b0f1a",
    hover_color="#8b1a2a",
    text_color="#f5f0e8",
    corner_radius=12,
    command=lambda: add_expense()
)
add_btn.pack(pady=14)

chart_btn = ctk.CTkButton(
    left_panel,
    text="Show Analytics",
    width=300,
    height=44,
    font=("Poppins", 16, "bold"),
    fg_color="#6b0f1a",
    hover_color="#8b1a2a",
    text_color="#f5f0e8",
    corner_radius=12,
    command=lambda: show_chart()
)
chart_btn.pack(pady=8)

export_btn = ctk.CTkButton(
    left_panel,
    text="Export Report",
    width=300,
    height=44,
    font=("Poppins", 16, "bold"),
    fg_color="#BAD797",
    hover_color="#d4eabc",
    text_color="#4a0010",
    corner_radius=12,
    command=lambda: export_csv()
)
export_btn.pack(pady=8)

# ---------------- RIGHT PANEL CONTENT ----------------

months = []
current_year = datetime.now().year
for year in range(current_year - 2, current_year + 3):
    for month in range(1, 13):
        month_name = datetime(year, month, 1).strftime("%B %Y")
        months.append(month_name)

selected_month = ctk.StringVar(value=datetime.now().strftime("%B %Y"))

month_menu = ctk.CTkOptionMenu(
    right_panel,
    values=months,
    variable=selected_month,
    width=180,
    height=38,
    corner_radius=12,
    fg_color="#6b0f1a",
    button_color="#8b1a2a",
    button_hover_color="#a32638",
    dropdown_fg_color="#BAD797",
    dropdown_hover_color="#d4eabc",
    text_color="#f5f0e8",
    dropdown_text_color="#2a0d14",
    font=("Poppins", 13),
    command=lambda x: refresh_dashboard()
)

# ── SPENDING LABELS AT TOP ──────────────────────────────────────────

total_label = ctk.CTkLabel(
    right_panel,
    text="Monthly Spending: ₹0",
    font=("Poppins", 18, "bold"),
    text_color="#BAD797"
)
total_label.pack(pady=(10, 0))

warning_label = ctk.CTkLabel(
    right_panel,
    text="",
    font=("Poppins", 13, "bold"),
    text_color="red"
)
warning_label.pack(pady=1)

insight_label = ctk.CTkLabel(
    right_panel,
    text="",
    font=("Poppins", 12),
    text_color="#BAD797",
    wraplength=440,
    justify="left"
)
insight_label.pack(pady=2)

# ── DASHBOARD TITLE THEN MONTH DROPDOWN ────────────────────────────

dashboard_title = ctk.CTkLabel(
    right_panel,
    text="Dashboard",
    font=("Poppins", 22, "bold"),
    text_color="#BAD797"
)
dashboard_title.pack(pady=(6, 0))

month_menu.pack(pady=5)

# ───────────────────────────────────────────────────────────────────

search_entry = ctk.CTkEntry(
    right_panel,
    placeholder_text="Search by category...",
    width=380,
    height=38,
    corner_radius=10,
    fg_color="#BAD797",
    border_color="#6b0f1a",
    border_width=2,
    text_color="#2a0d14",
    placeholder_text_color="#5a7a40"
)
search_entry.pack(pady=4)

search_btn = ctk.CTkButton(
    right_panel,
    text="Search",
    width=140,
    height=36,
    corner_radius=10,
    fg_color="#6b0f1a",
    hover_color="#8b1a2a",
    command=lambda: search_expenses()
)
search_btn.pack(pady=3)

expense_list = ctk.CTkScrollableFrame(
    right_panel,
    width=460,
    height=200,
    fg_color="#BAD797",
    corner_radius=12
)
expense_list.pack(pady=5)

# ── DELETE BUTTON AT BOTTOM OF RIGHT PANEL ─────────────────────────

delete_btn = ctk.CTkButton(
    right_panel,
    text="🗑 Delete Expense",
    width=220,
    height=40,
    fg_color="#8b1a2a",
    hover_color="#a32638",
    font=("Poppins", 14, "bold"),
    text_color="#f5f0e8",
    corner_radius=12,
    command=lambda: delete_expense()
)
delete_btn.pack(pady=8)

# ───────────────────────────────────────────────────────────────────

# ---------------- GLOBALS ----------------

selected_expense_id = None
selected_frame = None
expenses = []
expense_categories = {}

# ---------------- FUNCTIONS ----------------

def add_expense():
    name = expense_name.get()
    amount = amount_entry.get()
    category = category_menu.get()

    if name == "" or amount == "":
        return

    month = selected_month.get()
    cursor.execute(
        "INSERT INTO expenses (name, amount, category, month) VALUES (?, ?, ?, ?)",
        (name, float(amount), category, month)
    )
    conn.commit()

    expense_name.delete(0, "end")
    amount_entry.delete(0, "end")

    refresh_dashboard()


def delete_expense():
    global selected_expense_id

    if selected_expense_id is None:
        return

    cursor.execute("DELETE FROM expenses WHERE id = ?", (selected_expense_id,))
    conn.commit()

    selected_expense_id = None
    refresh_dashboard()


def show_chart():
    cursor.execute(
        "SELECT category, amount FROM expenses WHERE month = ?",
        (selected_month.get(),)
    )
    rows = cursor.fetchall()

    if not rows:
        print("No data found for this month")
        return

    chart_categories = {}
    for category, amount in rows:
        chart_categories[category] = chart_categories.get(category, 0) + float(amount)

    plt.figure(figsize=(6, 6))
    plt.pie(list(chart_categories.values()), labels=list(chart_categories.keys()), autopct='%1.1f%%')
    plt.title("Expense Breakdown (This Month)")
    plt.show()


def export_csv():
    cursor.execute(
        "SELECT name, amount, category FROM expenses WHERE month = ?", (selected_month.get(),)
    )
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["Name", "Amount", "Category"])
    df.to_csv("expenses_report.csv", index=False)
    print("Report Exported Successfully!")


def search_expenses():
    keyword = search_entry.get().lower()

    for widget in expense_list.winfo_children():
        widget.destroy()

    cursor.execute(
        "SELECT id, name, amount, category FROM expenses WHERE month = ?",
        (selected_month.get(),)
    )
    rows = cursor.fetchall()

    for row in rows:
        expense_id, name, amount, category = row
        if keyword in category.lower():
            expense_frame = ctk.CTkFrame(expense_list, fg_color="#6b0f1a", corner_radius=10)
            expense_frame.pack(fill="x", pady=5, padx=5)

            expense_label = ctk.CTkLabel(
                expense_frame,
                text=f"{name} | ₹{amount} | {category}",
                font=("Poppins", 13),
                text_color="white"
            )
            expense_label.pack(side="left", padx=10, pady=10)


def refresh_dashboard():
    global selected_expense_id, selected_frame

    for widget in expense_list.winfo_children():
        widget.destroy()

    selected_frame = None

    cursor.execute(
        "SELECT id, name, amount, category FROM expenses WHERE month = ?",
        (selected_month.get(),)
    )
    rows = cursor.fetchall()
    total_spending = 0

    for row in rows:
        expense_id, name, amount, category = row
        total_spending += float(amount)

        expense_frame = ctk.CTkFrame(
            expense_list,
            fg_color="#6b0f1a",
            corner_radius=10
        )
        expense_frame.pack(fill="x", pady=5, padx=5)

        expense_label = ctk.CTkLabel(
            expense_frame,
            text=f"{name} | ₹{amount} | {category}",
            font=("Poppins", 13),
            text_color="white"
        )
        expense_label.pack(side="left", padx=10, pady=10)

        # ── CLICK TO HIGHLIGHT ──────────────────────────────────────
        def select_expense(id=expense_id, frame=expense_frame):
            global selected_expense_id, selected_frame
            if selected_frame is not None:
                selected_frame.configure(fg_color="#6b0f1a")
            selected_expense_id = id
            selected_frame = frame
            frame.configure(fg_color="#a32638")
        # ────────────────────────────────────────────────────────────

        expense_frame.bind("<Button-1>", lambda e, id=expense_id, f=expense_frame: select_expense(id, f))
        expense_label.bind("<Button-1>", lambda e, id=expense_id, f=expense_frame: select_expense(id, f))

    total_label.configure(text=f"Monthly Spending: ₹{total_spending}")

    budget = budget_entry.get()
    if budget != "":
        if total_spending > float(budget):
            warning_label.configure(text="⚠️ Monthly Budget Exceeded!")
        else:
            warning_label.configure(text="")

    generate_ai_insights()


def generate_ai_insights():
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE month = ? GROUP BY category",
        (selected_month.get(),)
    )
    rows = cursor.fetchall()

    if not rows:
        insight_label.configure(text="")
        return

    highest_category = max(rows, key=lambda x: x[1])
    insight_label.configure(
        text=f"💡 Most spending this month was on {highest_category[0]} (₹{highest_category[1]:.0f})."
    )


# ---------------- RUN APP ----------------

refresh_dashboard()
app.mainloop()