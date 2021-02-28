from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import Question, Fixes
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.postgres.search import *

#Home page render 
def index(request):
    disp_type="Fixes"

    if request.method=="GET":
        questions=Question.objects.order_by('-created_on')
        disp_posts=Question.objects.order_by('-answers')[:4]

    else:
        #Check if POST request from filter or search query
        try:
            search_type=request.POST['type']
            if search_type=="fixes":
                disp_posts=Question.objects.order_by('-answers')[:4]
            elif search_type=="views":
                disp_type="Views"
                disp_posts=Question.objects.order_by('-views')[:4]
            else:
                pass

            questions=Question.objects.order_by('-created_on')

        except:
            term=request.POST['search']
            questions=Question.objects.filter(title__icontains=term)

    #fetch page no
    page = request.GET.get('page', 1)
    #Perform pagination on object
    paginator = Paginator(questions, 4)
    return render(request,"index.html",{"question":paginator.page(page),"type_of_order":disp_type,
    "disp_posts":disp_posts})

#Write about a question 
def ask_question(request):
    return render (request, "question.html")

#Save a question
def question(request):
    if request.method=='GET':
        return redirect("home")
    
    content=request.POST["editor"]
    title=request.POST["title"]
    tag=request.POST["tag"]

    obj=Question(tag=tag,title=title,content=content)
    obj.save()

    return render (request, "question.html")

#Load question 
def QuestionDetail(request,id):
    ob=Question.objects.get(pk=id)
    views=ob.views+1
    ob.views=views
    ob.save()

    fix=Fixes.objects.filter(question_id=id).order_by('-upvotes')

    cont=ob.content
    cont=cont.replace('&lt;','<')
    cont=cont.replace('&gt;','>')
    cont=cont.replace('&nbsp;',' ')
    cont=cont.replace('&ldquo;','"')
    cont=cont.replace('&rdquo;','"')

    content=' '.join(cont.split())

    return render(request,"write.html",{"object":ob,"content":content,"fix":fix})

#Load answer page
def Answer(request,id):
    return render(request,"answer.html",{"question_id":id})

#Save fix
def fixes(request):
    if request.method=='GET':
        return redirect('home')

    content=request.POST["fix"]
    id=request.POST["ids"]
    tag=request.POST["tag"]

    #Save the reply
    obj=Fixes(content=content,question_id=id,tag=tag)
    obj.save()

    #Increase answer count of question
    ob=Question.objects.get(pk=id)
    ob.answers+=1
    ob.save()

    return redirect('home')

#Upvote answer
def upvote(request,ans_id,question_id):
    obj=Fixes.objects.get(pk=ans_id)
    obj.upvotes+=1
    obj.save()

    return redirect('/question/'+str(question_id))

#Report answer
def report(request,ans_id,question_id):
    obj=Fixes.objects.get(pk=ans_id)
    obj.abuse=True 
    obj.save()

    return redirect('/question/'+str(question_id))

#Check for abuse 
def check_abuse(request):
    obj=Fixes.objects.filter(abuse=True)

    return render(request,'abuse_check.html',{'obj':obj})

#Delete abuse reply 
def confirm(request,ans_id,flag):
    #Extract reply 
    obj=Fixes.objects.get(pk=ans_id)
    qobj=Question.objects.get(pk=obj.question_id)

    #If flag is 0 (i.e not abuse) then set abuse as False
    if flag==0:
        obj.abuse=False 
        obj.save()

    else:
        qobj.answers-=1
        qobj.save()
        obj.delete()

    return redirect('abuse_check')

#Login user
def login_render(request):
    return render(request,"login.html")

#Authenicate user 
def login(request): 
    if request.method=="POST":
        user=auth.authenticate(username=request.POST['username'],password=request.POST['pass1'])
        if (user!=None):
            auth.login(request,user)
            return redirect("home")
        else:
            return render(request,"login.html",{'error':'User does not exist or password is wrong.'})
    else:
        return render(request,"login.html")