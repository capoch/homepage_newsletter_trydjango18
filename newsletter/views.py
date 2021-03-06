from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse
from django.conf import settings
# from django.contrib.auth.models import User, Permission

from .forms import SignUpForm, ContactForm
from .models import SignUp

# Create your views here.
def home(request):
    title = "Sign up now!"
    form = SignUpForm(request.POST or None)
    context = {
        "title" : title,
        "form" :  form,
    }

    if form.is_valid():
        instance = form.save(commit=False)
        full_name = form.cleaned_data.get('full_name')
        if not full_name:
            full_name = "Not specified"
        instance.full_name = full_name
        instance.save()
        context = {
            "title" : "Thank you",
        }

    if request.user.is_authenticated() and request.user.is_staff:
        queryset = SignUp.objects.all().order_by('-timestamp')
        # print(queryset)
        context = {
            "queryset": queryset
        }
    return render(request, "home.html", context)


def contact(request):
    form = ContactForm(request.POST or None)
    title_align_center = True
    context = {
        "title":"Contact Form",
        "form":form,
        "title_align_center":title_align_center,

    }
    if form.is_valid():
        # since it's not connected to a model we can't just save databases
        full_name = form.cleaned_data.get('full_name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')
        from_email = settings.EMAIL_HOST_USER
        to_email = [email, 'sorryyoucanthavemyemail@gmail.com']
        send_mail(
            'Site contact form: Message from {i}'.format(i=full_name),
            message,
            from_email,
            to_email,
            fail_silently=False,
        )
        context = {
            "title":"We will reply in due time"

        }
    return render(request, "forms.html", context)
