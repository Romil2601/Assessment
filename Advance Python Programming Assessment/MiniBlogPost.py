import tkinter as tk
from tkinter import messagebox
import os
import re
from tkinter import PhotoImage

# -------------------------
# Post Class (same as before)
# -------------------------
class Post:
    def __init__(self, username, title, content):
        self.username = username
        self.title = title
        self.content = content

    def save_to_file(self):
        filename = re.sub(r'\W+', '_', f"{self.username}_{self.title}") + ".txt"
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Author: {self.username}\n")
                file.write(f"Title: {self.title}\n\n")
                file.write(self.content)
            return filename
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save post:\n{e}")
            return None


# -------------------------
# Main App
# -------------------------
class MiniBlogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniBlog Pro")
        self.root.configure(bg="#f5f9ff")

        # ✅ LOAD ICONS FIRST
        self.icon_user = tk.PhotoImage(file="icons/user.png").subsample(20, 20)
        self.icon_post = tk.PhotoImage(file="icons/post.png").subsample(20, 20)
        self.icon_save = tk.PhotoImage(file="icons/save.png").subsample(25, 25)

        # ✅ THEN create UI
        self.create_widgets()
        self.load_posts()

    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Left Panel (Form)
        left_frame = tk.Frame(main_frame, bg="#ffffff", bd=0, highlightbackground="#d6e6ff", highlightthickness=1)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0,10))

        # Right Panel (Posts)
        right_frame = tk.Frame(main_frame, bg="#ffffff", bd=0, highlightbackground="#d6e6ff", highlightthickness=1)
        right_frame.pack(side="right", fill="both", expand=True)

        # Title
        tk.Label(left_frame, text="Create Post", fg="#1b1b1b",
        bg="#ffffff", font=("Segoe UI", 16, "bold")).pack(pady=10)

        # Username
        user_frame = tk.Frame(left_frame, bg="#2b2b2b")
        user_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(user_frame, image=self.icon_user, fg="#1b1b1b", bg="#ffffff", padx=5).pack(anchor="w", padx=10, pady=5)
        tk.Label(user_frame, text=" Username", fg="#1b1b1b", bg="#ffffff", padx=5).pack(anchor="w", padx=10, pady=5)

        self.username_entry = tk.Entry(left_frame,  bg="#eef5ff", fg="#1b1b1b", insertbackground="#1b1b1b", relief="flat")
        self.username_entry.pack(fill="x", padx=10, pady=5)

        # Title
        title_frame = tk.Frame(left_frame, bg="#2b2b2b")
        title_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(title_frame, image=self.icon_post, fg="#1b1b1b", bg="#ffffff", padx=5).pack(anchor="w", padx=10, pady=5)
        tk.Label(title_frame, text=" Title", fg="#1b1b1b", bg="#ffffff", padx=5).pack(anchor="w", padx=10, pady=5)
        
        self.title_entry = tk.Entry(left_frame, bg="#eef5ff", fg="#1b1b1b", insertbackground="#1b1b1b", relief="flat")
        self.title_entry.pack(fill="x", padx=10, pady=5)

        # Content
        tk.Label(left_frame, fg="#1b1b1b", bg="#ffffff", padx=5).pack(anchor="w", padx=10, pady=5)
        self.content_text = tk.Text(left_frame, height=10, bg="#eef5ff", fg="#1b1b1b", insertbackground="#1b1b1b", relief="flat")
        self.content_text.pack(fill="both", padx=10, pady=5)

        # Save Button
        tk.Button(
            left_frame,
            text=" Save Post",
            image=self.icon_save,
            compound="left",
            bg="#0077b6",
            fg="white",
            activebackground="#005f8e",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5,
            command=self.save_post
        ).pack(pady=15)

        # Right Panel Title
        tk.Label(right_frame, fg="#1b1b1b", bg="#ffffff", padx=5).pack(anchor="w", padx=10, pady=5)

        # Listbox
        self.post_listbox = tk.Listbox(
            right_frame,
            bg="#eef5ff",
            fg="#1b1b1b",
            selectbackground="#0077b6",
            selectforeground="white",
            relief="flat"
        )
        self.post_listbox.pack(fill="both", padx=10, pady=5)
        self.post_listbox.bind("<<ListboxSelect>>", self.display_post)

        # Display Area
        self.display_area = tk.Text(
            right_frame,
            bg="#ffffff",
            fg="#1b1b1b",
            relief="flat"
        )
        self.display_area.pack(fill="both", padx=10, pady=10)

    # -------------------------
    def save_post(self):
        username = self.username_entry.get().strip()
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        if not username or not title or not content:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        post = Post(username, title, content)
        filename = post.save_to_file()

        if filename:
            messagebox.showinfo("Success", "Post saved!")
            self.post_listbox.insert(tk.END, filename)
            self.clear_fields()

    # -------------------------
    def load_posts(self):
        for file in os.listdir():
            if file.endswith(".txt"):
                self.post_listbox.insert(tk.END, file)

    # -------------------------
    def display_post(self, event):
        try:
            selected = self.post_listbox.get(self.post_listbox.curselection())
            with open(selected, "r", encoding="utf-8") as file:
                content = file.read()

            self.display_area.delete("1.0", tk.END)
            self.display_area.insert(tk.END, content)

        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")

    # -------------------------
    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)


# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = MiniBlogApp(root)
    root.mainloop()