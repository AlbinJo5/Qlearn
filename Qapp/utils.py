import pandas as pd
from io import StringIO
import seaborn as sns 
from io import BytesIO
import base64
import numpy as np
import math
import matplotlib.pyplot as plt



output = StringIO()


def get_image():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    buffer.close()

    return graph

class Data_Frame:
    def __init__(self,url):
        self.data = pd.read_csv(url)
        self.data_json = self.data.to_json
        


    def GeneralInfo(self,headCount):
        self.data.info(buf=output)
        self.data_info = pd.DataFrame(columns=['Data Info'], data=output.getvalue().split('\n'))
        self.Info = self.data_info.to_html(classes='table table-stripped',index=None)
        self.Data = self.data.to_html(classes='table table-stripped')
        self.Describe = self.data.describe().to_html(classes='table table-stripped')
        self.Head = self.data.head(headCount).to_html(classes='table table-stripped')
        self.Index = self.data.columns

    def Head(self,headCount):
        if(headCount):
            self.Head = self.data.head(headCount).to_html(classes='table table-stripped')
        else:
            self.Head = self.data.head().to_html(classes='table table-stripped')   

    def Tail(self,headCount):
        if(headCount):
            self.Tail = self.data.tail(headCount).to_html(classes='table table-stripped')
        else:
            self.Tail = self.data.tail().to_html(classes='table table-stripped')   

    def Describe(self):
         self.Describe = self.data.describe().to_html(classes='table table-stripped')


    def Index(self):
        self.Index = self.data.index

    def Columns(self):
        self.Columns = self.data.columns    

    def Info(self):
        self.data.info(buf=output)
        self.data_info = pd.DataFrame(columns=['Data Info'], data=output.getvalue().split('\n'))
        self.Info = self.data_info.to_html(classes='table table-stripped',index=None)

    def Mean(self,axis):
        self.Mean = self.data.mean(axis)

    def Dtypes(self):
        self.Dtypes = self.data.dtypes

    def Shape(self):
        self.Shape = self.data.shape    

    def Size(self):
        self.Size = self.data.size  

    def Sample(self,sampleNum):
        self.Sample = self.data.sample(sampleNum).to_html(classes='table table-stripped') 

    def Isnull(self):
        self.Isnull = self.data.isnull().to_html(classes='table table-stripped') 

    def IsnullSum(self):
        self.IsnullSum = self.data.isnull().sum() 

    def Isna(self):
        self.Isna = self.data.isna().any() 

    def Nunique(self):
        self.Nunique = self.data.nunique  

    def MemoryUsage(self):
        self.MemoryUsage = self.data.memory_usage()   

    def SimpleLinePlot(self,column):
        plt.plot(self.data[column])
        plt.title(column)
        plt.tight_layout()
        self.SimpleLinePlot = get_image()    

    def SimpleLinePlot2(self,column1,column2):
        plt.plot(self.data[column1],self.data[column2])
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title("Simple Line Plot")
        plt.tight_layout()
        self.SimpleLinePlot2 = get_image()              
             
    def BarChart(self,column1,column2):
        courses = list(self.data[column1])
        values = list(self.data[column2])
        
        fig = plt.figure(figsize = (10, 5))
        plt.bar(courses, values, color ='maroon',width = 0.4)
        plt.xlabel("occupancy")
        plt.ylabel("loan_amount")
        self.BarChart = get_image()             
             

    def Lineplot(self,x,y):
        # plot = sns.lineplot(x=x,y=y,data=self.data)
        # plot_file = BytesIO() 
        # plot.figure.savefig(plot_file, format='png')
        # encoded_file = base64.b64encode(plot_file.getvalue())
        # self.Lineplot = encoded_file
        # print("hiii")
        plt.switch_backend('AGG')
        fig = plt.figure(figsize=[10,4])
        plt.title("Tirtle")
        plt.bar(x,y)
        plt.tight_layout()
        self.graph = get_image()