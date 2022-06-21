import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            service = Service.objects.get(id=i)
            total = (service.cena * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'service': {
                    'id': service.id,
                    'nazwa': service.nazwa,
                    'cena': service.cena,
                    'cena_wyswietlana': service.cena_wyswietlana,
                    'zdjecie': service.zdjecie.url,
                },
                'ilosc': cart[i]["quantity"],
                'get_total': total
            }
            items.append(item)
        except:
            pass

    return {'cartItems': cartItems, 'order':order, 'items':items}

def cartData(request):
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']
    return {'cartItems': cartItems, 'order':order, 'items':items}

def guestOrder(request, data):
    print('COOKIES', request.COOKIES)
    name = data['form']['fullname']
    email = data['form']['email']
    nr = data['form']['nr']
    com = data['form']['com']

    cookieData = cookieCart(request)
    items = cookieData['items']

    klient, created = Customer.objects.get_or_create(
        email=email,
    )
    klient.imie = name
    klient.email = email
    klient.firma = com
    klient.numer = nr
    klient.save()

    order = Order.objects.create(
        klient=klient,
        ukonczone=False,
    )

    for item in items:
        service = Service.objects.get(id=item['service']['id'])

        orderItem = OrderItem.objects.create(
            usluga=service,
            zamowienie=order,
            ilosc=item['ilosc']
        )

    return klient, order