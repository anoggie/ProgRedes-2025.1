from function import findNonce

textos = [
    "Esse é fácil",
    "Esse é fácil",
    "Esse é fácil",
    "Texto maior muda o tempo?",
    "Texto maior muda o tempo?",
    "Texto maior muda o tempo?",
    "É possív el calcular esse?",
    "É possível calcular esse?",
    "É possível calcular esse?"
]

bits = [8, 10, 15, 8, 10, 15, 18, 19, 20]

resultados = []

# para cada texto e quantidade de bits desejados, calcula o nonce e o tempo gasto.

for texto, bits_zero in zip(textos, bits):
    print(f"Processando: \"{texto}\" com {bits_zero} bits zerados...")
    nonce, tempo = findNonce(texto.encode(), bits_zero)
    resultados.append((texto, bits_zero, nonce, round(tempo, 3)))

# salva os resultados formatados em um arquivo de txt.
try:
    arquivo = open("tabela_resultado.txt", "w", encoding="utf-8")
    arquivo.write(f"{'Texto':<30} | {'Bits em zero':<12} | {'Nonce':<10} | {'Tempo (s)':<10}\n")
    arquivo.write("-" * 70 + "\n")

    for linha in resultados:
        arquivo.write(f"{linha[0]:<30} | {linha[1]:<12} | {linha[2]:<10} | {linha[3]:<10}\n")
    arquivo.close()
    
    print("Tabela salva em tabela_resultado.txt.")

except Exception:
    print(f"Erro ao escrever no arquivo")
