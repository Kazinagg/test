from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import openpyxl
import math

# Функция для удаления пробелов из строки
def remove_spaces(string):
    return string.replace(" ", "")

# Функция для удаления последнего символа из строки
def remove_last_character(string):
    return string[:-1]

# Настройка опций Chrome для исключения логирования
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Инициализация драйвера Selenium с опциями
driver = webdriver.Chrome(options=options)

# Создание новой книги Excel и выбор активного листа
wb = openpyxl.Workbook()
ws = wb.active

# Установка заголовков для столбцов
ws.append(['Продукт', 'Цена', 'Кэшбек', 'Кэшбек (%)'])

# Функция для извлечения данных со страницы
def scrape_page(url):
    # Открытие страницы в браузере
    driver.get(url)

    # Ожидание загрузки JavaScript
    driver.implicitly_wait(5)  # Указывает время ожидания в секундах

    # Поиск блоков с информацией о кэшбеке и названии продукта
    cashback_blocks = driver.find_elements(By.CSS_SELECTOR, '.item-block')

    # Извлечение и запись информации о кэшбеке и продукте в Excel
    for block in cashback_blocks:
        try:
            # Название продукта
            title_element = block.find_element(By.CSS_SELECTOR, ".item-title a")
            product_name = title_element.text.strip() if title_element else 'Название продукта не найдено'
            
            # Информация о цене
            cash_element = block.find_element(By.CSS_SELECTOR, ".item-price span")
            cash = cash_element.text.strip() if cash_element else 'Информация о цене не найдена'
            
            # Информация о кэшбеке
            cashback_element = block.find_element(By.CSS_SELECTOR, ".bonus-amount")
            cashback = cashback_element.text.strip() if cashback_element else 'Информация о кэшбеке не найдена'
            # print(math.ceil((float(remove_last_character(remove_spaces(cashback))) / float(remove_last_character(remove_spaces(cash)))) * 1000))
            # Расчет процента кэшбека от цены
            try:
                cashback_procent = math.ceil((float(remove_last_character(remove_spaces(cashback))) / float(remove_last_character(remove_spaces(cash)))) * 1000)
            except ValueError:
                cashback_procent = 'Невозможно рассчитать'
            
            # Запись в Excel
            ws.append([product_name, cash, cashback, cashback_procent])
        except NoSuchElementException:
            # Если информация о кэшбеке не найдена, записываем только название продукта и цену
            print('Информация о кэшбеке не найдена')
            # ws.append([product_name, cash, 'Информация о кэшбеке не найдена', 'Невозможно рассчитать'])

# Цикл для прохода по всем страницам
page_number = 1
while True and page_number < 3:
    print(page_number)
    try:
        # Построение URL для текущей страницы
        if (page_number >= 2):
            page_url = f'https://megamarket.ru/catalog/noutbuki/page-{page_number}/'
        else: page_url = f'https://megamarket.ru/catalog/noutbuki/'
        
        # Скрейпинг текущей страницы
        scrape_page(page_url)
        
        # Проверка наличия кнопки "Следующая страница"
        next_button = driver.find_element(By.CSS_SELECTOR, '.next')
        if 'disabled' in next_button.get_attribute('class'):
            break  # Если кнопка неактивна, выходим из цикла
        
        # Увеличение номера страницы
        page_number += 1
    except NoSuchElementException:
        # Если кнопка "Следующая страница" не найдена, выходим из цикла
        break

# Сохранение книги в файл
wb.save('products_cashback.xlsx')

# Закрытие браузера и Excel файла
driver.quit()

# Вывод сообщения об успешной записи
print("Информация успешно записана в 'products_cashback.xlsx'")
