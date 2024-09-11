from django.shortcuts import render, redirect
from .models import Question, UserAnswer, UserResult
import random
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

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
            return redirect('quiz:user_home')  # Redirect to userhome page
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz:user_home')  # Redirect to userhome page
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

        for question in questions:
            user_answer_str = selected_answers.get(f'question_{question.id}')
            
            # Check if the question was left unanswered
            if user_answer_str is None:
                user_answer = None  # Treat it as unanswered
            else:
                user_answer = user_answer_str == 'True'  # Convert the string to a boolean
            
            correct_answer = question.is_true
            is_correct = (correct_answer == user_answer) if user_answer is not None else False

            # Save the user's answer to the database
            UserAnswer.objects.create(
                user=request.user,
                question=question,
                selected_answer=user_answer,
                is_correct=is_correct
            )

            if is_correct:
                score += 1

        # Save the user's result to the database
        UserResult.objects.create(
            user=request.user,
            score=score
        )

        # Redirect to the results page with the score and total_questions
        return redirect(reverse('quiz:results', kwargs={'score': score, 'total': total_questions}))

    questions = list(Question.objects.all())
    random.shuffle(questions)

    return render(request, 'quiz/quiz.html', {'questions': questions})



@login_required
def results_view(request, score, total):
    questions = Question.objects.all()
    user_answers = {answer.question.id: answer for answer in UserAnswer.objects.filter(user=request.user)}
    score_percentage = round((score / total) * 100, 2)  # Round to 2 decimal places

    return render(request, 'quiz/results.html', {
        'questions': questions,
        'score_percentage': score_percentage,
        'user_answers': user_answers
    })

@login_required
def quiz_start(request):
    # Logic to start a new quiz
    return render(request, 'quiz/quiz.html')  # Modify as needed


@login_required
def view_profile(request):
    # Logic to show user's profile
    return render(request, 'quiz/profile.html')  # Modify as needed


@login_required
def user_home(request):
    # Logic to show user's profile
    return render(request, 'quiz/userhome.html')  # Modify as needed


@login_required
def previous_results_view(request):
    results = UserResult.objects.filter(user=request.user).order_by('-completed_at')  # Fetch and sort results by date
    average_score = results.aggregate(models.Avg('score'))['score__avg']  # Calculate average score
    return render(request, 'quiz/previous_results.html', {
        'results': results,
        'average_score': average_score
    })
