import requests
import json

if __name__ == '__main__':
    user_name = input('Введите свой логин:') or 'alishka242'
    url = f'https://api.github.com/users/{user_name}/repos'
    response_repo = requests.get(url)
    new_file = open('hw_1/repos.json', 'w', encoding='utf-8')

    # Хоть это и больше похоже на json, но это неверный вариант, т.к. сохраняется строка.
    # resp_dict = response_repo.text [1:-1]
    # print(type(resp_dict))
    # new_file.write(resp_dict)

    json.dump(response_repo.json(), new_file)

    for repo in response_repo.json():
        print(repo['name'])
