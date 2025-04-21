import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = "f9LHodD0cOLX7UGehN1HCPp6Pp9mAu-ebAySBD4VVbbhY9vnNiz_DSFlvcfrHBckhjbx3WJ3-W1P32DpMDgP"  # Храните в переменных окружения Heroku!

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        chat_id = data['message']['chat']['id']
        
        response = requests.post(
            'https://api.max.ru/bot/v1/messages/send',  # Проверьте URL!
            headers={'Authorization': f'Bearer {TOKEN}'},  # Фигурные скобки
            json={  # Корректный JSON
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))) 