from django.shortcuts import render, redirect
from .models import Question
import random
from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('quiz:login')  # Redirect to the login page after logout

def home_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('quiz')
    else:
        form = UserCreationForm()
    return render(request, 'home.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('quiz:quiz')  # Redirect to quiz page
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz:quiz')  # Redirect to quiz page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def quiz_view(request):
    if request.method == 'POST':
        selected_answers = request.POST
        score = 0
        questions = Question.objects.all()
        total_questions = questions.count()

        user_answers = {}

        for question in questions:
            user_answer = selected_answers.get(f'question_{question.id}')
            user_answers[f'question_{question.id}'] = user_answer
            correct_answer = question.is_true

            # Debug print statements
            print(f"Question ID: {question.id}")
            print(f"User Answer: {user_answer}")
            print(f"Correct Answer: {correct_answer}")

            if correct_answer == (user_answer == 'True'):
                score += 1

        # Store the user answers in session
        request.session['user_answers'] = user_answers

        # Debug print statement
        print(f"User Answers in Session: {request.session['user_answers']}")

        # Redirect to the results page with the score and total_questions
        return redirect(reverse('quiz:results', kwargs={'score': score, 'total': total_questions}))

    questions = list(Question.objects.all())
    random.shuffle(questions)

    return render(request, 'quiz/quiz.html', {'questions': questions})

def results_view(request, score, total):
    questions = Question.objects.all()
    user_answers = request.session.get('user_answers', {})
    score_percentage = round((score / total) * 100, 2)  # Round to 2 decimal places

    # Debug print statements
    print(f"User Answers from Session: {user_answers}")
    for question in questions:
        print(f"Question ID: {question.id}")
        print(f"User Answer for Question ID {question.id}: {user_answers.get(f'question_{question.id}')}")

    return render(request, 'quiz/results.html', {'questions': questions, 'score_percentage': score_percentage, 'user_answers': user_answers})
