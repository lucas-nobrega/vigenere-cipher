from vigenere_cipher import encrypt, decrypt

def main():
    # Example usage
    plaintext = "HELLO WORLD"
    key = "KEY"

    # Encrypt the plaintext
    encrypted_text = encrypt(plaintext, key)
    print(f"Encrypted: {encrypted_text}")

    # Decrypt the ciphertext
    decrypted_text = decrypt(encrypted_text, key)
    print(f"Decrypted: {decrypted_text}")
if __name__ == "__main__":
    main()
# This code is a simple implementation of the Vigenère cipher, which is a method of encrypting alphabetic text by using a simple form of polyalphabetic substitution.