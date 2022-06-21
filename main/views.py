import json
from django.shortcuts import redirect, render
from main.models import *
import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from foxtry2 import settings
import requests
import datetime
from django.http import JsonResponse
from main.utils import cookieCart, cartData, guestOrder

def home(request):
    context = {'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/home.html', context)

def contact(request):
    if request.method == 'POST':
        captcha_token=request.POST.get("g-recaptcha-response")
        captcha_url="https://www.google.com/recaptcha/api/siteverify"
        captcha_secret=settings.GOOGLE_RECAPTCHA_SECRET_KEY
        captcha_data={"secret":captcha_secret,"response":captcha_token}
        captcha_server_response=requests.post(url=captcha_url, data=captcha_data)
        captcha_json=json.loads(captcha_server_response.text)

        if captcha_json['success']==False:
            return redirect('main:contact')
        else:
            name = request.POST.get('fullname')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            data = {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message
            }

            temat = data['subject'] + " - " + data['name']
            html_content = render_to_string("main/nowa_wiadomosc.html", data)
            text_content = strip_tags(html_content)
            emaill = EmailMultiAlternatives(
                #temat
                temat,
                #tresc
                text_content,
                #od
                settings.EMAIL_HOST_USER,
                #do
                ['szymon.kalkowski@wp.pl', 'foxsentertainmentgroup@gmail.com']
            )
            emaill.attach_alternative(html_content, "text/html")
            emaill.send()

            temat2 = "Dziękujemy za wiadomość! - Foxtry"
            html_content2 = render_to_string("main/dziekujemy_wiadomosc.html", data)
            text_content2 = strip_tags(html_content2)
            emaill2 = EmailMultiAlternatives(
                #temat
                temat2,
                #tresc
                text_content2,
                #od
                settings.EMAIL_HOST_USER,
                #do
                [data['email']]
            )
            emaill2.attach_alternative(html_content2, "text/html")
            emaill2.send()
            
            time.sleep(3)
    context = {'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/contact.html', context)

def services(request):
    data  = cartData(request)
    cartItems = data['cartItems']
    services = Service.objects.all()
    context = {'services': services, 'cartItems': cartItems, 'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/services.html', context)

def cart(request):
    data  = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/cart.html', context)

def checkout(request):
    data  = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/checkout.html', context)

def portfolio(request):
    views=Portfolio.objects.all()
    context={'views':views, 'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/portfolio.html', context)

def view(request, id):
    view = Portfolio.objects.get(id=id)
    rows = PortfolioRow.objects.filter(portfolio=view)
    videos = PortfolioVideo.objects.filter(portfolio=view)
    context = {'view':view, 'rows':rows, 'videos':videos, 'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/view.html', context)

def about(request):
    workers=Workers.objects.all()
    context={'workers':workers, 'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/about.html', context)

def terms(request):
    context = {'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/terms.html', context)

def faq(request):
    context = {'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/faq.html', context)

def thx(request):
    context = {'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/thx.html', context)

def view_404(request, exception):
    context = {'secret_ga':settings.GOOGLE_ANALYTICS}
    return render(request, 'main/404.html', context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    customer, order = guestOrder(request, data)
    total = float(data['form']['total'].replace(",", "."))
    order.id_zamowienia = transaction_id
    if total == order.get_cart_total:
        order.ukonczone = True
    order.save()
    
    temat="Nowe zmówienie - " + data['form']['fullname']
    html_content = render_to_string("main/nowe_zamowienie.html", {'data':data['form']})
    text_content = strip_tags(html_content)
    emaill = EmailMultiAlternatives(
        #temat  
        temat,
        #tresc
        text_content,
        #od
        settings.EMAIL_HOST_USER,
        #do
        ['szymon.kalkowski@wp.pl', 'foxsentertainmentgroup@gmail.com']
    )
    emaill.attach_alternative(html_content, "text/html")
    emaill.send()

    temat2="Dziękujemy za zamówienie - Foxtry"
    html_content2 = render_to_string("main/dziekujemy_zamowienie.html", {'data': data['form']})
    text_content2 = strip_tags(html_content2)
    emaill2 = EmailMultiAlternatives(
        #temat
        temat2,
        #tresc
        text_content2,
        #od
        settings.EMAIL_HOST_USER,
        #do
        [data['form']['email']]
    )
    emaill2.attach_alternative(html_content2, "text/html")
    emaill2.send()

    return JsonResponse('Order complete', safe=False)
