```
O TCPdump Analyzer é uma ferramenta para análise de arquivos de captura de rede (PCAP)
que extrai informações detalhadas sobre os pacotes e gera relatórios em formato CSV.
```

## Funcionalidades
- Análise de um ou múltiplos arquivos PCAP simultaneamente

- Extração de cabeçalhos IP e informações de protocolo  

- Geração de relatórios estatísticos

- Identificação de pacotes truncados

- Exportação de dados para CSV

- Análise de tráfego entre pares de IPs

- Identificação do IP local mais ativo

## Formatos Suportados

- .pcap

- .cap

- .dump

- .pcapng

# Requisitos
- Python 3.6 ou superior

### Bibliotecas:

- tkinter

- tabulate

## Como Usar
Execute o script:

`python pcap_analyzer.py` 

Selecione um ou mais arquivos PCAP usando a janela de diálogo.

#### Os seguintes arquivos CSV serão gerados:

`cabecalhos_ip_[TIMESTAMP].csv` - Contém todos os cabeçalhos IP analisados

`pacotes_truncados_[TIMESTAMP].csv` - Lista pacotes com dados incompletos

`respostas_perguntas_[TIMESTAMP].csv` - Resumo estatístico da análise

## Saída
O programa gera três tipos de relatórios:

`Cabeçalhos IP completos:`

- Número do pacote

- Timestamp

- Versão IP

- IHL

- Protocolo

- IP de origem

- IP de destino

- Tamanho do pacote

- Indicador de truncamento

- Arquivo de origem

`Pacotes truncados:`

- Número do pacote

- Timestamp

- Bytes capturados

- Bytes originais

- Bytes perdidos

- Arquivo de origem

`Resumo estatístico:`

- Intervalo de tempo da captura

- Estatísticas TCP/UDP

- Par com maior tráfego

- IPs interagidos

- Lista de arquivos analisados