# Data Struct with Tkinter interface

Theese codes are data structure implementations in Python language with UI Tkinter library.

The main [menu](https://github.com/joaolevi/data_struct_w_tkinter/blob/master/main.py) is the initial code. There, you'll can choose one of the data structure types.

So, we have:

 - List
 - Graph
 - Tree
 - Queue
 - Stack

The data used to run this code aren't in this repository.
You need to put in some data as "**.csv**" and modify these lanes [here](https://github.com/joaolevi/data_struct_w_tkinter/blob/602ffd6c05b224a6ae59328d4f7e06418a58c8a0/graph.py#L83):

    #If you put the archive .csv in a folder named "dataset" for example
    datapath = os.path.join("dataset", "")
    
    #datapath is the path to archive. "usecols" are an example if you don't
    #want to have all data
    data = pd.read_csv(datapath + "archive.csv", usecols=[5,6,8,11,16])
   
  **Is very imporant that you need to have Pandas and OS lib instaled in your program.**
    
