import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import base64
from core.image_steg import encode_image, decode_image
from core.audio_steg import encode_audio, decode_audio
from core.video_steg import encode_video, decode_video
from core.security import encrypt_data, decrypt_data

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("800x600")
        self.root.configure(background="#000000")

        self.main_menu_frame = None
        self.encode_frame = None
        self.decode_frame = None

        self.create_main_menu()
        self.create_encode_frame()
        self.create_decode_frame()

        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.show_main_menu()

    def create_main_menu(self):
        self.main_menu_frame = ttk.Frame(self.root, style="TFrame")
        self.main_menu_frame.pack(expand=True, fill="both")

        title_label = ttk.Label(self.main_menu_frame, text="Steganography Tool", font=("Courier New", 24, "bold"), style="TLabel")
        title_label.pack(pady=50)

        button_frame = ttk.Frame(self.main_menu_frame, style="TFrame")
        button_frame.pack(pady=20)

        encode_button = ttk.Button(button_frame, text="Encode", command=self.show_encode_frame, style="Accent.TButton", width=20)
        encode_button.grid(row=0, column=0, padx=20, pady=10)

        decode_button = ttk.Button(button_frame, text="Decode", command=self.show_decode_frame, style="Accent.TButton", width=20)
        decode_button.grid(row=0, column=1, padx=20, pady=10)
    
    def create_encode_frame(self):
        self.encode_frame = ttk.Frame(self.root, style="TFrame")
        
        back_button = ttk.Button(self.encode_frame, text="< Back", command=self.show_main_menu)
        back_button.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        container = ttk.Frame(self.encode_frame, style="TFrame")
        container.grid(row=1, column=0, columnspan=3, padx=20, pady=20)
        
        # Cover file selection
        cover_file_label = ttk.Label(container, text="Cover File:")
        cover_file_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.cover_file_entry = ttk.Entry(container, width=60)
        self.cover_file_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        cover_file_button = ttk.Button(container, text="Browse...", command=self.select_cover_file)
        cover_file_button.grid(row=0, column=2, padx=10, pady=10)

        # Secret file selection
        secret_file_label = ttk.Label(container, text="Secret File:")
        secret_file_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.secret_file_entry = ttk.Entry(container, width=60)
        self.secret_file_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        secret_file_button = ttk.Button(container, text="Browse...", command=self.select_secret_file)
        secret_file_button.grid(row=1, column=2, padx=10, pady=10)

        # Password entry
        password_label = ttk.Label(container, text="Password:")
        password_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.password_entry = ttk.Entry(container, show="*")
        self.password_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        # Encode button
        encode_button = ttk.Button(container, text="Encode", command=self.encode, style="Accent.TButton")
        encode_button.grid(row=3, column=1, pady=20)

        # Progress bar
        self.encode_progress = ttk.Progressbar(container, orient="horizontal", length=400, mode="determinate")
        self.encode_progress.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        container.columnconfigure(1, weight=1)

    def create_decode_frame(self):
        self.decode_frame = ttk.Frame(self.root, style="TFrame")

        back_button = ttk.Button(self.decode_frame, text="< Back", command=self.show_main_menu)
        back_button.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        container = ttk.Frame(self.decode_frame, style="TFrame")
        container.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

        # Stego file selection
        stego_file_label = ttk.Label(container, text="Stego File:")
        stego_file_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.stego_file_entry = ttk.Entry(container, width=60)
        self.stego_file_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        stego_file_button = ttk.Button(container, text="Browse...", command=self.select_stego_file)
        stego_file_button.grid(row=0, column=2, padx=10, pady=10)

        # Password entry
        password_label = ttk.Label(container, text="Password:")
        password_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.decode_password_entry = ttk.Entry(container, show="*")
        self.decode_password_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        # Decode button
        decode_button = ttk.Button(container, text="Decode", command=self.decode, style="Accent.TButton")
        decode_button.grid(row=2, column=1, pady=20)

        # Progress bar
        self.decode_progress = ttk.Progressbar(container, orient="horizontal", length=400, mode="determinate")
        self.decode_progress.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        container.columnconfigure(1, weight=1)

    def show_main_menu(self):
        if self.encode_frame:
            self.encode_frame.pack_forget()
        if self.decode_frame:
            self.decode_frame.pack_forget()
        self.main_menu_frame.pack(expand=True, fill="both")

    def show_encode_frame(self):
        self.main_menu_frame.pack_forget()
        self.encode_frame.pack(expand=True, fill="both")

    def show_decode_frame(self):
        self.main_menu_frame.pack_forget()
        self.decode_frame.pack(expand=True, fill="both")

    def select_cover_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("Audio files", "*.wav"), ("Video files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.cover_file_entry.delete(0, tk.END)
            self.cover_file_entry.insert(0, file_path)

    def select_secret_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.secret_file_entry.delete(0, tk.END)
            self.secret_file_entry.insert(0, file_path)
            
    def select_stego_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("Audio files", "*.wav"), ("Video files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.stego_file_entry.delete(0, tk.END)
            self.stego_file_entry.insert(0, file_path)

    def encode(self):
        cover_file = self.cover_file_entry.get()
        secret_file = self.secret_file_entry.get()
        password = self.password_entry.get()

        if not all([cover_file, secret_file, password]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            self.status_bar.config(text="Encoding...")
            self.encode_progress.config(mode="indeterminate")
            self.encode_progress.start()

            secret_filename = os.path.basename(secret_file)
            with open(secret_file, "rb") as f:
                secret_data = f.read()
            
            data_to_hide = secret_filename.encode('utf-8') + b'|||' + secret_data
            encrypted_data = encrypt_data(data_to_hide, password)
            
            file_extension = os.path.splitext(cover_file)[1].lower()

            if file_extension in ['.png', '.jpg', '.jpeg']:
                output_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                if not output_file:
                    self.status_bar.config(text="Ready")
                    self.encode_progress.stop()
                    self.encode_progress.config(mode="determinate")
                    return
                
                if encode_image(cover_file, base64.b64encode(encrypted_data).decode('utf-8'), output_file):
                    self.status_bar.config(text="Encoding successful!")
                    messagebox.showinfo("Success", f"File saved to {output_file}")
                else:
                    self.status_bar.config(text="Encoding failed.")
                    messagebox.showerror("Error", "Encoding failed.")
            elif file_extension == '.wav':
                output_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
                if not output_file:
                    self.status_bar.config(text="Ready")
                    self.encode_progress.stop()
                    self.encode_progress.config(mode="determinate")
                    return
                
                if encode_audio(cover_file, base64.b64encode(encrypted_data).decode('utf-8'), output_file):
                    self.status_bar.config(text="Encoding successful!")
                    messagebox.showinfo("Success", f"File saved to {output_file}")
                else:
                    self.status_bar.config(text="Encoding failed.")
                    messagebox.showerror("Error", "Encoding failed.")
            elif file_extension in ['.mp4', '.avi', '.mov']:
                output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
                if not output_file:
                    self.status_bar.config(text="Ready")
                    self.encode_progress.stop()
                    self.encode_progress.config(mode="determinate")
                    return
                
                if encode_video(cover_file, base64.b64encode(encrypted_data).decode('utf-8'), output_file):
                    self.status_bar.config(text="Encoding successful!")
                    messagebox.showinfo("Success", f"File saved to {output_file}")
                else:
                    self.status_bar.config(text="Encoding failed.")
                    messagebox.showerror("Error", "Encoding failed.")
            else:
                messagebox.showerror("Error", "Unsupported file type for cover file.")

        except Exception as e:
            self.status_bar.config(text="Error during encoding.")
            messagebox.showerror("Error", str(e))
        finally:
            self.encode_progress.stop()
            self.encode_progress.config(mode="determinate")

    def decode(self):
        stego_file = self.stego_file_entry.get()
        password = self.decode_password_entry.get()

        if not all([stego_file, password]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            self.status_bar.config(text="Decoding...")
            self.decode_progress.config(mode="indeterminate")
            self.decode_progress.start()

            file_extension = os.path.splitext(stego_file)[1].lower()
            decrypted_data_with_filename = None

            if file_extension in ['.png', '.jpg', '.jpeg']:
                encrypted_data_b64 = decode_image(stego_file)
                if encrypted_data_b64:
                    encrypted_data = base64.b64decode(encrypted_data_b64)
                    decrypted_data_with_filename = decrypt_data(encrypted_data, password)
            elif file_extension == '.wav':
                encrypted_data_b64 = decode_audio(stego_file)
                if encrypted_data_b64:
                    encrypted_data = base64.b64decode(encrypted_data_b64)
                    decrypted_data_with_filename = decrypt_data(encrypted_data, password)
            elif file_extension in ['.mp4', '.avi', '.mov']:
                encrypted_data_b64 = decode_video(stego_file)
                if encrypted_data_b64:
                    encrypted_data = base64.b64decode(encrypted_data_b64)
                    decrypted_data_with_filename = decrypt_data(encrypted_data, password)

            if decrypted_data_with_filename:
                parts = decrypted_data_with_filename.split(b'|||', 1)
                if len(parts) == 2:
                    filename, decrypted_data = parts
                    output_file = filedialog.asksaveasfilename(initialfile=filename.decode('utf-8'), defaultextension=".*", filetypes=[("All files", "*.*")])
                else:
                    # Fallback for old format
                    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All files", "*.*")])
                    decrypted_data = decrypted_data_with_filename

                if not output_file:
                    self.status_bar.config(text="Ready")
                    self.decode_progress.stop()
                    self.decode_progress.config(mode="determinate")
                    return

                with open(output_file, "wb") as f:
                    f.write(decrypted_data)
                
                self.status_bar.config(text="Decoding successful!")
                messagebox.showinfo("Success", f"File saved to {output_file}")
            else:
                self.status_bar.config(text="Decoding failed.")
                messagebox.showerror("Error", "Decoding failed or no hidden message found.")

        except Exception as e:
            self.status_bar.config(text="Error during decoding.")
            messagebox.showerror("Error", "Decryption failed. Check your password or the file.")
        finally:
            self.decode_progress.stop()
            self.decode_progress.config(mode="determinate")

if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
