from flask import Flask, render_template, request, jsonify
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)

# Настройка Pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Главная страница с формой
@app.route('/')
def index():
    return render_template('index.html')

# Обработчик запроса трендов
@app.route('/get_trends', methods=['POST'])
def get_trends():
    # Получаем запрос от пользователя
    keywords = request.form.get('keywords').split(',')
    geo = request.form.get('geo')

    # Настройка для анализа трендов
    pytrends.build_payload(keywords, cat=0, timeframe='now 7-d', geo=geo, gprop='')

    # Получаем тренды
    interest_over_time_df = pytrends.interest_over_time()

    # Преобразуем временные метки в строки (для ключей и значений)
    if not interest_over_time_df.empty:
        interest_over_time_df = interest_over_time_df.reset_index()
        interest_over_time_df['date'] = interest_over_time_df['date'].dt.strftime('%Y-%m-%d')

        trends_data = interest_over_time_df.to_dict(orient='records')
    else:
        trends_data = []

    # Генерация рекомендованных товаров
    recommended_products = get_recommended_products(keywords)

    print(f"Recommended Products: {recommended_products}")  # Выводим товары в консоль для отладки

    return jsonify({
        'trends': trends_data,
        'products': recommended_products
    })

# Функция для генерации рекомендованных товаров
def get_recommended_products(keywords):
    # Пример статической базы данных товаров
    all_products = {
        'умные часы': ['Smartwatch A', 'Smartwatch B', 'Smartwatch C'],
        'наушники Bluetooth': ['Bluetooth Headset A', 'Bluetooth Headset B'],
        'фитнес-браслет': ['Fitness Band A', 'Fitness Band B'],
        'смартфоны': ['Smartphone A', 'Smartphone B', 'Smartphone C'],
        'телевизоры': ['TV A', 'TV B', 'TV C']
    }

    recommended = []
    for keyword in keywords:
        if keyword.strip() in all_products:  # Используем strip() для удаления лишних пробелов
            recommended.extend(all_products[keyword.strip()])

    return recommended

if __name__ == '__main__':
    app.run(debug=True)
