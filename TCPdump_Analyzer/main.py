import tkinter as tk
from tkinter import filedialog
from tabulate import tabulate
import csv
from datetime import datetime

# Mapeamento de protocolos
PROTOCOLOS = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
    2: "IGMP",
    58: "IPv6-ICMP"
}

def selecionar_arquivo():

    """Abre janela para seleção do arquivo PCAP"""

    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Selecione um arquivo PCAP",
        filetypes=[("Arquivos PCAP", "*.cap *.dump *.pcap *pcapng")]
    )

def ler_uint32(bytes_data, little_endian=True):

    """Lê um inteiro de 32 bits a partir de bytes"""

    return int.from_bytes(bytes_data, byteorder='little' if little_endian else 'big')

def exportar_csv(nome_arquivo, dados, cabecalhos=None):
    """Exporta dados para um arquivo CSV"""
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if cabecalhos:
            writer.writerow(cabecalhos)
        writer.writerows(dados)
    print(f"[EXPORTADO] {nome_arquivo}")

def analisar_pcap(caminho):

    """Lê o arquivo PCAP e extrai os pacotes"""

    pacotes = []
    with open(caminho, 'rb') as f:
        # Lê cabeçalho global
        global_header = f.read(24)
        magic = ler_uint32(global_header[0:4])
        version_major = ler_uint32(global_header[4:6], False)
        version_minor = ler_uint32(global_header[6:8], False)
        snaplen = ler_uint32(global_header[16:20])
        linktype = ler_uint32(global_header[20:24])

        # Exibe o cabeçalho global
        print("\n[INFO] Cabeçalho Global:")
        print(tabulate([
            ["Magic Number", hex(magic)],
            ["Versão", f"{version_major}.{version_minor}"],
            ["SnapLen", snaplen],
            ["LinkType", linktype]
        ], headers=["Campo", "Valor"], tablefmt="grid"))

        # Processa pacotes
        while True:
            header = f.read(16)
            if len(header) < 16:
                break

            # Ler o cabeçalho de cada pacote
            ts_sec = ler_uint32(header[0:4])
            ts_usec = ler_uint32(header[4:8])
            incl_len = ler_uint32(header[8:12])
            orig_len = ler_uint32(header[12:16])
            dados = f.read(incl_len)

            pacotes.append({
                'timestamp': ts_sec + ts_usec / 1_000_000,
                'caplen': incl_len,
                'origlen': orig_len,
                'dados': dados,
                'truncado': incl_len < orig_len
            })

    return pacotes

def processar_pacotes(pacotes):

    """Analisa os pacotes e gera relatórios"""

    # Estrutura para estatísticas
    stats = {
        'inicio': min(p['timestamp'] for p in pacotes),
        'fim': max(p['timestamp'] for p in pacotes),
        'total': len(pacotes),
        'tcp': {'count': 0, 'maior': 0, 'origem': '', 'destino': ''},
        'udp': {'count': 0, 'sum': 0, 'maior': 0},
        'trafego': {},
        'ips': set(),
        'contagem_ips': {}
    }

    # Preparando dados para CSVs
    todos_headers = []
    pacotes_truncados = []

    for i, p in enumerate(pacotes):
        if len(p['dados']) >= 34:
            ip = p['dados'][14:34]
            origem = ".".join(map(str, ip[12:16]))
            destino = ".".join(map(str, ip[16:20]))
            protocolo = ip[9]
            proto_nome = PROTOCOLOS.get(protocolo, f"Desconhecido ({protocolo})")

            # Para CSV de headers completo
            todos_headers.append([
                i+1, p['timestamp'],
                ip[0] >> 4, (ip[0] & 0xF) * 4,
                proto_nome,
                origem, destino,
                p['origlen'], p['truncado']
            ])

            # Estatísticas
            if protocolo == 6:  # TCP
                stats['tcp']['count'] += 1
                if p['origlen'] > stats['tcp']['maior']:
                    stats['tcp'].update({
                        'maior': p['origlen'],
                        'origem': origem,
                        'destino': destino
                    })
            elif protocolo == 17:  # UDP
                stats['udp']['count'] += 1
                stats['udp']['sum'] += p['origlen']
                if p['origlen'] > stats['udp']['maior']:
                    stats['udp']['maior'] = p['origlen']

            # Tráfego por par
            par = (origem, destino, proto_nome)
            stats['trafego'][par] = stats['trafego'].get(par, 0) + p['origlen']

            # Contagem de IPs
            stats['ips'].update([origem, destino])
            stats['contagem_ips'][origem] = stats['contagem_ips'].get(origem, 0) + 1

        # Pacotes truncados
        if p['truncado']:
            pacotes_truncados.append([
                i+1, p['timestamp'],
                p['caplen'], p['origlen'],
                p['origlen'] - p['caplen']
            ])

    # Exporta CSVs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    exportar_csv(
        f"cabecalhos_ip_{timestamp}.csv",
        todos_headers,
        ["Nº", "Timestamp", "Versão", "IHL", "Protocolo", "Origem", "Destino", "Tamanho", "Truncado"]
    )
    exportar_csv(
        f"pacotes_truncados_{timestamp}.csv",
        pacotes_truncados,
        ["Nº", "Timestamp", "Capturado", "Original", "Perdido"]
    )

    return stats, todos_headers[:20]  # Retorna amostra para exibição

def gerar_respostas_csv(pacotes, stats):

    """Gera CSV com respostas às perguntas específicas"""

    ip_local = max(stats['contagem_ips'].items(), key=lambda x: x[1])[0] if stats['contagem_ips'] else "N/A"
    par_maior = max(stats['trafego'].items(), key=lambda x: x[1]) if stats['trafego'] else (("N/A", "N/A", "N/A"), 0)
    truncados = sum(1 for p in pacotes if p['truncado'])

    # Mostra as respostas das questões
    respostas = [
        ["Pergunta", "Resposta", "Detalhes"],
        ["a) Campos headers IP", "Ver arquivo cabecalhos_ip_*.csv", f"{stats['total']} pacotes"],
        ["b) Início captura", f"{stats['inicio']:.6f}", "Timestamp Unix"],
        ["b) Fim captura", f"{stats['fim']:.6f}", "Timestamp Unix"],
        ["c) Maior TCP", f"{stats['tcp']['maior']} bytes", 
         f"Origem: {stats['tcp']['origem']}, Destino: {stats['tcp']['destino']}"],
        ["d) Pacotes truncados", f"{truncados} ({truncados/stats['total']:.1%})", 
         f"Total: {stats['total']}"],
        ["e) Média UDP", f"{stats['udp']['sum']/stats['udp']['count']:.2f} bytes" if stats['udp']['count'] else "N/A", 
         f"Baseado em {stats['udp']['count']} pacotes"],
        ["f) Par maior tráfego", f"{par_maior[0][0]} ↔ {par_maior[0][1]}", 
         f"Protocolo: {par_maior[0][2]}, Bytes: {par_maior[1]}"],
        ["g) IPs interagidos", f"{len(stats['ips'])-1} IPs" if ip_local != "N/A" else "N/A", 
         f"IP Local: {ip_local}"]
    ]
    # Gera o arquivo em CSV com as respostas da análise
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    exportar_csv(
        f"respostas_perguntas_{timestamp}.csv",
        respostas,
        None  # Sem cabeçalho adicional pois já está nos dados
    )

def mostrar_resultados(stats, amostra_headers):

    """Exibe os resultados no formato desejado na tela"""

    print("\n[INFO] Cabeçalhos IP (amostra):")
    print(tabulate(
        amostra_headers,
        headers=["Nº", "Timestamp", "Versão", "IHL", "Protocolo", "Origem", "Destino", "Tamanho", "Truncado"],
        tablefmt="grid"
    ))

    print("\n[INFO] Intervalo de Captura:")
    print(tabulate([
        ["Início", f"{stats['inicio']:.6f}"],
        ["Fim", f"{stats['fim']:.6f}"],
        ["Duração", f"{stats['fim']-stats['inicio']:.6f} segundos"]
    ], tablefmt="grid"))

    print("\n[INFO] Estatísticas TCP:")
    print(tabulate([
        ["Total pacotes TCP", stats['tcp']['count']],
        ["Maior pacote TCP", f"{stats['tcp']['maior']} bytes"],
        ["Origem", stats['tcp']['origem']],
        ["Destino", stats['tcp']['destino']]
    ], tablefmt="grid"))

    if stats['udp']['count'] > 0:
        print("\n[INFO] Estatísticas UDP:")
        print(tabulate([
            ["Total pacotes UDP", stats['udp']['count']],
            ["Tamanho médio", f"{stats['udp']['sum']/stats['udp']['count']:.2f} bytes"],
            ["Maior pacote UDP", f"{stats['udp']['maior']} bytes"]
        ], tablefmt="grid"))

    print("\n[INFO] Par com maior tráfego:")
    par_maior = max(stats['trafego'].items(), key=lambda x: x[1])
    print(tabulate([
        ["Origem", par_maior[0][0]],
        ["Destino", par_maior[0][1]],
        ["Protocolo", par_maior[0][2]],
        ["Total bytes", par_maior[1]]
    ], tablefmt="grid"))

    ip_local = max(stats['contagem_ips'].items(), key=lambda x: x[1])[0]
    print("\n[INFO] Interações de Rede:")
    print(tabulate([
        ["IP Local", ip_local],
        ["IPs únicos", len(stats['ips'])],
        ["IPs interagidos", len(stats['ips'])-1]
    ], tablefmt="grid"))
# Aqui orquestra todo o fluxo de análise dos arquivos PCAP

if __name__ == "__main__":
    caminho = selecionar_arquivo()
    
    if caminho:
        try:
            pacotes = analisar_pcap(caminho)
            stats, amostra = processar_pacotes(pacotes)
            gerar_respostas_csv(pacotes, stats)
            mostrar_resultados(pacotes, stats, amostra)
            print("\nAnálise concluída! Verifique os arquivos CSV gerados.")
        except Exception as e:
            print(f"\n[ERRO] {str(e)}")
    else:
        print("Nenhum arquivo selecionado!")