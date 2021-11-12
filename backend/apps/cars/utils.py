from django.db.models.base import Model
import requests
from bs4 import BeautifulSoup

from random import randint
from time import sleep
from itertools import cycle
import shutil

from apps.cars.models import *
from apps.cars.choices import Status


SITE = 'https://www.rockauto.com'
PROXIE_LIST_REQUEST = requests.get('http://proxy.link/list/get/50266e6be7448405f09a9309d4de5058')
PROXIES_LIST = [{'https': i} for i in PROXIE_LIST_REQUEST.text.split()]

def pick_proxie():
    for proxie in cycle(PROXIES_LIST):
        yield proxie

proxie = pick_proxie()


def get_picture(part_page_link, proxie):
    page_response = requests.get(part_page_link, proxies={'http': proxie})
    page_soup = BeautifulSoup(page_response.text, 'lxml').\
                find('img', {'class': 'listing-inline-image listing-inline-image-moreinfo'})
    return f"{SITE}{page_soup['src']}"


def download_picture(picture_link, proxie):
    filename = picture_link.split('/')[-1]
    picture_request = requests.get(picture_link, stream=True, proxies={'http': proxie})
    picture_request.raw.decode_content = True
    with open(f'pics/{filename}', 'wb') as f:
        shutil.copyfileobj(picture_request.raw, f)


# takes link, then makes request, then makes a soup
def make_soup(link, proxie):
    response = requests.get(link, proxies={'http': proxie})
    soup = BeautifulSoup(response.text, 'lxml').find_all('div', {'class': 'ranavnode'})
    return soup


def get_marks(proxie) -> list:
    soup = make_soup(SITE, proxie)
    marks = []
    for i in range(len(soup[:1])):
        mark_dict = {}

        mark = soup[i].find('a', {'id': f'navhref[{i + 1}]'})
        mark_obj, _ = Mark.objects.get_or_create(name=mark.text)

        flags = soup[i].find('td', {'class': 'rc nflags'}).find_all('span')
        for j in flags:
            country_obj, _ = Country.objects.get_or_create(name=j.text)
            mark_obj.countries.add(country_obj)
        mark_obj.save()

        mark_dict['obj'] = mark_obj
        mark_dict['link'] = SITE + mark['href']

        marks.append(mark_dict)
    return marks


def get_years(mark_link, mark_obj, proxie) -> list:
    soup = make_soup(mark_link, proxie)
    years = []
    for year in soup[1:]:
        year_dict = {}

        _year = year.find('a', {'class': 'navlabellink nvoffset nnormal'})
        year_obj, _ = Year.objects.get_or_create(
            year=int(_year.text), mark=mark_obj
        )

        flags = year.find('td', {'class': 'rc nflags'}).find_all('span')
        for j in flags:
            country_obj, _ = Country.objects.get_or_create(name=j.text)
            year_obj.countries.add(country_obj)
        year_obj.save()

        year_dict['obj'] = year_obj
        year_dict['link'] = SITE + _year['href']

        years.append(year_dict)
    return years


def get_models(year_link, year_obj, proxie) -> list:
    soup = make_soup(year_link, proxie)
    models = []
    for model in soup[2:3]:
        model_dict = {}

        _model = model.find('a', {'class': 'navlabellink nvoffset nnormal'})
        mark_model_obj, _ = MarkModel.objects.get_or_create(
            name=_model.text, year=year_obj
        )

        model_dict['obj'] = mark_model_obj
        model_dict['link'] = SITE + _model['href']

        models.append(model_dict)
    return models


def get_complectations(model_link, mark_model_obj, proxie) -> list:
    soup = make_soup(model_link, proxie)
    complectations = []
    for complectation in soup[3:4]:
        complectation_dict = {}

        _complectation = complectation.find('a', {'class': 'navlabellink nvoffset nnormal'})
        complectation_obj, _ = Complectation.objects.get_or_create(
            name=_complectation.text,
            mark_model=mark_model_obj
        )

        complectation_dict['obj'] = complectation_obj
        complectation_dict['link'] = SITE + _complectation['href']

        complectations.append(complectation_dict)
    return complectations


def get_details(complectation_link, complectation_obj, proxie) -> list:
    soup = make_soup(complectation_link, proxie)
    details = []
    for detail in soup[4:5]:
        detail_dict = {}

        _detail = detail.find('a', {'class': 'navlabellink nvoffset nnormal'})
        detail_obj, _ = Detail.objects.get_or_create(
            name=_detail.text, complectation=complectation_obj
        )

        detail_dict['obj'] = detail_obj
        detail_dict['link'] = SITE + _detail['href']

        details.append(detail_dict)
    return details


def get_sub_details(detail_link, detail_obj, proxie) -> list:
    soup = make_soup(detail_link, proxie)
    subdetails = []
    for subdetail in soup[5:6]:
        subdetail_dict = {}

        _subdetail_normal = subdetail.find('a', {'class': 'navlabellink nvoffset nnormal'})
        _subdetail = subdetail.find('a', {'class': 'navlabellink nvoffset nimportant'})
        
        if _subdetail_normal is not None:
            subdetail_name = _subdetail_normal.text
            
        if _subdetail is not None:
            subdetail_name = _subdetail.text

        subdetail_obj, _ = SubDetail.objects.get_or_create(
            name=subdetail_name,
            detail=detail_obj
        )
        
        subdetail_dict['obj'] = subdetail_obj
        subdetail_dict['link'] = SITE + _subdetail['href']

        subdetails.append(subdetail_dict)
    return subdetails


def get_parts(sub_detail_link, sub_detail_obj, proxie):
    parts_response = requests.get(sub_detail_link, proxies={'http': proxie})
    parts_soup = BeautifulSoup(parts_response.text, 'lxml').find_all('a', {'class': 'ra-btn ra-btn-moreinfo'})
    table = BeautifulSoup(parts_response.text, 'lxml').find_all('tbody', {'class': 'listing-inner'})
    for i in table:
        name = ' '.join([
            i.text for i in i.find('div', {'class': 'listing-text-row-moreinfo-truck'}).find_all('span')
        ])
        price = i.find('span', {'class': 'ra-formatted-amount listing-price listing-amount-bold'}).text

        part_obj, _ = Part.objects.get_or_create(name=name, sub_detail=sub_detail_obj)

        if price == 'See Options at Left':
            choices = i.find('select', {'class': 'listing-optionchoice-multiple'}).find_all('option')
            for i in choices[1:]:
                variety = str(i.text.split('{')[0])
                variety_title = variety.split('$')[0].replace('(', '')
                variety_price = variety.split('$')[1].replace(')', '').replace(' ', '')
                part_variety, _ = PartVariety.objects.get_or_create(
                    name=variety_title,
                    part=part_obj
                )
                part_variety.price = float(variety_price)
                part_variety.save()
        elif price == 'Out of Stock':
            part_obj.status = Status.OOS
        else:
            part_obj.price = float(price.split('$')[1])
        part_obj.save()

    parts = []
    for part in parts_soup:
        parts.append(part['href'])
    return parts


def main():
    marks = get_marks(next(proxie))

    for mark in marks:
        years = get_years(mark['link'], mark['obj'],next(proxie))
        sleep(1)

        for year in years:
            models = get_models(year['link'], year['obj'], next(proxie))
            sleep(1)

            for model in models:
                complectations = get_complectations(
                    model['link'], model['obj'], next(proxie)
                )
                sleep(1)

                for complectation in complectations:
                    details = get_details(
                        complectation['link'], complectation['obj'], next(proxie)
                    )
                    sleep(1)

                    for detail in details:
                        sub_details = get_sub_details(
                            detail['link'], detail['obj'],  next(proxie)
                        )
                        sleep(1)

                        for sub_detail in sub_details:
                            parts = get_parts(
                                sub_detail['link'], sub_detail['obj'], next(proxie)
                            )
                            sleep(1)


def delete_all():
    Country.objects.all().delete()
    Mark.objects.all().delete()
    Year.objects.all().delete()
    MarkModel.objects.all().delete()
    Complectation.objects.all().delete()
    Detail.objects.all().delete()
    SubDetail.objects.all().delete()
    Part.objects.all().delete()
    PartVariety.objects.all().delete()
    return
