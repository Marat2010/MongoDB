from decouple import Config, RepositoryEnv, AutoConfig
import json
from os.path import join
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# DEBUG = True  # local "mongodb://localhost:27017/", ...
DEBUG = False

config = AutoConfig()

# ========== Telegram ==========

TOKEN_TG = config('TOKEN_TG')
WEBHOOK_HOST = 'https://rupyt.alwaysdata.net'
WEBHOOK_PATH = '/MongoDB/'
# webserver settings
WEBAPP_HOST = '::'  # Only IPv6 (Аналог IP4: 0.0.0.0)
WEBAPP_PORT = 8350  # Ports: 8300-8499

if DEBUG:
    File_ENV = '.env_dev'
    config = Config(RepositoryEnv(join(BASE_DIR, File_ENV)))
    WEBHOOK_HOST = 'https://c555-178-205-54-105.ngrok-free.app'
    WEBHOOK_PATH = ''
    WEBAPP_HOST = 'localhost'  # Only IPv6 (Аналог IP4: 0.0.0.0)

help_message = '  Подсчет суммы всех выплат в зависимости от единицы группировки.\n' \
                'Типы агрегации (group_type) могут быть следующие:\n' \
                ' "hour", "day", "month"\n' \
                ' Пример входных данных:\n' \
                ' {\n' \
                ' "dt_from":"2022-09-01T00:00:00",\n' \
                ' "dt_upto":"2022-12-31T23:59:00",\n' \
                ' "group_type":"month"\n' \
                ' }\n\n' \
                'Доступные команды:\n' \
                '/help - Данное описание\n' \
                'Полное описание: \n' \
                'https://github.com/Marat2010/mongoDB/doc/Jun Python dev.docx \n'

# ========== MongoDB ==========

Mongo_URI = config('Mongo_URI')
DB = "sampleDB"
COLLECTION = "sample_collection"
GROUP_TYPE = ['month', 'day', 'hour']


def get_pipelines():
    pl = {}
    for group_type in GROUP_TYPE:
        file = join(BASE_DIR, f'pipelines/pipeline_{group_type}.json')
        with open(file) as f:
            pl[group_type] = json.load(f)

    return pl


pipelines = get_pipelines()


# ========================================
# File_ENV = '.env_dev' if DEBUG else '.env'
# config = Config(RepositoryEnv(join(BASE_DIR, File_ENV)))
# ========================================
# Mongo_URI = "mongodb://localhost:27017/"
# Mongo_URI = "mongodb+srv://<USER>:<PASSWORD>@xxclusterxxx.xxxxx.mongodb.net/?retryWrites=true&w=majority"
# =======================================

