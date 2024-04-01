from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Настройка опций Chrome для исключения логирования
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Инициализация драйвера Selenium с опциями
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Открытие страницы в браузере
driver.get('https://megamarket.ru/catalog/noutbuki/')

# Ожидание загрузки JavaScript
driver.implicitly_wait(5)  # Указывает время ожидания в секундах

# Поиск блоков с информацией о кэшбеке и названии продукта
cashback_blocks = driver.find_elements(By.CSS_SELECTOR, '.item-block')

# Извлечение и вывод информации о кэшбеке и продукте
for block in cashback_blocks:
    try:
        # Название продукта
        title_element = block.find_element(By.CSS_SELECTOR, ".item-title a")
        product_name = title_element.text.strip() if title_element else 'Название продукта не найдено'
        
        # Информация о кэшбеке
        cashback_element = block.find_element(By.CSS_SELECTOR, ".bonus-amount")
        cashback = cashback_element.text.strip() if cashback_element else 'Информация о кэшбеке не найдена'

        # Информация о кэшбеке
        cash_element = block.find_element(By.CSS_SELECTOR, ".item-price span")
        cash = cash_element.text.strip() if cash_element else 'Информация о цене не найдена'
        
        
        print(f'Продукт: {product_name}, цена: {cash}, Кэшбек: {cashback}\n')
    except NoSuchElementException:
        print(f'Продукт: {product_name}, цена: {cash}, Кэшбек: Информация о кэшбеке не найдена\n')

# Закрытие браузера
driver.quit()
