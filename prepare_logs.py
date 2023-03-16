import datetime
import pathlib


def get_date() -> str:
    return str(datetime.datetime.now())[:10]


def update_today_logs():
    log_dir = str(pathlib.Path(__file__).parent) + "\\logs\\"

    with open(f'{log_dir+get_date()}_raw.log', 'r') as f:
        report = {
            'ar': [],
        }
        for i in f.readlines():
            li = i.split(' ')
            if li[-1].startswith('Starting') or li[-1].startswith('minutes'):
                pass
            else:
                try:
                    report[li[-1][:2]].append(li[:-1])
                except KeyError:
                    report[li[-1][:2]] = []
                    report[li[-1][:2]].append(li[:-1])
    # write blocked mirrors
    with open(f'{log_dir+get_date()}_blocked.log', 'w') as f:
        for key in report:
            for item in report[key]:
                if 'blocked' in item:
                    f.writelines(f'{key} - {item[-1][7:]} {" ".join(item[2:5])}\n')
        f.write('______\n')
        for key in report:
            for item in report[key]:
                if 'plug' in item:
                    f.writelines(f'{key} - {item[-1][7:]} plugged\n')


if __name__ == '__main__':
    update_today_logs()
