import socket
import ssl

def extrair_info_url(url):

    '''Extrai informações de uma URL'''

    if not url.startswith(("http://", "https://")):
        raise ValueError("Apenas URLs com protocolo HTTP ou HTTPS são aceitas.") # check para URLs inválidas

    protocolo = "http"
    if url.startswith("https://"):
        protocolo = "https"
        url = url[8:]
    elif url.startswith("http://"):
        url = url[7:]

    partes = url.split("/", 1)
    hostname = partes[0]
    caminho = "/" + partes[1] if len(partes) > 1 else "/" # caminho padrão
    nome_arquivo = caminho.split("/")[-1] or "index.html"

    return protocolo, hostname, caminho, nome_arquivo

def criar_socket(protocolo, hostname):

    '''Cria um socket para conexão com o servidor'''

    porta = 443 if protocolo == "https" else 80
    sock = socket.create_connection((hostname, porta))

    '''Se o protocolo for HTTPS, envolve o socket em um contexto SSL'''

    if protocolo == "https":
        contexto_ssl = ssl.create_default_context()
        sock = contexto_ssl.wrap_socket(sock, server_hostname=hostname)
    return sock

def enviar_requisicao(sock, hostname, caminho):

    '''Envia uma requisição HTTP para o servidor'''

    requisicao = f"GET {caminho} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n" # requisicao HTTP padrão com os headers necessários
    sock.sendall(requisicao.encode())

def receber_resposta(sock):

    '''Recebe a resposta do servidor e retorna o corpo da resposta'''

    resposta = b""
    while True:
        dados = sock.recv(4096) # lê os dados do socket em blocos de 4096 bytes
        if not dados:
            break
        resposta += dados
    return resposta

def tratar_chunked(corpo):

    '''Trata o corpo da resposta se estiver usando codificação chunked'''

    resultado = b""
    while True:
        pos = corpo.find(b"\r\n")
        if pos == -1:
            break
        tamanho_str = corpo[:pos].decode().strip() # obtém o tamanho do chunk
        try:
            tamanho = int(tamanho_str, 16)

        except ValueError:
            break
        if tamanho == 0:
            break
        corpo = corpo[pos+2:]
        resultado += corpo[:tamanho]
        corpo = corpo[tamanho+2:]
    return resultado

def baixar_url(url, redirecionamentos=3):

    '''Baixa o conteúdo de uma URL, seguindo redirecionamentos, se necessário'''

    if redirecionamentos == 0:
        raise Exception("Número máximo de redirecionamentos atingido.")
    
    '''Tratamento contra erros'''
    try:
        protocolo, hostname, caminho, nome_arquivo = extrair_info_url(url)
    except ValueError as ve:
        print("Erro:", ve)
        return

    print("HOST:", hostname)
    print("Caminho:", caminho)
    print("Nome do Arquivo:", nome_arquivo)

    try:
        sock = criar_socket(protocolo, hostname)
        enviar_requisicao(sock, hostname, caminho)
        resposta = receber_resposta(sock)
        sock.close()

    except Exception as e:
        print("Erro ao conectar ou enviar requisição:", e)
        return

    try:
        header_raw, corpo = resposta.split(b"\r\n\r\n", 1)
    except ValueError:
        print("Erro: resposta sem cabeçalho.")
        return

    header = header_raw.decode(errors="replace")

    '''Salva o cabeçalho da resposta em um arquivo de texto'''

    with open("header_resposta.txt", "w", encoding="utf-8") as f:
        f.write(header)

    status_line = header.splitlines()[0]
    status_code = status_line.split()[1] if len(status_line.split()) > 1 else "" # obtém o status code da resposta

    '''Exibe o status code e a primeira linha do cabeçalho'''

    if status_code in ["301", "302", "303", "307"]:
        for linha in header.splitlines():
            if linha.lower().startswith("location:"):
                destino = linha.split(":", 1)[1].strip()
                if destino.startswith("/"):
                    nova_url = f"{protocolo}://{hostname}{destino}"
                elif destino.startswith("http://") or destino.startswith("https://"):
                    nova_url = destino
                else:
                    nova_url = f"{protocolo}://{hostname}/{destino}"

                print("Redirecionando para:", nova_url)
                return baixar_url(nova_url, redirecionamentos - 1)

    if "transfer-encoding: chunked" in header.lower():
        corpo = tratar_chunked(corpo)

    tipo_texto = "content-type: text/html" in header.lower() # verifica se o conteúdo é do tipo texto/html
    modo = "w" if tipo_texto else "wb"

    try:
        with open(nome_arquivo, modo, encoding="utf-8", errors="replace" if tipo_texto else None) as f:
            f.write(corpo.decode("utf-8", errors="replace") if tipo_texto else corpo)
    except Exception as e:
        print("Erro ao salvar o conteúdo:", e)
        return

    print("Download concluído.")

# ===== Execução com repetição =====
while True:
    url = input("\nDigite a URL (ou 'sair' para encerrar): ").strip()
    if url.lower() == "sair":
        break
    try:
        baixar_url(url)
    except Exception as e:
        print("Erro inesperado:", e)