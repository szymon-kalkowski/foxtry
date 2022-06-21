import email
from pyexpat import model
from django.db import models


class Workers(models.Model):
    zdjecie=models.FileField(blank=False)
    imie_i_nazwisko=models.CharField(max_length=100)
    specjalizacja=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    linkedin=models.CharField(max_length=300)

    def __str__(self):
        return self.imie_i_nazwisko
    
    class Meta:
        verbose_name="Pracownik"
        verbose_name_plural="Pracownicy"

class Portfolio(models.Model):
    miniaturka=models.FileField(blank=False)
    logo=models.FileField(blank=True)
    nazwa=models.CharField(max_length=300, blank=False)
    link=models.CharField(max_length=400, blank=True)
    grafika=models.FileField(blank=True)
    grafika_mobilna=models.FileField(blank=True) 
    opis=models.TextField(blank=True)
   
    class Meta:
        verbose_name="Portfolio"
        verbose_name_plural="Portfolio"
    
    def __str__(self):
        return self.nazwa

class PortfolioRowType(models.Model):
    def __str__(self):
        return self.nazwa
    nazwa = models.CharField(max_length=60)

class PortfolioRow(models.Model):
    portfolio = models.ForeignKey(Portfolio, default=None, on_delete=models.CASCADE)
    portfolioRowType = models.ForeignKey(PortfolioRowType, null=True, blank=True, on_delete=models.CASCADE)
    photo1 = models.FileField(blank=True)
    photo2 = models.FileField(blank=True)

    def __str__(self):
        return self.portfolio.nazwa

class PortfolioVideo(models.Model):
    portfolio = models.ForeignKey(Portfolio, default=None, on_delete=models.CASCADE)
    link = models.CharField(max_length=300)

    def __str__(self):
        return self.portfolio.nazwa

class Service(models.Model):
    nazwa = models.CharField(max_length=300)
    opis = models.TextField(max_length=400)
    cena = models.DecimalField(max_digits=8, decimal_places=2)
    cena_wyswietlana = models.CharField(max_length=100)
    zdjecie = models.FileField(blank=False)

    class Meta:
        verbose_name = "Usługa"
        verbose_name_plural = "Usługi"

    def __str__(self):
        return self.nazwa

class Customer(models.Model):
    imie = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    firma = models.CharField(max_length=200, null=True)
    numer = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.imie

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"

class Order(models.Model):
    klient = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    data_zamowienia = models.DateTimeField(auto_now_add=True)
    ukonczone = models.BooleanField(default=False, null=True, blank=False)
    id_zamowienia = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.ilosc for item in orderitems])
        return total

class OrderItem(models.Model):
    usluga = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True)
    zamowienie = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    ilosc = models.IntegerField(default=0, null=True, blank=True)
    data_dodania = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.usluga.cena * self.ilosc
        return total
