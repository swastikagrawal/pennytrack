import customtkinter as ctk
from database import initialize_db
from seed import seed_categories
from main_view import MainView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Penny Track")
        self.geometry("1000x650")
        self.resizable(False, False)

        initialize_db()
        seed_categories()

        MainView(self).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()