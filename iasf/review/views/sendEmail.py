from django.views import View
from django.utils import timezone
from django.urls import reverse_lazy
from iasf.apply.models import Application
from iasf.review.mixins import UserIsStaffMixin
from django.core.mail import send_mass_mail, EmailMessage
from django.conf import settings
from django.http import HttpResponseRedirect
    
class SendEmail(UserIsStaffMixin, View):
    def post(self, request, *args, **kwargs):
        """Send mass emails."""
        emails = self.request.POST['recipients'].split(",")
        emails.append(self.request.user.email) # send the email to this user, too.
        emails = [email.strip() for email in emails if email.strip()]
        print(emails)
        subject = self.request.POST['subject']
        body = self.request.POST['body']
        messages = [(subject, body, settings.DEFAULT_FROM_EMAIL, (email,)) for email in emails]
        send_mass_mail(messages, fail_silently=False)

        # self.request.user.email_user(subject, body, settings.DEFAULT_FROM_EMAIL)
        
        # msg = EmailMessage(
        #   subject=subject,
        #   body=body,
        #   from_email=settings.DEFAULT_FROM_EMAIL,
        #   to=["aramaswamis+44@gmail.com"],
        #   bcc=emails
        # ).send()
        # todo: split up (share same connection but less emails per batch. sendgrid max is around 1000)
        return HttpResponseRedirect(reverse_lazy('review:send-email-success'))