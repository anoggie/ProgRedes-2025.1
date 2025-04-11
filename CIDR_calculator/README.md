# 🧮 Calculadora de Sub-redes CIDR
Este programa em Python calcula informações detalhadas sobre sub-redes a partir de um endereço IP e um intervalo de valores CIDR (por exemplo, de /24 até /30).

### 📋 Funcionalidades:

- Valida o IP fornecido em 4 octetos que vão de `0` a `255`.

- Converte IPs e máscaras entre formatos `decimal` e `binário`.

Calcula:

- Endereço de rede

- Primeiro e último IP de host

- Endereço de broadcast

- Máscara de sub-rede (decimal e binária)

- Quantidade de hosts válidos

- Exibe os dados em formato de tabela.

- Salva os resultados em um arquivo .json.


## 🛠️ Como usar:
Caso não tenha a biblioteca tabulate, rode o seguinte comando para instalá-lo:
```
pip install tabulate
```
Em seguida, execute o script e insira as seguintes informações solicitadas:

- Um endereço IP (ex: 192.168.0.1)

- Um valor CIDR inicial (ex: 24)

- Um valor CIDR final (ex: 30)

O programa mostrará os cálculos formatados no terminal para cada faixa, e salvará todas as informações automaticamente em um arquivo `.json`.
## ✨ Desenvolvido por:

- [@anoggie](https://www.github.com/anoggie)
- [@lovszksj](https://www.github.com/lovszksj)

