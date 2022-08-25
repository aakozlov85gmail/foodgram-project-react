import csv

from django.http.response import HttpResponse
from django.db.models import Sum


def get_csv_shopping_cart(ingredient_recipe):
    ingredients = ingredient_recipe.values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(ingredient_amount=Sum('amount')).values_list(
        'ingredient__name', 'ingredient_amount',
        'ingredient__measurement_unit',
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = ('attachment;'
                                       'filename="Shoppingcart.csv"')
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    for item in list(ingredients):
        writer.writerow(item)
    return response
