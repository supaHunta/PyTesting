import os
import random

root = '/Users/fusion_tech/Desktop/FOTKI_NAFIG/'
random_file = None
files_list = []


for items in os.listdir(root):
    if not items.startswith('.'):
        files_list.append(items)  

def get_a_random_file():
    random_file = random.choice(files_list)
    return root+random_file

print(get_a_random_file())