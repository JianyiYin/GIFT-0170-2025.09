import random

with open("name_list.txt", "r") as file:
    names = file.readlines()

chosen_name = random.choice(names).strip()
print(chosen_name)