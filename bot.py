import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Clients
anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Histórico de conversa por usuário (em memória)
conversation_history: dict[int, list] = {}

SYSTEM_PROMPT = """Você é um assistente inteligente e prestativo no Telegram. 
Responda de forma clara, concisa e amigável em português. 
Seja direto nas respostas e use formatação simples (sem markdown complexo)."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"Olá, {user.first_name}! 👋\n\n"
        "Sou um assistente com IA. Pode me fazer qualquer pergunta!\n\n"
        "Comandos disponíveis:\n"
        "/start - Iniciar conversa\n"
        "/limpar - Limpar histórico da conversa\n"
        "/ajuda - Ver ajuda"
    )


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /ajuda"""
    await update.message.reply_text(
        "🤖 *Como usar o bot:*\n\n"
        "Basta enviar uma mensagem de texto e eu responderei usando IA.\n\n"
        "Eu lembro do contexto da nossa conversa, então pode fazer perguntas de acompanhamento!\n\n"
        "Use /limpar para começar uma nova conversa do zero.",
        parse_mode="Markdown"
    )


async def limpar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /limpar - apaga o histórico"""
    user_id = update.effective_user.id
    conversation_history.pop(user_id, None)
    await update.message.reply_text("✅ Histórico limpo! Começando uma nova conversa.")


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde mensagens de texto usando Claude"""
    user_id = update.effective_user.id
    user_message = update.message.text

    # Inicializa histórico se necessário
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Adiciona mensagem do usuário ao histórico
    conversation_history[user_id].append({
        "role": "user",
        "content": user_message
    })

    # Mantém no máximo 20 mensagens no histórico (10 trocas)
    if len(conversation_history[user_id]) > 20:
        conversation_history[user_id] = conversation_history[user_id][-20:]

    # Mostra "digitando..."
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    try:
        response = anthropic_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=conversation_history[user_id]
        )

        assistant_message = response.content[0].text

        # Adiciona resposta ao histórico
        conversation_history[user_id].append({
            "role": "assistant",
            "content": assistant_message
        })

        await update.message.reply_text(assistant_message)

    except Exception as e:
        logger.error(f"Erro ao chamar API: {e}")
        await update.message.reply_text(
            "❌ Ocorreu um erro ao processar sua mensagem. Tente novamente."
        )


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("limpar", limpar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    logger.info("Bot iniciado!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
