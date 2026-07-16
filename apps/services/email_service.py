import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

class EmailService:
    def send_contact_notification(self, contact_data: dict) -> bool:
        try:
            # Письмо владельцу
            owner_message = f"""
Новое обращение с сайта:

Имя: {contact_data['name']}
Телефон: {contact_data['phone']}
Email: {contact_data['email']}

Сообщение:
{contact_data['comment']}

---
Отправлено через API контактной формы
            """
            
            send_mail(
                subject=f"Новое сообщение от {contact_data['name']}",
                message=owner_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            # Письмо пользователю
            user_message = f"""
Здравствуйте, {contact_data['name']}!

Спасибо за ваше сообщение. Мы получили его и свяжемся с вами в ближайшее время.

Ваше сообщение:
{contact_data['comment']}

С уважением,
Команда разработчиков

---
Это автоматическое письмо, не отвечайте на него.
            """
            
            send_mail(
                subject="Спасибо за ваше сообщение!",
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact_data['email']],
                fail_silently=False,
            )
            
            logger.info(f"Email sent to {contact_data['email']}")
            return True
            
        except Exception as e:
            logger.error(f"Email sending failed: {e}", exc_info=True)
            return False

email_service = EmailService()