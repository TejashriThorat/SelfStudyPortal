from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .forms import UserRegistrationForm

# Create your views here.
def home(req):
    return render(req,"home.html")

@login_required
def notes(req):
    if req.method=="POST":
        form=NotesForm(req.POST)
        if form.is_valid():
            notes=Notes(user=req.user,title=req.POST['title'],desc=req.POST['desc'])
            notes.save()
            messages.success(req,f"Notes added successfully")
    else:
        form=NotesForm()
    notes=Notes.objects.filter(user=req.user)
    context={'notes':notes,'form':form}
    return render(req,"notes.html",context)

@login_required
def delete_note(req,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")
    
class NotesDetailView(generic.DetailView):
    model=Notes
    template_name = "notes_detail.html"

@login_required
def homework(req):
    if req.method == "POST":
        form=HomeworkForm(req.POST)
        if form.is_valid():
            try:
                finished=req.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks=Homework(
                user=req.user,
                subject=req.POST['subject'],
                title=req.POST['title'],
                description=req.POST['description'],
                due=req.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(req,f"Homework Added from {req.user.username}....")
    else:
        form=HomeworkForm()
    homework=Homework.objects.filter(user=req.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    context={"homeworks":homework,'homeworks_done':homework_done,'form':form}
    return render(req,"homework.html",context)
    
@login_required   
def update_homework(req,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
         homework.is_finished = True
    homework.save()
    return redirect('homework') 

""" ef update_homework(req,uval,pk=None):
    if uval==1:
        print("uval is 1")
    else:
        print("uval is 2")
    hw=Homework.objects.filter(id=pk) """
    



@login_required
def delete_homework(req,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

def youtube(req):
    if req.method == "POST":
        form = SearchForm(req.POST)
        text = req.POST['text']
        video = VideosSearch(text,limit=10)
        result_list=[]
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(req,"youtube.html",context)

    else:
        form=SearchForm()
    context={'form':form}
    return render(req,"youtube.html",context)

@login_required
def todo(req):
    if req.method == 'POST':
        form=TodoForm(req.POST)
        if form.is_valid():
            try:
                finished=req.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos=Todo(
                user = req.user,
                title=req.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(req,f"Todo Added From {req.user.username}....")
    else:
        form=TodoForm
    todo=Todo.objects.filter(user=req.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False 
    context={'todos':todo,
             'form':form,
             'todos_done':todos_done
             }
    return render(req,"todo.html",context)

@login_required
def update_todo(req,pk=None):
    todo =Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(req,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

def books(req):
    if req.method == "POST":
        form = SearchForm(req.POST)
        text = req.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
                
            }
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(req,"books.html",context)

    else:
        form=SearchForm()
    context={'form':form}
    return render(req,"books.html",context)

def dictionary(req):
    if req.method == "POST":
        form = SearchForm(req.POST)
        text = req.POST['text']
        url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r=requests.get(url)
        answer=r.json()
        try:
            phonetics=answer[0]['phonetics'][0]['text']
            audio=answer[0]['phonetics'][0]['audio']
            definition=answer[0]['meanings'][0]['definitions'][0]['definition']
            example=answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context={
                'form':form,
                'input':''
            }
            return render(req,"dictionary.html",context)
    else:
        form=SearchForm()
        context={'form':form}
    return render(req,"dictionary.html",context)

def wiki(req):
    if req.method == 'POST':
        text = req.POST['text']
        form = SearchForm(req.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(req,"wiki.html",context)
    else:
        form=SearchForm()
        context={'form':form}
    return render(req,"wiki.html",context)

@login_required
def conversion(req):
    if req.method == "POST":
        form = ConversionForm(req.POST)
        if req.POST['measurement']=='length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in req.POST:
                first=req.POST['measure1']
                second=req.POST['measure2']
                input=req.POST['input']
                answer = ''
                if input and int(input)>= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input*3)} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                'form':form,
                'm_form':measurement_form,
                'input':True,
                'answer':answer
                }
        if req.POST['measurement'] =='mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in req.POST:
                first=req.POST['measure1']
                second=req.POST['measure2']
                input=req.POST['input']
                answer = ''
                if input and int(input)>= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                context = {
                'form':form,
                'm_form':measurement_form,
                'input':True,
                'answer':answer
                }        

    
    else:            

        form = ConversionForm()
        context={
            'form':form,
            'input':False
    }
    return render(req,"conversion.html",context)
    

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account Has Been Created For {username}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request,'register.html',context)

""" def register(req):
    form = UserRegistrationForm()
    if req.method == "POST":
        form = UserRegistrationForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req,"User Created Successfully")
            return redirect("/")
        else:
            messages.error(req,"Incorrect Username or Password Format")
    context = {'form':form}
    return render(req,"register.html",context)
 """
""" def login_user(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req,username=username,password=password)
        if user is not None:
            login(req,user)
            messages.success(req,("Logged in Successfully"))
            return redirect("/")
        else:
            messages.error(req,("There was an error. Try Again!!!"))
            return redirect("/login")
    else:
        return render(req,"login.html") """

def logout_user(req):
    logout(req)
    messages.success(req,("Logged Out Successfully"))
    return redirect("/") 

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'homeworks' : homeworks,
        'todos'     : todos,
        'homework_done':homework_done,
        'todos_done' : todos_done
    }
    return render(request,'profile.html',context)