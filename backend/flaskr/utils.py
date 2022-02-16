import hashlib
import re


def string_md5(s: str):
    return hashlib.md5(s.encode()).hexdigest()


def validate_username(username):
    if not (5 <= len(username) <= 20):
        return False
    if re.search("[^A-Za-z0-9]", username):
        return False
    return True


def validate_email(email):
    if not email:
        return False
    return re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None


def validate_password(password):
    if not password:
        return False
    if not (8 <= len(password) <= 20):
        print('length', password)
        return False
    if not re.search("[A-Z]", password):
        print('capital', password)
        return False
    if not re.search("[a-z]", password):
        print('lower', password)
        return False
    if not re.search("[^A-Za-z0-9_\f\n\r\t\v]", password):
        print('specila', password)
        return False
    return True


if __name__ == '__main__':
    print(string_md5('test_md5'))
    print(validate_email('asd@qq.com'))
    print(validate_email('asdqq.com'))
    print(validate_email('asdqq.com@'))
    print(validate_email('asd@qq.abc.com'))
    print('validate_password')
    print(1,validate_password('ssssssss'))
    print(2,validate_password('AAAAAAAA'))
    print(3,validate_password('AAAAssss'))
    print(4,validate_password('AAss123$'))
    print(validate_password('AAss123$12345678901234567890'))
    print(validate_password('AAss12$'))
    print(7, validate_password('AAss123_'))
    print('username')
    print(validate_username('1234'))
    print(validate_username('12345678901234567890123sds'))
    print(validate_username('12345678901234567890_'))
    print(validate_username('1234sadf$'))
    print(validate_username('1234sadf'))

