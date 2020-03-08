import logging
import calendar
from datetime import date
from datetime import datetime
from datetime import timedelta
from harvest.auth import PersonalAccessAuthClient
from harvest.api import TimeEntry
from harvest.api import Projects
from harvest.api import Tasks
from harvest.api import UsersMe
from harvest.api import UsersAssignments

class BaseService(object):

    def __init__(self, personal_token=None, account_id=None, cfg=None):
        self.client = PersonalAccessAuthClient(
            personal_token,
            account_id,
            cfg,
        )


class TimeRangeBaseService(BaseService):

    def __init__(self, personal_token=None, account_id=None):
        super(TimeRangeBaseService, self).__init__(personal_token, account_id)
        self.today = datetime.now()

    def get_date_range(self):
        pass

    def all(self, page=1):
        date_range = self.get_date_range()
        logging.debug(
            'Quering from {} to {}'.format(date_range[0], date_range[1])
        )
        api = TimeEntry(client=self.client)
        resp = api.get(params={
            'from': date_range[0],
            'to': date_range[1],
        })
        logging.debug('Encoding = {}'.format(resp.encoding))
        return resp.json()

    def blanks(self):
        resp = self.all()
        empty_time_entries = []
        for entry in resp['time_entries']:
            if not entry['notes']:
                empty_time_entries.append(entry)
        resp['time_entries'] = empty_time_entries
        return resp


class SingleDayTimeEntries(TimeRangeBaseService):

    def set_date(self, date):
        self.date = date

    def get_date_range(self):
        self.date_from = self.date
        self.date_to = self.date
        return (self.date_from, self.date_to)


class Today(TimeRangeBaseService):

    def get_date_range(self):
        self.date_from = self.today.strftime('%Y-%m-%d')
        self.date_to = self.today.strftime('%Y-%m-%d')
        return (self.date_from, self.date_to)


class MonthTimeEntries(TimeRangeBaseService):

    def set_month(self, year, month):
        self.year = year
        self.month = month
        self.last_day = calendar.monthrange(year,month)[1]

    def get_date_range(self):
        self.date_from = date(self.year, self.month, 1)
        self.date_to = date(self.year, self.month, self.last_day)
        return (self.date_from, self.date_to)


class CurrentWeek(TimeRangeBaseService):

    def get_date_range(self):
        self.date_from = (self.today - timedelta(days=self.today.weekday()))
        self.date_to = (self.date_from + timedelta(days=6)).strftime(
            '%Y-%m-%d')
        self.date_from = self.date_from.strftime('%Y-%m-%d')
        return (self.date_from, self.date_to)


class PreviousWeek(TimeRangeBaseService):

    def get_date_range(self):
        # Today from last week
        self.today = self.today - timedelta(days=(6 - self.today.weekday()))
        self.date_from = (self.today - timedelta(days=self.today.weekday()))
        self.date_to = (self.date_from + timedelta(days=6)).strftime(
            '%Y-%m-%d')
        self.date_from = self.date_from.strftime('%Y-%m-%d')
        return (self.date_from, self.date_to)


class AllProjects(BaseService):

    def all(self):
        ret = []
        resp = Projects(client=self.client).get()
        total_pages = resp.json()['total_pages']
        for i in range(1, total_pages + 1):
            resp = Projects(client=self.client).get(page=i)
            ret += resp.json()['projects']
        return ret


class AllTasks(BaseService):

    def all(self):
        ret = []
        resp = Tasks(client=self.client).get()
        total_pages = resp.json()['total_pages']
        for i in range(1, total_pages + 1):
            resp = Tasks(client=self.client).get(page=i)
            ret += resp.json()['tasks']
        return ret


class CurrentUser(BaseService):

    def get(self):
        ret = []
        resp = UsersMe(client=self.client).get()
        return resp.json()


class UsersAllAssignments(BaseService):

    def all(self):
        ret = []
        resp = UsersMe(client=self.client).get()
        user_id = resp.json()['id']
        resp = UsersAssignments(client=self.client, user_id=user_id).get()
        total_pages = resp.json()['total_pages']
        for i in range(1, total_pages + 1):
            resp = UsersAssignments(client=self.client, user_id=user_id).get(page=i)
            ret += resp.json()['project_assignments']
        return ret