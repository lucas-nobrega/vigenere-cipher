def generate_key(msg, key):
    '''
    Generate a key that is as long as the message,
    because the Vigenère cipher requires a key that is repeated to match the length of the message.
    '''
    key = list(key)
    if len(msg) == len(key):
        return key
    else:
        for i in range(len(msg) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


def encrypt(msg, key):
    '''
    Encrypt the message using the Vigenère cipher.
    '''
    encrypted_text = []
    key = generate_key(msg, key)
    for i in range(len(msg)):
        char = msg[i]
        if char.isupper():
            # The formula for encryption is (P + K) mod 26
            # where P is the plaintext letter, K is the key letter
            # and the result is converted back to a letter
            # The ord() function returns the Unicode code point of the character
            # The chr() function converts the Unicode code point back to a character
            # The -2 * ord('A') is used to adjust the range of the result
            # to be within the uppercase letters A-Z
            # The % 26 ensures that the result wraps around if it exceeds 25
            # The + ord('A') converts the result back to the ASCII range for uppercase letters
            # The same logic applies for lowercase letters
            encrypted_char = chr(
                (ord(char) + ord(key[i]) - 2 * ord('A')) % 26 + ord('A'))
            
        elif char.islower():
            encrypted_char = chr(
                (ord(char) + ord(key[i]) - 2 * ord('a')) % 26 + ord('a'))
        else:
            encrypted_char = char
        encrypted_text.append(encrypted_char)
    return "".join(encrypted_text)


def decrypt(msg, key):
    '''
    Decrypt the message using the Vigenère cipher.
    '''
    decrypted_text = []
    key = generate_key(msg, key)
    for i in range(len(msg)):
        char = msg[i]
        if char.isupper():
            # The formula for decryption is (C - K + 26) mod 26
            # where C is the ciphertext letter, K is the key letter
            # and the result is converted back to a letter
            # The + 26 is used to ensure that the result is non-negative
            # The % 26 ensures that the result wraps around if it exceeds 25
            # The - ord('A') is used to adjust the range of the result
            # to be within the uppercase letters A-Z
            # The + ord('A') converts the result back to the ASCII range for uppercase letters
            # The same logic applies for lowercase letters
            # The -2 * ord('A') is used to adjust the range of the result
            # to be within the uppercase letters A-Z
            decrypted_char = chr(
                (ord(char) - ord(key[i]) + 26) % 26 + ord('A'))
        elif char.islower():
            decrypted_char = chr(
                (ord(char) - ord(key[i]) + 26) % 26 + ord('a'))
        else:
            decrypted_char = char
        decrypted_text.append(decrypted_char)
    return "".join(decrypted_text)
