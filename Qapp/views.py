from multiprocessing import context
import re
import pyrebase
from django.contrib import messages
from django.shortcuts import render, redirect
import urllib
from .models import *
from .utils import Data_Frame
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
            kwargs={"user":user,"dfName":dfName}

            db.child("Work").child(user).set(data)
            return redirect('work',**kwargs)

            
            # df1 = Data_Frame(url)
            # df1.GeneralInfo(5)
            # context = {
            # "username": user,
            # "dataFrame" : df1.Data,
            # "dataDescribe" : df1.Describe,
            # "dataHead" : df1.Head,
            # "dataInfo" : df1.Info,
            # }

    
    return render(request,'index.html',context)

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        cpsw = request.POST.get('cpsw')
        # TODO username check
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

def work(request,user,dfName):
        
    
    userData = db.child("Work").child(user).get()
    for i in userData.each():
        url = i.val()

    df1 = Data_Frame(url)
    df1.GeneralInfo(5)
           
    context = {
        "dataframeName":dfName,
        "username":user,
        "dataFrame" : df1.Data,
        "dataDescribe" : df1.Describe,
        "dataHead" : df1.Head,
        "dataInfo" : df1.Info,  
        }

    if request.method == 'POST':
        cmd = request.POST.get('cmd')
        if(cmd=="index"):
            print(df1.Index)
            context={
                "index": df1.Index
            }
            return render(request,'work.html',context)
    
            

    return render(request,'work.html',context)

def work2(request):
    return render(request,'work2.html')    