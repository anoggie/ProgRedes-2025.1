# RawFetch

RawFetch é um pequeno utilitário em Python que realiza requisições HTTP e HTTPS utilizando apenas a biblioteca `socket`, sem o uso de bibliotecas de alto nível como `requests` ou `urllib`.

O programa:
- Analisa URLs completas.
- Detecta o protocolo (`http` ou `https`) e a porta correta (80 ou 443).
- Conecta-se via socket (com suporte a SSL).
- Envia requisições `GET` manualmente.
- Trata redirecionamentos (`3xx`).
- Lida com respostas `Content-Length` e `Transfer-Encoding: chunked`.
- Salva o conteúdo (HTML ou binário) em arquivo.
- Salva os headers HTTP da resposta em um arquivo separado (`header_resposta.txt`).

---

## 🚀 Como usar

1. Clone ou baixe este repositório.
2. Execute o script:

```bash
python rawfetch.py
````

3. Insira a URL desejada, como por exemplo:

```
Digite a URL (http ou https): https://www.exemplo.com/index.html
```

---

## 📂 Saídas

* `index.html` ou o nome correspondente ao arquivo da URL
* `header_resposta.txt`: contém o header da resposta HTTP

---

## 📌 Exemplo de uso

```
Digite a URL (http ou https): https://anoggie.net/
HOST: anoggie.net
Caminho: /
Nome do Arquivo: index.html
Download concluído.
```

---

## ⚙️ Requisitos

* Python 3.x
* Nenhuma dependência externa. Apenas `socket` e `ssl` da biblioteca padrão.

---

## ✍️ Autor

Criado para fins educacionais por [anoggie](https://github.com/anoggie) e [lovszksj](https://github.com/lovszksj) para fins de aprendizado de sockets com HTTP pela disciplina de **Programação para Redes**.