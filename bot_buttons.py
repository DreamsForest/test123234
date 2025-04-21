import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешаем все CORS-запросы

TOKEN = os.environ.get("TOKEN", "f9LHodD0cOLX7UGehN1HCPp6Pp9mAu-ebAySBD4VVbbhY9vnNiz_DSFlvcfrHBckhjbx3WJ3-W1P32DpMDgP")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        
        # Проверяем, что это команда /start
        if 'message' in data and 'text' in data['message'] and data['message']['text'] == '/start':
            response = {
                'chat_id': data['message']['chat']['id'],
                'text': 'Привет! Я бот для подготовки к ЕГЭ по математике. Выберите действие:',
                'reply_markup': {
                    'inline_keyboard': [
                        [{'text': 'Теория', 'url': 'https://chipper-flan-72a78b.netlify.app/theory'}],
                        [{'text': 'Задачи', 'callback_data': 'tasks'}]
                    ]
                }
            }
            return jsonify(response)
        
        # Обработка других сообщений
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))