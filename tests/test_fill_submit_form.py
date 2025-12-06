from qa_guru_homework_9.pages.registration_page import RegistrationPage


def test_fill_submit_form(setup_browser):
    registration_page = RegistrationPage()
    registration_page.open()

# Заполняем основные данные
    registration_page.type_first_name('Alex')
    registration_page.type_last_name('Bagel')
    registration_page.type_user_email('alexbagel@mail.ru')
    registration_page.check_male('Male')
    registration_page.type_user_number('9021778990')

# Заполняем дату рождения
    registration_page.type_date_of_birth('1990', 'Jun', 19)

# Выбираем предмет
    registration_page.check_subject('English')

# Выбираем хобби
    registration_page.check_hobbie('Sports')

# Загружаем файл
    registration_page.upload_picture('mount.jpg')

# Заполняем адрес
    registration_page.type_street_address('Lomonosov str. 8')

    registration_page.check_state_address('Haryana')

    registration_page.check_city_address('Panipat')

# Отправляем форму
    registration_page.submit_form()

# Проверяем успешную отправку формы
    registration_page.should_registered_user_info({
        "Student Name": "Alex Bagel",
        "Student Email": "alexbagel@mail.ru",
        "Gender": "Male",
        "Mobile": "9021778990",
        "Date of Birth": "19 June,1990",
        "Subjects": "English",
        "Hobbies": "Sports",
        "Picture": "mount.jpg",
        "Address": "Lomonosov str. 8",
        "State and City": "Haryana Panipat"
    }
    )



