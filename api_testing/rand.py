import random
import string


def generate_random_email(length):
    """
    Generates a random e-mail with a given lenght
    """
    all_symbols = string.ascii_uppercase + string.digits
    result = ''.join(random.choice(all_symbols)
                     for i in range(length))+"@yandex.ru"
    return result


def generate_random_wrong_email(length):
    '''
    Generates random bunch of symbols with a "@" on the end
    '''
    all_symbols = string.ascii_uppercase + string.digits
    result = ''.join(random.choice(all_symbols) for i in range(length))
    return result + "@"
