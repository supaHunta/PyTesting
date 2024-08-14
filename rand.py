
import random 
import string


def generate_random_email(length):
    '''
    This function generates random E-Mail address
    '''
    all_symbols = string.ascii_uppercase + string.digits
    result =''.join(random.choice(all_symbols) for i in range(length))+"@yandex.ru"
    return result

def generate_random_wrong_email(length):
    '''
    This function generates random E-Mail address without a domain (ex.yandex.ru)
    '''
    all_symbols = string.ascii_uppercase + string.digits
    result =''.join(random.choice(all_symbols) for i in range(length))
    return result + "@"
