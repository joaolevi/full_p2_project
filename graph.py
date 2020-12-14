###########################
## Nó
###########################

class Twitter:
    def __init__(self, ch, name, followers, country):
        self.ch = ch                    #id
        self.user_name = name           #nome
        self.followers = followers      #seguidores
        self.country = country          #país
        self.explored = False

    #Imprime os atributos
    def __repr__(self):
        return "%i: %s" %(self.ch, self.user_name)

###########################
## Grafo
###########################

from collections import defaultdict

class Graph():

    #Inicializa o grafo
    #Por padrão "não-dirigido" ou "directed=False" 
    def __init__(self, connections, edges, directed=False):
        self._graph = [[] for _ in range(edges)]
        self._directed = directed
        self.add_connections(connections)

    #Através de uma lista tuplas de pares cria as conexões
    def add_connections(self, connections):
    
        for node1, node2 in connections:
            self.add(node1, node2)

    #Adiciona uma conexão entre dois nós
    def add(self, node1, node2):
        
        if node1 == node2:
            return None
        if node2 in self._graph[node1.ch]:
            return None
        self._graph[node1.ch].append(node2)
        if not self._directed:
            self._graph[node2.ch].append(node1)

    #Encontra o caminho de conexão entre dois nós
    def explore(self, node1, node2, path=[]):
        node1.explored = True
        path = path+[node1]
        if node1.ch == node2.ch:
            return path
        for n in self._graph[node1.ch]:
            if not n.explored:
                new_path = self.explore(n, node2, path)
                if new_path:
                    return new_path
        return None

    def dfs(self, node1, node2, main):
        for v in self._graph:
            for w in v:
                w.explored = False
        main.explored = True
        path = self.explore(node1, node2)
        return path

    #Impressão do grafo
    def __str__(self):
        return self._graph

###############################
## Leitura dos dados com Pandas lib
###############################

import pandas as pd
import os
import numpy as np

#Localiza o arquivo de acordo com o OS
datapath = os.path.join("dataset", "")
#Lê o arquivo .csv selecionando as colunas desejadas
data = pd.read_csv(datapath + "hashtag_joebiden.csv", usecols=[5,6,8,11,16])
#Exclui dados com atributos faltantes(NaN)
data = data.dropna(subset=["user_screen_name"])




#########################
##  Interface gráfica com Tkinter
#########################

import tkinter

class GraphWindow:

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Grafos")
        self.window.geometry("690x720")
        self.window.maxsize(width=690, height=720)

        self.bar_config_frame = tkinter.Frame(self.window, height=30)
        self.bar_config_frame.pack(fill='x')

        self.num_nodes_label = tkinter.Label(self.bar_config_frame, text="Nº de Nós: ")
        self.num_nodes_label.pack(side="left")

        self.num_nodes = tkinter.Spinbox(self.bar_config_frame, from_=1, to=20)
        self.num_nodes.pack(side="left")

        self.num_connections_label = tkinter.Label(self.bar_config_frame, text="Nº conexões: ")
        self.num_connections_label.pack(side="left")

        self.num_connections = tkinter.Spinbox(self.bar_config_frame, from_=1, to=20)
        self.num_connections.pack(side="left")

        self.update_btn = tkinter.Button(self.bar_config_frame, text="Gerar", command=lambda: self.graph_generator())
        self.update_btn.pack(side="left")

        self.frame_results = tkinter.Frame(self.window)
        self.frame_results.pack(fill="x")

        self.graph_result_frame = tkinter.Frame(self.frame_results)
        self.graph_result_frame.pack(side="left")

        self.graph_result_text = tkinter.Text(self.graph_result_frame, font="arial 15", width=30, height=80)
        self.graph_result_text.pack(side="left")

        self.frame_names = tkinter.Frame(self.frame_results, padx=10)
        self.frame_names.pack(side="left")

        self.name1_frame = tkinter.Frame(self.frame_names)
        self.name1_frame.pack()

        self.node_name1 = tkinter.Label(self.name1_frame, text="Primeiro nó: ")
        self.node_name1.pack(side="left")

        self.screen_node_name1 = tkinter.Entry(self.name1_frame, font='arial 15')
        self.screen_node_name1.pack(side="left")

        self.name2_frame = tkinter.Frame(self.frame_names, pady=5)
        self.name2_frame.pack()

        self.node_name2 = tkinter.Label(self.name2_frame, text="Segundo nó: ")
        self.node_name2.pack(side="left")

        self.screen_node_name2 = tkinter.Entry(self.name2_frame, font='arial 15')
        self.screen_node_name2.pack(side="left")

        self.result_connection_frame = tkinter.Frame(self.frame_names)
        self.result_connection_frame.pack()

        self.connection_btn = tkinter.Button(self.result_connection_frame, text="Verificar", command=lambda: self.is_connected(), pady=15)
        self.connection_btn.pack()

        self.connection_result_text = tkinter.Text(self.result_connection_frame, font='arial 15', width=65)
        self.connection_result_text.pack()

        self.window.mainloop()

    def graph_generator(self):

        #Cria um array com valores permutados entre 0 e len(data)
        perm_array = np.random.permutation(len(data))

        tam = int(self.num_nodes.get())
        connects_num = int(self.num_connections.get())

        #Seleciona todos os dados entre de "data" do 0 ao número de nós escolhido pelo usuário
        index = perm_array[:tam]


        #Cria uma lista de consulta que conterá todos os nós (Twitters)
        global data_list
        data_list = []
        ch = 0
        for i in index:
            d = data.iloc[i]
            tw = Twitter(ch, d["user_screen_name"], d["user_followers_count"], d["country"])
            data_list.append(tw)
            ch += 1

        #Cria a lista de conexões:
        #Para cada índice em index
        connections = []
        for d1 in data_list:
            random_tam = np.random.randint(connects_num, size=1) #Gera um número aleatório entre 0 e connects_num
            if random_tam == 0:
                random_tam = 1
            ###
            # Cria um array do tamanho "random_tam" com valores entre 0 e "tam"
            # Lembrando que "tam" foi a quantidade de nós escolhido pelo usuário
            ###
            arr = np.random.randint(tam, size=random_tam)
            #Para cada valor no array
            for val in arr:
                d2 = data_list[val] #Usa val como referência para encontrar o índice em index
                if d1.ch != d2.ch:
                    connections.append((d1, d2)) #insere uma tupla com os nós indicando a conexão e insere na lista

        #Cria o grafo
        global g
        g = Graph(connections, tam, directed=True)

        self.graph_result_text.configure(state='normal')
        self.graph_result_text.delete('1.0', tkinter.END)
        #Imprime o gráfico na caixa de texto
        for t in range(tam):
            self.graph_result_text.insert('end',  '{}: \n '.format(data_list[t]))
            for n in g._graph[t]:
                self.graph_result_text.insert(tkinter.END, '     {}\n '.format(data_list[n.ch]))
            self.graph_result_text.insert(tkinter.END, ' \n')


    def is_connected(self):
        #Recebe as chaves do usuário
        ch1 = int(self.screen_node_name1.get())
        ch2 = int(self.screen_node_name2.get())

        self.connection_result_text.configure(state='normal')
        self.connection_result_text.delete('1.0', tkinter.END)

        #Busca o caminho entre os nós e imprime na caixa de texto
        path = None
        #Para cada conexão do nó
        for i in g._graph[ch1]:
            #Busca um novo caminho
            path = g.dfs(data_list[i.ch], data_list[ch2], data_list[ch1])
            if path:
                self.connection_result_text.insert('end', '-> {}\n'.format(data_list[ch1]))
                for p in path:
                    self.connection_result_text.insert('end', '-> {}\n'.format(p))
                self.connection_result_text.insert('end', '\nTamanho: {}'.format(len(path)+1))
                self.connection_result_text.insert('end', '\n-----------\n\n')
        #Caso não haja caminho
        if not path:
            self.connection_result_text.delete('1.0', tkinter.END)
            self.connection_result_text.insert('end', 'Não há conexão entre os nós.')

    