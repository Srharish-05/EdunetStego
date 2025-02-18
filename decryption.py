import cv2
import os

def create_mappings():
    return {i: chr(i) for i in range(256)}

def xor_decrypt(value, key):
    return chr(value ^ ord(key))

def decrypt_message(img, length, password):
    c = create_mappings()
    rows, cols, _ = img.shape
    message = ""
    n, m, z = 0, 0, 0
    key_length = len(password)

    if key_length == 0:
        raise ValueError("Password cannot be empty.")

    for i in range(length):
        decrypted_char = xor_decrypt(img[n, m, z], password[i % key_length])
        message += decrypted_char
        z = (z + 1) % 3
        if z == 0:
            m += 1
            if m == cols:
                m = 0
                n += 1

    return message

def main():
    image_path = "encryptedImage.png"
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Encrypted image not found!")
        return
    
    try:
        with open("key.txt", "r") as f:
            saved_password, length = f.read().split("\n")
            length = int(length)
    except:
        print("Error: Key file missing or corrupted!")
        return
    
    pas = input("Enter passcode for decryption: ")
    if pas == saved_password:
        decrypted_msg = decrypt_message(img, length, pas)
        print("\nDecrypted message:", decrypted_msg)
    else:
        print("\nYOU ARE NOT AUTHORIZED!")

if __name__ == "__main__":
    main()

