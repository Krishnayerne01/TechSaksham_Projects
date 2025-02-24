import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox

# Scraping Function
def fetch_books():
    url = "http://books.toscrape.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        messagebox.showinfo("✅ Success", "Successfully fetched the book list! 📚")
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        
        book_list.delete(*book_list.get_children())  # Clear existing data
        
        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            rating_class = book.p["class"]
            rating = rating_class[1]  # Extracts rating (e.g., "Three", "Four")

            book_list.insert("", "end", values=(title, price, f"⭐ {rating}"))

    else:
        messagebox.showerror("❌ Error", f"Failed to fetch the page. Status Code: {response.status_code}")

# UI Setup
root = tk.Tk()
root.title("📚 Book Scraper UI")
root.geometry("700x500")
root.configure(bg="#2C2F33")  # Dark Theme

# Title Label
tk.Label(root, text="📚 Book Scraper", font=("Helvetica", 22, "bold"), fg="#00FFD1", bg="#2C2F33").pack(pady=20)

# Fetch Button
fetch_btn = tk.Button(root, text="🔍 Fetch Books", font=("Arial", 14, "bold"), bg="#00FFD1", fg="black", padx=10, pady=5, relief="flat", command=fetch_books)
fetch_btn.pack(pady=10, ipadx=10, ipady=5)

# Book List Display (Treeview)
columns = ("Title", "Price", "Rating")
book_list = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    book_list.heading(col, text=col)
    book_list.column(col, width=200, anchor="center")

book_list.pack(pady=20, fill="both", expand=True)

# Run Application
root.mainloop()
