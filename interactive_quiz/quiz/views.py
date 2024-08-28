from django.shortcuts import render, redirect
from .models import Question
import random
from django.urls import reverse

def quiz_view(request):
    if request.method == 'POST':
        selected_answers = request.POST
        score = 0
        questions = Question.objects.all()

        for question in questions:
            correct_answer = question.is_true
            user_answer = selected_answers.get(f'question_{question.id}') == 'True'

            if correct_answer == user_answer:
                score += 1

        # Redirect to the results page with the score parameter
        return redirect(reverse('quiz:results', kwargs={'score': score}))

    questions = list(Question.objects.all())
    random.shuffle(questions)
    selected_questions = questions[:5]

    return render(request, 'quiz/quiz.html', {'questions': selected_questions})

def results_view(request, score):
    questions = Question.objects.all()
    return render(request, 'quiz/results.html', {'questions': questions, 'score': score})
