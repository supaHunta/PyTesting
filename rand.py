import email
import random 
import string

def generate_random_email(length):
  allSymbols = string.ascii_uppercase + string.digits
  result =''.join(random.choice(allSymbols) for i in range(length))+"@yandex.ru"
  return result

def generate_random_wrong_email(length):
  allSymbols = string.ascii_uppercase + string.digits
  result =''.join(random.choice(allSymbols) for i in range(length))
  return result + "@"
