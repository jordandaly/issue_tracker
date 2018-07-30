from django.shortcuts import get_object_or_404
from issues.models import Issue


def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering every page
    """
    
    cart = request.session.get('cart', {})
    
    cart_items = []
    total = 0
    issue_upvote_count = 0
    for id, quantity in cart.items():
        issue = get_object_or_404(Issue, pk=id)
        total += quantity * issue.price
        issue_upvote_count += quantity
        cart_items.append({'id':id, 'quantity': quantity, 'issue': issue})
        
    return { 'cart_items': cart_items, 'total': total, 'issue_upvote_count': issue_upvote_count }
    