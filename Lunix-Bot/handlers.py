from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from commands import find_command, format_command_response, generate_help_message
import re

def escape_markdown_v2(text):
    """
    Escapa caracteres especiais para uso seguro com MarkdownV2 do Telegram.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Mensagem de boas-vindas e instruções iniciais.
    """
    message = (
        "🤖 *Lunix Command Bot*\n\n"
        "Olá\\! Eu sou o Linux, e minha missão é ajudar você a entender comandos Linux\\!\n\n"
        "Digite / para ver a lista de comandos disponíveis\n"
        "Ou envie /\\[comando\\] \\(ex\\: /ls\\)"
    )
    await update.message.reply_markdown_v2(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Exibe a mensagem de ajuda com todos os comandos.
    """
    commands = context.bot_data['commands']
    message = generate_help_message(commands)
    await update.message.reply_markdown_v2(message)

async def generic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Trata comandos dinâmicos: busca e responde sobre o comando solicitado.
    """
    command_name = update.message.text[1:].lower()
    commands = context.bot_data['commands']
    command_info = find_command(command_name, commands)
    
    if command_info:
        response = format_command_response(command_name, command_info)
        await update.message.reply_markdown_v2(response)
    else:
        await update.message.reply_text(
            "⚠️ [ERRO]: Comando não encontrado! Digite / para ver a lista."
        )

def setup_handlers(application, commands):
    """
    Registra todos os handlers (comandos) no bot.
    """
    application.bot_data['commands'] = commands

    # Handlers fixos
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ajuda", help_command))

    # Handlers dinâmicos para cada comando do JSON
    for category in commands.values():
        for cmd in category:
            application.add_handler(CommandHandler(cmd, generic_command))