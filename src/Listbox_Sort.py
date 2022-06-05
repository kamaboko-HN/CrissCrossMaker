import tkinter as tk

def CCMsort(Listboxobject, sort_type, up_or_down):
    list_size = Listboxobject.size()
    if list_size > 0:
        word_list = []
        for ind in range(list_size):
            word_list.append(Listboxobject.get(ind))

        for ind in range(list_size):
            Listboxobject.delete(0)

        if sort_type == "alphabetical":
            sorted_word_list = sorted(word_list, key=lambda word: (len(word), word), reverse=up_or_down)
        elif sort_type == "stroke":
            sorted_word_list = sorted(word_list, reverse=up_or_down)

        for word in sorted_word_list:
            Listboxobject.insert(0, word)