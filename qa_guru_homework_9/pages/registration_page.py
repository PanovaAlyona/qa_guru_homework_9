import time

from selene import browser, by, be, have, query
from selene.core.command import js

from qa_guru_homework_9 import resource


class RegistrationPage:
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

        browser.element(by.text('Practice Form')).should(be.visible)  # Ждем заголовок

    def type_first_name(self, value):
        browser.element('#firstName').type(value)

    def type_date_of_birth(self, year, month, day):
        browser.element('#dateOfBirthInput').click()
        browser.element('.react-datepicker__month-select').type(month)
        browser.element('.react-datepicker__year-select').type(year)
        browser.element(f'.react-datepicker__day--0{day}:not(.react-datepicker__day--outside-month)').click()

    def type_last_name(self, value):
        browser.element('#lastName').type(value)

    def type_user_email(self, value):
        browser.element('#userEmail').type(value)

    def check_male(self, value):
        browser.element(by.text(value)).click()

    def type_user_number(self, value):
        browser.element('#userNumber').type(value)

    def check_subject(self, value):
        browser.element('#subjectsInput').type(value)
        browser.element('.subjects-auto-complete__menu').with_(timeout=5).should(be.visible)
        browser.all('.subjects-auto-complete__option').first.click()

    def check_hobbie(self, value):
        browser.element(by.text(value)).click()

    def upload_picture(self, picture):
        browser.element('#uploadPicture').send_keys(resource.path(picture))

    def type_street_address(self, value):
        browser.element('#currentAddress').type(value)
        browser.element('#submit').perform(js.scroll_into_view)

    def check_state_address(self, value):
        browser.element('#state').click()
        browser.element('.css-26l3qy-menu').with_(timeout=5).should(be.visible)

        browser.element('.css-26l3qy-menu').element(
            by.text(value)
        ).click()

    def check_city_address(self, value):
        browser.element('#city').click()
        browser.element('.css-26l3qy-menu').with_(timeout=5).should(be.visible)

        browser.element('.css-26l3qy-menu').element(
            by.text(value)
        ).click()

    def submit_form(self):
        browser.element('#submit').click()

    def should_registered_user_info(self, expected_data: dict):
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
        time.sleep(10)
