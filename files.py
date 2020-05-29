with open('referat.txt', 'r', encoding = 'utf-8') as f:
    my_text = f.read()
    text_length = len(my_text)
    print(text_length)
    words = my_text.split()
    print(len(words))
    my_text2 = my_text.replace('.','!')
    print(my_text2)
    with open('referat2.txt', 'w', encoding='utf-8') as f:
        f.write(my_text2)
    