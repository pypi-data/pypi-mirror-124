"""
Celery 실행 방법:
celery -A tasks worker --loglevel=INFO --concurrency=1 -n worker1@%h
"""
import os
import redis
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

load_dotenv(override=True)

REMOTE_RABBIT_HOST = os.getenv('REMOTE_RABBIT_HOST')
REMOTE_RABBIT_USER = os.getenv('REMOTE_RABBIT_USER')
REMOTE_RABBIT_PASS = os.getenv('REMOTE_RABBIT_PASS')
REMOTE_RABBIT_PORT = os.getenv('REMOTE_RABBIT_PORT')

RABBIT_URL = f'amqp://{REMOTE_RABBIT_USER}:{REMOTE_RABBIT_PASS}@{REMOTE_RABBIT_HOST}:{REMOTE_RABBIT_PORT}/'

REMOTE_REDIS_HOST = os.getenv('REMOTE_REDIS_HOST')
REMOTE_REDIS_PASS = os.getenv('REMOTE_REDIS_PASS')
REMOTE_REDIS_PORT = os.getenv('REMOTE_REDIS_PORT')

REDIS_URL = f'redis://:{REMOTE_REDIS_PASS}@{REMOTE_REDIS_HOST}:{REMOTE_REDIS_PORT}/0'

app = Celery('tasks', broker=RABBIT_URL, backend=REDIS_URL, result_expires=(60 * 60 * 4))
cache = redis.StrictRedis(host=REMOTE_REDIS_HOST, port=REMOTE_REDIS_PORT, db=0, password=REMOTE_REDIS_PASS)

app.conf.celery_timezone = 'Asia/Seoul'
app.conf.celery_enable_utc = True

app.conf.beat_schedule = {
    # '파란자산운용 자동 출근': {
    #     'task': 'paran.entry_click',
    #     'schedule': crontab(hour=kr_cron_hour(8), minute=30, day_of_week='1-5'),
    #     'args': (),
    # },
    # '파란자산운용 자동 퇴근': {
    #     'task': 'paran.exit_click',
    #     'schedule': crontab(hour=kr_cron_hour(17), minute=30, day_of_week='1-5'),
    #     'args': (),
    # },

    # '파란자산운용 테스트 코드': {
    #     'task': 'paran.example',
    #     'schedule': 30.0,
    #     'args': (),
    # },

    # 'robo_backup_database_schedule': {
    #     'task': 'robo.backup_database',
    #     'schedule': 60 * 60,
    #     'args': (),
    # },

}