# Penny Track

Penny Track is an offline expense management tool built with Python and SQLite. It provides a local system for recording financial transactions without requiring an internet connection.

---

## Features

- Transaction management for adding, viewing, and deleting expenses
- Contextual filtering by Today, This Week, This Month, This Year, or All Time
- 16 pre-seeded categories (Groceries, Rent, Utilities, etc.) to maintain organization
- SQLite-based local storage to keep data private and lightweight
- Real-time calculation of total expenses based on active filters
- Persistent history across sessions using a local database file

---

## Tech Stack

- Python
- SQLite

---

## How it Works

1. User enters an expense amount, category, and date
2. Data is stored locally in the `pennytrack.db` file
3. The interface queries the database based on the selected time filter
4. Total spending is automatically calculated and displayed
5. Users can remove transactions which immediately updates the local storage

---

## Design Decisions

- Local-first architecture ensures the app works without internet and keeps data private.
- Using a pre-seeded category list prevents manual setup and ensures immediate usability.
- Filter-based querying reduces clutter and keeps the transaction view relevant.
- Database logic is separated into dedicated modules for better maintainability.

---

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```
Run:
```bash
main.py
```

---

## Download
**The standalone Windows executable is available for direct use:**
[Downlaod pennytrack.exe](https://github.com/swastikagrawal/pennytrack/releases/tag/v1.0.0)
