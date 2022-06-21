from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('kontakt/', contact, name='contact'),
    path('uslugi/', services, name='services'),
    path('portfolio/', portfolio, name='portfolio'),
    path('portfolio/<int:id>', view, name='view'),
    path('onas/', about, name='about'),
    path('regulamin/', terms, name='terms'),
    path('faq/', faq, name='faq'),
    path('dziekujemy/', thx, name='thx'),
    path('koszyk/', cart, name='cart'),
    path('podsumowanie/', checkout, name='checkout'),
    path('process_order/', processOrder, name="process_order"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)