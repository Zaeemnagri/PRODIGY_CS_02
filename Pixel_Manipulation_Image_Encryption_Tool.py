import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np

selected_image = None
processed_image = None
photo_preview = None
shuffle_indices = None

# ================= IMAGE LOAD & SAVE =================

def update_preview(img, title_text):
    global photo_preview
    img_copy = img.copy()
    img_copy.thumbnail((350, 350))
    photo_preview = ImageTk.PhotoImage(img_copy)
    preview_img_label.config(image=photo_preview, bg="#F4F6F9")
    preview_title.config(text=title_text)

def open_image():
    global selected_image
    path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if path:
        try:
            selected_image = Image.open(path).convert("RGB")
            update_preview(selected_image, "Original Image (Preview)")
            status_label.config(text="Status: Image loaded successfully", fg="#50C878")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image.\n{e}")

def save_image():
    global processed_image
    if processed_image is None:
        messagebox.showerror("Error", "No image to save")
        return
    path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG file", "*.png")])
    if path:
        try:
            processed_image.save(path)
            status_label.config(text="Status: Image saved successfully", fg="#50C878")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image.\n{e}")

# ================= BASIC METHODS =================

def pixel_shift(img, key, encrypt=True):
    arr = np.array(img)
    if encrypt:
        arr = (arr + key) % 256
    else:
        arr = (arr - key) % 256
    return Image.fromarray(arr.astype('uint8'))

def channel_swap(img):
    arr = np.array(img)
    arr = arr[..., [2, 0, 1]]
    return Image.fromarray(arr.astype('uint8'))

def negative(img):
    arr = np.array(img)
    arr = 255 - arr
    return Image.fromarray(arr.astype('uint8'))

def xor_encrypt(img, key):
    arr = np.array(img)
    arr = arr ^ key
    return Image.fromarray(arr.astype('uint8'))

# ================= STRONG ENCRYPTION =================

def strong_encrypt(img, key):
    arr = np.array(img)
    flat = arr.reshape(-1, 3)

    np.random.seed(key)
    indices = np.random.permutation(len(flat))

    shuffled = flat[indices]
    encrypted = shuffled ^ key

    encrypted = encrypted.reshape(arr.shape)
    return Image.fromarray(encrypted.astype('uint8')), indices

def strong_decrypt(img, key, indices):
    arr = np.array(img)
    flat = arr.reshape(-1, 3)

    decrypted = flat ^ key
    reverse = np.argsort(indices)
    unshuffled = decrypted[reverse]

    unshuffled = unshuffled.reshape(arr.shape)
    return Image.fromarray(unshuffled.astype('uint8'))

# ================= PROCESS FUNCTION =================

def process_image(mode):
    global processed_image, shuffle_indices

    if selected_image is None:
        messagebox.showerror("Error", "Upload image first")
        return

    method = method_var.get()
    img = selected_image.copy()

    try:
        key_str = key_entry.get()
        # For methods that don't need a key, default to 0
        key = int(key_str) if key_str else 0
    except ValueError:
        messagebox.showerror("Error", "Key must be a valid number")
        return

    try:
        if method == "Pixel Shift":
            processed_image = pixel_shift(img, key, encrypt=(mode=="encrypt"))

        elif method == "Channel Swap":
            processed_image = channel_swap(img)

        elif method == "Negative":
            processed_image = negative(img)

        elif method == "XOR Encryption":
            processed_image = xor_encrypt(img, key)

        elif method == "Strong Encryption":
            if mode == "encrypt":
                processed_image, shuffle_indices = strong_encrypt(img, key)
            else:
                if shuffle_indices is None:
                    messagebox.showerror("Error", "Encrypt first before decrypting this session")
                    return
                processed_image = strong_decrypt(img, key, shuffle_indices)

        update_preview(processed_image, f"Processed Image ({mode.capitalize()}ed)")
        status_label.config(text=f"Status: {mode.capitalize()}ion completed!", fg="#50C878")
    except Exception as e:
        messagebox.showerror("Process Error", f"An error occurred:\n{str(e)}")
        status_label.config(text="Status: Error during processing", fg="#E74C3C")

# ================= GUI SETUP =================

root = tk.Tk()
root.title("Advanced Image Encryption Tool")
root.geometry("850x550")
root.configure(bg="#F4F6F9")
root.resizable(False, False)

# Style configuration
style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground="#FFFFFF", background="#F8F9FA", foreground="#2C3E50", arrowcolor="#2C3E50")
style.map('TCombobox', fieldbackground=[('readonly', '#FFFFFF')], selectbackground=[('readonly', '#E2E6EA')], selectforeground=[('readonly', '#2C3E50')])

# Title
title_frame = tk.Frame(root, bg="#F4F6F9")
title_frame.pack(fill="x", pady=(20, 10))
title_label = tk.Label(title_frame, text="🛡️ Advanced Image Encryption", font=("Segoe UI", 22, "bold"), bg="#F4F6F9", fg="#2C3E50")
title_label.pack()

# Main Container
main_frame = tk.Frame(root, bg="#F4F6F9")
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Left Column (Controls)
left_frame = tk.Frame(main_frame, bg="#FFFFFF", bd=0, relief="flat", highlightbackground="#E0E0E0", highlightthickness=1)
left_frame.pack(side="left", fill="y", ipadx=20, ipady=20)

# Right Column (Preview)
right_frame = tk.Frame(main_frame, bg="#FFFFFF", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
right_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

# --- Left Frame Widgets ---

lbl_method = tk.Label(left_frame, text="Select Encryption Method", font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#34495E")
lbl_method.pack(pady=(20, 5), anchor="w", padx=20)

method_var = tk.StringVar()
method_combo = ttk.Combobox(left_frame, textvariable=method_var, font=("Segoe UI", 10), state="readonly", width=25)
method_combo['values'] = ("Pixel Shift", "Channel Swap", "Negative", "XOR Encryption", "Strong Encryption")
method_combo.current(0)
method_combo.pack(pady=(0, 20), padx=20)

lbl_key = tk.Label(left_frame, text="Encryption Key (Number)", font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg="#34495E")
lbl_key.pack(pady=(5, 5), anchor="w", padx=20)

key_entry = tk.Entry(left_frame, width=28, font=("Segoe UI", 11), bg="#F8F9FA", fg="#2C3E50", insertbackground="black", relief="solid", highlightthickness=1, highlightbackground="#E0E0E0", highlightcolor="#4A90E2")
key_entry.pack(pady=(0, 30), padx=20, ipady=5)

# Action Buttons
btn_frame = tk.Frame(left_frame, bg="#FFFFFF")
btn_frame.pack(pady=10)

btn_encrypt = tk.Button(btn_frame, text="Encrypt Image", font=("Segoe UI", 10, "bold"), bg="#50C878", fg="white", activebackground="#3CB371", activeforeground="white", relief="flat", width=14, cursor="hand2", command=lambda: process_image("encrypt"))
btn_encrypt.grid(row=0, column=0, padx=5, pady=5, ipady=3)

btn_decrypt = tk.Button(btn_frame, text="Decrypt Image", font=("Segoe UI", 10, "bold"), bg="#E74C3C", fg="white", activebackground="#C0392B", activeforeground="white", relief="flat", width=14, cursor="hand2", command=lambda: process_image("decrypt"))
btn_decrypt.grid(row=0, column=1, padx=5, pady=5, ipady=3)

# File Buttons
file_btn_frame = tk.Frame(left_frame, bg="#FFFFFF")
file_btn_frame.pack(pady=20)

btn_upload = tk.Button(file_btn_frame, text="Upload File", font=("Segoe UI", 10), bg="#4A90E2", fg="white", activebackground="#357ABD", activeforeground="white", relief="flat", width=14, cursor="hand2", command=open_image)
btn_upload.grid(row=0, column=0, padx=5, ipady=3)

btn_save = tk.Button(file_btn_frame, text="Save File", font=("Segoe UI", 10), bg="#F39C12", fg="white", activebackground="#D68910", activeforeground="white", relief="flat", width=14, cursor="hand2", command=save_image)
btn_save.grid(row=0, column=1, padx=5, ipady=3)

info_text = "Note: Use the exact same key for decryption.\nStrong Encryption provides highest security."
lbl_info = tk.Label(left_frame, text=info_text, font=("Segoe UI", 9, "italic"), bg="#FFFFFF", fg="#7F8C8D", justify="left")
lbl_info.pack(side="bottom", pady=20)

# --- Right Frame Widgets ---

preview_title = tk.Label(right_frame, text="Image Preview", font=("Segoe UI", 14, "bold"), bg="#FFFFFF", fg="#2C3E50")
preview_title.pack(pady=(20, 10))

# A frame to hold the image, acting as a background border
img_container = tk.Frame(right_frame, bg="#F4F6F9", width=360, height=360, highlightbackground="#E0E0E0", highlightthickness=1)
img_container.pack(expand=True)
img_container.pack_propagate(False)

preview_img_label = tk.Label(img_container, text="No image loaded", font=("Segoe UI", 12), bg="#F4F6F9", fg="#7F8C8D")
preview_img_label.pack(expand=True, fill="both")

status_label = tk.Label(right_frame, text="Status: Waiting for action...", font=("Segoe UI", 10), bg="#FFFFFF", fg="#7F8C8D")
status_label.pack(pady=(10, 20), anchor="w", padx=20)

root.mainloop()