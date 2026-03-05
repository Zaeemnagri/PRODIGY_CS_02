# PRODIGY_CS_02
A Python-based GUI tool that performs image encryption and decryption using multiple techniques including Pixel Shift, Channel Swap, XOR encryption, and strong encryption using XOR with pixel shuffling.
Here is a **clean and professional `README.md`** you can directly paste into your GitHub repository.

---

# 🔐 Image Encryption Tool

## 📌 Project Overview

The ** Image Encryption Tool** is a Python-based application that allows users to encrypt and decrypt images using different encryption techniques. The application provides a graphical user interface (GUI) that makes it easy for users to select an image, choose an encryption method, and secure the image using a key.

This project demonstrates how image data can be protected by manipulating pixel values and positions using various algorithms.

---

## ✨ Features

* User-friendly graphical interface (GUI)
* Upload and process image files
* Multiple image encryption techniques
* Decryption using the same key
* Strong encryption using XOR and pixel shuffling
* Save encrypted and decrypted images
* Supports common image formats

---

## 🔐 Encryption Methods Implemented

### 1. Pixel Shift Encryption

This method changes the RGB values of each pixel by adding a key value. The original image can be restored by subtracting the same key during decryption.

### 2. Channel Swap

This technique rearranges the RGB color channels of the image to distort its colors.

Example:

```
(R, G, B) → (B, R, G)
```

### 3. Negative Transformation

This method inverts the pixel values using the formula:

```
New Value = 255 - Original Value
```

### 4. XOR Encryption

This method applies a bitwise XOR operation between the pixel values and a secret key.

```
Encrypted Pixel = Pixel XOR Key
```

The same key is required to decrypt the image.

### 5. Strong Encryption (XOR + Pixel Shuffle)

This is the most secure method implemented in the tool.

It combines:

* **Pixel Shuffling:** Randomly rearranges pixel positions using a key.
* **XOR Encryption:** Changes pixel values using the same key.

This removes both the **image structure** and the **original pixel values**, making the encrypted image appear as random noise.

---

## 🛠 Technologies Used

* **Python**
* **Tkinter** – for GUI development
* **Pillow (PIL)** – for image processing
* **NumPy** – for efficient pixel manipulation

---

## 📦 Installation

### 1. Clone the Repository

```
git clone https://github.com/yourusername/image-encryption-tool.git
```

### 2. Navigate to the Project Folder

```
cd image-encryption-tool
```

### 3. Install Required Libraries

```
pip install pillow numpy
```

---

## ▶ Running the Application

Run the Python script using:

```
python image_encryptor_gui.py
```

---

## 🖥 How to Use

1. Launch the application.
2. Click **Upload Image** to select an image file.
3. Choose an encryption method from the dropdown menu.
4. Enter a numeric key if required.
5. Click **Encrypt** to encrypt the image.
6. Save the encrypted image.
7. Use the same key and method to decrypt the image.

---

## 📊 Security Comparison

| Method         | Key Required | Structure Hidden | Security Level |
| -------------- | ------------ | ---------------- | -------------- |
| Negative       | No           | No               | Low            |
| Channel Swap   | No           | No               | Low            |
| Pixel Shift    | Yes          | Partial          | Medium         |
| XOR Encryption | Yes          | Partial          | High           |
| XOR + Shuffle  | Yes          | Yes              | Very High      |

---

## 🎯 Purpose of the Project

This project is designed for **educational purposes** and demonstrates:

* Image data representation
* Pixel-level manipulation
* Basic and advanced encryption concepts
* GUI-based cybersecurity tools

---

## 📷 Supported Image Formats

* PNG
* JPG
* JPEG
* BMP

---

## 👨‍💻 Author

**Zaeem Hussain**
Computer System Engineering Student
Dawood University of Engineering and Technology, Karachi



