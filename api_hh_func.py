import requests
import json


def getFromIdEmployer(id_employer):
    employer = []
    req = requests.get('https://api.hh.ru/employers/' + str(id_employer))
    data = req.content.decode()
    req.close()
    jsObj = json.loads(data)
    try:
        employer.append(jsObj['id'])
        employer.append(jsObj['name'])
        employer.append(jsObj['alternate_url'])
        employer.append(jsObj['open_vacancies'])
        #print(employer)

    except:
        print('Упс, ошибка!')

    return employer


def getPage(page, id_employer):
    params = {
        'employer_id': id_employer,
        'page': page,
        'per_page': 100
    }
    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()

    return data


def getVacancies(id_employer):
    vacancies = []
    for page in range(0, 20):
        jsObj = json.loads(getPage(page, id_employer))
        for item in jsObj['items']:
            vacancy = []
            try:
                vacancy.append(id_employer)
                vacancy.append(item['id'])
                vacancy.append(item['name'])
                vacancy.append(item['alternate_url'])
                if item['snippet']['responsibility'] != None:
                    vacancy.append(item['snippet']['responsibility'])
                else:
                    vacancy.append('-')
                if item['salary'] != None:
                    if item['salary']['from'] != None:
                        vacancy.append(item['salary']['from'])
                    else:
                        vacancy.append(0)
                    if item['salary']['to'] != None:
                        vacancy.append(item['salary']['to'])
                    else:
                        vacancy.append(0)
                    if item['salary']['currency'] != None:
                        vacancy.append(item['salary']['currency'])
                    else:
                        vacancy.append('-')
                else:
                    vacancy.append(0)
                    vacancy.append(0)
                    vacancy.append('-')

            except:
                print('Упс, ошибка!')

            vacancies.append(vacancy)
            #print(vacancy)
        if (jsObj['pages'] - page) <= 1:
            break

    return vacancies
