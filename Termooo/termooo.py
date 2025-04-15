import random

def ler_arquivo(path):

    '''lê o arquivo de palavras e retorna
    uma lista de palavras válidas'''

    try:
        arquivo = open(path, "r", encoding="utf-8")
        palavras = []
        for linha in arquivo:
            palavra = linha.strip().upper()
            if 5 <= len(palavra) <= 8:
                palavras.append(palavra)
        arquivo.close()
        return palavras
    
    except FileNotFoundError:
        print("Erro: arquivo não encontrado.")
        return

def sortear_palavra(palavras):
    return random.choice(palavras)

def boas_vindas():
    print("=" * 100)
    print("BEM VINDO AO TERMO!")
    print("\nVocê deve descobrir as palavras corretas. A cada tentativa, você verá o quão perto estará da solução.")
    print('A\033[1;32mD\033[0mAGA -> a letra  "A" faz parte da palavra e está na posição correta')
    print('VE\033[1;33mN\033[0mTO -> a letra  "N" faz parte da palavra, mas em outra posição')
    print('PUL\033[1;30mG\033[0mA -> a letra  "G" não faz parte da palavra')
    print("\nAs palavras podem possuir letras repetidas!")
    print("=" * 100)
    print()

def feedback(palpite, palavra_sorteada):

    '''dá o feedback sobre o palpite do jogador e
    marca as letras corretas, existentes ou erradas
    onde:

    - existente, mas fora do lugar: amarelo
    - existente e na posição correta: verde
    - não existente: cinza'''

    resultado = ""
    letras_usadas = list(palavra_sorteada)

    # corretas
    for i in range(len(palpite)):
        if palpite[i] == palavra_sorteada[i]:
            resultado += f"\033[1;32m{palpite[i]}\033[0m" # verde
            letras_usadas[i] = None  # marca como já usada
        else:
            resultado += "_"
    
    # existentes, mas fora do lugar e não existentes
    feedback_final = ""
    for i in range(len(palpite)):
        if resultado[i] != "_":
            feedback_final += resultado[i]
        elif palpite[i] in letras_usadas:
            feedback_final += f"\033[1;33m{palpite[i]}\033[0m"  # amarelo
            letras_usadas[letras_usadas.index(palpite[i])] = None
        else:
            feedback_final += f"\033[1;30m{palpite[i]}\033[0m"  # cinza
    print(feedback_final)


def jogar(palavra_sorteada):

    '''função principal do jogo, onde o jogador
    tenta adivinhar a palavra sorteada em até
    6 tentativas. A cada tentativa, o jogador recebe
    feedback sobre o palpite.'''

    print(f"A palavra sorteada tem {len(palavra_sorteada)} letras. Você tem 6 tentativas.\n")

    for tentativa in range(1, 7):
        while True:
            palpite = input(f"Tentativa {tentativa}/6 - Digite uma palavra: ").strip().upper()
            if len(palpite) != len(palavra_sorteada):
                print(f"Erro: a palavra deve ter exatamente {len(palavra_sorteada)} letras.\n")
            else:
                break

        if palpite == palavra_sorteada:
            print(f"\n\033[1;32mParabéns! Você acertou a palavra '{palavra_sorteada}' em {tentativa} tentativa(s)!\033[0m")
            return
        else:
            feedback(palpite, palavra_sorteada)
            print()

    print(f"\n\033[1;31mFim de jogo! A palavra era: {palavra_sorteada}\033[0m")

def main():
    
    '''inicializa o jogo, lê o arquivo de palavras,
    sorteia uma palavra e inicia a contagem de tentativas'''

    caminho = "palavras.txt"
    lista = ler_arquivo(caminho)

    if not lista:
        print("Nenhuma palavra válida para jogar.")
        return

    palavra = sortear_palavra(lista)
    boas_vindas()
    jogar(palavra)

main()
