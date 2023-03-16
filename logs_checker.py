# import asyncio
import collections
import datetime
import pathlib

from configs import mirrors
from countries import abbreviatures


# from tg_notifier import get_date, send_balance


def get_date() -> str:
    return str(datetime.datetime.now())[:10]


def get_file_name():
    file_name = str(pathlib.Path(__file__).parent) + "\\logs\\" + get_date()
    return file_name


class Checks:
    def __init__(self):
        self.list_of_logs = []
        self.missed = 0
        with open(f'{get_file_name()}_raw.log', 'r') as logs:
            self.list_of_logs = [i[:-1] for i in logs.readlines()]

    def check_logs(self) -> None:
        """
        check created logs
        :return: None
        """
        blocked_by_providers = collections.defaultdict(list)
        plugs = collections.defaultdict(list)
        redirects = collections.defaultdict(list)
        reached = collections.defaultdict(list)
        balance = 1
        # print(dict.fromkeys([i for i in mirrors], 0))
        for i in self.list_of_logs:
            if 'blocked' in i:
                blocked_by_providers[i[-2:]].append(i)
            if 'redirect' in i:
                redirects[i[-2:]].append(i)
            if 'plug' in i:
                plugs[i[-2:]].append(i)
            if 'reached' in i:
                reached[i[-2:]].append(i)
            if 'balance' in i:
                balance -= 1

        amount_of_blocked = sum([len(i) for i in blocked_by_providers.values()])
        amount_of_plugs = sum([len(i) for i in plugs.values()])
        amount_of_redirects = sum([len(i) for i in redirects.values()])
        amount_of_reached = sum([len(i) for i in reached.values()])
        print(f'missed in check_logs(): {self.missed}')
        # update_tg(amount_of_blocked, amount_of_plugs, amount_of_redirects, amount_of_reached)
        # send_reports(amount_of_blocked, amount_of_plugs, amount_of_redirects, amount_of_reached)
        if balance < 1:
            print('sending balance')
            ...

    def check_missed(self) -> list:
        """
        Checks if there are missed countries in logs
        :return: list if there are missed countries
        """
        countries = []
        for i in self.list_of_logs:
            countries.append(i[-2:])
        missed = [i for i in abbreviatures if i not in countries]
        if missed:
            print(f'countries might be missed: {missed}')
        return missed

    def prepare_missed(self, to_check, country, domains) -> dict:
        """
        Adds unchecked mirrors to the dict for a given country
        :param to_check: dict of missed mirrors
        :param country: current country
        :param domains: list of checked domains
        :return: country: [missed mirrors]
        """
        domains = [i[:-1] for i in domains]

        missed = [item for item in mirrors if item not in domains]
        for mirror in missed:
            try:
                to_check[country].append(mirror)
            except KeyError:
                to_check[country] = []
                to_check[country].append(mirror)

        return to_check

    def get_report_dict(self) -> dict:
        """
        collects unchecked countries from the report
        :return: country: [mirrors]
        """
        with open(f'{get_file_name()}_raw.log', 'r') as f:
            report = {
                'ar': [],
            }
            for i in f.readlines():
                li = i.split(' ')
                if li[-1].startswith('Starting') or li[-1].startswith('minutes'):
                    pass
                else:
                    try:
                        report[li[-1][:2]].append(li[-2])
                    except KeyError:
                        report[li[-1][:2]] = []
                        report[li[-1][:2]].append(li[-2])
        unchecked = {}
        for i in report.items():
            if len(i[1]) != 13:
                try:
                    unchecked[i[0]].append(i[1])
                except KeyError:
                    unchecked[i[0]] = []
                    unchecked[i[0]].append(i[1])
        return unchecked

    def check_again(self) -> dict:
        """
        Adds missed mirrors for all missed countries
        :return: country: [missed mirror]
        """
        checked = self.get_report_dict()
        to_check = {}
        for pair in checked:
            self.prepare_missed(to_check, pair, *checked[pair])
        print(f'missed dict in check_again(): {to_check}')
        return to_check
