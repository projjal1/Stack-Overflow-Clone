from django.shortcuts import render, redirect
from .models import Question, Fixes
from django.core.paginator import Paginator
from django.http import JsonResponse

#Home page render 
def index(request):
    #fetch page no
    page = request.GET.get('page', 1)

    #Perform pagination on object
    questions=Question.objects.order_by('-created_on')
    paginator = Paginator(questions, 4)
    return render(request,"index.html",{"question":paginator.page(page)})

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
    fix=Fixes.objects.filter(question_id=id)

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

def upvote(request,ans_id):
    print (ans_id)
    '''obj=Fixes.objects.get(pk=ans_id)
    obj.upvotes+=1
    ret_votes=obj.upvotes
    obj.save()'''

    return JsonResponse({'upvote':0})
