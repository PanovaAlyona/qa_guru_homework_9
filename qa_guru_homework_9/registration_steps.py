import os

from selene import browser, by, be, have, query
from selene.core.command import js

from qa_guru_homework_9.user import User
import calendar

class RegistrationSteps:
    def open(self):
        browser.open('https://demoqa.com/automation-practice-form')

        browser.driver.execute_script("""
                // Удаляем рекламные баннеры
                const banners = document.querySelectorAll('[id^="google_ads_iframe"], .ads, .ad, iframe');
                banners.forEach(banner => banner.remove());
                // Удаляем футер, если он мешает
                const footer = document.querySelector('footer');
                if (footer) footer.style.display = 'none';
                // Убираем фиксированные элементы
                const fixedElements = document.querySelectorAll('body > *');
                fixedElements.forEach(el => {
                    if (getComputedStyle(el).position === 'fixed') {
                        el.style.display = 'none';
                    }
                });
            """)

        browser.element(by.text('Practice Form')).should(be.visible)

    def register(self, user: User):
        # Заполняем основные данные
        browser.element('#firstName').type(user.first_name)
        browser.element('#lastName').type(user.last_name)
        browser.element('#userEmail').type(user.email)
        browser.element(by.text('Male')).click()
        browser.element('#userNumber').type(user.mobile_number)

        # Заполняем дату рождения
        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__month-select').type(calendar.month_name[user.date_of_birth.month])
        browser.element('.react-datepicker__year-select').type(user.date_of_birth.year)
        browser.element(f'.react-datepicker__day--0{user.date_of_birth.day}:not(.react-datepicker__day--outside-month)').click()

        # Выбираем предмет
        browser.element('#subjectsInput').type(user.subject)
        browser.element('.subjects-auto-complete__menu').with_(timeout=5).should(be.visible)
        browser.all('.subjects-auto-complete__option').first.click()

        # Выбираем хобби
        browser.element(by.text(user.hobbies)).click()

        # Загружаем файл
        browser.element('#uploadPicture').send_keys(user.picture)

        # Заполняем адрес
        browser.element('#currentAddress').type(user.street_address)
        browser.element('#submit').perform(js.scroll_into_view)

        browser.element('#state').click()
        browser.element('.css-26l3qy-menu').with_(timeout=5).should(be.visible)

        browser.element('.css-26l3qy-menu').element(
            by.text(user.state_address)
        ).click()

        browser.element('#city').click()
        browser.element('.css-26l3qy-menu').with_(timeout=5).should(be.visible)

        browser.element('.css-26l3qy-menu').element(
            by.text(user.city_address)
        ).click()

        # Отправляем форму
        browser.element('#submit').click()

    def should_have_registered(self, user: User):
        # Проверяем успешную отправку формы

        expected_data = {
            "Student Name": user.first_name + ' ' + user.last_name,
            "Student Email": user.email,
            "Gender": user.gender,
            "Mobile": user.mobile_number,
            "Date of Birth": user.date_of_birth.strftime("%d %B") +', ' + user.date_of_birth.strftime("%Y"),
            "Subjects": user.subject,
            "Hobbies": user.hobbies,
            "Picture": os.path.basename(user.picture),
            "Address": user.street_address,
            "State and City": user.state_address + ' ' + user.city_address
        }

        # Получаем все строки таблицы
        rows = browser.all('tbody tr')

        for row in rows:
            # Получаем ячейки в строке
            cells = row.all('td')
            if cells.should(have.size(2)):
                field_name = cells.first.get(query.text)
                actual_value = cells.second.get(query.text)

                # Проверяем, есть ли поле в ожидаемых данных
                if field_name in expected_data:
                    expected_value = expected_data[field_name]
                    assert actual_value == expected_value, (
                        f"Поле '{field_name}': ожидалось '{expected_value}', "
                        f"получено '{actual_value}'"
                    )
                    print(f"✓ {field_name}: {actual_value}")

