from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_string_validator.plugin import StringValidatorAction
import pytest
import random


@pytest.mark.email
def test_email():
    import random
    import string
    number = 0

    def random_char(char_num):
        return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))

    while not number == 10:
        a = random_char(12) + "@" + random_char(5) + "." + random_char(3)
        number += 1
        init = {'validation_name': "email",
                'data': a}
        payload = {}
        klass = run_plugin(StringValidatorAction, init, payload)
        if klass.output.value:
            assert True
        else:
            assert False


def test_url():
    init = {'validation_name': "url",
            'data': f"https://www.polska.com/api/e/w/2"}
    klass = run_plugin(StringValidatorAction, init, {})
    if klass.output.value:
        assert True
    else:
        assert False



@pytest.mark.date
def test_date():
    a = 0
    while not a == 1000:
        c = random.randint(1, 12)
        if c == 2:
            b = random.randint(1, 28)
        else:
            b = random.randint(1, 30)
        d = random.randint(1600, 2021)
        a += 1
        init = {'validation_name': "date",
                'data': f"{b}-{c}-{d}"}
        klass = run_plugin(StringValidatorAction, init, {})
        if klass.output.value:
            assert True
        else:
            assert False


def test_int():
    a = 0
    while not a == 1000:
        c = random.randint(1, 100000)
        a += 1
        init = {'validation_name': "int",
                'data': c}
        klass = run_plugin(StringValidatorAction, init, {})
        if klass.output.value:
            assert True
        else:
            assert False


def test_float():
    a = 0
    while not a == 1000:
        c = random.uniform(1.0, 100000.0)
        a += 1
        init = {'validation_name': "float",
                'data': c}
        klass = run_plugin(StringValidatorAction, init, {})
        if klass.output.value:
            assert True
        else:
            assert False


def test_timer():
    a = 0
    while not a == 1000:
        c = random.randint(1, 23)
        d = random.randint(1, 59)
        if d < 10:
            d = "0" + str(d)

        a += 1
        init = {'validation_name': "time",
                'data': f"{c}:{d}"}
        klass = run_plugin(StringValidatorAction, init, {})
        if klass.output.value:
            assert True
        else:
            assert False


def test_ean():
    a = "5901234123457"
    init = {'validation_name': "ean",
            'data': a}
    klass = run_plugin(StringValidatorAction, init, {})
    if klass.output.value:
        assert True
    else:
        assert False


def test_number_phone():
    a = 0
    while not a == 1000:
        d = random.randint(1, 999)
        if d<10:
            d = '+0' + str(d)
        else:
            d = '+' + str(d)

        c = random.randint(1000000, 999999999)
        a += 1
        init = {'validation_name': "number_phone",
                'data': f"{d}{c}"}
        klass = run_plugin(StringValidatorAction, init, {})
        if klass.output.value:
            assert True
        else:
            print(init)
            assert False


@pytest.mark.ip
def test_ip():
    a = 0
    while not a == 1000:
        b = random.randint(1, 255)
        c = random.randint(1, 255)
        d = random.randint(1, 255)
        e = random.randint(1, 255)
        a += 1
        init = {'validation_name': "ipv4",
                'data': f"{b}.{c}.{d}.{e}"}
        klass = run_plugin(StringValidatorAction, init, {})
        if klass.output.value:
            assert True
        else:
            assert False

