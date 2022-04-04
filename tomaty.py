import requests
import datetime
from gazpacho import Soup
import sys
import json
import os.path
import time

def write_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f)

def read_config():
    if not os.path.isfile('config.json'):
        default_config = {'urls': []}
        write_config(default_config)
    with open('config.json') as f:
        return json.load(f)

def add_link(url):
    config = read_config()
    urls = set(config['urls'])
    urls.add(url)
    config['urls'] = list(urls)
    write_config(config)

def remove_link(url):
    config = read_config()
    urls = config['urls']
    if url in urls:
        urls.remove(url)
    config["urls"] = list(urls)
    writeConfig(config)

def my_links():
    config = read_config()
    urls = config['urls']
    for url in urls:
        print(url)

def release_check(release_date, today_date):
    if release_date.date() == today_date.date():
        print("Беги на нетфликс, новый сезон вышел!")
    elif release_date.date() > today_date.date():
        days_to_release = release_date - today_date
        print("Новый сезон ещё не вышел, осталось {} дней".format(days_to_release.days))
    elif release_date.date() < today_date.date():
        print('Сериал уже давно вышел, беги смотреть!')

def get_series_info():
    config = read_config()
    for i in config['urls']:
        response = requests.get(i)
        html = response.text
        soup = Soup(html)
        release_date = soup.find("meta", {"name" : "startDate"}).attrs["content"]
        today = datetime.datetime.today()
        release_date_datetime = datetime.datetime.strptime(release_date, '%Y-%m-%d')
        release_check(release_date_datetime, today)

def start_prog():
    config = read_config()
    config['active_pid'] = os.getpid()
    write_config(config)
    threading.Timer(1, get_series_info).start()

def stop_prog():
    config = read_config()
    if 'active_pid' in config:
        pid = config['active_pid']
        os.kill(pid, 9)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Нужно закинуть ссылку')
        sys.exit(1)
    command = sys.argv[1]
    if command == "add":
        add_link(sys.argv[2])
    elif command == "list":
        my_links()
    elif command == "remove":
        remove_link(sys.argv[3])
    elif command == "start":
        start_prog()
    elif command == "stop":
        stop_prog()
    else:
        print('Ты написал(а) что-то не то')
