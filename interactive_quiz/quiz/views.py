from django.shortcuts import render, redirect
from .models import Question
import random
from django.urls import reverse


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

            if correct_answer == (user_answer == 'True'):
                score += 1

        # Store the user answers in session
        request.session['user_answers'] = user_answers

        # Redirect to the results page with the score and total_questions
        return redirect(reverse('quiz:results', kwargs={'score': score, 'total': total_questions}))

    questions = list(Question.objects.all())
    random.shuffle(questions)

    return render(request, 'quiz/quiz.html', {'questions': questions})


def results_view(request, score, total):
    questions = Question.objects.all()
    user_answers = request.session.get('user_answers', {})
    score_percentage = round((score / total) * 100, 2)  # Round to 2 decimal places
    return render(request, 'quiz/results.html', {'questions': questions, 'score_percentage': score_percentage, 'user_answers': user_answers})
