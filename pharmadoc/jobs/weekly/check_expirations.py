from django_extensions.management.jobs import WeeklyJob


class Job(WeeklyJob):
    help = ""

    def execute(self):
        from django.conf import settings
        from datetime import datetime, timedelta
        from pharmadoc.models import Pharmacy, Person, Submission, DrugClass, Company, Order, Profile
        from django.core.mail import send_mail, EmailMessage
        from django.core import management
        from django.template.loader import render_to_string
        import sys

        try:
            recipients = Profile.objects.filter(get_expiration_info = True)
            if recipients:
                for recipient in recipients:
                    delta = 7
                    today = datetime.now().date()
                    orderlist = Order.objects.filter(state='active').order_by('expiry_date')
                    for o in orderlist:
                        if o.expiry_date > today + timedelta(days=7) or o.expiry_date < today:
                            orderlist = orderlist.exclude(pk=o.pk)
                    if len(orderlist)>0:                        
                        message = render_to_string('mail/expiration_mail.html',{'delta':delta, 'orderlist':orderlist, 'first_name':recipient.user.first_name})
                        subject = "Pharmacy Expirations" 
                        msg = EmailMessage(subject, message, "noreply@leibniz-fli.de", [recipient.user.email])
                        msg.content_subtype = "html"
                        msg.send()
        except BaseException as e:
            TEC_ADMIN_EMAIL = getattr(settings, "TEC_ADMIN_EMAIL", None)
            send_mail("Pharmacy Scriptfehler Check Expirations", 'Fehler {} in Zeile {}'.format(e,sys.exc_info()[2].tb_lineno), TEC_ADMIN_EMAIL, [TEC_ADMIN_EMAIL])
