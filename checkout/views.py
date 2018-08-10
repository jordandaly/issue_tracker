from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import Order, OrderLineItem
from django.conf import settings
from django.utils import timezone
from issues.models import Issue
from issues.views import get_issues
import stripe


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

@login_required()
def checkout(request):
    if request.method=="POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        
        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            
            cart = request.session.get('cart', {})
            total = 0
            for id, quantity in cart.items():
                issue = get_object_or_404(Issue, pk=id)
                total += quantity * issue.price
                order_line_item = OrderLineItem(
                    order = order, 
                    issue = issue, 
                    quantity = quantity
                    )
                order_line_item.save()
                
            try:
                customer = stripe.Charge.create(
                    amount = int(total * 100),
                    currency = "EUR",
                    description = request.user.email,
                    card = payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
                
            if customer.paid:
                messages.success(request, "You have successfully paid")
                '''If customer has paid increase each Issue Upvotes by quantity of items paid'''
                for id, quantity in cart.items():
                    issue = Issue.objects.get(pk=id)
                    issue.upvotes += quantity
                    issue.save()

                request.session['cart'] = {}
                return redirect(reverse('get_issues'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
        
    return render(request, "checkout.html", {'order_form': order_form, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})
                
            