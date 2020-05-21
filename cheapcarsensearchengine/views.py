from django.shortcuts import render, redirect
from .forms import SearchForm
from django.contrib import messages
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
# Create your views here.
posts_list = []

def IndexView(request):
    form = SearchForm
    search = None

    context = {
        'form':form,
        }

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = quote_plus(form.cleaned_data['search'])
          
        return redirect(f'results/{search}')

    return render(request, 'cheapcarsensearchengine/index.html', context)

def SearchResult(request, search):
    
    # data from ebay.co.uk cars 
    source = requests.get(f'https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2499334.m570.l1313.TR10.TRC0.A0.H0.Xtoyota.TRS0&_nkw={search}&_sacat=9800').text
    bsObj = BeautifulSoup(source, "lxml")
    posts = bsObj.find_all('li', {'class':'sresult lvresult clearfix li'})
    for post in posts:
        try : 
            link = post.find('div', {'class':'lvpicinner full-width picW'}).a["href"]
        except Exception as e:
            link = post.find('div', {'class':'lvpicinner full-width picW'}).a["href"]

        title = post.find('h3').text

        try : 
            img = post.find('div', {'class':'lvpicinner full-width picW'}).a.img["imgurl"]
        except Exception as e:
            img = post.find('div', {'class':'lvpicinner full-width picW'}).img["src"]
        except Exception as e:
            img = None

        
        if_bid = post.find('li', {'class':'lvformat'}).span
        if if_bid == None :
            if_bid = 'Fix price'
        else:
            if_bid = 'Auction'

        price = post.find('span', {'class':'bold'}).text.strip()

        posts_list.append((title, img, price, 'eBay.co.uk', quote_plus(title), link, if_bid))
        print(if_bid)

       
            
    context = {
        'posts_list':posts_list,
    }

    return render(request, 'cheapcarsensearchengine/SearchResult.html', context)


def DetailsView(request, ebay_link):
    
    

    for item in posts_list:
        for i in item :
            if i == ebay_link:
                source = requests.get(item[5]).text
                bsObj = BeautifulSoup(source, 'lxml')
                category = bsObj.find('li', {'class':'bc-w'}).a.span.text
                Item_specifics_in_tabel = bsObj.find('div', {'id':'viTabs_0_is'}).div
                decription_iframe = bsObj.find('div',{'id':'desc_div'}).iframe.attrs['src']
                post_ellemnts_tupel = (category, decription_iframe, Item_specifics_in_tabel) + item 

                context = {'post_ellemnts_tupel':post_ellemnts_tupel,}      

                return render(request, 'cheapcarsensearchengine/details.html', context)
        # post_ellemnts_tupel=()
        # context = {'post_ellemnts_tupel':post_ellemnts_tupel,}      
        # return render(request, 'cheapcarsensearchengine/details.html', context)
           
    
