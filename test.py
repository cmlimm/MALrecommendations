from tkinter import *

root = Tk()

check_var = IntVar()

label_state = Label(root, text='Состояние: ' + str(check_var.get()))

check = Checkbutton(root, text='Текст', variable=check_var)

check.pack()
label_state.pack()


def on_change(*args):
    label_state.config(text='Состояние: ' + str(check_var.get()))

check_var.trace('w', on_change)  # Следим за состоянием переменной, при изменении выполняем функцию


Button(root, text='Включить', command=lambda : check_var.set(1)).pack()
Button(root, text='Выключить', command=lambda : check_var.set(0)).pack()

mainloop()
