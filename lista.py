class Node:

    def __init__(self, data):
        self.data = data
        self.next = None

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

class LinkedList:

    def __init__(self):
        self.head = None

    # adiciona no final da lista
    def append(self, elem):
        if self.head:
            pointer = self.head
            while(pointer.next):
                pointer = pointer.next
            pointer.next = Node(elem)
        # primeira insercao
        else:
            self.head = Node(elem)

    # adiciona no inicio da lista
    def insert(self, elem):
        # primeira insercao
        if not self.head:
            self.head = Node(elem)
        else:
            pointer = Node(elem)
            pointer.next = self.head
            self.head = pointer


    def show(self):
        pointer = self.head
        while(pointer):
            print(pointer.data)
            pointer = pointer.next


    def search(self, ch):
        pointer = self.head
        while(pointer):
            if pointer.data.ch == ch:
                return pointer
                break
            else:
                pointer = pointer.next
        if not pointer:
            return None

    def showNode(self, ch):
        pointer = self.search(ch)
        if pointer:
            return pointer.data
        else:
            print("NAO ENCONTRAMOS DADOS COM ESSA CHAVE!")


    def edit(self, ch, d):
        pointer = self.search(ch)
        if pointer:
            pointer.data = Data_climate(index ,d["dt"], d["AverageTemperature"], d["AverageTemperatureUncertainty"], d["Country"])
        else:
            print("NAO ENCONTRAMOS DADOS COM ESSA CHAVE!")


    def remove(self, ch):
        if self.head.data.ch == ch:
            self.head = self.head.next
        else:
            previous = self.head
            current = previous.next

            while(current):
                if current.data.ch == ch:
                    previous.next = current.next
                    break
                previous = current
                current = previous.next



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

class ListWindow:

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

        self.update_btn = tkinter.Button(self.bar_config_frame, text="Gerar", command=lambda: self.lista_generator())
        self.update_btn.pack(side="left")

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

        self.options_buttons_frame = tkinter.Frame(self.show_frame)
        self.options_buttons_frame.pack()

        self.show_button = tkinter.Button(self.options_buttons_frame, text="Detalhes", command=lambda: self.ch_details())
        self.show_button.pack(pady=2, side="left")

        self.pop_button = tkinter.Button(self.options_buttons_frame, text="Excluir", command=lambda: self.pop_list())
        self.pop_button.pack(side="left")

        self.show_text = tkinter.Text(self.show_frame, width=29, height=16, font="arial 15")
        self.show_text.pack(pady=5)

        self.window.mainloop()

    def lista_generator(self):
        shuffled_indices = np.random.permutation(len(data))
        tam = int(self.num_nodes.get())
        index_arr = shuffled_indices[:tam]
        global lista
        lista = LinkedList()     #Cria a lista
        c = 0
        for index in index_arr:
            d = data.iloc[index]    #Usa o índice aleatório do array como referência
            dados = Data_climate(c ,d["dt"], d["AverageTemperature"], d["AverageTemperatureUncertainty"], d["Country"])
            lista.insert(dados)  #Armazena os dados na última posição da lista
            c += 1
        self.lista_show()
    
    def lista_show(self):
        self.lista_result_text.configure(state="normal")
        self.lista_result_text.delete('1.0', tkinter.END)
        pointer = lista.head
        while(pointer):
            self.lista_result_text.insert(tkinter.INSERT, "{} - {}\n".format(pointer.data.ch, pointer.data.country))
            pointer = pointer.next

    def ch_details(self):
        ch = int(self.ch_textbox.get())
        no = lista.showNode(ch)
        self.show_text.configure(state="normal")
        self.show_text.delete('1.0', tkinter.END)
        if no:
            self.show_text.insert(tkinter.END, "Chave: {}\n".format(no.ch))
            self.show_text.insert(tkinter.END, "Data: {}\n".format(no.date))
            self.show_text.insert(tkinter.END, "Temperatura Média: %.2f\n" %(no.avg_temp))
            self.show_text.insert(tkinter.END, "Margem: %.2f\n" %(no.avg_temp_unc))
            self.show_text.insert(tkinter.END, "País: {}\n".format(no.country))
        else: 
            self.show_text.insert(tkinter.END, "Chave não encontrada")

    def pop_list(self):
        ch = int(self.ch_textbox.get())
        lista.remove(ch)
        self.lista_show()


    
