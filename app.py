import os
from flask import Flask, request
import telegram
from gemini import gemini

TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

bot = telegram.Bot(token=TOKEN)
client = gemini(api_key=gemini_KEY)

app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    update = telegram.Update.de_json(data, bot)

    if update.message:
        user_text = update.message.text

        prompt = f"""
你是商业内容生产系统。
根据用户输入生成结构化商业内容。

用户输入：{user_text}

输出包含：
1. 项目定位
2. 商业模式
3. 收入来源
4. 市场策略
5. 风险分析
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response.choices[0].message.content
        update.message.reply_text(reply)

    return "ok"

@app.route("/")
def index():
    return "Bot running"
