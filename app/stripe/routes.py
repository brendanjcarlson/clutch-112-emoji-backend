from flask import Blueprint
from ..models import User, Tweet, Comment, Like

stripe = Blueprint('stripe', __name__, url_prefix='/stripe')

@stripe.get('/test')
def test():
    return {'status': 'ok', 'message': 'Stripe route works'}, 200

# TODO: Create routes to handle the following:
# 1. Create a customer
# 2. Create a payment method
# 3. Create a subscription
# 4. Cancel a subscription
# 5. Update a subscription
# 6. Create a payment intent
# 7. Create a setup intent
# 8. Create a charge
# 9. Create a refund