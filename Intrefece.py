import os
from tkinter import ttk
import customtkinter as ctk
import tkinter as tk
import pandas as pd
from SearchBook import search
from PIL import Image, ImageTk
import urllib.request
import io

class PrimaryWindow(tk.Tk):
    def __init__(self, master=None):  
        super().__init__(master)
        self.create_widgets()
        self.dataset = pd.DataFrame()
        self.dataset_file = None
        
    def create_widgets(self):
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(sticky="nsew")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(self.frame, text="AG Project", font=("Arial", 20))
        self.title.grid(row=0, column=0,columnspan=2, sticky="nsew")
        
        self.search_frame = ctk.CTkFrame(self.frame)
        self.search_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        
        self.search = ctk.CTkEntry(self.search_frame,width=300)
        self.search.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.search_button = ctk.CTkButton(self.search_frame, text="Search", command=self.search_book)
        self.search_button.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        self.LoadFrame = ctk.CTkFrame(self.frame, width=500)
        self.LoadFrame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        self.load_dataset = ctk.CTkLabel(self.LoadFrame, text="Load Dataset: ", font=("Arial", 15))
        self.load_dataset.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.button = ctk.CTkButton(self.LoadFrame, text="Open File", command=self.open_file)
        self.button.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        self.results_frame = ctk.CTkScrollableFrame(self.frame,width=900, height=600)
        self.results_frame.grid(row=3, column=0,columnspan=2, sticky="nsew", padx=10, pady=10)
        
        self.data_Frame = ctk.CTkFrame(self.frame,width=600)
        self.data_Frame.grid(row=0, column=2, rowspan=4, sticky="nsew", padx=10, pady=10)
        
        self.tree = ttk.Treeview(self.data_Frame)
        self.tree.place(relwidth=1, relheight=1) 

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        for i in range(4):
            self.results_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            self.results_frame.grid_rowconfigure(i, weight=1)
            
    def open_file(self):
        file = tk.filedialog.askopenfilename(title="Open File", filetypes=[("CSV Files", "*.csv")])
        if file:
            self.dataset = pd.read_csv(file)
            self.dataset_file = file
            self.update_table()
            
    def search_book(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        search_query = self.search.get()
        books = search(search_query)
        for i, book in enumerate(books):
            book_frame = ctk.CTkFrame(self.results_frame)
            book_frame.grid(row=i // 4, column=i % 4, padx=5, pady=5)

            raw_data = urllib.request.urlopen(book['image_link']).read()
            im = Image.open(io.BytesIO(raw_data))
            im = im.resize((120, 180))
            photo = ImageTk.PhotoImage(im)
            book_image = tk.Label(book_frame, image=photo)
            book_image.image = photo
            book_image.pack()

            book_label = ctk.CTkLabel(book_frame, text=book['title'], wraplength=120)
            book_label.pack(fill="x", expand=True)

            book_button = ctk.CTkButton(book_frame, text="+", command=lambda book=book: self.add_book_to_dataset(book))
            book_button.pack()
    
    def add_book_to_dataset(self, book):
        book_df = pd.DataFrame([book])
        
        if self.dataset_file is None:
            os.makedirs('dataset', exist_ok=True)
            self.dataset_file = 'dataset/books.csv'
            book_df.to_csv(self.dataset_file, index=False)
        else:
            book_df.to_csv(self.dataset_file, mode='a', header=False, index=False)
        
        self.dataset = pd.concat([self.dataset, book_df], ignore_index=True)
        
        # Actualiza la tabla
        self.update_table()
        
    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        self.tree = ttk.Treeview(self.data_Frame)
        self.tree.place(relwidth=1, relheight=1)
        self.tree["show"] = "headings" 
        dataset_without_image_link = self.dataset.drop(columns=['image_link'])
        
        self.tree["columns"] = list(dataset_without_image_link.columns)
        for column in dataset_without_image_link.columns:
            self.tree.column(column, width=30)
            self.tree.heading(column, text=column)
        
        for index, row in dataset_without_image_link.iterrows():
            self.tree.insert("", "end", values=list(row))