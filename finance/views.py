from django.shortcuts import render, redirect
from accounts.models import User
from .models import Category , Expense, Income
from django.db.models import Sum 

def create_category(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # se não estiver logado

    # pega a instância do User
    user = User.objects.get(id_user=user_id)

    if request.method == "POST":
        name = request.POST.get("name")

        Category.objects.create(
            name=name,
            user=user  # <- usa a instância, não o ID
        )

        return redirect("create_category")

    return render(request, "finance/create_category.html")



def create_income(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id_user=user_id)

    # categorias só deste user (para o dropdown)
    categories = Category.objects.filter(user=user)

    error = None

    if request.method == "POST":
        category_id = request.POST.get("category")   # vem do <select>
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        date = request.POST.get("date")

        # valida categoria (garante que é do user)
        try:
            category = Category.objects.get(id=category_id, user=user)
        except Category.DoesNotExist:
            error = "Categoria inválida."
            return render(request, "finance/create_income.html", {
                "categories": categories,
                "error": error
            })

        Income.objects.create(
            user=user,
            category=category,
            amount=amount,
            description=description,
            date=date
        )

        return redirect("list_incomes")  # ou dashboard

    return render(request, "finance/create_income.html", {
        "categories": categories,
        "error": error
    })


def list_categories(request):
    error = None
    user_id = request.session.get('user_id')

    if not user_id:
        error ="you did not login"
        return redirect('login') 
    else:
        user = User.objects.get(id_user=user_id)

    categories = Category.objects.filter(user=user)

    return render(request, "finance/list_categories.html", {
        "categories": categories
    })

def list_incomes(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  

    user = User.objects.get(id_user=user_id)

    incomes = Income.objects.filter(user=user)

    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0

    return render(
        request,
        'finance/list_incomes.html',
        {
            'incomes': incomes,
            'user': user,
            'total_income': total_income
        }
    )

def list_expenses(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  

    user = User.objects.get(id_user=user_id)

    expenses = Expense.objects.filter(user=user)

    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0

    return render(
        request,
        'finance/list_expenses.html',
        {
            'expenses': expenses,
            'user': user,
            'total_expense': total_expense
        }
    )

def create_expense(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id_user=user_id)
    categories = Category.objects.filter(user=user)

    error = None

    if request.method == "POST":
        category_id = request.POST.get("category")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        date = request.POST.get("date")

        try:
            category = Category.objects.get(id=category_id, user=user)
        except Category.DoesNotExist:
            error = "Categoria inválida."
            return render(request, "finance/create_expenses.html", {
                "categories": categories,
                "error": error
            })

        Expense.objects.create(
            user=user,
            category=category,
            amount=amount,
            description=description,
            date=date
        )

        return redirect("list_expenses")

    return render(request, "finance/create_expenses.html", {
        "categories": categories,
        "error": error
    })

    
def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  

    user = User.objects.get(id_user=user_id)

    incomes = Income.objects.filter(user=user)

    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0

    return render(
        request,
        'finance/dashboard.html',
        {
            'incomes': incomes,
            'user': user,
            'total_income': total_income
        }
    )
