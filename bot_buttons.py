import os
import logging
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешаем все CORS-запросы

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TOKEN", "f9LHodD0cOLX7UGehN1HCPp6Pp9mAu-ebAySBD4VVbbhY9vnNiz_DSFlvcfrHBckhjbx3WJ3-W1P32DpMDgP")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        logger.info(f"Получены данные: {data}")  # Логируем входящий запрос

        # Проверка структуры сообщения
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid request format'}), 400

        message = data['message']
        chat_id = message['chat']['id']

        # Обработка команды /start
        if 'text' in message and message['text'].startswith('/start'):
            response = {
                'method': 'sendMessage',
                'chat_id': chat_id,
                'text': 'Привет! Я бот для подготовки к ЕГЭ по математике.\nВыберите действие:',
                'reply_markup': {
                    'inline_keyboard': [
                        [{'text': '📚 Теория', 'url': 'https://chipper-flan-72a78b.netlify.app/theory'}],
                        [{'text': '📝 Задачи', 'callback_data': 'tasks'}],
                        [{'text': 'ℹ️ Помощь', 'callback_data': 'help'}]
                    ]
                }
            }
            return jsonify(response)

        # Ответ на другие сообщения
        return jsonify({
            'method': 'sendMessage',
            'chat_id': chat_id,
            'text': 'Используйте команду /start для начала работы'
        })

    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))