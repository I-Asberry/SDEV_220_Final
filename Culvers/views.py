from django.shortcuts import render
from django.views import View
from .models import MenuItem, Category, Ordering

# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Culvers/index.html')




class Order(View):
    def get(self, request, *args, **kwargs):
        
        #get item from each category
        Entrees = MenuItem.objects.filter(category__name__contains='Entree')
        Sides = MenuItem.objects.filter(category__name__contains='Side')
        Desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        Drinks = MenuItem.objects.filter(category__name__contains='Drink')
        Sauces = MenuItem.objects.filter(category__name__contains='Sauce')
        
        #pass into context
        context = {
            'Entrees': Entrees,
            'Sides': Sides,
            'Desserts': Desserts,
            'Drinks': Drinks,
            'Sauces': Sauces, 
        }

        #render templates
        return render(request, 'Culvers/order.html', context)
    
    #method to calculate total
    def post(self, request, *args, **kwargs):
        #order item dictionary with a list of items
        order_items = {
            'items': []
        }

        #grab all selected items
        items = request.POST.getlist('items[]')
        #get the item data for each selected item
        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name':menu_item.name,
                'price': menu_item.price
            }

            #append selected data to a list
            order_items['items'].append(item_data)

            #price and item id variables
            price = 0
            item_ids = []

        #loop through and get the price and id
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])


        #set price to total price
        order = Ordering.objects.create(price=price)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }
        #go to confirmation page
        return render(request, 'Culvers/order_confirmation.html', context)