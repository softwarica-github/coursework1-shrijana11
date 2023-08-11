import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from cryptography.fernet import Fernet

key = b'lnTv6Mo7j4i5zhFLpqvD1KjTfVIo49F-7TPZuJWitCg='
keyfernet = Fernet(key)

class Coursework1:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption Decryption")

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.files_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Contents", menu=self.files_menu)
        self.files_menu.add_command(label="New File", command=self.file_creation)
        self.files_menu.add_command(label="Write File", command=self.write_to_file)

        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Encryption", command=self.encrypt_content)
        self.edit_menu.add_command(label="Decryption", command=self.decrypt_content)

        self.browse_button = tk.Button(self.root, text="Browse Directory", command=self.browse_directory)
        self.browse_button.pack()

        self.changes_button = tk.Button(self.root, text="Changes", command=self.show_changes)
        self.changes_button.pack()

    def browse_directory(self):
        chosen_path = filedialog.askdirectory(title="Select Directory")
        if chosen_path:
            self.current_path = chosen_path

    def file_creation(self):
        if hasattr(self, 'current_path'):
            file_name = filedialog.asksaveasfilename(title="Create File", initialdir=self.current_path)
            if file_name:
                try:
                    with open(file_name, "w") as file:
                        file.write("")
                    self.message("created a file")
                except Exception as e:
                    messagebox.showerror("Error", f"Error creating file: {str(e)}")

    def write_to_file(self):
        if hasattr(self, 'current_path'):
            file_name = filedialog.asksaveasfilename(title="Write File", initialdir=self.current_path)
            if file_name:
                content = simpledialog.askstring("Write Content", "Enter content:")
                if content:
                    try:
                        with open(file_name, "w") as file:
                            file.write(content)
                        self.message("wrote to file")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error writing to file: {str(e)}")

    def encrypt_content(self):
        if hasattr(self, 'current_path'):
            file_name = filedialog.askopenfilename(title="Select File to Encrypt", initialdir=self.current_path)
            if file_name:
                encrypted_path = encrypt_file(file_name)
                if encrypted_path:
                    self.message(f"Encrypted and saved as {encrypted_path}")
                else:
                    messagebox.showerror("Error", "Encryption Failed.")

    def decrypt_content(self):
        if hasattr(self, 'current_path'):
            file_name = filedialog.askopenfilename(title="Select File to Decrypt", initialdir=self.current_path)
            if file_name:
                decrypted_path = decrypt_file(file_name)
                if decrypted_path:
                    self.message(f"Decrypted and saved as {decrypted_path}")
                else:
                    messagebox.showerror("Error", "Decryption Failed.")

    def show_changes(self):
        if hasattr(self, 'current_path'):
            file_name = filedialog.askopenfilename(title="Select File to Show Changes", initialdir=self.current_path)
            if file_name:
                try:
                    with open(file_name, "r") as file:
                        content = file.read()
                    simpledialog.messagebox.showinfo("Changes", content)
                except Exception as e:
                    messagebox.showerror("Error", f"Error reading file: {str(e)}")

    def message(self, text):
        messagebox.showinfo("Message", text)

def encrypt_file(filepath):
    with open(filepath, 'rb') as f:
        contents = f.read()
    encrypted = keyfernet.encrypt(contents)
    encrypted_path = filepath + '.encrypt'
    with open(encrypted_path, 'wb') as f:
        f.write(encrypted)
    return encrypted_path

def decrypt_file(filepath):
    with open(filepath, 'rb') as f:
        contents = f.read()
    try:
        decrypted = keyfernet.decrypt(contents)
        decrypted_path = filepath.replace('.encrypt', '_decrypted.txt')
        with open(decrypted_path, 'wb') as f:
            f.write(decrypted)
        return decrypted_path
    except:
        return None

root = tk.Tk()
root.geometry("500x200")

explorer = Coursework1(root)

frame = tk.Frame(root)
frame.pack(pady=20)

result_label = tk.Label(root, font=('Calibri', 15))
result_label.pack(pady=20)

# Exit button
exit_button = tk.Button(root, text="Exit", font=('Calibri', 12), padx=10, command=root.destroy)
exit_button.pack()

root.mainloop()
