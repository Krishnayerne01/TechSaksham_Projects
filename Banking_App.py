import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk

# Custom Exception for Insufficient Funds
class InsufficientFundsError(Exception):
    pass

# Account Class
class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"💰 Deposited {amount}. New balance: {self.balance}")
            return f"✅ Deposited {amount}. New balance is {self.balance}."
        return "⚠️ Deposit amount must be positive."

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"🚨 Insufficient funds! Available balance is {self.balance}.")
        elif amount > 0:
            self.balance -= amount
            self.transactions.append(f"💸 Withdrew {amount}. New balance: {self.balance}")
            return f"✅ Withdrew {amount}. New balance is {self.balance}."
        return "⚠️ Withdrawal amount must be positive."

    def transfer(self, to_account, amount):
        if amount > self.balance:
            raise InsufficientFundsError("🚨 Insufficient funds for transfer.")
        self.withdraw(amount)
        to_account.deposit(amount)
        self.transactions.append(f"🔁 Transferred {amount} to {to_account.account_number}")
        to_account.transactions.append(f"💳 Received {amount} from {self.account_number}")
        return f"✅ Transferred {amount} to {to_account.account_number}."

# Banking App
class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 Digital Banking")
        self.root.geometry("500x700")
        self.root.configure(bg="#121212")  # Dark background
        self.accounts = {}
        self.current_account = None
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="🏦 Welcome to Digital Bank", font=("Helvetica", 22, "bold"), bg="#121212", fg="#00FFD1").pack(pady=20)
        tk.Label(self.root, text="🔢 Enter Account Number", font=("Arial", 14), bg="#121212", fg="white").pack()
        
        self.account_entry = tk.Entry(self.root, font=("Arial", 14), width=25, bg="#1E1E1E", fg="white", insertbackground="white")
        self.account_entry.pack(pady=5)

        self.create_button("🔐 Login", self.login, "#00FFD1", "#00CCAA")
        self.create_button("📝 Sign Up", self.create_signup_screen, "#FF007F", "#CC0066")

    def create_signup_screen(self):
        self.clear_window()

        tk.Label(self.root, text="🆕 Create New Account", font=("Helvetica", 18, "bold"), bg="#121212", fg="#00FFD1").pack(pady=20)
        
        tk.Label(self.root, text="🔢 Account Number", font=("Arial", 14), bg="#121212", fg="white").pack()
        self.new_account_entry = tk.Entry(self.root, font=("Arial", 14), width=25, bg="#1E1E1E", fg="white", insertbackground="white")
        self.new_account_entry.pack(pady=5)

        tk.Label(self.root, text="👤 Account Holder", font=("Arial", 14), bg="#121212", fg="white").pack()
        self.new_holder_entry = tk.Entry(self.root, font=("Arial", 14), width=25, bg="#1E1E1E", fg="white", insertbackground="white")
        self.new_holder_entry.pack(pady=5)

        self.create_button("✅ Create Account", self.create_account, "#00FFD1", "#00CCAA")
        self.create_button("🔙 Back", self.create_login_screen, "#FF007F", "#CC0066")

    def create_main_dashboard(self):
        self.clear_window()

        tk.Label(self.root, text=f"👋 Welcome, {self.current_account.account_holder}!", font=("Helvetica", 20, "bold"), bg="#121212", fg="#00FFD1").pack(pady=20)

        self.create_button("📄 View Account Info", self.view_account_info, "#0080FF", "#0066CC")
        self.create_button("💰 Deposit Money", self.deposit_money, "#00FFD1", "#00CCAA")
        self.create_button("💸 Withdraw Money", self.withdraw_money, "#FFDD00", "#CCAA00")
        self.create_button("🔁 Transfer Money", self.transfer_money, "#FF007F", "#CC0066")
        self.create_button("📜 Transaction History", self.transaction_history, "#FFA500", "#CC8400")
        self.create_button("🚪 Logout", self.create_login_screen, "#FF3B3B", "#CC2D2D")

    def create_button(self, text, command, color, hover_color):
        def on_enter(e):
            btn["background"] = hover_color

        def on_leave(e):
            btn["background"] = color

        btn = tk.Button(self.root, text=text, font=("Arial", 14, "bold"), bg=color, fg="white", activebackground=hover_color, padx=10, pady=5, relief="flat", command=command)
        btn.pack(pady=5, ipadx=5, ipady=3, fill="x")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        account_number = self.account_entry.get()
        if account_number in self.accounts:
            self.current_account = self.accounts[account_number]
            self.create_main_dashboard()
        else:
            messagebox.showerror("❌ Error", "Account not found!")

    def create_account(self):
        account_number = self.new_account_entry.get()
        account_holder = self.new_holder_entry.get()

        if account_number and account_holder:
            self.accounts[account_number] = Account(account_number, account_holder, 0)
            messagebox.showinfo("✅ Success", "Account Created Successfully!")
            self.create_login_screen()
        else:
            messagebox.showerror("❌ Error", "Please enter valid details!")

    def view_account_info(self):
        messagebox.showinfo("ℹ️ Account Info", f"📌 Account Number: {self.current_account.account_number}\n👤 Holder: {self.current_account.account_holder}\n💲 Balance: {self.current_account.balance}")

    def deposit_money(self):
        try:
            amount = float(simpledialog.askstring("💰 Deposit", "Enter deposit amount:"))
            messagebox.showinfo("✅ Deposit", self.current_account.deposit(amount))
        except ValueError:
            messagebox.showerror("❌ Error", "Invalid amount entered!")

    def withdraw_money(self):
        try:
            amount = float(simpledialog.askstring("💸 Withdraw", "Enter withdrawal amount:"))
            messagebox.showinfo("✅ Withdraw", self.current_account.withdraw(amount))
        except InsufficientFundsError as e:
            messagebox.showerror("❌ Error", str(e))
        except ValueError:
            messagebox.showerror("❌ Error", "Invalid amount entered!")

    def transfer_money(self):
        to_account_number = simpledialog.askstring("🔁 Transfer", "Enter recipient account number:")
        try:
            amount = float(simpledialog.askstring("🔁 Transfer", "Enter amount to transfer:"))
            if to_account_number in self.accounts:
                messagebox.showinfo("✅ Transfer", self.current_account.transfer(self.accounts[to_account_number], amount))
            else:
                messagebox.showerror("❌ Error", "Recipient account not found!")
        except InsufficientFundsError as e:
            messagebox.showerror("❌ Error", str(e))
        except ValueError:
            messagebox.showerror("❌ Error", "Invalid amount entered!")

    def transaction_history(self):
        history = "\n".join(self.current_account.transactions)
        messagebox.showinfo("📜 Transaction History", history if history else "No transactions yet.")

# Running the App
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
