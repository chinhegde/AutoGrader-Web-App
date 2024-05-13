from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from .grading import grade_solution
from .dynamodb_utils import save_score_to_dynamodb

@login_required
def problem_view(request):
    if request.method == 'POST':
        solution_text = request.POST.get('solution', '')  # Get solution from text area
        solution_file = request.FILES.get('file')  # Get solution from uploaded file

        if solution_text:
            solution = solution_text
        elif solution_file:
            solution = solution_file.read().decode('utf-8')  # Read file content
        else:
            return HttpResponse("No solution provided.")

        # Print solution
        print("Received solution:")
        print(solution)
        # Grade the solution
        score, test_results = grade_solution(solution)
        print("BEFORE RENDER SCORE: ", score)

        # TODO: Save student score to dynamodb with useremail and best score
        # If no score yet, save student with current score
        # If score exists, update score only if current score > current best_score

        # Get the current user
        user = request.user

        # Get the user's email
        user_email = user.email

        # Get or create the student record
        student, created = Student.objects.get_or_create(user=user)

        # If the student doesn't have a best score yet or the current score is better than the best score, update it
        if not student.best_score or score > student.best_score:
            student.best_score = score
            student.save()

            # TODO: Save the score to DynamoDB, using email and best score
            save_score_to_dynamodb(user_email, score)

        return render(request, 'problem.html', {'score': score, 'test_results': test_results})

    return render(request, 'problem.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to success page or login page
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')