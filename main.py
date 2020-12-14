from graph import GraphWindow
from lista import ListWindow
from stack import StackWindow
from tree import TreeWindow
from queue import QueueWindow

import tkinter

window = tkinter.Tk()
window.title("Estrutura de Dados")
window.geometry("320x350")
window.maxsize(width=320, height=400)

menu_frame = tkinter.Frame(window)
menu_frame.pack()

list_button = tkinter.Button(menu_frame, text="Lista", command=lambda: ListWindow(), width=60, height=3)
list_button.pack()

queue_button = tkinter.Button(menu_frame, text="Fila", command=lambda:QueueWindow(), width=60, height=3)
queue_button.pack()

stack_button = tkinter.Button(menu_frame, text="Pilha", command=lambda: StackWindow(), width=60, height=3)
stack_button.pack()

tree_button = tkinter.Button(menu_frame, text="Árvore", command=lambda: TreeWindow(), width=60, height=3)
tree_button.pack()

graph_button = tkinter.Button(menu_frame, text="Grafo", command=lambda: GraphWindow(), width=60, height=3)
graph_button.pack()

window.mainloop()