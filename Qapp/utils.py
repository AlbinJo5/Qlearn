import pandas as pd
from io import StringIO

output = StringIO()
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

    def Head(self):
        self.Head = self.data.head().to_html(classes='table table-stripped')  

    def Index(self):
        self.Index = self.data.columns
