import os

def receber_parametros():

    '''recebe os parâmetros de entrada do usuário
    retorna None, quando dá erro caso os parâmetros
    (origem, chave e destino) não sejam válidos'''

    origem = input("Arquivo de origem: ")
    if not origem.lower().endswith(".txt"):
        origem += ".txt"

    if not os.path.exists(origem):
        print("Arquivo de origem não encontrado.")
        return None, None, None

    destino = input("Arquivo de destino: ")
    if not destino.lower().endswith(".txt"):
        destino += ".txt"

    if os.path.exists(destino):
        print("Arquivo de destino já existe. Operação cancelada.")
        return None, None, None

    chave = input("Palavra-passe: ")
    return origem, chave, destino


def processar_arquivo(origem, chave, destino):

    '''processa o arquivo de origem, aplicando a cifra XOR
    com a chave fornecida e salva o resultado no arquivo de destino'''

    try:
        arquivo_de_origem = open(origem, 'rb')
        dados = arquivo_de_origem.read()
        arquivo_de_origem.close()

    except Exception:
        print("Erro ao ler o arquivo de origem.")
        return

    chave_bytes = chave.encode() # converte a chave para bytes
    if len(chave_bytes) == 0:
        print("A chave não pode ser vazia!")
        return
    resultado = []


    for i in range(len(dados)):
        byte = dados[i]
        indice_chave = i % len(chave_bytes)
        byte_chave = chave_bytes[indice_chave]
        resultado.append(byte ^ byte_chave)

    resultado_bytes = bytes(resultado) # converte a lista de bytes para bytes

    try:
        arquivo_de_destino = open(destino, 'wb')
        arquivo_de_destino.write(resultado_bytes)
        arquivo_de_destino.close()
        print("Arquivo salvo com sucesso.")

    except Exception:
        print("Erro ao salvar o arquivo de destino.")
        return
    
origem, chave, destino = receber_parametros()
if origem and chave and destino:
    processar_arquivo(origem, chave, destino)