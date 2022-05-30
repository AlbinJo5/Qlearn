from multiprocessing import context
import re
import pyrebase
from django.contrib import messages
from django.shortcuts import render, redirect
import urllib
from .models import *
from .utils import Data_Frame, Data_Frame2
import pandas as pd

firebaseConfig = {
  "apiKey": "AIzaSyAHXZVQMXO5hvBiEfg-vB6zjJGuIz1-2hs",
  "authDomain": "qlearn-edfc1.firebaseapp.com",
  "projectId": "qlearn-edfc1",
  "databaseURL": "https://qlearn-edfc1-default-rtdb.firebaseio.com",
  "storageBucket": "qlearn-edfc1.appspot.com",
  "messagingSenderId": "1005750912201",
  "appId": "1:1005750912201:web:c081c2b6c2b350b57df918",
  "measurementId": "G-174MSH8R0M"
}
firebase = pyrebase.initialize_app(firebaseConfig)

db=firebase.database()
storage=firebase.storage()
auth=firebase.auth()



# Create your views here.
def index(request,user):
    
    context = {"username":user}
    if request.method == 'POST':
        if 'dataUpload' in request.POST:

            file = request.FILES["excel"] 
            dfName = request.POST.get('dfname') # collecting values from the form
            
            cloudFileName = user+"Main.csv"
            storage.child("Files").child(user).child(cloudFileName).put(file)
            url=storage.child("Files").child(user).child(cloudFileName).get_url(None) #uploading the file to the firebase storage

            data = {
                "dfName": dfName,
                "fileUrl": url
             }
            kwargs={"user":user,"dfName":dfName,"setNum":1}

            db.child("Work").child(user).set(data)
            return redirect('work',**kwargs)

    
    return render(request,'index.html',context)

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        cpsw = request.POST.get('cpsw')
        if psw == cpsw:
            try:
                auth.create_user_with_email_and_password(email,psw)
                try:
                    data = {
                        "username":username,
                        "email":email,
                        "password":psw
                    }
                    db.child("Users").push(data)
                    return redirect("index",user=username)
                except:
                    messages.info(request, "Oops, an error occurred, try again with another account")
                    return redirect('signup')
            except:
                messages.info(request,"Account already exists")
                return redirect('signup')
        else:
            messages.info(request, "Passwords does not match")
            return redirect('signup')

    return render(request,'signUp.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        psw = request.POST.get('password')


        try:
            auth.sign_in_with_email_and_password(email,psw)
            users=db.child("Users").get()
            for user in users.each():
                if user.val()['email']==email:
                    return redirect('index',user=user.val()['username'])
            else:
                messages.info(request, "Invalid Credentials")
                return redirect('signin')

        except:
            messages.info(request,"Invalid Credentials")
            return redirect('signin')

    return render(request,'signIn.html')

def work(request,user,dfName,setNum):
    
    userData = db.child("Work").child(user).get()
    for i in userData.each():
        url = i.val()

    if setNum==1:
        df1 = Data_Frame(url)
        context={
            'dfName':dfName
        }
    elif setNum==2:
        context={
            'dfName':dfName,
            'subSet':True
        }
        try:
            columnList=db.child("Work").child(user).child("SubSet").get()
        except:
             kwargs={"user":user,"dfName":dfName,"setNum":1}
             return redirect('work',**kwargs)   
        for i in columnList.each():
            subList = i.val()
        df1 = Data_Frame2(url,subList)
    
           
 

    if request.method == 'POST':
        if setNum==1:
            context={
                'dfName':dfName
            }
        else:
            context={
            'dfName':dfName,
            'subSet':True
            }


        if 'newCol' in request.POST:
            colNum = request.POST.get('colNum')
            subDfName = request.POST.get('subDfName')
            colList = []
            for i in range(1,int(colNum)+1):
                colName='Column'+str(i) 
                
                Name = request.POST.get(colName)

                colList.append(Name)
            data = {
                        "colList":colList,
                    }
                    
            db.child("Work").child(user).child("SubSet").set(data)
            
            
            kwargs={"user":user,"dfName":subDfName,"setNum":2}
            return redirect('work',**kwargs)

        
        block1 = request.POST.get('block1')
        block2 = request.POST.get('block2')
        block3 = request.POST.get('block3')

        
            
        if block1 == 'Pandas':
            function = request.POST.get('block1PandasFunctions')

            if function == 'Panda Function':
                pass

            # elif function == 'Head':
            #     headValue = request.POST.get('block1PandasHeadFunction') 
            #     df1.Head(int(headValue))
            #     context.update({'block1': df1.Head})
            #     context.update({'block1Function': 'Head'})

            elif function == 'Index':
                df1.Index()
                context.update({'block1': df1.Index})    
                context.update({'block1Function': 'Index'})

            elif function == 'Tail':
                headValue = request.POST.get('block1PandasTailFunction') 
                df1.Tail(int(headValue))
                context.update({'block1': df1.Tail})
                context.update({'block1Function': 'Tail'})

            elif function == 'Sample':
                headValue = request.POST.get('block1PandasSampleFunction') 
                df1.Sample(int(headValue))
                context.update({'block1': df1.Sample})
                context.update({'block1Function': 'Sample'})    

            elif function == 'Describe':
                df1.Describe()
                context.update({'block1': df1.Describe})
                context.update({'block1Function': 'Describe'})

            elif function == 'Info':
                df1.Info()
                context.update({'block1': df1.Info})
                context.update({'block1Function': 'Info'})     

            elif function == 'Columns':
                df1.Columns()
                context.update({'block1': df1.Columns})
                context.update({'block1Function': 'Columns'})

            elif function == 'Mean(X axis)':
                df1.Mean(0)
                context.update({'block1': df1.Mean})
                context.update({'block1Function': 'MeanX'})

            elif function == 'Mean(Y axis)':
                df1.Mean(1)
                context.update({'block1': df1.Mean})
                context.update({'block1Function': 'MeanY'})

            elif function == 'Dtypes':
                df1.Dtypes()
                context.update({'block1': df1.Dtypes})
                context.update({'block1Function': 'Dtypes'})

            elif function == 'Size':
                df1.Size()
                context.update({'block1': df1.Size})
                context.update({'block1Function': 'Size'})

            elif function == 'Shape':
                df1.Shape()
                context.update({'block1': df1.Shape})
                context.update({'block1Function': 'Shape'})    

            elif function == 'Isnull':
                df1.Isnull()
                context.update({'block1': df1.Isnull})
                context.update({'block1Function': 'Isnull'}) 

            elif function == 'Isnull (Sum)':
                df1.IsnullSum()
                context.update({'block1': df1.IsnullSum})
                context.update({'block1Function': 'IsnullSum'})     

            elif function == 'Isna':
                df1.Isna()
                context.update({'block1': df1.Isna})
                context.update({'block1Function': 'Isna'})     

            elif function == 'Nunique':
                df1.Nunique()
                context.update({'block1': df1.Nunique})
                context.update({'block1Function': 'Nunique'})

            elif function == 'Memory Usage':
                df1.MemoryUsage()
                context.update({'block1': df1.MemoryUsage})
                context.update({'block1Function': 'MemoryUsage'})             

        elif block1 == 'Matplotlib':
            function = request.POST.get('block1MatplotlibFunctions')

            if(function == 'SimpleLinePlot'):

                column1 = request.POST.get('block1MatplotlibLinePlotFunction1')
                column2 = request.POST.get('block1MatplotlibLinePlotFunction2')

                try:
                    if(column1 and column2):
                        df1.SimpleLinePlot2(column1,column2)
                        context.update({'block1': df1.SimpleLinePlot2})
                        context.update({'block1Function': 'SimpleLinePlot2'})   
                    elif(column1):
                        df1.SimpleLinePlot(column1)
                        context.update({'block1': df1.SimpleLinePlot})
                        context.update({'block1Function': 'SimpleLinePlot'})  
                    elif(column2):
                        df1.SimpleLinePlot(column2)
                        context.update({'block1': df1.SimpleLinePlot})
                        context.update({'block1Function': 'SimpleLinePlot'}) 
                    else:
                        context.update({'block1': "The column chosen is invalid"})
                        context.update({'block1Function': 'Error'})   
                except:
                    context.update({'block1': "The column chosen is invalid"})
                    context.update({'block1Function': 'Error'}) 

            if(function == 'BarChart'):

                column1 = request.POST.get('block1MatplotlibBarChartFunction1')
                column2 = request.POST.get('block1MatplotlibBarChartFunction2')

                try:
                    df1.BarChart(column1,column2)
                    context.update({'block1': df1.BarChart})
                    context.update({'block1Function': 'BarChart'}) 
                except:
                    context.update({'block1': "The column chosen is invalid"})
                    context.update({'block1Function': 'Error'})  

            if(function == 'ScatterPlot'):

                column1 = request.POST.get('block1MatplotlibBarChartFunction1')
                column2 = request.POST.get('block1MatplotlibBarChartFunction2')

                try:
                    df1.ScatterPlot(column1,column2)
                    context.update({'block1': df1.ScatterPlot})
                    context.update({'block1Function': 'ScatterPlot'}) 
                except:
                    context.update({'block1': "The column chosen is invalid"})
                    context.update({'block1Function': 'Error'})
                                 
        elif block1 == 'Sklearn':
            function = request.POST.get('block1SklearnFunctions')
            if(function == 'LinearRegression'):

                column1 = request.POST.get('block1MatplotlibBarChartFunction1')
                column2 = request.POST.get('block1MatplotlibBarChartFunction2')

                try:
                    df1.LinearRegression(column1,column2)
                    context.update({'block1': df1.LinearRegression})
                    context.update({'block1Function': 'LinearRegression'}) 
                except:
                    context.update({'block1': "The column chosen is invalid"})
                    context.update({'block1Function': 'Error'})
        # except:
        #     context.update({'block1': "Invalid command"})
        #     context.update({'block1Function': 'Error'})
        
        # try:    
        if block2 == 'Pandas':
            function = request.POST.get('block2PandasFunctions')

            if function == 'Panda Function':
                pass

            # elif function == 'Head':
            #     headValue = request.POST.get('block2PandasHeadFunction') 
            #     df1.Head(int(headValue))
            #     context.update({'block2': df1.Head})
            #     context.update({'block2Function': 'Head'})

            elif function == 'Index':
                df1.Index()
                context.update({'block2': df1.Index})    
                context.update({'block2Function': 'Index'})

            elif function == 'Tail':
                headValue = request.POST.get('block2PandasTailFunction') 
                df1.Tail(int(headValue))
                context.update({'block2': df1.Tail})
                context.update({'block2Function': 'Tail'})

            elif function == 'Sample':
                headValue = request.POST.get('block2PandasSampleFunction') 
                df1.Sample(int(headValue))
                context.update({'block2': df1.Sample})
                context.update({'block2Function': 'Sample'})    

            elif function == 'Describe':
                df1.Describe()
                context.update({'block2': df1.Describe})
                context.update({'block2Function': 'Describe'})

            elif function == 'Info':
                df1.Info()
                context.update({'block2': df1.Info})
                context.update({'block2Function': 'Info'})     

            elif function == 'Columns':
                df1.Columns()
                context.update({'block2': df1.Columns})
                context.update({'block2Function': 'Columns'})

            elif function == 'Mean(X axis)':
                df1.Mean(0)
                context.update({'block2': df1.Mean})
                context.update({'block2Function': 'MeanX'})

            elif function == 'Mean(Y axis)':
                df1.Mean(1)
                context.update({'block2': df1.Mean})
                context.update({'block2Function': 'MeanY'})

            elif function == 'Dtypes':
                df1.Dtypes()
                context.update({'block2': df1.Dtypes})
                context.update({'block2Function': 'Dtypes'})

            elif function == 'Size':
                df1.Size()
                context.update({'block2': df1.Size})
                context.update({'block2Function': 'Size'})

            elif function == 'Shape':
                df1.Shape()
                context.update({'block2': df1.Shape})
                context.update({'block2Function': 'Shape'})    

            elif function == 'Isnull':
                df1.Isnull()
                context.update({'block2': df1.Isnull})
                context.update({'block2Function': 'Isnull'}) 

            elif function == 'Isnull (Sum)':
                df1.IsnullSum()
                context.update({'block2': df1.IsnullSum})
                context.update({'block2Function': 'IsnullSum'})     

            elif function == 'Isna':
                df1.Isna()
                context.update({'block2': df1.Isna})
                context.update({'block2Function': 'Isna'})     

            elif function == 'Nunique':
                df1.Nunique()
                context.update({'block2': df1.Nunique})
                context.update({'block2Function': 'Nunique'})

            elif function == 'Memory Usage':
                df1.MemoryUsage()
                context.update({'block2': df1.MemoryUsage})
                context.update({'block2Function': 'MemoryUsage'})             

        elif block2 == 'Matplotlib':
            function = request.POST.get('block2MatplotlibFunctions')

            if(function == 'SimpleLinePlot'):

                column1 = request.POST.get('block2MatplotlibLinePlotFunction1')
                column2 = request.POST.get('block2MatplotlibLinePlotFunction2')

                try:
                    if(column1 and column2):
                        df1.SimpleLinePlot2(column1,column2)
                        context.update({'block2': df1.SimpleLinePlot2})
                        context.update({'block2Function': 'SimpleLinePlot2'})   
                    elif(column1):
                        df1.SimpleLinePlot(column1)
                        context.update({'block2': df1.SimpleLinePlot})
                        context.update({'block2Function': 'SimpleLinePlot'})  
                    elif(column2):
                        df1.SimpleLinePlot(column2)
                        context.update({'block2': df1.SimpleLinePlot})
                        context.update({'block2Function': 'SimpleLinePlot'}) 
                    else:
                        context.update({'block2': "The column chosen is invalid"})
                        context.update({'block2Function': 'Error'})   
                except:
                    context.update({'block2': "The column chosen is invalid"})
                    context.update({'block2Function': 'Error'}) 

            if(function == 'BarChart'):

                column1 = request.POST.get('block2MatplotlibBarChartFunction1')
                column2 = request.POST.get('block2MatplotlibBarChartFunction2')

                try:
                    df1.BarChart(column1,column2)
                    context.update({'block2': df1.BarChart})
                    context.update({'block2Function': 'BarChart'}) 
                except:
                    context.update({'block2': "The column chosen is invalid"})
                    context.update({'block2Function': 'Error'})  

            if(function == 'ScatterPlot'):

                column1 = request.POST.get('block2MatplotlibBarChartFunction1')
                column2 = request.POST.get('block2MatplotlibBarChartFunction2')

                try:
                    df1.ScatterPlot(column1,column2)
                    context.update({'block2': df1.ScatterPlot})
                    context.update({'block2Function': 'ScatterPlot'}) 
                except:
                    context.update({'block2': "The column chosen is invalid"})
                    context.update({'block2Function': 'Error'})

            
        elif block2 == 'Sklearn':
            function = request.POST.get('block2SklearnFunctions')
            if(function == 'LinearRegression'):

                column1 = request.POST.get('block2MatplotlibBarChartFunction1')
                column2 = request.POST.get('block2MatplotlibBarChartFunction2')

                try:
                    df1.LinearRegression(column1,column2)
                    context.update({'block2': df1.LinearRegression})
                    context.update({'block2Function': 'LinearRegression'}) 
                except:
                    context.update({'block2': "The column chosen is invalid"})
                    context.update({'block2Function': 'Error'})
            
        # except:
        #     context.update({'block2': "Invalid command"})
        #     context.update({'block2Function': 'Error'})

        # try:
        if block3 == 'Pandas':
            function = request.POST.get('block3PandasFunctions')

            if function == 'Panda Function':
                pass

            # elif function == 'Head':
            #     headValue = request.POST.get('block3PandasHeadFunction') 
            #     df1.Head(int(headValue))
            #     context.update({'block3': df1.Head})
            #     context.update({'block3Function': 'Head'})

            elif function == 'Index':
                df1.Index()
                context.update({'block3': df1.Index})    
                context.update({'block3Function': 'Index'})

            elif function == 'Tail':
                headValue = request.POST.get('block3PandasTailFunction') 
                df1.Tail(int(headValue))
                context.update({'block3': df1.Tail})
                context.update({'block3Function': 'Tail'})

            elif function == 'Sample':
                headValue = request.POST.get('block3PandasSampleFunction') 
                df1.Sample(int(headValue))
                context.update({'block3': df1.Sample})
                context.update({'block3Function': 'Sample'})    

            elif function == 'Describe':
                df1.Describe()
                context.update({'block3': df1.Describe})
                context.update({'block3Function': 'Describe'})

            elif function == 'Info':
                df1.Info()
                context.update({'block3': df1.Info})
                context.update({'block3Function': 'Info'})     

            elif function == 'Columns':
                df1.Columns()
                context.update({'block3': df1.Columns})
                context.update({'block3Function': 'Columns'})

            elif function == 'Mean(X axis)':
                df1.Mean(0)
                context.update({'block3': df1.Mean})
                context.update({'block3Function': 'MeanX'})

            elif function == 'Mean(Y axis)':
                df1.Mean(1)
                context.update({'block3': df1.Mean})
                context.update({'block3Function': 'MeanY'})

            elif function == 'Dtypes':
                df1.Dtypes()
                context.update({'block3': df1.Dtypes})
                context.update({'block3Function': 'Dtypes'})

            elif function == 'Size':
                df1.Size()
                context.update({'block3': df1.Size})
                context.update({'block3Function': 'Size'})

            elif function == 'Shape':
                df1.Shape()
                context.update({'block3': df1.Shape})
                context.update({'block3Function': 'Shape'})    

            elif function == 'Isnull':
                df1.Isnull()
                context.update({'block3': df1.Isnull})
                context.update({'block3Function': 'Isnull'}) 

            elif function == 'Isnull (Sum)':
                df1.IsnullSum()
                context.update({'block3': df1.IsnullSum})
                context.update({'block3Function': 'IsnullSum'})     

            elif function == 'Isna':
                df1.Isna()
                context.update({'block3': df1.Isna})
                context.update({'block3Function': 'Isna'})     

            elif function == 'Nunique':
                df1.Nunique()
                context.update({'block3': df1.Nunique})
                context.update({'block3Function': 'Nunique'})

            elif function == 'Memory Usage':
                df1.MemoryUsage()
                context.update({'block3': df1.MemoryUsage})
                context.update({'block3Function': 'MemoryUsage'})             

        elif block3 == 'Matplotlib':
            function = request.POST.get('block3MatplotlibFunctions')

            if(function == 'SimpleLinePlot'):

                column1 = request.POST.get('block3MatplotlibLinePlotFunction1')
                column2 = request.POST.get('block3MatplotlibLinePlotFunction2')

                try:
                    if(column1 and column2):
                        df1.SimpleLinePlot2(column1,column2)
                        context.update({'block3': df1.SimpleLinePlot2})
                        context.update({'block3Function': 'SimpleLinePlot2'})   
                    elif(column1):
                        df1.SimpleLinePlot(column1)
                        context.update({'block3': df1.SimpleLinePlot})
                        context.update({'block3Function': 'SimpleLinePlot'})  
                    elif(column2):
                        df1.SimpleLinePlot(column2)
                        context.update({'block3': df1.SimpleLinePlot})
                        context.update({'block3Function': 'SimpleLinePlot'}) 
                    else:
                        context.update({'block3': "The column chosen is invalid"})
                        context.update({'block3Function': 'Error'})   
                except:
                    context.update({'block3': "The column chosen is invalid"})
                    context.update({'block3Function': 'Error'}) 

            if(function == 'BarChart'):

                column1 = request.POST.get('block3MatplotlibBarChartFunction1')
                column2 = request.POST.get('block3MatplotlibBarChartFunction2')

                try:
                    df1.BarChart(column1,column2)
                    context.update({'block3': df1.BarChart})
                    context.update({'block3Function': 'BarChart'}) 
                except:
                    context.update({'block3': "The column chosen is invalid"})
                    context.update({'block3Function': 'Error'})  

            if(function == 'ScatterPlot'):

                column1 = request.POST.get('block3MatplotlibBarChartFunction1')
                column2 = request.POST.get('block3MatplotlibBarChartFunction2')

                try:
                    df1.ScatterPlot(column1,column2)
                    context.update({'block3': df1.ScatterPlot})
                    context.update({'block3Function': 'ScatterPlot'}) 
                except:
                    context.update({'block3': "The column chosen is invalid"})
                    context.update({'block3Function': 'Error'})

        elif block3 == 'Sklearn':
            function = request.POST.get('block3SklearnFunctions')
            if(function == 'LinearRegression'):

                column1 = request.POST.get('block3MatplotlibBarChartFunction1')
                column2 = request.POST.get('block3MatplotlibBarChartFunction2')

                print(column1,"asdsdsdsdds",column2)

                # try:
                df1.LinearRegression(column1,column2)
                context.update({'block3': df1.LinearRegression})
                context.update({'block3Function': 'LinearRegression'}) 
                # except:
                    # context.update({'block3': "The column chosen is invalid"})
                    # context.update({'block3Function': 'Error'})
                
        # except:
        #     context.update({'block3': "Invalid command"})
        #     context.update({'block3Function': 'Error'})

        
        
        return render(request,'work2.html',context)
    
            

    return render(request,'work2.html',context)

def work2(request):
    return render(request,'work2.html')    