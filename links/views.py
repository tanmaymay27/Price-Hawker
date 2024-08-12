from django.shortcuts import render, redirect
from .models import Link
from .forms import AddLinkForm
from django.views.generic import DeleteView
from django.urls import reverse_lazy
import pandas as pd
from django.http import JsonResponse

# Create your views here.
def main_func(request):
    return render(request,'links/homepage.html')

def home_view(request):
    no_discounted=0
    error = None

    form = AddLinkForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()

        except AttributeError:
            error = "oops ... couldnt get name or price"

        except:
            error = "something went wrong"

    form = AddLinkForm()


    qs = Link.objects.all()
    items_no = qs.count()

    if items_no>0:
        discount_list = []
        for item in qs:
            if item.old_price > item.current_price:
                discount_list.append(item)
                no_discounted=len(discount_list)

    context = {
        'qs':qs,
        'items_no' : items_no,
        'no_discounted': no_discounted,
        'form': form,
        'error' : error,
    }   

    return render(request,'links/main.html',context)                           


class LinkDeleteView(DeleteView):
    model = Link
    template_name = 'links/confirm_del.html'
    success_url = reverse_lazy('tracker')


def update_prices(request):
    qs = Link.objects.all()
    for link in qs:
        link.save()
        return redirect('tracker')

def export_data_to_excel(request):
    objs = Link.objects.all();

    data = []

    for obj in objs:
        data.append({
            'name' : obj.name,
            'current_price' : obj.current_price,
            'old_price' : obj.old_price,
            'price_difference' : obj.price_difference,
            'url' : obj.url,
        })

    pd.DataFrame(data).to_excel('Data.xlsx')

    