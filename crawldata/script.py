# Import
from selenium import webdriver
import csv
from bs4 import BeautifulSoup
driver = webdriver.Chrome(executable_path='.\Driver\chromedriver.exe')
url = 'https://www.agencyvietnam.com'
driver.get(url)
""" driver.find_element_by_id('5680').click() """


def GetURL():
    page_source = BeautifulSoup(driver.page_source)
    profile_agencys = page_source.find_all(
        'a', class_='agency-card')
    all_agency_URL = []
    for profile_agency in profile_agencys:
        agency_ID = profile_agency.get('href')
        agency_URL = "https://www.agencyvietnam.com/" + agency_ID
        if agency_URL not in all_agency_URL:
            all_agency_URL.append(agency_URL)
    return all_agency_URL


with open('output.csv', 'w',  newline='') as file_output:
    headers = ['Name Agency', 'Email', 'Personel']
    writer = csv.DictWriter(file_output, delimiter=',',
                            lineterminator='\n', fieldnames=headers)
    writer.writeheader()
    URL_get_page = GetURL()
    for agency_link in URL_get_page:
        driver.get(agency_link)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        info_div = page_source.find(
            'div', class_='col-12 col-sm-8 col-md-9 mt-10')
        name = info_div.find('h1').get_text().strip()
        infor_plus = info_div.find('div', class_='gap-items-1 gap-y')
        infor_plusssss = infor_plus.find_all('div')
        check_email = infor_plusssss[2].find('a')
        if check_email is None:
            email = "The value is not null"
        else:
            email = infor_plusssss[2].find('a').get_text().strip()
        personal = page_source.find(
            'div', class_='media-list media-list-divided media-list-sm')
        personal_span = personal.find('span')
        personal_spans = personal_span.find_all(
            'span', class_='fw-600')
        name_personal = []
        for name_personalss in personal_spans:
            name_personal.append(name_personalss.get_text().strip())
        writer.writerow({headers[0]: name, headers[1]
                        : email, headers[2]: name_personal})

""" for namepersonal in personal_spans:
    print(namepersonal) """
