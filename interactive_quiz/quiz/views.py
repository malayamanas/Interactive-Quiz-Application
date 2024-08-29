from django.shortcuts import render, redirect
from .models import Question
import random
from django.urls import reverse


# views.py
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
