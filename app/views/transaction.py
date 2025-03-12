from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Transaction

@login_required
def user_transactions(request):
    transactions_list = Transaction.objects.filter(openai_request__audio_record__user=request.user).order_by('-created_at')
    
    # Pagination - 10 transactions per page
    paginator = Paginator(transactions_list,4)
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)

    return render(request, "transactions.html", {"transactions": transactions})
