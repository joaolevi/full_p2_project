#! /usr/bin/python3

class Node:

    def __init__(self, data):

        self.data = data
        self.left = None
        self.right = None


class Data_climate:
    def __init__(self, ch, date, averange_temp, averange_temp_uncertain, country):
        self.ch = ch
        self.date = date                               #Data
        self.avg_temp = averange_temp                   #Temperatura média
        self.avg_temp_unc = averange_temp_uncertain     #Temperatura média incerta
        self.country = country                          #País
    #Imprime os atributos com limite de duas casas decimais para pontos flutuantes
    def __repr__(self):
        return "%d %s, %s, %.2f, %.2f" %(self.ch, self.country, self.date, self.avg_temp, self.avg_temp_unc)


class Tree:

    def __init__(self):
        self.root = None


    def isEmpty(self):
        if self.root == None:
            return True
        return False


    def printInOrder(self, root):
        if root != None:
            self.printInOrder(root.left)
            print(root.data)
            self.printInOrder(root.right)
    

    def add(self, elem):
        if self.root == None:
            self.root = Node(elem)
            return
        
        nodeAux = self.root
        nodeParentAux = None
        
        while(nodeAux):
            nodeParentAux = nodeAux
            if nodeAux.data.ch < elem.ch:
                nodeAux = nodeAux.right
            elif nodeAux.data.ch > elem.ch:
                nodeAux = nodeAux.left

        if nodeParentAux.data.ch < elem.ch:
            nodeParentAux.right = Node(elem)
        else:
            nodeParentAux.left = Node(elem)

    def min(self, node = "root"):
        if node == "root":
            node = self.root
        while node.left:
            node = node.left
        return node.data

    def max(self, node = "root"):
        if node == "root":
            node = self.root
        while node.right:
            node = node.right
        return node.data

    def remove(self, value, node = "root"):
        if node == "root":
            node = self.root
        
        if node == None:
            return None
        elif value > node.data.ch:
            node.right = self.remove(value, node.right)
        elif value < node.data.ch:
            node.left = self.remove(value, node.left)
        else:
            if node.right == None:
                return node.left
            elif node.left == None:
                return node.right
            else:
                substitute = self.min(node.right)
                node.data = substitute
                node.right = self.remove(substitute.ch, node.right)

        return node 
        

###############################
## Leitura dos dados com Pandas lib
###############################
import pandas as pd
import numpy as np
import os

#Localiza o arquivo de acordo com o OS
datapath = os.path.join("dataset", "")
data = pd.read_csv(datapath + "GlobalLandTemperaturesByCountry.csv")

import tkinter

class TreeWindow:

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Lista")
        self.window.geometry("690x550")
        self.window.maxsize(width=690, height=720)

        self.bar_config_frame = tkinter.Frame(self.window, height=30)
        self.bar_config_frame.pack(fill='x')

        self.lista_tam = tkinter.Label(self.bar_config_frame, text="Nº de elementos: ")
        self.lista_tam.pack(side="left")

        self.num_nodes = tkinter.Spinbox(self.bar_config_frame, from_=1, to=100)
        self.num_nodes.pack(side="left")

        self.upch_btn = tkinter.Button(self.bar_config_frame, text="Gerar", command=lambda: self.tree_generator())
        self.upch_btn.pack(side="left")

        self.frame_results = tkinter.Frame(self.window)
        self.frame_results.pack(fill="x")

        self.lista_result = tkinter.Frame(self.frame_results)
        self.lista_result.pack(side="left")

        self.lista_result_text = tkinter.Text(self.lista_result, font="arial 15", width=30, height=20)
        self.lista_result_text.pack(side="left", pady=5, padx=5)

        self.show_frame = tkinter.Frame(self.frame_results)
        self.show_frame.pack()

        self.no_number_label = tkinter.Label(self.show_frame, text="Chave: ")
        self.no_number_label.pack(pady=3)

        self.ch_textbox = tkinter.Entry(self.show_frame)
        self.ch_textbox.pack()

        self.options_frame = tkinter.Frame(self.show_frame)
        self.options_frame.pack()

        self.show_button = tkinter.Button(self.options_frame, text="Detalhes", command=lambda: self.show_node(int(self.ch_textbox.get()), arvore.root))
        self.show_button.pack(pady=2, padx=3, side="left")

        self.pop_button = tkinter.Button(self.options_frame, text="Exlcuir", command=lambda: self.remove_node())
        self.pop_button.pack(pady=2)

        self.show_text = tkinter.Text(self.show_frame, width=29, height=16, font="arial 15")
        self.show_text.pack(pady=5)

        self.window.mainloop()

    def tree_generator(self):

        #Cria um array com a permutação de valores de 0 a len(data)
        tam = int(self.num_nodes.get())
        shuffled_indices = np.random.permutation(len(data))
        index_arr = shuffled_indices[:tam]

        global arvore
        arvore = Tree()     #Cria a arvore
        for index in index_arr:
            d = data.iloc[index]    #Usa o índice aleatório do array como referência
            dados = Data_climate(index ,d["dt"], d["AverageTemperature"], d["AverageTemperatureUncertainty"], d["Country"])
            arvore.add(dados)  #Armazena os dados na arvore

        self.lista_result_text.configure(state="normal")
        self.lista_result_text.delete('1.0', tkinter.END)

        self.tree_show_recursion(arvore.root)

    def tree_show_recursion(self, root):

        if root != None:
            self.tree_show_recursion(root.left)
            self.lista_result_text.insert(tkinter.END, "{} - {}\n".format(root.data.ch, root.data.country))
            self.tree_show_recursion(root.right)

    def show_node(self, ch, root):

        if root:
            if root.data.ch == ch:
                self.show_text.configure(state="normal")
                self.show_text.delete('1.0', tkinter.END)
                self.show_text.insert(tkinter.END, "Chave: {}\n".format(root.data.ch))
                self.show_text.insert(tkinter.END, "Data: {}\n".format(root.data.date))
                self.show_text.insert(tkinter.END, "Temperatura Média: %.2f\n" %(root.data.avg_temp))
                self.show_text.insert(tkinter.END, "Margem: %.2f\n" %(root.data.avg_temp_unc))
                self.show_text.insert(tkinter.END, "País: {}\n".format(root.data.country))
                return None
            self.show_node(ch, root.left)
            self.show_node(ch, root.right)

    def remove_node(self):
        ch = int(self.ch_textbox.get())
        arvore.remove(ch)
        self.lista_result_text.configure(state="normal")
        self.lista_result_text.delete('1.0', tkinter.END)
        self.show_text.configure(state="normal")
        self.show_text.delete('1.0', tkinter.END)
        self.tree_show_recursion(arvore.root)
        




    