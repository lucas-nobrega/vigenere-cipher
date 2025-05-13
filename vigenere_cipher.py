def encrypt(text, key):
    """
    Encrypts the given text using the Vigenère cipher with the provided key.
    
    :param text: The text to encrypt.
    :param key: The key to use for encryption.
    :return: The encrypted text.
    """
    encrypted_text = []
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    text_as_int = [ord(i) for i in text]
    
    for i in range(len(text_as_int)):
        value = (text_as_int[i] + key_as_int[i % key_length]) % 256
        encrypted_text.append(chr(value))
    
    return ''.join(encrypted_text)


def decrypt(ciphertext, key):
    """
    Decrypts a Vigenère cipher using the provided key.

    :param ciphertext: The encrypted text to decrypt.
    :param key: The key used for decryption.
    :return: The decrypted plaintext.
    """
    decrypted_text = []
    key_length = len(key)
    key_as_int = [ord(i) - ord('A') for i in key.upper()]
    ciphertext_int = [ord(i) - ord('A') for i in ciphertext.upper()]

    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
        decrypted_text.append(chr(value + ord('A')))

    return ''.join(decrypted_text)