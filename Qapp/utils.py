import pandas as pd
from io import StringIO
import seaborn as sns 
from io import BytesIO
import base64
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression as lr



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
        plt.title("Simple Line Plot")
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
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title("BarChart")
        self.BarChart = get_image()  

    # def Histogram(self,column1,column2):
    #     courses = list(self.data[column1])
    #     values = list(self.data[column2])
    #     plt.hist(courses,  bins=9)
    #     plt.xlabel(column1)
    #     plt.ylabel(column1)
    #     plt.title('Histogram')
    #     plt.show()
    #     self.BarChart = get_image()   

    def ScatterPlot(self,column1,column2):
        new_data = self.data.dropna()
        x = list(new_data[column1])
        y = list(new_data[column2])
        plt.scatter(x,y)
        plt.xlabel(column1)                
        plt.ylabel(column2)
        plt.title('ScatterPlot')
        self.ScatterPlot = get_image()                    
             

    def LinearRegression(self,column1,column2):

        print(column1,column2)
        new_data = self.data.dropna()
        x=np.array(new_data[column1])
        y=np.array(new_data[column2])
        print(x,y)
        linreg = lr()
        x = x.reshape(-1,1)
        linreg.fit(x,y)
        y_pred = linreg.predict(x)
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.scatter(x,y)
        plt.plot(x,y_pred,color='red')     
        self.LinearRegression = get_image()












class Data_Frame2:
    def __init__(self,url,colList):
        self.old_data = pd.read_csv(url)
        self.data = self.old_data[colList]
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
        plt.title("Simple Line Plot")
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
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title("BarChart")
        self.BarChart = get_image()  

    # def Histogram(self,column1,column2):
    #     courses = list(self.data[column1])
    #     values = list(self.data[column2])
    #     plt.hist(courses,  bins=9)
    #     plt.xlabel(column1)
    #     plt.ylabel(column1)
    #     plt.title('Histogram')
    #     plt.show()
    #     self.BarChart = get_image()   

    def ScatterPlot(self,column1,column2):
        new_data = self.data.dropna()
        x = list(new_data[column1])
        y = list(new_data[column2])
        plt.scatter(x,y)
        plt.xlabel(column1)                
        plt.ylabel(column2)
        plt.title('ScatterPlot')
        self.ScatterPlot = get_image()                    
             

    def LinearRegression(self,column1,column2):
        new_data = self.data.dropna()
        x=np.array(new_data[column1])
        y=np.array(new_data[column2])
        linreg = lr()
        x = x.reshape(-1,1)
        linreg.fit(x,y)
        y_pred = linreg.predict(x)
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.scatter(x,y)
        plt.plot(x,y_pred,color='red')      
        self.LinearRegression = get_image()
 
