from quart import Quart, request, redirect, render_template
from database import check_user_credentials, generate_code, save_auth_code, verify_code
import datetime
import telegram
import asyncio

app = Quart(__name__)
BOT_TOKEN = ''
bot = telegram.Bot(token=BOT_TOKEN)

async def send_code_via_telegram(chat_id, code):
    try:
        await bot.send_message(chat_id=chat_id, text=f'🔐 Ваш код подтверждения: {code}')
    except Exception as e:
        print(f"Ошибка отправки кода: {e}")

@app.route('/')
async def home():
    return await render_template('login.html')

@app.route('/login', methods=['POST'])
async def login():
    form = await request.form
    user = check_user_credentials(form['username'], form['password'])
    
    if user:
        user_id, chat_id = user
        code = generate_code()
        expires = datetime.datetime.now() + datetime.timedelta(minutes=5)
        save_auth_code(user_id, code, expires)
        await send_code_via_telegram(chat_id, code)
        return redirect('/verify')
    
    return await render_template('login.html', error='Неверный логин или пароль')

@app.route('/verify', methods=['GET', 'POST'])
async def verify():
    if request.method == 'POST':
        code = (await request.form)['code']
        if verify_code(code):
            return redirect('/success')
        return await render_template('verify.html', error='Неверный код')
    return await render_template('verify.html')

@app.route('/success')
async def success():
    return await render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)