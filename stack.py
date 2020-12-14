from node import Node

class Data_climate:
    def __init__(self, ch, date, averange_temp, averange_temp_uncertain, country):
        self.ch = ch
        self.date = date                                #Data
        self.avg_temp = averange_temp                   #Temperatura média
        self.avg_temp_unc = averange_temp_uncertain     #Temperatura média incerta
        self.country = country                          #País
    #Imprime os atributos com limite de duas casas decimais para pontos flutuantes
    def __repr__(self):
        return "%d %s, %s, %.2f, %.2f" %(self.ch, self.country, self.date, self.avg_temp, self.avg_temp_unc)

class Stack:

    def __init__(self):
        self.top = None

    def isEmpty(self):
        if self.top == None:
            return True
        else:
            return False

    
    def push(self, elem):
        if not self.top:
            self.top = Node(elem)
        else:
            pointer = Node(elem)
            pointer.next = self.top
            self.top = pointer

    def pop(self):
        if not self.top:
            return None
        else:
            d = self.top.data
            self.top = self.top.next
            return d

    def peek(self):
        if not self.top:
            return None
        else:
            return self.top.data


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

class StackWindow:

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

        self.update_btn = tkinter.Button(self.bar_config_frame, text="Gerar", command=lambda: self.stack_generator())
        self.update_btn.pack(side="left")

        self.frame_results = tkinter.Frame(self.window)
        self.frame_results.pack(fill="x")

        self.lista_result = tkinter.Frame(self.frame_results)
        self.lista_result.pack(side="left")

        self.lista_result_text = tkinter.Text(self.lista_result, font="arial 15", width=30, height=20)
        self.lista_result_text.pack(side="left", pady=5, padx=5)

        self.show_frame = tkinter.Frame(self.frame_results)
        self.show_frame.pack()

        self.no_number_label = tkinter.Label(self.show_frame, text="Topo")
        self.no_number_label.pack(pady=3)

        self.action_button_frame = tkinter.Frame(self.show_frame)
        self.action_button_frame.pack()

        self.show_button = tkinter.Button(self.action_button_frame, text="Detalhes", command=lambda: self.top_details())
        self.show_button.pack(side="left", padx=3)

        self.pop_button = tkinter.Button(self.action_button_frame, text="Excluir", command=lambda: self.pop_stack())
        self.pop_button.pack(side="left")

        self.show_text = tkinter.Text(self.show_frame, width=29, height=16, font="arial 15")
        self.show_text.pack(pady=5)

        self.window.mainloop()

    def stack_show(self):
        p = pilha.top
        proximo = p
        if p:
            self.lista_result_text.configure(state="normal")
            self.lista_result_text.delete('1.0', tkinter.END)
            while proximo:
                self.lista_result_text.insert(tkinter.END, "{} - {}\n".format(proximo.data.ch, proximo.data.country))
                proximo = proximo.next

    def stack_generator(self):

        tam = int(self.num_nodes.get())
        #Cria um array com a permutação de valores de 0 a len(data)
        shuffled_indices = np.random.permutation(len(data))
        #Guarda os 100 primeiros valores da permutação
        index_arr = shuffled_indices[:tam]

        global pilha
        pilha = Stack()     #Cria a pilha
        c = 0
        for index in index_arr:
            d = data.iloc[index]    #Usa o índice aleatório do array como referência
            dados = Data_climate( c, d["dt"], d["AverageTemperature"], d["AverageTemperatureUncertainty"], d["Country"])
            pilha.push(dados)  #Armazena os dados na pilha
            c += 1
        
        self.stack_show()

    def top_details(self):
        
        no = pilha.peek()

        self.show_text.configure(state="normal")
        self.show_text.delete('1.0', tkinter.END)
        if no:
            self.show_text.insert(tkinter.END, "Chave: {}\n".format(no.ch))
            self.show_text.insert(tkinter.END, "Data: {}\n".format(no.date))
            self.show_text.insert(tkinter.END, "Temperatura Média: %.2f\n" %(no.avg_temp))
            self.show_text.insert(tkinter.END, "Margem: %.2f\n" %(no.avg_temp_unc))
            self.show_text.insert(tkinter.END, "País: {}\n".format(no.country))

    def pop_stack(self):
        pilha.pop()
        self.stack_show()
        self.show_text.delete('1.0', tkinter.END)
