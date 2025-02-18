import cv2
import os
import numpy as np

def create_mappings():
    return {chr(i): i for i in range(256)}

def xor_encrypt(char, key):
    return ord(char) ^ ord(key)

def encrypt_message(img, msg, password):
    d = create_mappings()
    rows, cols, _ = img.shape
    total_pixels = rows * cols * 3
    
    if len(msg) > total_pixels:
        raise ValueError("Message too long to encode in this image.")
    
    key_length = len(password)
    if key_length == 0:
        raise ValueError("Password cannot be empty.")
    
    n, m, z = 0, 0, 0
    for i, char in enumerate(msg):
        encrypted_value = xor_encrypt(char, password[i % key_length])
        img[n, m, z] = encrypted_value
        z = (z + 1) % 3
        if z == 0:
            m += 1
            if m == cols:
                m = 0
                n += 1
    
    return img

def main():
    image_path = "spiderman.png"
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found!")
        return
    
    msg = input("Enter secret message: ")
    password = input("Enter a passcode: ")
    
    encrypted_img = encrypt_message(img, msg, password)
    output_path = "encryptedImage.png"
    cv2.imwrite(output_path, encrypted_img)
    
    with open("key.txt", "w") as f:
        f.write(password + "\n" + str(len(msg)))
    
    print("Encryption complete! Image saved as", output_path)
    if os.name == "nt":
        os.system("start " + output_path)  # Windows
    else:
        os.system("xdg-open " + output_path)  # Linux/macOS

if __name__ == "__main__":
    main()
