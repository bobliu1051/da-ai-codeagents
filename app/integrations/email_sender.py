"""
Email sending. Currently outputs to console.

Production should use SendGrid or similar. Stub left for now.
"""
import os


def send_email(to, subject, body):
    provider = os.getenv("EMAIL_PROVIDER", "console")
    if provider == "console":
        print(f"[EMAIL] to={to} subject={subject}")
        print(f"        body={body[:80]}...")
    else:
        # TODO: implement SendGrid / SES
        raise NotImplementedError(f"unknown email provider: {provider}")


def send_order_confirmation(user_id, order_id):
    # Note: pulls user email itself - violates the "service owns this" pattern
    from app.repositories.user_repo import UserRepository
    user = UserRepository().find_by_id(user_id)
    if user:
        send_email(user.email, f"Order #{order_id} confirmed", f"Thanks! Order ID: {order_id}")
