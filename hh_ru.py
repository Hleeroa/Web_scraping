import json
import bs4
import requests
from fake_headers import Headers


def get_headers():
    return Headers(os="win", browser="chrome").generate()


def gather_data():
    print('Gathering data...')
    response = requests.get("https://spb.hh.ru/search/vacancy?ored_clusters=true&area=1&area=2&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=python+Django+Flask", headers=get_headers())

    html_data = response.text
    soup = bs4.BeautifulSoup(html_data, features='lxml')
    vacancies_pyle = soup.find(class_='vacancy-serp-content')
    vacancies_list = vacancies_pyle.find_all('div', class_='vacancy-serp-item__layout')
    return vacancies_list


def vacancy_creation():
    parsed_data = []
    print('Creating a dictionary...')
    for vacancy in gather_data():
        link = vacancy.find('a')['href']
        name_data = vacancy.find('span', class_='serp-item__title-link serp-item__title')
        city_n_company = vacancy.find('div', class_='vacancy-serp-item__info')
        city_data = city_n_company.find_all('div', class_='bloko-text')[1]
        company_data = city_n_company.find('div', class_='vacancy-serp-item__meta-info-company')
        salary = vacancy.find('span', class_='bloko-header-section-2')
        if salary:
            salary = salary.text
        else:
            salary = 'Не указана'
        company = company_data.text
        city = city_data.text
        name = name_data.text
        if '\u202f' in salary or '\xa0' in company or '\xa0' in city:
            salary = salary.replace('\u202f', ' ')
            company = company.replace('\xa0', ' ')
            city = city.replace('\xa0', ' ')
        vacancy_info = {
                    'name': name,
                    'link': link,
                    'company': company,
                    'city': city,
                    'salary': salary
        }
        parsed_data.append(vacancy_info)
    return parsed_data


def info_fixation(data, file):
    print('Saving into a json file...')
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    info_fixation(vacancy_creation(), 'saved_info/vacancies.json')
    print('Done!')