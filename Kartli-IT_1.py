import pandas as pd                     # Библиотека для работы с файлами формата xlsx               
from datetime import datetime           # Библиотека для работы с датами                     
import matplotlib.pyplot as plt         # Библиотека для работы с графиками и визуализации данных
import yfinance as yf                   # Библиотека для получения информации с платформы Yahoo! Finance

while True:                                                                                         # Бесконечный цикл для проверки ввода данных
    ticker = str(input('Введите тикер: ')).upper()                                                  # Ввод тикера в верхнем регистре
    date_start = input('Ввод дат осуществляйте в формате YYYY-MM-DD\nНачальная дата: ')             # Ввод начальной даты
    date_end = input('Конечная дата: ')                                                             # Ввод конечной даты
    try:
        yf.Ticker(ticker).info                                                                      # Проверка существования тикера
        valid_date_start = datetime.strptime(date_start, '%Y-%m-%d')                                # Перевод дат в нужный формат
        valid_date_end = datetime.strptime(date_end, '%Y-%m-%d')
        if valid_date_end > valid_date_start:                                                       # Проверка является ли первая введенная дата меньше второй
            break
        else:
            print('Дата введена некорректно\nВведите данные повторно')                              # Сообщение об ошибке
    except:
        print('Данные введены некорректно\nВведите данные повторно')                                # Сообщение об ошибке

data = pd.DataFrame({'Close': yf.download(ticker, date_start, date_end)['Close']})                  # Получаем необходимую информацию с платформы                                                       

max_row = data.shape[0]                                                                             # Находим кол-во строк в таблице    
max_column = data.shape[1]                                                                          # Находим кол-во столбцов в таблице

date = pd.to_datetime(data.index).to_list()                                                         # Преобразуем колонку с датами в список
close = data['Close'].to_list()                                                                     # Преобразуем колонку Close в список
long_xl, short_xl, long_exit, short_exit, position, daily_yield = [0], [0], [0], [0], [0], [0]      # Объявляем необходимые списки, и добавляем в них перове значение равное 0, т.к. алгоритм начинает работу при на основе 2 предыдущих дней

for i in range(1, max_row):                                                                                                                                                             # Реализация торгового алгоритма           
    long_xl.append(1) if (close[i] > close[i-1]) and (close[i-1] > close[i-2]) and (position[i-1] == 0) else long_xl.append(0)                                                          # Long
    short_xl.append(1) if (close[i] < close[i-1]) and (close[i-1] < close[i-2]) and (position[i-1] == 0) else short_xl.append(0)                                                        # Short
    long_exit.append(1) if (position[i-1] == 1) and (close[i] < close[i-1]) and (close[i-1] < close[i-2]) else long_exit.append(0)                                                      # Long exit
    short_exit.append(1) if (position[i-1] == -1) and (close[i] > close[i-1]) and (close[i-1] > close[i-2]) else short_exit.append(0)                                                   # Short exit
    position.append(long_xl[i] - short_xl[i]) if (position[i-1] == 0) else position.append(0) if (long_exit[i] + short_exit[i]) == 1 else position.append(position[i-1])                # Позиция
    daily_yield.append((float(close[i])/float(close[i-1])-1)*position[i-1]) if (position[i-1] != 0) else daily_yield.append(0)                                                          # Дневная доходность

df = pd.DataFrame({                                                                                 # Формируем датафрейм                         
    'Date': date,
    'Close': close,
    'Long': long_xl,
    'Short': short_xl,
    'Long exit': long_exit,
    'Short exit': short_exit,
    'Position': position,
    'Дневная доходность': daily_yield
}) 
df.to_excel('End.xlsx', sheet_name='TA', index = False)                                             # Полученный датафрейм записываем в таблицу excel

df = pd.read_excel('End.xlsx')                                                                      # Строим график Дневной доходности
df.plot(x='Date', y='Дневная доходность', figsize=(15, 10), grid=True, marker='.')   
plt.show()