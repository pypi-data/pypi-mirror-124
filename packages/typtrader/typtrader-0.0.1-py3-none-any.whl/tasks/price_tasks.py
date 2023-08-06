"""
주기적으로 가격 데이터를 DB에 저장하는 태스크
"""
from tasks.app import app


@app.task(name='trader.hour_price_task')
def hour_price_task():
    pass


@app.task(name='trader.minute_price_task')
def minute_price_task():
    pass


if __name__ == '__main__':
    pass