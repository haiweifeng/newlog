import os
import random
import string

import time
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from newapp.captcha.image import ImageCaptcha
from newapp.models import Admin137, Dept, Emp
def regview(request):
    return render(request,"newapp/regist.html")
# 1注册页面展示
def reglogic(request):
    if request.session.get("codefail"):
        del request.session["codefail"]
    realcode=request.session.get("code")
    print("code",realcode)
    usercode=request.POST.get("number")
    if realcode.lower()!=usercode.lower():
        request.session["codefail"]='y'
        return redirect("newapp:regview")
    userpwd=request.POST.get("password")
    password=make_password(userpwd)
    print('密码',password)
    l=["username","realname","gender","birth"]
    a=[]
    for i in l:
        a.append(request.POST.get(i))

    img=request.FILES.get("headimg")
    if not img:
        img = "headimg/testImage4.jpg"
    print(img)
    print(a)
    with transaction.atomic():
        Admin137(username=a[0],realname=a[1],password=password,gender=a[2],birth=a[3],head_img=img).save()
    return redirect("newapp:logview")
# 2注册逻辑处理
def logview(request):
    if request.session.get("codefail"):
        del request.session["codefail"]
    if request.COOKIES.get("username"):
        username=str(request.COOKIES.get("username").encode("latin-1"),"utf-8")
        return render(request, "newapp/login.html",{"username":username})
    return render(request, "newapp/login.html")
# 3登录页面展示
def loglogic(request):
    l=["username","password","remember"]
    a=[]
    for i in l:
        a.append(request.POST.get(i))
    print(a)
    res=redirect("newapp:deptview")
    if Admin137.objects.filter(username=a[0]):
        pwd=Admin137.objects.get(username=a[0]).password
        print(pwd)
        print(check_password(a[1],pwd))
        if check_password(a[1],pwd):
            print("right")
            request.session['username'] = str(a[0].encode("utf-8"), "latin-1")
            request.session['login'] = 'y'
            request.session["headimg"] = Admin137.objects.get(username=a[0]).head_img.url
            if a[2]:
                res.set_cookie("username", str(a[0].encode("utf-8"), "latin-1"), max_age=60 * 60 * 24 * 7)
                res.set_cookie("gender", Admin137.objects.get(username=a[0]).gender)
            return res
    request.session['login'] = 'n'
    return redirect("newapp:logview")
# 4登录逻辑处理
def deptview(request):
    if not request.session.get("login")=='y':
        return redirect("newapp:logview")
    if request.session.get("deptid"):
        del request.session["deptid"]
    username=str(request.session.get("username").encode("latin-1"),"utf-8")
    headimg=request.session.get("headimg")
    if not num:
        num = 1
    page = Paginator(depts, 3).page(num)
    gender=request.COOKIES.get("gender")
    depts=Dept.objects.all()
    num=request.GET.get("number")

    return render(request, "newapp/departmentlist.html",{"page":page,"username":username,"headimg":headimg})
# 5登录之后显示所有部门
def empbydept(request):
    if not request.session.get("login")=='y':
        return redirect("newapp:logview")
    deptid=request.GET.get("deptid")
    if not deptid:
        deptid=request.session.get("deptid")
    print(deptid)
    dept=Dept.objects.filter(pk=deptid)[0]
    emps=Emp.objects.filter(depts_id=deptid)
    request.session["deptid"]=deptid
    return render(request,"newapp/emplist.html",{"dept":dept,"emps":emps})
# 6部门功能逻辑处理
def updatedeptview(request):
    if not request.session.get("login")=='y':
        return redirect("newapp:logview")
    id=request.GET.get("deptid")
    print(id)
    dept=Dept.objects.get(pk=id)
    return render(request,"newapp/updateDept.html",{"dept":dept})
# 7部门更新页面
def updatelogic(request):
    l=["id","name","note"]
    a=[]
    for i in l:
        a.append(request.POST.get(i))
    newdept=Dept.objects.get(pk=a[0])
    newdept.name=a[1]
    newdept.note=a[2]
    newdept.save()
    return redirect("newapp:deptview")
# 8部门更新逻辑
def addeptview(request):
    if not request.session.get("login")=='y':
        return redirect("newapp:logview")

    return render(request,"newapp/addDepartment.html")
# 9增加部门显示
def addeptlogic(request):
    l=["name","note"]
    a=[]
    for i in l:
        a.append(request.POST.get(i))
    with transaction.atomic():
        Dept(name=a[0],note=a[1]).save()

    return redirect("newapp:deptview")
# 10增加部门逻辑
def addempview(request):
    if not request.session.get("login")=='y':
        return redirect("newapp:logview")
    deptid=request.GET.get("deptid")
    print(deptid)
    request.session["deptid"]=deptid
    return render(request,"newapp/addEmp.html")
# 11增加员工页面展示
def addemplogic(request):
    l=["name","salary","age"]
    a=[]
    for i in l:
        a.append(request.POST.get(i))
    headimg=request.FILES.get("headimg")
    deptid=request.session.get("deptid")
    print(deptid)
    dept=Dept.objects.get(pk=deptid)
    if not headimg:
        headimg="images/testImage3.jpg"
    with transaction.atomic():
        Emp(name=a[0],salary=a[1],age=a[2],depts=dept,headimg=headimg).save()

    return redirect("newapp:empbydept")
# 12增加员工逻辑
def updateempview(request):
    if not request.session.get("login")=='y':
        return redirect("newapp:logview")
    id=request.GET.get("id")
    print("更新",id)
    emp=Emp.objects.get(pk=id)
    return render(request, "newapp/updateEmp.html",{"emp":emp})
# 13更新员工页面展示
def updateemplogic(request):
    l=["name","salary","age","depts","id"]
    a=[]
    for i in l:
        a.append(request.POST.get(i))
    print(a)
    headimg=request.FILES.get("headimg")
    if not headimg:
        headimg=Emp.objects.get(pk=a[4]).headimg
    print("up的head",headimg)
    with transaction.atomic():
        dept = Dept.objects.get(pk=a[3])
        emp=Emp.objects.get(pk=a[4])
        emp.name=a[0]
        emp.salary=a[1]
        emp.age=a[2]
        emp.depts=dept
        emp.headimg=headimg
        emp.save()
    return redirect("newapp:empbydept")
# 14更新员工逻辑
def deleteemp(request):
    id=request.GET.get("id")
    with transaction.atomic():
        Emp.objects.get(pk=id).delete()
    # if request.session.get("deptid"):
    #     del request.session["deptid"]
    return redirect("newapp:empbydept")
# 15删除员工
def getcaptcha(request):
    path=os.path.abspath("newapp/fonts/1.ttf")
    img=ImageCaptcha(fonts=[path])
    code=random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,3)
    code_str="".join(code)
    print(code_str)
    request.session["code"]=code_str
    data=img.generate(code_str)
    return HttpResponse(data,"image/png")
# 16验证码生成
def ajax_username(request):
    name=request.GET.get("username")
    print("name",name)
    if Admin137.objects.filter(username=name):
        return HttpResponse("该用户名已存在")
    return HttpResponse("可以注册")


# 17用户名重复校验
def ajax_captcha(request):

    realcode = request.session.get("code")
    usercode = request.POST.get("number")
    if realcode.lower() == usercode.lower():
        return HttpResponse("y")
    return HttpResponse("验证码错误")
# 18验证码重复校验




