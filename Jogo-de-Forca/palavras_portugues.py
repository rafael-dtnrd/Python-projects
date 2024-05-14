#palavras.py
#Gerador de constante com lista de palavras em Português

word_list = list()

with open('palavras-sem-acentos.txt', encoding = 'latin1') as file:
    for word in file:
        word = word.rstrip()
        word = word.lower()
    
        if len(word) > 1:
            word_list.append(word)

PALAVRAS = word_list #Lista final de palavras


