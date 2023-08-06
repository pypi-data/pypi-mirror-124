import datetime


class Event(object):

    def _time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    def message(self, module: str):
        raise NotImplementedError('Event needs to have message method implemented.')
