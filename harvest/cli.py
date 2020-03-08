import os
import sys
import logging
import re
import argparse
from datetime import datetime
from harvest.auth import PersonalAccessAuthClient
from harvest.api import Projects
from harvest.api import Tasks
from harvest.api import TimeEntry
from harvest.services import AllProjects
from harvest.services import AllTasks
from harvest.services import UsersAllAssignments
from harvest.services import UsersMe
try:
    from ConfigParser import ConfigParser
except ModuleNotFoundError as ex:
    from configparser import ConfigParser

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
logging.basicConfig(level=LOGLEVEL)
logger_hvt = logging.getLogger('Harvest CLI')

def old_main():
    # logging.basicConfig(level=logging.DEBUG)
    client = PersonalAccessAuthClient(
        # cfg='.harvest.cfg'
    )
    cfg = os.environ.get(
        'HARVEST_CFG',
        os.path.expanduser('~/.harvest.cfg'),
    )
    config = ConfigParser()
    config.read(cfg)
    if sys.argv[1] == 'projects':
        api = Projects(client)
        if sys.argv[2] == 'get':
            if sys.argv[3] == 'all':
                # logging.info(api.get().json())
                for entity in AllProjects(cfg='harvest.cfg').all():
                    logging.info('{} - #{}'.format(
                        entity['name'], entity['id']))
    elif sys.argv[1] == 'tasks':
        api = Tasks(client)
        if sys.argv[2] == 'get':
            if sys.argv[3] == 'all':
                for entity in AllTasks(cfg='harvest.cfg').all():
                    logging.info('{} - #{}'.format(
                        entity['name'], entity['id']))
    elif sys.argv[1] == 'timeentry':
        api = TimeEntry(client)
        if sys.argv[2] == 'new':
            NOTES_ARG = 3
            SPENTDATE_ARG = 4
            TASKID_ARG = 5
            PROJECTID_ARG = 6
            HOURS = 7
            notes = sys.argv[NOTES_ARG]
            spent_date = sys.argv[SPENTDATE_ARG]
            if spent_date == 'today':
                spent_date = datetime.now().strftime('%Y-%m-%d')

            task_id = sys.argv[TASKID_ARG]
            if not task_id.isnumeric():
                task_id = config.get('tasks', task_id)

            if not sys.argv[PROJECTID_ARG]:
                logging.info('Missing project(s) ID list')
            project_id_list = []
            for entry in sys.argv[PROJECTID_ARG].split(','):
                if entry.isnumeric():
                    project_id_list.append(entry)
                else:
                    project_id_list.append(config.get('projects', entry))
            try:
                if re.match(r'[0-9]+:[0-9]+', sys.argv[HOURS]):
                    hours, minutes = sys.argv[HOURS].strip().split(':')
                    hours = (1.0 / 60) * float(int(minutes) + (int(hours) * 60))
                elif re.match(r'[0-9]+\.[0-9]+', sys.argv[HOURS]):
                    hours = float(sys.argv[HOURS])
                else:
                    raise Exception('Format not supported: {}'.format(sys.argv[HOURS]))
                hours = hours / len(project_id_list)
            except IndexError:
                hours = 0.00
            for project_id in project_id_list:
                data = {
                    'notes': notes,
                    'spent_date': spent_date,
                    'task_id': task_id,
                    'project_id': project_id,
                    'hours': hours,
                }
                TimeEntry(client).post(data=data)


class BaseAction(argparse.Action):

    def __init__(self, **kwargs):
        super(BaseAction, self).__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        self.cmd(namespace)

    def cmd(self, namespace):
        raise NotImplementedError(_('.cmd() not defined'))


class TimeEntryNew(BaseAction):

    def cmd(self, namespace):
        logging.debug(namespace)
        if namespace.spent_date == 'today':
            pass
        for project_id in namespace.project_id:
            payload = {
                'notes': namespace.notes,
                'project_id': project_id,
                'spent_date': namespace.spent_date,
                'hours': namespace.hours,
                'task_id': namespace.task_id,
            }
            print(payload)


class ProjectList(BaseAction):

    def cmd(self, namespace):
        logger_hvt.debug(namespace)
        resp = AllProjects(cfg='harvest.cfg').all()
        if namespace.output == 'text':
            for entity in resp:
                logger_hvt.info('#{}\t{}'.format(
                    entity['id'],
                    entity['name'], 
                    ))
        elif namespace.output == 'json':
            print(resp)
        else:
            print(resp)


class TasksList(BaseAction):

    def cmd(self, namespace):
        logger_hvt.debug(namespace)
        for entity in AllTasks(cfg='harvest.cfg').all():
            logger_hvt.info('#{}\t{}'.format(
                entity['id'],
                entity['name'], 
                ))


class AssignmentList(BaseAction):

    def cmd(self, namespace):
        logger_hvt.debug(namespace)
        for assignment in UsersAllAssignments(cfg='harvest.cfg').all():
            logger_hvt.info(f"#{assignment['project']['id']}\t{assignment['project']['name']}")
            for task in assignment['task_assignments']:
                logger_hvt.info(f"\t#{task['task']['id']}\t{task['task']['name']}")


if __name__ == '__main__':
    # Root (rt)
    rt_parser = argparse.ArgumentParser(
            prog='harvest',
            description='unofficial harvest cli',
            )
    rt_sbparsers = rt_parser.add_subparsers(help='sub-command help')
    
    # Time Entry (te)
    te_parser = rt_sbparsers.add_parser('timeentry')
    te_sbparsers = te_parser.add_subparsers(help='time entry management')

    # Time Entry (te) actions
    te_new_parser = te_sbparsers.add_parser('new', help='create new time entry')
    te_new_parser.add_argument('project_id', nargs='+', type=str, help="one or more project id's")
    te_new_parser.add_argument('task_id', help='single task id')
    te_new_parser.add_argument('notes', type=str, help='description of entry')
    te_new_parser.add_argument('--hours', default=0, help='hours spent (default: 0)')
    te_new_parser.add_argument('--spent_date', type=str, default='today', help='date entry happend (default: today)')
    te_new_parser.add_argument('run', nargs=0, action=TimeEntryNew, help=argparse.SUPPRESS)

    # Projects (pj)
    pj_parser = rt_sbparsers.add_parser('projects')
    pj_sbparsers = pj_parser.add_subparsers(help='project entity management')

    # Projects (pj) actions
    pj_list_parser = pj_sbparsers.add_parser('list', help='retrieve a list of current projects')
    pj_list_parser.add_argument('--output', type=str, default='text', help='output format')
    pj_list_parser.add_argument('run', nargs=0, action=ProjectList, help=argparse.SUPPRESS)

    # Tasks (tk)
    tk_parser = rt_sbparsers.add_parser('tasks')
    tk_sbparser = tk_parser.add_subparsers(help='tasks management')

    # Tasks (tk) actions
    tk_list_parser = tk_sbparser.add_parser('list', help='retrieve a list of registered tasks')
    tk_list_parser.add_argument('run', nargs=0, action=TasksList, help=argparse.SUPPRESS)

    # Users (us)
    us_parser = rt_sbparsers.add_parser('users')
    us_sbparser = us_parser.add_subparsers(help='users management')

    # Users Assignments (as)
    us_as_parser = us_sbparser.add_parser('assignments')
    us_as_sbparser = us_as_parser.add_subparsers(help="user's tasks management")

    us_as_list_parser = us_as_sbparser.add_parser('list')
    us_as_list_parser.add_argument('run', nargs=0, action=AssignmentList, help=argparse.SUPPRESS)

    args = rt_parser.parse_args()
