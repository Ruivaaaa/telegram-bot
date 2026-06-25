# 🤖 Bot Telegram com IA (Claude)

Bot de Telegram que responde perguntas usando a API do Claude (Anthropic).

---

## 📋 Pré-requisitos

- Conta no [GitHub](https://github.com)
- Conta no [Railway](https://railway.app)
- Token do bot Telegram (via @BotFather)
- Chave da API Anthropic (https://console.anthropic.com)

---

## 🚀 Passo a Passo

### 1. Criar o bot no Telegram

1. Abra o Telegram e pesquise por **@BotFather**
2. Envie `/newbot`
3. Escolha um nome e um username para o bot
4. Copie o **token** gerado (parece com `123456789:AAF...`)

### 2. Obter a chave da API Anthropic

1. Acesse https://console.anthropic.com
2. Vá em **API Keys** → **Create Key**
3. Copie a chave gerada

### 3. Subir o código no GitHub

```bash
git init
git add .
git commit -m "primeiro commit"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
git push -u origin main
```

### 4. Deploy no Railway

1. Acesse https://railway.app e faça login
2. Clique em **New Project** → **Deploy from GitHub repo**
3. Selecione seu repositório
4. Vá em **Variables** e adicione:
   - `TELEGRAM_BOT_TOKEN` → seu token do BotFather
   - `ANTHROPIC_API_KEY` → sua chave da Anthropic
5. Railway detecta o `Procfile` e faz o deploy automaticamente

---

## ✅ Funcionalidades

- `/start` — Inicia a conversa
- `/ajuda` — Mostra instruções
- `/limpar` — Apaga o histórico da conversa
- Qualquer mensagem de texto → respondida pela IA com contexto da conversa

---

## 🗂 Estrutura

```
telegram-bot/
├── bot.py              # Código principal
├── requirements.txt    # Dependências Python
├── Procfile            # Comando de inicialização (Railway)
├── .env.example        # Exemplo de variáveis de ambiente
└── README.md           # Este arquivo
```

---

## ⚠️ Importante

- **Nunca** suba o arquivo `.env` com suas chaves reais para o GitHub
- No Railway, as variáveis de ambiente são configuradas pela interface web
- O histórico de conversa fica em memória; reiniciar o bot apaga o histórico
