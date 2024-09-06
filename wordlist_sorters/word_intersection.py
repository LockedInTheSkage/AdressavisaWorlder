# Read words from ordliste.txt
with open('ordliste.txt', 'r') as file1:
    words1 = set(file1.read().split())

# Read words from third_words.txt
with open('third_words.txt', 'r') as file2:
    words2 = set(file2.read().split())

# Find common words
common_words = words1.intersection(words2)

# Write common words to common_words.txt
with open('common_words.txt', 'w') as output_file:
    output_file.write('\n'.join(common_words))