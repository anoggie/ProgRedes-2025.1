import json
import os
from tabulate import tabulate

def validar_ip(ip):

    '''valida se o IP tem 4 partes
    e vê se cada uma está entre 0 e 255'''

    partes = ip.split('.')
    if len(partes) != 4:
        return False

    for parte in partes:
        try:
            numero = int(parte)
            if numero < 0 or numero > 255:
                return False
        except ValueError:
            return False
    return True

def ip_para_binario(ip):

    '''converte o IP em binário,
    preenchendo com zeros à esquerda'''

    partes = ip.split('.')
    binarios = ''
    for parte in partes:
        binario = bin(int(parte))[2:]
        binarios += binario.zfill(8)
    return binarios

def binario_para_ip(binario):

    '''divide os 32 bits em grupos de 8,
    percorre a string de 8 em 8,
    e converte cada grupo para decimal'''

    ip = ''
    for i in range(0, 32, 8):
        grupo = binario[i:i+8]
        numero = str(int(grupo, 2))
        if i == 0:
            ip += numero
        else:
            ip += '.' + numero
    return ip

def calcular_subrede(ip, cidr):
    ip_bin = ip_para_binario(ip)

    '''cria a máscara binária
    1s no começo e 0s no final'''

    mascara_bin = ''
    for i in range(32):
        if i < cidr:
            mascara_bin += '1'
        else:
            mascara_bin += '0'

    rede_bin = ''
    for i in range(32):
        if ip_bin[i] == '1' and mascara_bin[i] == '1':  # operacao 'AND' entre IP e máscara
            rede_bin += '1'
        else:
            rede_bin += '0'

    broadcast_bin = ip_bin[:cidr] + '1' * (32 - cidr)
    primeiro_host_bin = rede_bin[:-1] + '1'
    ultimo_host_bin = broadcast_bin[:-1] + '0'


    # casos ecspeciais (CIDR /31 e /32)
    if cidr == 32:
        hosts_validos = "não aplicável"
        primeiro_host = ip
        ultimo_host = ip
    elif cidr == 31:
        hosts_validos = "2 (ponto-a-ponto)"
        primeiro_host = binario_para_ip(primeiro_host_bin)
        ultimo_host = binario_para_ip(ultimo_host_bin)
        
    else:
        hosts_validos = (2 ** (32 - cidr)) - 2
        primeiro_host = binario_para_ip(primeiro_host_bin)
        ultimo_host = binario_para_ip(ultimo_host_bin)

    return {
        'rede': binario_para_ip(rede_bin),
        'primeiro_host': primeiro_host,
        'ultimo_host': ultimo_host,
        'broadcast': binario_para_ip(broadcast_bin),
        'mascara': binario_para_ip(mascara_bin),
        'mascara_bin': mascara_bin,
        'hosts_validos': hosts_validos
    }



def salvar_resultados(lista, nome_base='subredes.json'):
    '''Salva os dados num arquivo JSON
    evitando sobrescrever arquivos existentes'''
    contador = 1
    nome_final = nome_base
    while os.path.exists(nome_final):
        nome_final = f"resultados_subredes_{contador}.json"
        contador += 1

    with open(nome_final, 'w') as f:
        json.dump(lista, f, indent=4)

def main():
    '''Coleta os dados do usuário,
    calcula e exibe os resultados'''
    print("Calculadora de Sub-redes CIDR")
    print("----------------------------")

    ip = input("Digite o IP (ex: 192.168.1.1): ")
    while not validar_ip(ip):
        print("IP inválido! Tente novamente.")
        ip = input("Digite o IP (ex: 192.168.1.1): ")

    # Leitura e validação do CIDR
    while True:
        try:
            cidr_ini = int(input("CIDR inicial (ex: 24): ").strip('/'))
            cidr_fim = int(input("CIDR final (ex: 30): ").strip('/'))
            if not (0 <= cidr_ini <= 32) or not (0 <= cidr_fim <= 32):
                print("CIDR deve estar entre 0 e 32.")
                continue
            break
        except ValueError:
            print("CIDR inválido. Digite apenas números.")

    if cidr_ini > cidr_fim:
        cidr_ini, cidr_fim = cidr_fim, cidr_ini

    resultados = []

    for cidr in range(cidr_ini, cidr_fim + 1):
        dados = calcular_subrede(ip, cidr)

        resultado = {'CIDR': f'/{cidr}'}
        for chave in dados:
            resultado[chave] = dados[chave]
        resultados.append(resultado)

        print(f"\nResultados para /{cidr}:")
        print(tabulate([
            ["Endereço IP", ip],
            ["Máscara", f"{dados['mascara']} (/{cidr})"],
            ["Máscara Binária", dados['mascara_bin']],
            ["Rede", dados['rede']],
            ["Primeiro Host", dados['primeiro_host']],
            ["Último Host", dados['ultimo_host']],
            ["Broadcast", dados['broadcast']],
            ["Hosts Válidos", dados['hosts_validos']]
        ], tablefmt="grid"))

    salvar_resultados(resultados)
    print("\nResultados salvos em arquivo JSON!")

main()