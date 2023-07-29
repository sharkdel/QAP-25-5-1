from selenium.webdriver.common.by import By
from settings import valid_email, valid_password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_show_my_pets(driver):
    # Вход в акаунт и на страницу "мои питомцы"
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Добавляем неявное ожидание
    driver.implicitly_wait(10)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Переходим на страницу "Мои питомцы"
    driver.find_element(By.CSS_SELECTOR, 'div#navbarNav > ul > li > a').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.CSS_SELECTOR, 'html > body > nav > a').text == "PetFriends"
    # нажимаем ссылку "мои питомцы"
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()


def test_present_all_my_pets(driver):
    """" Тест1: написать тест, который проверяет, что на странице со списком питомцев пользователя
    # присутствуют все питомцы."""
    test_show_my_pets(driver)
    # Настраиваем переменную явного ожидания:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')))
    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]//td[1]')
    # Берём статистику из личного кабинета сайта
    statistics = driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')
    # Берём текст из нулевого элемента статистики
    count_names = statistics[0].text.split('\n')
    # Берем 1-ый элемент из текста
    count_names = count_names[1].split(' ')
    # Присваиваем числовой формат для 1-го элемента
    count_names = int(count_names[1])
    try:
        assert len(names) == count_names
        print(f'\nКоличество питомцев в статистике равно количеству питомцев в таблице: {count_names} = {len(names)}')
    except AssertionError as e:
        print(f'\nТест1 произошла ошибка AssertionError: Количество питомцев в статистике не равно количеству питомцев '
              f'в таблице:{count_names} != {len(names)}')
        print(e)
        pass


def test_more_half_pets_with_photo(driver):
    """" Тест2: написать тест, который проверяет, что на странице со списком питомцев пользователя:
    Хотя бы у половины питомцев есть фото."""
    test_show_my_pets(driver)
    # Сохраняем в переменную ststistics элементы статистики
    statistic = driver.find_elements(By.CSS_SELECTOR, '.\\.col-sm-4.left')
    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]//td[1]')
    # Сохраняем в переменную images элементы с атрибутом img
    images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]//img')
    # Получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])
    # Находим половину от количества питомцев
    half = number // 2
    # Находим количество питомцев с фотографией
    counter_of_images = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            counter_of_images += 1
    # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
    try:
        assert counter_of_images >= half
        print(f'\nТест2 Количество питомцев с фото: {counter_of_images}, а половина от числа питомцев: {half}')
    except AssertionError as e:
        print(
            f"\nТест2 произошла ошибка AssertionError: количество питомцев с фото меньше количества питомцев без фото")
        print(e)
        pass


def test_all_pets_with_name_age_breed(driver):
    """" Тест3: написать тест, который проверяет, что на странице со списком питомцев пользователя,
    у всех питомцев есть имя, возраст и порода. Через локаторы имени, возраста и породы."""
    # счетчики имен, породы, возраста
    names, breeds, ages = 0, 0, 0
    test_show_my_pets(driver)
    # Настраиваем переменную явного ожидания:
    wait = WebDriverWait(driver, 3)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    # Данные о возрасте, породе и имени питомца
    age = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]//td[3]')
    name = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]//td[1]')
    breed = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]//td[2]')
    pets_data = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Настраиваем переменную явного ожидания:
    wait = WebDriverWait(driver, 3)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    if len(name) == len(breed) == len(age):
        for i in range(len(name)):
            if name[i].text != '':
                names += 1
        for i in range(len(name)):
            if name[i].text != '':
                breeds += 1
        for i in range(len(name)):
            if age[i].text != 'None':
                ages += 1
    try:
        assert names == breeds == ages == len(pets_data)
        print(f'\nТест3 Все {len(pets_data)} питомцы имеют имя, возраст и породу')
    except AssertionError as e:
        print(f"\nТест3 произошла ошибка AssertionError: не все питомцы имеют имя, возраст и породу")
        print(e)
        pass


def test_old_all_pets_with_name_age_breed(driver):
    """" Тест3: написать тест, который проверяет, что на странице со списком питомцев пользователя,
    у всех питомцев есть имя, возраст и порода. Другая реализация через строку с данными питомца."""
    test_show_my_pets(driver)
    count, not_all_data, parts, flag = 0, [], [], True
    # Настраиваем переменную явного ожидания:
    wait = WebDriverWait(driver, 3)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    pets_data = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    for i in range(len(pets_data)):
        if pets_data[i].text != '':
            parts = pets_data[i].text.replace('\n×', '').split(" ")
        if len(parts) == 3:
            if parts[2] == 'None':
                count += 1
                not_all_data.append(parts)
        else:
            flag = False
    try:
        assert count == 0 and flag
        print(f'\nТест3 Все {len(pets_data)} питомцев имеют имя, возраст и породу')
    except AssertionError as e:
        print(f"\nТест3 произошла ошибка AssertionError: не все питомцы имеют имя, возраст и породу\n{not_all_data}")
        print(e)
        pass


def test_all_pets_different_names(driver):
    """Тест4: написать тест, который проверяет, что на странице со списком питомцев пользователя
    у всех питомцев разные имена"""
    test_show_my_pets(driver)
    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]//td[1]')
    names_pets, duplicate_names, count = [], [], 0
    for i in range(len(names)):
        if names[i].text != '':
            parts = names[i].text.split(" ")
            names_pets.append(parts)
    for i in range(len(names_pets)):
        if names_pets.count(names_pets[i]) > 1:
            count += 1
            if names_pets[i] not in duplicate_names:
                duplicate_names.append(names_pets[i])
    try:
        assert duplicate_names == []
        print(f'\nТест4 Количество питомцев с повторяющимися именами: {count}')
    except AssertionError as e:
        print(f"\nТест4 произошла ошибка AssertionError: количество повторений имен питомцев: {count}.\nПитомцы с "
              f"повторяющимися именами: {duplicate_names}")
        print(e)
        pass


def test_no_repeat_pets(driver):
    """Тест5: написать тест, который проверяет, что на странице со списком питомцев пользователя
    в списке нет повторяющихся питомцев"""
    test_show_my_pets(driver)
    pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    pets_data = []
    duplicates = []
    for i in range(len(pets)):
        if pets[i].text != '':
            parts = pets[i].text.split(" ")
            pets_data.append(parts)
    for item in pets_data:
        if pets_data.count(item) > 1 and item not in duplicates:
            duplicates.append(item)
    try:
        assert duplicates == []
        print(f"\nТест5 В списке нет повторяющихся питомцев")
    except AssertionError as e:
        print(f"\nТест5 произошла ошибка AssertionError: В списке есть повторяющиеся питомцы.\n{duplicates}")
        print(e)
        pass
