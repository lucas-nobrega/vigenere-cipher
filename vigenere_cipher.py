def gerar_chave(mensagem, chave):
    chave = list(chave)
    if len(mensagem) == len(chave):
        return chave
    else:
        for i in range(len(mensagem) - len(chave)):
            chave.append(chave[i % len(chave)])
    return "".join(chave)


def criptografar(mensagem, chave):
    texto_criptografado = []
    chave = gerar_chave(mensagem, chave)
    for i in range(len(mensagem)):
        caractere = mensagem[i]
        if caractere.isupper():
            caractere_criptografado = chr(
                (ord(caractere) + ord(chave[i]) - 2 * ord('A')) % 26 + ord('A'))
        elif caractere.islower():
            caractere_criptografado = chr(
                (ord(caractere) + ord(chave[i]) - 2 * ord('a')) % 26 + ord('a'))
        else:
            caractere_criptografado = caractere
        texto_criptografado.append(caractere_criptografado)
    return "".join(texto_criptografado)


def descriptografar(mensagem, chave):
    texto_descriptografado = []
    chave = gerar_chave(mensagem, chave)
    for i in range(len(mensagem)):
        caractere = mensagem[i]
        if caractere.isupper():
            caractere_descriptografado = chr(
                (ord(caractere) - ord(chave[i]) + 26) % 26 + ord('A'))
        elif caractere.islower():
            caractere_descriptografado = chr(
                (ord(caractere) - ord(chave[i]) + 26) % 26 + ord('a'))
        else:
            caractere_descriptografado = caractere
        texto_descriptografado.append(caractere_descriptografado)
    return "".join(texto_descriptografado)


def main():
    while True:
        print("\n--- Cifra de Vigenère ---")
        mensagem_original = input(
            "Digite a mensagem que deseja criptografar (ou 'sair' para terminar): ")

        if mensagem_original.lower() == 'sair':
            break

        chave = input("Digite a chave: ")

        if not chave or not chave.isalpha():
            print("Erro: A chave não pode ser vazia e deve conter apenas letras.")
            continue

        # Criptografar
        mensagem_criptografada = criptografar(mensagem_original, chave)
        print(f"Mensagem Criptografada: {mensagem_criptografada}")

        # Descriptografar
        mensagem_descriptografada = descriptografar(
            mensagem_criptografada, chave)
        print(f"Mensagem Descriptografada: {mensagem_descriptografada}")

    print("Programa encerrado.")

if __name__ == "__main__":
    main()
