import os
import time
from datetime import date

from selene import browser, have, be, by, query
from selene.core.command import js

from qa_guru_homework_9.registration_steps import RegistrationSteps
from qa_guru_homework_9.user import User


def test_fill_submit_form(setup_browser):
    student = User(
        first_name='Alex',
        last_name='Bagel',
        email='alexbagel@mail.ru',
        gender='Male',
        mobile_number='9021778990',
        date_of_birth=date(1990, 6, 19),
        subject='English',
        hobbies='Sports',
        picture=os.path.join(os.path.dirname(os.path.dirname(__file__)),'mount.jpg'),
        street_address='Lomonosov str. 8',
        state_address='Haryana',
        city_address='Panipat'
    )

    registration_steps = RegistrationSteps()
    registration_steps.open()
    registration_steps.register(student)
    registration_steps.should_have_registered(student)


    time.sleep(10)
