import json
import re

def load_commands():
    """Carrega os comandos do arquivo JSON."""
    with open('comandos.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def escape_markdown_v2(text):
    """
    Escapa caracteres especiais para uso seguro com MarkdownV2 do Telegram.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def format_command_response(command, info):
    """
    Formata a resposta detalhada de um comando para o Telegram.
    """
    command_esc = escape_markdown_v2(command.upper())
    significado_esc = escape_markdown_v2(info.get('significado', ''))
    descricao_esc = escape_markdown_v2(info.get('descricao', ''))

    response = f"📌 *{command_esc}* \\- _{significado_esc}_\n\n"
    response += f"📝 *O que faz\\:* {descricao_esc}\n\n"

    # Adiciona parâmetros, se existirem
    if 'parametros' in info and info['parametros']:
        response += "🔧 *Parâmetros comuns\\:*\n"
        for param, desc in info['parametros'].items():
            param_esc = escape_markdown_v2(param)
            desc_esc = escape_markdown_v2(desc)
            response += f"`{param_esc}` \\- {desc_esc}\n"
        response += "\n"

    exemplo_esc = escape_markdown_v2(info.get('exemplo', ''))
    response += f"💡 *Exemplo de uso\\:*\n```\n{exemplo_esc}\n```"
    return response

def generate_help_message(commands):
    """
    Gera a mensagem de ajuda com todos os comandos disponíveis.
    """
    message = "📚 *Guia de Comandos Linux*\n\n"
    message += "Envie /comando para obter explicações detalhadas\n\n"

    for category_name, category_commands in commands.items():
        category_esc = escape_markdown_v2(category_name.upper())
        message += f"🔹 *{category_esc}* 🔹\n"
        for cmd in category_commands:
            cmd_esc = escape_markdown_v2(cmd)
            message += f"/{cmd_esc}\n"
        message += "\n"

    message += "Exemplo\\: `/ls` para ver sobre o comando ls"
    return message

def find_command(command_name, commands):
    """
    Busca um comando pelo nome em todas as categorias.
    """
    for category in commands.values():
        if command_name in category:
            return category[command_name]
    return None