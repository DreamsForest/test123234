import os
from flask import Flask, request, jsonify, redirect, send_from_directory
import requests
from flask_cors import CORS  # Для обработки CORS-запросов

app = Flask(__name__)
CORS(app)  # Разрешаем запросы от фронтенда

TOKEN = os.environ.get("TOKEN", "f9LHodD0cOLX7UGehN1HCPp6Pp9mAu-ebAySBD4VVbbhY9vnNiz_DSFlvcfrHBckhjbx3WJ3-W1P32DpMDgP")

# Перенаправление с корневого пути на фронтенд
@app.route('/')
def home():
    return redirect('https://chipper-flan-72a78b.netlify.app')

# Обработка вебхука от бота
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        chat_id = data['message']['chat']['id']
        
        response = requests.post(
            'https://api.max.ru/bot/v1/messages/send',
            headers={'Authorization': f'Bearer {TOKEN}'},
            json={
                'chat_id': chat_id,
                'text': 'Выберите действие:',
                'reply_markup': {
                    'inline_keyboard': [
                        [{'text': 'Теория', 'url': 'https://chipper-flan-72a78b.netlify.app/theory'}],
                        [{'text': 'Задачи', 'callback_data': 'tasks'}]
                    ]
                }
            }
        )
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Если нужно отдавать статику Vue.js через Flask (альтернативный вариант)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))