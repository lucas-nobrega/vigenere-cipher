import collections
import re

FREQ_INGLES = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}
ALFABETO = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
IC_INGLES = 0.067


def limpar_texto(texto):
    return re.sub(r'[^A-Z]', '', texto.upper())


def calcular_ic(texto):
    n = len(texto)
    if n < 2:
        return 0.0

    contagens_freq = collections.Counter(texto)
    soma_ic = sum(contagem * (contagem - 1)
                  for contagem in contagens_freq.values())
    ic = soma_ic / (n * (n - 1))
    return ic


def encontrar_tamanho_chave(texto_cifrado, max_tam_chave=20):
    melhor_tam_chave = 1
    min_diferenca = float('inf')

    for tam_chave in range(1, max_tam_chave + 1):
        ic_medio_para_tam_chave = 0.0
        num_colunas_validas = 0
        for i in range(tam_chave):
            coluna = texto_cifrado[i::tam_chave]
            if len(coluna) > 1:
                ic_medio_para_tam_chave += calcular_ic(coluna)
                num_colunas_validas += 1

        if num_colunas_validas > 0:
            ic_medio_para_tam_chave /= num_colunas_validas
            diferenca = abs(ic_medio_para_tam_chave - IC_INGLES)
            if diferenca < min_diferenca:
                min_diferenca = diferenca
                melhor_tam_chave = tam_chave

    return melhor_tam_chave


def obter_colunas(texto_cifrado, tamanho_chave):
    colunas = [''] * tamanho_chave
    for i, caractere in enumerate(texto_cifrado):
        colunas[i % tamanho_chave] += caractere
    return colunas


def calcular_qui_quadrado(texto):
    n = len(texto)
    if n == 0:
        return float('inf')

    contagens_observadas = collections.Counter(texto)
    valor_qui_quadrado = 0.0

    for i, letra in enumerate(ALFABETO):
        observado = contagens_observadas.get(letra, 0)
        esperado = FREQ_INGLES[letra] * n

        if esperado == 0:
            if observado > 0:
                valor_qui_quadrado += float('inf')
        else:
            valor_qui_quadrado += ((observado - esperado)**2) / esperado

    return valor_qui_quadrado


def encontrar_letra_chave_coluna(texto_coluna):
    melhor_qui_quadrado = float('inf')
    melhor_deslocamento = 0

    for deslocamento in range(26):
        coluna_deslocada = ""
        for codigo_char in [ord(c) for c in texto_coluna]:
            codigo_char_dec = (codigo_char - ord('A') -
                               deslocamento + 26) % 26 + ord('A')
            coluna_deslocada += chr(codigo_char_dec)

        qui_quadrado_atual = calcular_qui_quadrado(coluna_deslocada)

        if qui_quadrado_atual < melhor_qui_quadrado:
            melhor_qui_quadrado = qui_quadrado_atual
            melhor_deslocamento = deslocamento

    return ALFABETO[melhor_deslocamento]


def decifrar_vigenere(texto_cifrado, chave):
    chave = chave.upper()
    tam_chave = len(chave)
    texto_plano = []

    for i, codigo_char in enumerate([ord(c) for c in texto_cifrado]):
        codigo_char_chave = ord(chave[i % tam_chave])
        deslocamento_chave = codigo_char_chave - ord('A')

        codigo_char_dec = (codigo_char - ord('A') -
                           deslocamento_chave + 26) % 26 + ord('A')
        texto_plano.append(chr(codigo_char_dec))

    return "".join(texto_plano)


def ataque_frequencia_vigenere(texto_cifrado, max_tam_chave=20):
    print("Iniciando Ataque de Análise de Frequência Vigenère...")

    texto_cifrado_limpo = limpar_texto(texto_cifrado)
    if not texto_cifrado_limpo:
        print("O texto cifrado está vazio após a limpeza.")
        return "", ""
    print(
        f"Texto Cifrado Limpo (primeiros 100 caracteres): {texto_cifrado_limpo[:100]}...")

    tam_chave_estimado = encontrar_tamanho_chave(
        texto_cifrado_limpo, max_tam_chave)
    print(f"\n[Passo 1] Tamanho da Chave Estimado: {tam_chave_estimado}")
    if tam_chave_estimado == 0:
        print("Não foi possível determinar um tamanho de chave válido.")
        return "", ""

    colunas = obter_colunas(texto_cifrado_limpo, tam_chave_estimado)
    print(f"[Passo 2] Texto cifrado dividido em {len(colunas)} colunas.")

    chave_estimada = ""
    print("\n[Passo 3] Encontrando letras da chave para cada coluna:")
    for i, texto_coluna in enumerate(colunas):
        if not texto_coluna:
            print(
                f"   Coluna {i+1} está vazia. Não é possível determinar a letra da chave.")
            continue
        letra_chave = encontrar_letra_chave_coluna(texto_coluna)
        chave_estimada += letra_chave
        print(f"   Coluna {i+1}: Letra da chave mais provável = {letra_chave}")

    if not chave_estimada:
        print("Não foi possível determinar nenhuma letra da chave.")
        return "", ""
    print(f"Chave Estimada Completa: {chave_estimada}")

    texto_plano_decifrado = decifrar_vigenere(
        texto_cifrado_limpo, chave_estimada)
    print("\n[Passo 4] Decifrando com a chave estimada...")
    print(
        f"Texto Plano Decifrado (primeiros 200 caracteres): {texto_plano_decifrado[:200]}...")

    return chave_estimada, texto_plano_decifrado


if __name__ == "__main__":
    texto_cifrado1 = """
    LPEOV YMSRX FTBTX IMZPE UTLVI WMXEK VVXMS RYXIF TBTXI XNSRT
    IPEWM XEKVL PIWMX JVSXF IPXZX IWMXT BTXIM XUIAX XFXFT BTXIW
    MXMXS RXIZP ELXFI PTBTX IWMXY MXXZX IXSRX IMXTBTX IMXEK VVXMS
    RYXZX IWMXX ZXJVS XFIPX ZXIWM XXFTB TXIMX LPEOV YMSRX FEKVV
    XMSRY XFTBT XIXNS RXFTB TXIWM SRXIX FTBTX IMX
    """

    texto_cifrado2 = """
    VPVLZ RSEZR ZWMXA XAAXY VVZWW NZXMA XAWVT VHZXM WAVXC XWVZL XQYEB XQZXM
    WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM
    WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM
    WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM
    WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM
    WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM
    WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM
    WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM
    WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM
    WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM
    WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM WAVXC XWVZL XQYEB XQZXM
    """

    print("--- Atacando Texto Cifrado 1 ---")
    chave1, plano1 = ataque_frequencia_vigenere(
        texto_cifrado1, max_tam_chave=10)
    print(f"Chave Estimada Final para o Texto Cifrado 1: {chave1}")

    print("\n\n--- Atacando Texto Cifrado 2 ---")
    chave2, plano2 = ataque_frequencia_vigenere(
        texto_cifrado2, max_tam_chave=15)
    print(f"Chave Estimada Final para o Texto Cifrado 2: {chave2}")

    texto_plano_longo = """
    Call me Ishmael. Some years ago—never mind how long precisely—having
    little or no money in my purse, and nothing particular to interest me
    on shore, I thought I would sail about a little and see the watery part
    of the world. It is a way I have of driving off the spleen and
    regulating the circulation. Whenever I find myself growing grim about
    the mouth; whenever it is a damp, drizzly November in my soul;
    whenever I find myself involuntarily pausing before coffin warehouses,
    and bringing up the rear of every funeral I meet; and especially
    whenever my hypos get such an upper hand of me, that it requires a
    strong moral principle to prevent me from deliberately stepping into
    the street, and methodically knocking people’s hats off—then, I
    account it high time to get to sea as soon as I can. This is my
    substitute for pistol and ball. With a philosophical flourish Cato
    throws himself upon his sword; I quietly take to the ship. There is
    nothing surprising in this. If they but knew it, almost all men in
    their degree, some time or other, cherish very nearly the same
    feelings towards the ocean with me.
    """

    def cifrar_vigenere(texto_plano, chave):
        texto_plano = limpar_texto(texto_plano)
        chave = chave.upper()
        tam_chave = len(chave)
        texto_cifrado = []
        for i, codigo_char in enumerate([ord(c) for c in texto_plano]):
            codigo_char_chave = ord(chave[i % tam_chave])
            deslocamento_chave = codigo_char_chave - ord('A')
            codigo_char_enc = (codigo_char - ord('A') +
                               deslocamento_chave) % 26 + ord('A')
            texto_cifrado.append(chr(codigo_char_enc))
        return "".join(texto_cifrado)

    chave_verdadeira_longa = "SECRETKEY"
    texto_cifrado_longo_exemplo = cifrar_vigenere(
        texto_plano_longo, chave_verdadeira_longa)

    print("\n\n--- Atacando Texto Cifrado Longo (excerto Moby Dick, Chave: SECRETKEY) ---")
    chave_longa, plano_longo = ataque_frequencia_vigenere(
        texto_cifrado_longo_exemplo, max_tam_chave=15)
    print(f"Chave Estimada Final para o Texto Cifrado Longo: {chave_longa}")
