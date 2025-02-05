import telebot
import pandas as pd


# указываем токен бота
bot = telebot.TeleBot('8044498486:AAFx-u1Aov-9l4fnt73xo7GkDLN0oe0kWvg')


# события по кнопке старт
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    # создаем клавиатуру с кнопками
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="Бедные регионы")
    button2 = telebot.types.KeyboardButton(text="Бизнес-регионы")
    button3 = telebot.types.KeyboardButton(text="Производственные регионы")
    button4 = telebot.types.KeyboardButton(text="Среднестатистические регионы")    
    keyboard.add(button1, button2, button3, button4)
    # приветствуем нового пользователя
    bot.send_message(chat_id,
                     ('Привет! Здесь ты можешь узнать больше о регионах РФ.\n' 
                     'Введите название региона или выберите из меню кнопку для получения списка регионов'),
                     reply_markup=keyboard)


# события при вводе текста
@bot.message_handler(content_types=['text'], 
                     func=lambda message: message.text != 'Бедные регионы' and 
                     message.text != 'Бизнес-регионы' and 
                     message.text != 'Производственные регионы' and 
                     message.text != 'Среднестатистические регионы')
def cluster_region(message):
    # запоминаем id чата
    chat_id = message.chat.id
    # это полученное от пользователя сообщение
    text = message.text
    # ищем регион
    region_str = find_region(text)
    # выводим информацию
    bot.send_message(chat_id, region_str)
    

# функция поиска региона в датасете с метками
def find_region(name_region):
    data = pd.read_csv('data/data_labels.csv')      
    data = data.rename(columns={'Unnamed: 0': 'region'})
    # в эту переменную запишем результат
    region_str = ''
    # создаем доп.колонку с именами регионов в нижнем регистре и без пробелов
    data['region_name'] = data['region'].apply(lambda x: x.lower().replace(' ', ''))
    # ищем введенное имя в нашей таблице, 
    # предварительно имя привели к нижнему регистру и сделали без пробелов
    filtered = data[data['region_name'].str.contains(name_region.lower().replace(' ', ''))]
    
    # если найдено несколько регионов, 
    # удовлетворяющих поиску, то выводим все
    for index, region_data in filtered.iterrows():
        # если регион в первом кластере
        if region_data['cluster']==0:
            region_str = region_str + region_data['region'] + (". Бедный регион. Основные характеристики: самый высокий процент людей, " 
            "живущих за чертой бедности, самые низкие доходы населения, " 
            "самый большой процент пенсионеров, больше всего людей, испытывающих стесненность при проживании, " 
            "самое маленькое значение валового регионального продукта на душу населения, "   
            "самый маленький оборот розничной торговли. ")
        # если регион во втором кластере
        elif region_data['cluster']==1:
            region_str = region_str + region_data['region'] + (". Бизнес-регион. Основные характеристики: " 
            "больше всего инвалидов, самые высокие доходы населения, " 
            "самый большой процент детей, самый большой валовый региональный продукт на душу населения, "  
            "самый большой оборот розничной торговли, "
            "больше всего людей с заболеваниями и страдающих алкогольной или наркотической зависимостями.")    
        # если регион в третьем кластере
        elif region_data['cluster']==2:
            region_str = region_str + region_data['region'] + (". Производственный регион. Основные характеристики: " 
            "самая высокая детская смертность, "
            "больше всего населения, самый большой объем отгруженных товаров собственного производства или работ/услуг, " 
            "выполненных собственными силами, больше всего рожденных и больше всего преступлений, хорошие доходы населения.")           
        # если регион в четвертом кластере
        elif region_data['cluster']==3:
            region_str = region_str + region_data['region'] + (". Среднестатистический регион. " 
            "Основные характеристики: самый большой процент трудоспособного населения, " 
            "по всем показателям имеет средние значения.") 
        region_str = region_str + "\n" 
    
    # ничего не нашли, вернем информацию об этом         
    if len(filtered)==0:
        region_str = 'Регион не найден'
                           
    return region_str   
    
    
# события при выборе бедных регионов
@bot.message_handler(
    func=lambda message: message.text == 'Бедные регионы')
def cluster_region(message):
    # запоминаем id чата
    chat_id = message.chat.id
    # указываем номер кластера
    num_cluster = 0
    # находим информацию по кластеру
    region_str = info_region(num_cluster)
    # отправляем сообщение в чат
    bot.send_message(chat_id, region_str)
    
    
# события при выборе Бизнес-регионы    
@bot.message_handler(
    func=lambda message: message.text == 'Бизнес-регионы')
def cluster_region(message):
    # запоминаем id чата
    chat_id = message.chat.id
    # указываем номер кластера
    num_cluster = 1
    # находим информацию по кластеру
    region_str = info_region(num_cluster)
    # отправляем сообщение в чат
    bot.send_message(chat_id, region_str)    
    
 
# события при выборе Производственные регионы     
@bot.message_handler(
    func=lambda message: message.text == 'Производственные регионы')
def cluster_region(message):
    # запоминаем id чата
    chat_id = message.chat.id
    # указываем номер кластера
    num_cluster = 2
    # находим информацию по кластеру
    region_str = info_region(num_cluster)
    # отправляем сообщение в чат
    bot.send_message(chat_id, region_str)  
    
    
# события при выборе Среднестатистические регионы      
@bot.message_handler(
    func=lambda message: message.text == 'Среднестатистические регионы')
def cluster_region(message):
    # запоминаем id чата
    chat_id = message.chat.id
    # указываем номер кластера
    num_cluster = 3
    # находим информацию по кластеру
    region_str = info_region(num_cluster)
    # отправляем сообщение в чат
    bot.send_message(chat_id, region_str)      
          
  
# функция получения информации по номеру кластера    
def info_region(num_cluster):
    data = pd.read_csv('data/data_labels.csv')      
    data = data.rename(columns={'Unnamed: 0': 'region'})
    
    # собираем регионы и сортируем по имени
    regions = data[data['cluster']==num_cluster]['region'].sort_values()
    # создаем из списка строку регионов, разделенных запятой
    region_str = str.join(', ', list(regions))
    
    return region_str


if __name__ == '__main__':
    print('Бот запущен!')
    
bot.infinity_polling()      
        
        
     