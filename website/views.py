from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code

import openai
import os

openai.api_key = os.getenv('OPENAI_SECRET_KEY')

def home(request):

    code_list = ['bash', 'c', 'clike', 'cpp', 'csharp', 'css', 'django', 'docker', 'graphql', 'javascript', 'javadoclike',
                'jsx', 'mongodb', 'php', 'php-extras', 'phpdoc', 'powershell', 'python', 'regex', 'scss', 'sql', 'tsx', 'typescript']
    has_code = False
    response = ''
    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']
        if code != '':
            has_code = True

    else:
        code = 'print("Hello World")'
        lang = 'python'
    ## response = code

    if lang == "Select Programming Language":
        lang = "python"

    # Only send code to OpenAI if the user has entered code.
    if has_code:
        try:
            openai_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Respond only with code. Can you fix my code? \n\nCode:\n{code}\n\it's using the following Language: {lang}\n Response:",
                temperature=0,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            response = (openai_response['choices'][0]['text']).strip()
            update_db = Code(question=code, code_answer=response, language=lang, user=request.user)
            update_db.save()

        except Exception as e:
            code = e

    context = {
        'code': code,
        'response': response,
        'lang': lang,
        'code_list': code_list
    }

    return render(request, 'home.html', context)

def suggest(request):
    if not request.user.is_authenticated:
        return redirect('home')

    code_list = ['bash', 'c', 'clike', 'cpp', 'csharp', 'css', 'django', 'docker', 'graphql', 'javascript', 'javadoclike',
                'jsx', 'mongodb', 'php', 'php-extras', 'phpdoc', 'powershell', 'python', 'regex', 'scss', 'sql', 'tsx', 'typescript']
    has_code = False
    response = ''
    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']
        if code != '':
            has_code = True

    else:
        code = 'Write a function that takes in a string and returns the string reversed.'
        lang = 'python'
    ## response = code

    if lang == "Select Programming Language":
        lang = "python"

    # Only send code to OpenAI if the user has entered code.
    if has_code:
        try:
            openai_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Respond only with code. Code:\n{code}\n in the coding language {lang}\n\Response:",
                temperature=0,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            response = (openai_response['choices'][0]['text']).strip()
            update_db = Code(question=code, code_answer=response, language=lang, user=request.user)
            update_db.save()
        except Exception as e:
            code = e

    context = {
        'code': code,
        'response': response,
        'lang': lang,
        'code_list': code_list,
        }


    return render(request, 'suggest.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request, 'home.html',{})


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def past(request):
    if request.user.is_authenticated:
        code = Code.objects.filter(user_id=request.user.id)
        return render(request, 'past.html', {"code": code})
    else:
        return redirect('home')


def delete_past(request, past_id):
    past = get_object_or_404(Code, pk=past_id)
    if past.user == request.user:
        past.delete()
    else:
        return redirect('home')

    return redirect('past')



