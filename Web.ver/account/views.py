from django.shortcuts import render
from .form import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from .models import Bodydata
import datetime

def register_view(request): # 透過此fn回傳到前端
    if request.method == 'POST':
         form = RegisterForm(request.POST)
         if form.is_valid():
            form.save()
            return render(request, 'regist_success.html')
         else: 
             print("NOOOOOOOOOOOOOOOOOOOOO")
             
    else:
        form = RegisterForm()
    context = {
        'form': form  # 註冊頁面格式設定
    }
    return render(request, 'register.html', context)

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    
    if request.user.is_authenticated:
        print("auhten")
        return render(request, 'home.html')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST) # 這裡要加上data
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                print("not none")
                return render(request, 'home.html')
            else:
                print("None")
    else:
        print("nothing")
        form = AuthenticationForm()
        
    context = {
        'form': form  # 註冊頁面格式設定
    }
    print("fin")
    return render(request, 'login.html', context)
    
def logout_view(request):
    auth.logout(request)
    return render(request, 'logout.html')

def member_view(request):
    if request.user.is_authenticated:
        print("auhten")
        data = Bodydata.objects.filter(member=request.user.id).order_by('-time')[:1]
        
        if(len(data)==0):
            nodata = True
            today= datetime.datetime.now()
            time = today.strftime("%Y/%m/%d   %H:%M")
            context = {
            'time':time,
            'nodata':nodata
            }
        else:
            nodata = False
            context = {
            'time':data[0].time,            
            'height':data[0].height,
            'weight':data[0].weight,
            'bmi':data[0].BMI,
            'nodata':nodata
            
            }
        return render(request, 'member.html',context)
    
def addata_view(request):
    if request.user.is_authenticated:
        if(request.method == 'POST'):
            h = float(request.POST['height'])
            w = float(request.POST['weight'])
            bmi = round(w / ((h*0.01))**2,1)
        if('cal' in request.POST):
            context = {
                'h':h,
                'w':w,
                'bmi': bmi,
                'cal': True}
            return render(request, 'addata.html',context)
        elif('save' in request.POST):
            Bodydata.objects.create(member=request.user,height=h,weight=w,BMI=bmi,time=datetime.datetime.now())
            data = Bodydata.objects.all().order_by('-time')[:1]
            context = {
                'time':data[0].time,            
                'height':data[0].height,
                'weight':data[0].weight,
                'bmi':data[0].BMI
                }
            return render(request, 'member.html',context)    
    
        return render(request, 'addata.html')

def history_view(request):
    if request.user.is_authenticated:
        data = Bodydata.objects.filter(member=request.user.id)
        if(len(data)==0):
            nodata = True
            context = {
            'nodata':nodata
            }
        else:
            context = {
            'alldata': data,
            'length':len(data),
            }
            
        return render(request, 'history.html',context)
def deldata_view(request):
    if request.user.is_authenticated:
        data = Bodydata.objects.filter(member=request.user.id)
        context = {
        'alldata': data
        }
        if(request.method == 'POST'):
            num = int(request.POST['delete'])
            if(num<=len(data) and num>=1):
                data[num-1].delete()
            return render(request, 'history.html',context)
        return render(request, 'deldata.html',context)