from django.shortcuts import render

# Create your views here.

def home(request):
    code_list = ['bash', 'c', 'clike', 'cpp', 'csharp', 'css', 'django', 'docker', 'graphql', 'javascript', 'javadoclike',
                'jsx', 'mongodb', 'php', 'php-extras', 'phpdoc', 'powershell', 'python', 'regex', 'scss', 'sql', 'tsx', 'typescript']

    return render(request, 'home.html', {'code_list': code_list})

