import re
from telegram import BotCommand
from telegram.ext import ApplicationBuilder
from commands import load_commands
from handlers import setup_handlers

def is_valid_command(cmd):
    """
    Verifica se o comando é válido para o menu do Telegram.
    Apenas letras minúsculas, números e sublinhado.
    """
    return re.fullmatch(r'[a-z0-9_]{1,32}', cmd) is not None

async def set_menu_commands(application):
    """
    Define o menu de comandos do Telegram dinamicamente,
    apenas com comandos válidos.
    """
    commands = application.bot_data['commands']
    menu_commands = []
    for category_name, category in commands.items():
        if category_name == "atalhos":
            continue  # Ignora atalhos de teclado
        for cmd, info in category.items():
            if not is_valid_command(cmd):
                continue
            desc = info.get('significado', '')[:32]
            menu_commands.append(BotCommand(cmd, desc if desc else "Comando Linux"))
    menu_commands = menu_commands[:100]  # Limite do Telegram
    await application.bot.set_my_commands(menu_commands)

def main():
    commands = load_commands()
    application = (
        ApplicationBuilder()
        .token('SEU-TOKEN')
        .post_init(set_menu_commands)
        .build()
    )
    setup_handlers(application, commands)
    application.bot_data['commands'] = commands

    print("Bot está rodando...")
    application.run_polling()

if __name__ == '__main__':
    main()