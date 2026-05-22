# 📧 SmartMail AI

AI-powered email reply generator built with **Streamlit** and **OpenAI GPT**.

Paste any email → pick a tone → get a professional reply in seconds.

---

## ✨ Features

- **6 reply tones** — Professional, Friendly, Formal, Concise, Apologetic, Assertive
- **One-click generation** powered by GPT-3.5-turbo
- **Editable output** — tweak the reply before you send
- **Regenerate** as many times as you need
- Clean, modern UI with custom styling

---

## 🚀 Quick Start

### 1. Clone / Download the project

```bash
git clone https://github.com/yourname/smartmail-ai.git
cd smartmail-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your OpenAI API key

Open `.env` and replace the placeholder:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Get your key at → https://platform.openai.com/api-keys

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## 📁 Project Structure

```
smartmail-ai/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # Your API key (never commit this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## 🎨 Reply Tones

| Tone | Best For |
|------|----------|
| 💼 Professional | Business emails, client communication |
| 😊 Friendly | Colleagues, casual partners |
| 🏛️ Formal | Official correspondence, legal/govt |
| ⚡ Concise | Quick replies, busy recipients |
| 🙏 Apologetic | Delays, mistakes, complaints |
| 💪 Assertive | Negotiations, setting boundaries |

---

## 🔧 Customisation

**Change the model** — in `app.py`, find this line and swap the model:
```python
model="gpt-3.5-turbo",   # or "gpt-4o-mini", "gpt-4o"
```

**Change max reply length** — adjust `max_tokens`:
```python
max_tokens=500,   # increase for longer replies
```

**Add a new tone** — add an entry to the `TONES` dict in `app.py`:
```python
"Persuasive": {
    "emoji": "🎯",
    "desc": "Convincing and motivating",
    "prompt_hint": "Use persuasive language to convince the reader."
},
```

---

## ⚠️ Important

- Never commit your `.env` file — it's already in `.gitignore`
- OpenAI API usage incurs small costs (GPT-3.5 is very cheap)
- Check your usage at https://platform.openai.com/usage

---

## 🛠️ Built With

- [Streamlit](https://streamlit.io) — UI framework
- [OpenAI Python SDK](https://github.com/openai/openai-python) — GPT API
- [python-dotenv](https://pypi.org/project/python-dotenv/) — env management

---

*SmartMail AI — reply smarter, not harder.*
