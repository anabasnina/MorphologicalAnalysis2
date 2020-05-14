# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox


def read_file():
    """
    Open the selected file and read it.
    :return: list with correct words
    """
    with open(file_name, 'r') as file:
        all_words = file.read()
        list_word = all_words.split(', ')
        return list_word


def get_errors(list_word, incorrect_word):
    """
    Call function 'distance'.
    :param list_word: list with correct words
    :param incorrect_word: word to check
    :return: dictionary with words and errors
    """
    dict_words_and_errors = {}
    for word in list_word:
        errors = distance(incorrect_word.lower(), word.lower())
        dict_words_and_errors.update({word: errors})
    return dict_words_and_errors


def sort_list(dict_words_and_errors):
    """
    Sorted dictionary.
    :param dict_words_and_errors: dictionary with words and errors
    :return: sorted list with words and errors
    """
    list_with_tuple = list(dict_words_and_errors.items())
    list_with_tuple.sort(key=lambda i: i[1])
    return list_with_tuple


def show_result(sorted_list, count_errors):
    """
    Reading and output to UI.
    :param sorted_list: sorted list with words and errors
    :param count_errors: number of permissible errors
    :return: view on UI
    """
    for word in sorted_list[::-1]:
        if int(word[1]) < int(count_errors) + 1:
            list_box.insert(0, str(word[0]) + ' ' + str(word[1]))


def distance(a, b):
    """
    Calculates the Levenshtein distance between a and b.
    :param a: first word
    :param b: second word
    :return: count errors
    """
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def get_filename():
    """
    :return: name open file
    """
    global file_name
    file_name = fd.askopenfilename(filetypes=(("Doc files", "*.doc"),))


file_name = ''


def implementation():
    """
    The main function to call other functions.
    :return: performance of functions
    """
    if file_name != '':
        incorrect_word = calculated_text.get(1.0, END)
        incorrect_word = incorrect_word.replace('\n', '')
        count_errors = calculated_text2.get(1.0, END)
        count_errors = count_errors.replace('\n', '')
        if count_errors != '' and incorrect_word != '':
            list_box.delete(0, END)
            list_word = read_file()
            dict_words_and_errors = get_errors(list_word, incorrect_word)
            sorted_list = sort_list(dict_words_and_errors)
            show_result(sorted_list, count_errors)


def info():
    """
    :return: help for user
    """
    messagebox.askquestion("Помощь?", "1. Открыть файл  с правильными словами.\n"
                                      "2. Написать в первой строке неправильное слово.\n"
                                      "3. Написать во второй строке количество допустимых ошибок.\n"
                                      "4. Снизу увидите упорядоченный список с вариантами.", type='ok')


root = Tk()
root.title("Textedit ")
root.resizable(width=False, height=False)
# root.geometry("480x250+300+300")
label = Label(root, text='Неправильное слово:')
label.grid(row=1, column=0)
calculated_text = Text(root, height=1, width=20)
calculated_text.grid(row=1, column=1, sticky='nsew', columnspan=4)
label2 = Label(root, text='Количество ошибок:')
label2.grid(row=3, column=0)
calculated_text2 = Text(root, height=1, width=5)
calculated_text2.grid(row=3, column=1, sticky='nsew')

b1 = Button(text="Готово", command=implementation, width=10)
b1.grid(row=3, column=2)
b2 = Button(text="Открыть файл", command=get_filename)
b2.grid(row=3, column=3)
b2 = Button(text="Помощь?", command=info, width=10)
b2.grid(row=3, column=4)
list_box = Listbox(root, height=10, width=65)
scrollbar = Scrollbar(root, command=list_box.yview)
scrollbar.grid(row=4, column=5, sticky='nsew')
list_box.grid(row=4, column=0, sticky='nsew', columnspan=5)
list_box.configure(yscrollcommand=scrollbar.set)
root.mainloop()
