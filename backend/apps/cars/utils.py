import requests
from bs4 import BeautifulSoup

from random import randint
from time import sleep
from itertools import cycle
import shutil


SITE = 'https://www.rockauto.com'

PROXIE_LIST_REQUEST = requests.get('http://proxy.link/list/get/50266e6be7448405f09a9309d4de5058')

PROXIES_LIST = [{'https': i} for i in PROXIE_LIST_REQUEST.text.split()]


def pick_proxie():
    for proxie in cycle(PROXIES_LIST):
        yield proxie

proxie = pick_proxie()


# takes link, then makes request, then makes a soup
def make_soup(link, proxie):
    response = requests.get(link, proxies={'http': proxie})
    soup = BeautifulSoup(response.text, 'lxml').find_all('div', {'class': 'ranavnode'})
    return soup


def get_marks(proxie) -> dict:
    soup = make_soup(SITE, proxie)
    marks = {}
    for i in range(len(soup[:13])):
        mark = soup[i].find('a', {'id': f'navhref[{i + 1}]'})
        # flag = soup[i].find('td', {'class': 'rc nflags'}).find_all('span')
        # print(mark.text)
        # for j in flag:
        #     print(j.text)
        # print('-'*80)
        marks[mark.text] = SITE + mark['href']
    return marks


def get_years(mark_link, proxie) -> dict:
    soup = make_soup(mark_link, proxie)
    years = {}
    for year in soup[1:2]:
        _year = year.find('a', {'class': 'navlabellink nvoffset nnormal'})
        # flag = year.find('td', {'class': 'rc nflags'}).find_all('span')
        # for j in flag:
        #     print(_year.text)
        #     print(j.text)
        # print('-'*80)
        years[_year.text] = SITE + _year['href']
    return years


def get_models(year_link, proxie) -> dict:
    soup = make_soup(year_link, proxie)
    models = {}
    for model in soup[2:3]:
        _model = model.find('a', {'class': 'navlabellink nvoffset nnormal'})
        models[_model.text] = SITE + _model['href']
    return models


def get_complectations(model_link, proxie) -> dict:
    soup = make_soup(model_link, proxie)
    complectations = {}
    for complectation in soup[3:4]:
        _complectation = complectation.find('a', {'class': 'navlabellink nvoffset nnormal'})
        complectations[_complectation.text] = SITE + _complectation['href']
    return complectations


def get_details(complectation_link, proxie) -> dict:
    soup = make_soup(complectation_link, proxie)
    details = {}
    for detail in soup[4:5]:
        _detail = detail.find('a', {'class': 'navlabellink nvoffset nnormal'})
        details[_detail.text] = SITE + _detail['href']
    return details


def get_sub_details(detail_link, proxie) -> dict:
    soup = make_soup(detail_link, proxie)
    subdetails = {}
    for subdetail in soup[5:6]:
        _subdetail_normal = subdetail.find('a', {'class': 'navlabellink nvoffset nnormal'})
        _subdetail = subdetail.find('a', {'class': 'navlabellink nvoffset nimportant'})
        
        if _subdetail_normal is not None:
            subdetails[_subdetail_normal.text] = SITE + _subdetail_normal['href']
            
        if _subdetail is not None:
            subdetails[_subdetail.text] = SITE + _subdetail['href']
    return subdetails


def get_parts(sub_detail_link, proxie):
    parts_response = requests.get(sub_detail_link, proxies={'http': proxie})
    parts_soup = BeautifulSoup(parts_response.text, 'lxml').find_all('a', {'class': 'ra-btn ra-btn-moreinfo'})
    table = BeautifulSoup(parts_response.text, 'lxml').find_all('tbody', {'class': 'listing-inner'})
    for i in table:
        name = ' '.join([
            i.text for i in i.find('div', {'class': 'listing-text-row-moreinfo-truck'}).find_all('span')
        ])
        price = i.find('span', {'class': 'ra-formatted-amount listing-price listing-amount-bold'}).text
        print(f'{name}======{price}')
        if price == 'See Options at Left':
            choices = i.find('select', {'class': 'listing-optionchoice-multiple'}).find_all('option')
            for i in choices[1:]:
                variety = str(i.text.split('{')[0])
                variety_title = variety.split('$')[0].replace('(', '')
                variety_price = variety.split('$')[1].replace(')', '').replace(' ', '')
                print(f'{variety_title}---{variety_price}$')
        print('-'*80)

    parts = []
    for part in parts_soup:
        parts.append(part['href'])
    return parts


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


part_link = 'https://www.rockauto.com/en/catalog/abarth,1969,1000,982cc+l4,1438885,cooling+system,coolant+/+antifreeze,11393'
# part_page_link = 'https://www.rockauto.com/en/moreinfo.php?pk=11751273&cc=1438885&pt=1684'
picture_link = 'https://www.rockauto.com/info/27/MGD9M_FRO__ra_p.jpg'
# get_parts(part_link, next(proxie))


def main():
    marks = get_marks(next(proxie))

    for mark, mark_link in marks.items():
        print(mark)
        print('-'*80)
        years = get_years(mark_link, next(proxie))
        sleep(1)

        for year, year_link in years.items():
            print('YEAR =', year)
            models = get_models(year_link, next(proxie))
            sleep(1)

            for model, model_link in models.items():
                print('MODEL =', model)
                complectations = get_complectations(model_link, next(proxie))
                sleep(1)

                for complectation, complectation_link in complectations.items():
                    print('COMPLECTATION =', complectation)
                    details = get_details(complectation_link, next(proxie))
                    sleep(1)

                    for detail, detail_link in details.items():
                        print('DETAIL =', detail)
                        sub_details = get_sub_details(detail_link, next(proxie))
                        sleep(1)

                        for sub_detail, sub_detail_link in sub_details.items():
                            print('SUB DETAIL =', sub_detail)
                            parts = get_parts(sub_detail_link, next(proxie))
                            print(parts)
                            sleep(1)
            print('='*80)


main()
