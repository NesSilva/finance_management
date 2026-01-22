from django.shortcuts import render, redirect
from accounts.models import User
from .models import Category , Expense, Income
from django.db.models import Sum 
from django.utils import timezone
from django.db.models.functions import TruncDay



def create_category(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = User.objects.get(id_user=user_id)

    if request.method == "POST":
        name = request.POST.get("name")

        Category.objects.create(
            name=name,
            user=user  
        )

        return redirect("create_category")

    return render(request, "finance/create_category.html")



def create_income(request):
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

        return redirect("list_incomes")

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
    today = timezone.now().date()
    incomes = Income.objects.filter(
        user=user,
        date__year=today.year,
        date__month=today.month        
    )

    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0

    return render(
        request,
        'finance/list_incomes.html',
        {
            'incomes': incomes,
            'user': user,
            'total_income': total_income,
            'date_year': today.year,
            'date_month': today.month
        }
    )

def list_expenses(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id_user=user_id)

    today = timezone.now().date()

    expenses = Expense.objects.filter(
        user=user,
        date__year=today.year,
        date__month=today.month
    )

    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0

    return render(
        request,
        'finance/list_expenses.html',
        {
            'expenses': expenses,
            'user': user,
            'total_expense': total_expense,
            'date_year': today.year,
            'date_month': today.month
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
    today = timezone.now().date()
    year = today.year

    incomes_year = Income.objects.filter(user=user, date__year=year)
    expenses_year = Expense.objects.filter(user=user, date__year=year)

    total_income = incomes_year.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = expenses_year.aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    incomes_last = Income.objects.filter(user=user).order_by('-date')[:5]

    income_by_month_qs = (
        incomes_year
        .values('date__month')
        .annotate(total=Sum('amount'))
        .order_by('date__month')
    )

    expense_by_month_qs = (
        expenses_year
        .values('date__month')
        .annotate(total=Sum('amount'))
        .order_by('date__month')
    )

    income_map = {row['date__month']: float(row['total']) for row in income_by_month_qs}
    expense_map = {row['date__month']: float(row['total']) for row in expense_by_month_qs}

    months = list(range(1, 13))
    chart_income = [income_map.get(m, 0) for m in months]
    chart_expense = [expense_map.get(m, 0) for m in months]
    chart_balance = [chart_income[i] - chart_expense[i] for i in range(12)]

    month_labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    return render(request, 'finance/dashboard.html', {
        'user': user,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'incomes': incomes_last,  
        'chart_year': year,
        'month_labels': month_labels,
        'chart_income': chart_income,
        'chart_expense': chart_expense,
        'chart_balance': chart_balance,
    })
