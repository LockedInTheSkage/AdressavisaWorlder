import re

input_file = "fullformsliste.txt"
output_file = "third_words.txt"

with open(input_file, "r", encoding="latin-1") as file:
    lines = file.readlines()

third_words = [line.split()[2] for line in lines if re.match(r'^[a-zA-ZæøåÆØÅ]{5}$', line.split()[2])]

with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(third_words))