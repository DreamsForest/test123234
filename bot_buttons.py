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
        # Проверяем наличие необходимых данных
        if not request.json or 'message' not in request.json:
            return jsonify({'error': 'Invalid request format'}), 400
            
        data = request.json
        chat_id = data['message']['chat']['id']
        
        # Формируем ответ для Max
        response_data = {
            'chat_id': chat_id,
            'text': 'Выберите действие:',
            'reply_markup': {
                'inline_keyboard': [
                    [{'text': 'Теория', 'url': 'https://chipper-flan-72a78b.netlify.app/theory'}],
                    [{'text': 'Задачи', 'callback_data': 'tasks'}]
                ]
            }
        }
        
        # Отправляем ответ сразу, без дополнительного запроса к API Max
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))