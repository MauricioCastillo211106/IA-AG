import customtkinter as tk
from Intrefece import PrimaryWindow

class Main:
    def __init__(self):
        self.primary = PrimaryWindow()
        self.primary.mainloop()
        
if __name__ == "__main__":
    app = Main()
    app.mainloop()