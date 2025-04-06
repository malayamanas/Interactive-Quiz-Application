from django.shortcuts import render, redirect
from .models import Question, UserAnswer, UserResult
import random
from django.urls import reverse
from django.db import models
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

from .forms import CustomUserCreationForm  # Import the custom form

        
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz:user_home')  # Redirect to userhome page
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


from django.utils import timezone
from datetime import datetime, timezone as dt_timezone  # Import Python's timezone

@login_required
def quiz_view(request):
    # Fetch all questions in the quiz
    questions = list(Question.objects.all())
    total_questions = len(questions)
    time_limit = 30  # Time limit in seconds

    # Initialize or get the current question index from session
    if 'current_question_index' not in request.session or request.method == 'GET':
        request.session['current_question_index'] = 0

        # Set the start time for the quiz when the user begins
        if 'quiz_start_time' not in request.session:
            request.session['quiz_start_time'] = timezone.now().isoformat()

        # Clear previous answers when starting a new quiz
        UserAnswer.objects.filter(user=request.user).delete()

    current_question_index = request.session['current_question_index']

    # Parse the quiz start time from the session
    quiz_start_time_str = request.session['quiz_start_time']
    quiz_start_time = datetime.fromisoformat(quiz_start_time_str).replace(tzinfo=dt_timezone.utc)

    # Calculate the elapsed time
    elapsed_time = (timezone.now() - quiz_start_time).total_seconds()

    # If time limit is exceeded, auto-submit the quiz
    if elapsed_time > time_limit:
        score = UserAnswer.objects.filter(user=request.user, is_correct=True).count()
        UserResult.objects.create(user=request.user, score=score)

        # Reset session data for a fresh start on the next quiz
        del request.session['current_question_index']
        del request.session['quiz_start_time']

        return redirect(reverse('quiz:results', kwargs={'score': score, 'total': total_questions}))

    if request.method == 'POST':
        # Handle the answer submission
        question_id = request.POST.get('question_id')
        answer = request.POST.get(f'question_{question_id}')

        if answer is not None:
            question = Question.objects.get(id=question_id)
            is_correct = (answer == question.correct_option)
            UserAnswer.objects.create(
                user=request.user,
                question=question,
                selected_option=answer,  # Use the correct field name here
                is_correct=is_correct
            )

        # Move to the next question or submit quiz
        if 'next' in request.POST:
            current_question_index += 1
        elif 'previous' in request.POST and current_question_index > 0:
            current_question_index -= 1
        elif 'submit' in request.POST or current_question_index >= total_questions - 1:
            # On submit, finalize the quiz and redirect to results page
            score = UserAnswer.objects.filter(user=request.user, is_correct=True).count()
            UserResult.objects.create(user=request.user, score=score)

            # Reset the session data for a fresh start on the next quiz
            del request.session['current_question_index']
            del request.session['quiz_start_time']

            return redirect(reverse('quiz:results', kwargs={'score': score, 'total': total_questions}))

        # Update the current question index in session
        request.session['current_question_index'] = current_question_index

    # Fetch the current question to display
    current_question = questions[current_question_index]
    is_last_question = current_question_index == total_questions - 1

    return render(request, 'quiz/quiz.html', {
        'current_question': current_question,
        'current_question_index': current_question_index,
        'total_questions': total_questions,
        'is_last_question': is_last_question,
        'time_left': max(0, time_limit - int(elapsed_time))  # Send remaining time to template
    })

@login_required
def results_view(request, score, total):
    # Fetch all questions
    questions = list(Question.objects.all())
    total_questions = len(questions)

    # Initialize or get the current result index from session
    if 'current_result_index' not in request.session or request.method == 'GET':
        request.session['current_result_index'] = 0

    current_result_index = request.session['current_result_index']

    if request.method == 'POST':
        # Navigate through results with "next" and "previous" buttons
        if 'next' in request.POST:
            current_result_index += 1
        elif 'previous' in request.POST and current_result_index > 0:
            current_result_index -= 1

        # Update the current result index in session
        request.session['current_result_index'] = current_result_index

    # Fetch the current question and user answers
    current_question = questions[current_result_index]
    user_answers = {answer.question.id: answer for answer in UserAnswer.objects.filter(user=request.user)}

    # Get the user's selected answer and the correct answer for the current question
    selected_answer = user_answers.get(current_question.id)
    selected_option = selected_answer.selected_option if selected_answer else "None"
    correct_option = current_question.correct_option

    # Calculate the percentage based on correct answers
    score_percentage = round((score / total) * 100, 2)

    # Determine if it's the last or first question
    is_last_result = current_result_index == total_questions - 1
    is_first_result = current_result_index == 0

    return render(request, 'quiz/results.html', {
        'current_question': current_question,
        'current_result_index': current_result_index,
        'total_questions': total_questions,
        'score_percentage': score_percentage,
        'user_answers': user_answers,
        'selected_option': selected_option,
        'correct_option': correct_option,
        'is_last_result': is_last_result,
        'is_first_result': is_first_result
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
