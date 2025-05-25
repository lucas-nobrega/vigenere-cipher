import collections
import re

PORTUGUESE_FREQ = {
    'A': 0.1463, 'B': 0.0104, 'C': 0.0388, 'D': 0.0499, 'E': 0.1257,
    'F': 0.0102, 'G': 0.0130, 'H': 0.0128, 'I': 0.0618, 'J': 0.0040,
    'K': 0.0002, 'L': 0.0278, 'M': 0.0474, 'N': 0.0505, 'O': 0.1073,
    'P': 0.0252, 'Q': 0.0120, 'R': 0.0653, 'S': 0.0781, 'T': 0.0434,
    'U': 0.0463, 'V': 0.0167, 'W': 0.0001, 'X': 0.0021, 'Y': 0.0001,
    'Z': 0.0047
}
ALFABETO = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
PORTUGUESE_IC = 0.07813849


def limpar_texto(texto):
    # Normalização para remover acentos
    substituicoes = {
        'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A',
        'É': 'E', 'Ê': 'E',
        'Í': 'I', 'Î': 'I',
        'Ó': 'O', 'Õ': 'O', 'Ô': 'O',
        'Ú': 'U', 'Û': 'U',
        'Ç': 'C',
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e',
        'í': 'i', 'î': 'i',
        'ó': 'o', 'õ': 'o', 'ô': 'o',
        'ú': 'u', 'û': 'u',
        'ç': 'c'
    }
    texto_sem_acentos = texto
    for acentuado, sem_acento in substituicoes.items():
        texto_sem_acentos = texto_sem_acentos.replace(acentuado, sem_acento)

    return re.sub(r'[^A-Z]', '', texto_sem_acentos.upper())


def calcular_ic(texto):
    n = len(texto)
    if n < 2:
        return 0.0  # IC não é significativo para textos muito curtos

    contagem_freq = collections.Counter(texto)
    # Fórmula do IC: sum(fi * (fi - 1)) / (N * (N - 1))
    # onde fi é a frequência da i-ésima letra, N é o número total de letras.
    soma_ic = sum(contador * (contador - 1)
                  for contador in contagem_freq.values())
    ic = soma_ic / (n * (n - 1))
    return ic


def encontrar_tamanho_chave(texto_cifrado, max_tam_chave=20):
    melhor_tam_chave = 1
    min_diff = float('inf')

    for tam_chave in range(1, max_tam_chave + 1):
        ic_medio_para_tam_chave = 0.0
        num_colunas_validas = 0
        for i in range(tam_chave):
            # Fatiamento para obter cada k-ésimo caractere
            coluna = texto_cifrado[i::tam_chave]
            if len(coluna) > 1:  # Precisa de pelo menos 2 caracteres para calcular o IC
                ic_medio_para_tam_chave += calcular_ic(coluna)
                num_colunas_validas += 1

        if num_colunas_validas > 0:
            ic_medio_para_tam_chave /= num_colunas_validas
            diff = abs(ic_medio_para_tam_chave - PORTUGUESE_IC)
            if diff < min_diff:
                min_diff = diff
                melhor_tam_chave = tam_chave

    return melhor_tam_chave


def obter_colunas(texto_cifrado, tamanho_chave):
    colunas = [''] * tamanho_chave
    for i, char in enumerate(texto_cifrado):
        colunas[i % tamanho_chave] += char
    return colunas


def calcular_qui_quadrado(texto):
    n = len(texto)
    if n == 0:
        # Evitar divisão por zero
        return float('inf')

    contagens_observadas = collections.Counter(texto)
    valor_qui_quadrado = 0.0

    for i, letra in enumerate(ALFABETO):
        # Frequência observada da letra atual no texto
        observado = contagens_observadas.get(letra, 0)
        # Frequência esperada da letra atual em texto em português de tamanho N
        esperado = PORTUGUESE_FREQ[letra] * n
        
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
        for char_code in [ord(c) for c in texto_coluna]:
            dec_char_code = (char_code - ord('A') -
                             deslocamento + 26) % 26 + ord('A')
            coluna_deslocada += chr(dec_char_code)

        qui_quadrado_atual = calcular_qui_quadrado(coluna_deslocada)

        if qui_quadrado_atual < melhor_qui_quadrado:
            melhor_qui_quadrado = qui_quadrado_atual
            melhor_deslocamento = deslocamento

    return ALFABETO[melhor_deslocamento]


def vigenere_descriptografar(texto_cifrado, chave):
    chave = chave.upper()
    tam_chave = len(chave)
    texto_plano = []

    for i, char_code in enumerate([ord(c) for c in texto_cifrado]):
        key_char_code = ord(chave[i % tam_chave])
        deslocamento_chave = key_char_code - ord('A')

        dec_char_code = (char_code - ord('A') -
                         deslocamento_chave + 26) % 26 + ord('A')
        texto_plano.append(chr(dec_char_code))

    return "".join(texto_plano)


def ataque_frequencia_vigenere(texto_cifrado, max_tam_chave=20):
    print("Iniciando Ataque de Análise de Frequência à Cifra de Vigenère...")

    texto_cifrado_limpo = limpar_texto(texto_cifrado)
    if not texto_cifrado_limpo:
        print("O texto cifrado está vazio após a limpeza.")
        return "", ""
    print(
        f"Texto Cifrado Limpo (primeiros 100 caracteres): {texto_cifrado_limpo[:100]}...")

    # 1. Estimar Tamanho da Chave
    tam_chave_estimado = encontrar_tamanho_chave(
        texto_cifrado_limpo, max_tam_chave)
    print(f"\n[Passo 1] Tamanho Estimado da Chave: {tam_chave_estimado}")
    if tam_chave_estimado == 0:
        print("Não foi possível determinar um tamanho de chave válido.")
        return "", ""

    # 2. Obter Colunas
    colunas = obter_colunas(texto_cifrado_limpo, tam_chave_estimado)
    print(f"[Passo 2] Texto cifrado dividido em {len(colunas)} colunas.")

    # 3. Encontrar Letras da Chave para cada Coluna
    chave_estimada = ""
    print("\n[Passo 3] Encontrando letras da chave para cada coluna:")
    for i, texto_coluna in enumerate(colunas):
        if not texto_coluna:
            print(
                f"  Coluna {i+1} está vazia. Não é possível determinar a letra da chave.")
            continue
        letra_chave = encontrar_letra_chave_coluna(texto_coluna)
        chave_estimada += letra_chave
        print(f"  Coluna {i+1}: Letra da chave mais provável = {letra_chave}")

    if not chave_estimada:
        print("Não foi possível determinar nenhuma letra da chave.")
        return "", ""
    print(f"Chave Estimada Completa: {chave_estimada}")

    # 4. Descriptografar com a Chave Estimada
    texto_plano_descriptografado = vigenere_descriptografar(
        texto_cifrado_limpo, chave_estimada)
    print("\n[Passo 4] Descriptografando com a chave estimada...")
    print(
        f"Texto Plano Descriptografado (primeiros 200 caracteres): {texto_plano_descriptografado[:200]}...")

    return chave_estimada, texto_plano_descriptografado

if __name__ == "__main__":
    def vigenere_criptografar(texto_plano, chave):
        texto_plano = limpar_texto(texto_plano)
        chave = chave.upper()
        tam_chave = len(chave)
        texto_cifrado = []
        for i, char_code in enumerate([ord(c) for c in texto_plano]):
            key_char_code = ord(chave[i % tam_chave])
            deslocamento_chave = key_char_code - ord('A')
            enc_char_code = (char_code - ord('A') +
                             deslocamento_chave) % 26 + ord('A')
            texto_cifrado.append(chr(enc_char_code))
        return "".join(texto_cifrado)

    texto_original_pt = "Ola mundo esta e uma mensagem de teste para a cifra de Vigenere em portugues vamos ver se o ataque de frequencia consegue descobrir a chave secreta espero que sim pois deu um certo trabalho adaptar tudo para o nosso idioma com suas particularidades de frequencia de letras e acentos que precisam ser tratados antes da analise estatistica para que os resultados sejam os mais precisos possiveis e a quebra da criptografia seja bem sucedida"
    chave_real_pt = "LINGUAGEM"

    texto_cifrado_pt_real = vigenere_criptografar(
        texto_original_pt, chave_real_pt)

    print("--- Atacando Texto Cifrado em Português (Chave Real: LINGUAGEM) ---")
    # print(f"Texto Cifrado para análise: {texto_cifrado_pt_real[:200]}...") # Descomente para ver o texto cifrado
    chave_estimada, texto_plano = ataque_frequencia_vigenere(
        texto_cifrado_pt_real, max_tam_chave=15)
    print(f"\nChave Estimada Final para Texto em Português: {chave_estimada}")
    # print(f"Texto Plano Descriptografado Final: {texto_plano}") # Descomente para ver o texto plano completo

    if chave_estimada.upper() == chave_real_pt.upper():
        print("\nSUCESSO! A chave estimada corresponde à chave real.")
    else:
        print(
            f"\ERRO! A chave estimada ({chave_estimada}) não corresponde à chave real ({chave_real_pt}).")
        print("Isso pode ocorrer se o texto for muito curto, a chave muito longa, ou as estatísticas não forem suficientes.")
