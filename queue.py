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


class Queue:

    def __init__(self):
        self.first = None
        self.last = None

    def isEmpty(self):
        if self.first == None:
            return True
        return False

    def enqueue(self, elem):
        pointer = Node(elem)
        if self.first == None:
            self.first = pointer
            self.last = pointer
        else:
            self.last.next = pointer
            self.last = self.last.next

    def dequeue(self):
        if self.first == None:
            return None
        
        d = self.first.data
        self.first = self.first.next

        if self.first == None:
            self.last = None

        return d

    def peek(self):
        if self.first == None:
            return None

        return self.first.data


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

class QueueWindow:

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Lista")
        self.window.geometry("690x550")
        self.window.maxsize(width=690, height=720)

        self.bar_config_frame = tkinter.Frame(self.window, height=30)
        self.bar_config_frame.pack(fill='x', pady=3)

        self.lista_tam = tkinter.Label(self.bar_config_frame, text="Nº de elementos: ")
        self.lista_tam.pack(side="left", padx=5)

        self.num_nodes = tkinter.Spinbox(self.bar_config_frame, from_=1, to=100)
        self.num_nodes.pack(side="left")

        self.frame_results = tkinter.Frame(self.window)
        self.frame_results.pack(fill="x")

        self.lista_result = tkinter.Frame(self.frame_results)
        self.lista_result.pack(side="left")

        self.queue_options_frame = tkinter.Frame(self.lista_result)
        self.queue_options_frame.pack(fill="x")
        
        self.create_queue_button = tkinter.Button(self.queue_options_frame, text="Gerar", command=lambda: self.queue_generator())
        self.create_queue_button.pack(side="left", padx=3)

        self.pop_button = tkinter.Button(self.queue_options_frame, text="Excluir", command=lambda: self.pop_queue())
        self.pop_button.pack(side="left", padx=3)

        self.lista_result_text = tkinter.Text(self.lista_result, font="arial 15", width=30, height=20)
        self.lista_result_text.pack(pady=5, padx=5)

        self.show_frame = tkinter.Frame(self.frame_results)
        self.show_frame.pack()

        self.no_number_label = tkinter.Label(self.show_frame, text="Detalhes")
        self.no_number_label.pack(pady=3)

        self.action_button_frame = tkinter.Frame(self.show_frame)
        self.action_button_frame.pack()

        self.first_show_button = tkinter.Button(self.action_button_frame, text="Primeiro", command=lambda: self.first_show())
        self.first_show_button.pack(side="left", padx=3)

        self.last_show_button= tkinter.Button(self.action_button_frame, text="Último", command=lambda: self.last_show())
        self.last_show_button.pack(side="left")

        self.show_text = tkinter.Text(self.show_frame, width=29, height=16, font="arial 15")
        self.show_text.pack(pady=5)

        self.window.mainloop()

    def queue_generator(self):

        #Cria um array com a permutação de valores de 0 a len(data)
        shuffled_indices = np.random.permutation(len(data))
        #Guarda os 100 primeiros valores da permutação
        tam = int(self.num_nodes.get())
        index_arr = shuffled_indices[:tam]

        global fila
        fila = Queue()     #Cria a fila
        c = 0
        for index in index_arr:
            d = data.iloc[index]    #Usa o índice aleatório do array como referência
            dados = Data_climate(c, d["dt"], d["AverageTemperature"], d["AverageTemperatureUncertainty"], d["Country"])
            fila.enqueue(dados)  #Armazena os dados na fila
            c = c+1

        self.lista_result_text.configure(state="normal")
        self.lista_result_text.delete('1.0', tkinter.END)
        self.queue_show(fila.first)
    
    def queue_show(self, p):
        while p:
            self.lista_result_text.insert(tkinter.END, "{} - {}\n".format(p.data.ch, p.data.country))
            p = p.next


    def first_show(self):
        self.show_text.configure(state="normal")
        self.show_text.delete('1.0', tkinter.END)
        no = fila.first
        if no:
            self.show_text.insert(tkinter.END, "Chave: {}\n".format(no.data.ch))
            self.show_text.insert(tkinter.END, "Data: {}\n".format(no.data.date))
            self.show_text.insert(tkinter.END, "Temperatura Média: %.2f\n" %(no.data.avg_temp))
            self.show_text.insert(tkinter.END, "Margem: %.2f\n" %(no.data.avg_temp_unc))
            self.show_text.insert(tkinter.END, "País: {}\n".format(no.data.country))
    
    def last_show(self):
        self.show_text.configure(state="normal")
        self.show_text.delete('1.0', tkinter.END)
        no = fila.last
        if no:
            self.show_text.insert(tkinter.END, "Chave: {}\n".format(no.data.ch))
            self.show_text.insert(tkinter.END, "Data: {}\n".format(no.data.date))
            self.show_text.insert(tkinter.END, "Temperatura Média: %.2f\n" %(no.data.avg_temp))
            self.show_text.insert(tkinter.END, "Margem: %.2f\n" %(no.data.avg_temp_unc))
            self.show_text.insert(tkinter.END, "País: {}\n".format(no.data.country))
    
    def pop_queue(self):
        fila.first = fila.first.next
        self.lista_result_text.configure(state="normal")
        self.lista_result_text.delete('1.0', tkinter.END)
        self.queue_show(fila.first)