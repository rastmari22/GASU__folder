import itertools
from datetime import datetime, timezone, timedelta
from schedulle.common_data import TIME_PARA, days_translate, data, week_types, url, url_rasp
import re
import requests


def get_current_subject(search):
    current_time = datetime.now(timezone(timedelta(hours=3))).time()
    current_para = 0
    for num_para, time_range in TIME_PARA.items():
        start_time_str, end_time_str = time_range.split('-')
        start_para = datetime.strptime(start_time_str, '%H:%M').time()
        end_para = datetime.strptime(end_time_str, '%H:%M').time()
        if start_para <= current_time <= end_para:
            current_para = num_para
            break

    current_date = datetime.now()

    week_day = (days_translate[current_date.strftime('%A')]).upper()

    match = re.search(r'window.NUMBER_WEEK = (\d+)', requests.get(url_rasp).text)
    if match:
        week_number = int(match.group(1))
    else:
        week_number = 0
    week_type = "числ." if week_number % 2 > 0 else "знам."

    datamy = dict()
    datamy["SERACH"] = search
    # print(search)
    datamy.update(data)

    response = requests.post(url, data=datamy)
    # print(response)
    if response.status_code == 200:
        json_response = response.json()
        # print(json_response)
        try:
            return re.sub(r' \(.+?\)', '', json_response["R"][week_day][current_para][week_type]["LESSON"])
        except:
            return "Общая"
    else:
        # error Расписание не найдено
        return "Общая"

# print(get_current_subject('ИСТб-3'))
async def get_subjects(search):
    datamy = dict()
    datamy["SERACH"] = search
    datamy.update(data)
    response = requests.post(url, data=datamy)
    all_subjects = []
    # try:
    json_response = response.json()
    for day_key in days_translate:
        for para_key in TIME_PARA:
            for week_type_key in week_types:
                try:
                    all_subjects.append(re.sub(r' \(.+?\)', '',
                                               json_response["R"][days_translate[day_key].upper()][para_key][
                                                   week_type_key]["LESSON"]))
                except:
                    pass
    return set(all_subjects)

# print(get_subjects('ИСТб-3'))
def get_groups_1():
    response = requests.post(url, data=data)
    all_groups = []
    json_response = response.json()
    for day_key in days_translate:
        for para_key in TIME_PARA:
            for week_type_key in week_types:
                try:
                    all_groups = all_groups + json_response["R"][days_translate[
                        day_key].upper()][para_key][week_type_key]["GROUP"].split("<br>")
                except:
                    pass
    return list(set(all_groups))
async def get_groups():
    response = requests.post(url, data=data)
    groups = set()
    json_response = response.json()

    for day_name, lesson_time, week_type in itertools.product(days_translate.values(), TIME_PARA.keys(), week_types):
        try:
            groups.update(json_response["R"][day_name.upper()][lesson_time][week_type]["GROUP"].split("<br>"))
        except:
                pass
    return list(groups)


async def get_subjects1(search):
    datamy = {"SERACH": search, **data}
    response = requests.post(url, data=datamy)
    all_subjects = set()
    json_response = response.json()
    for day_name, lesson_time, week_type in itertools.product(days_translate.values(), TIME_PARA.keys(), week_types):
        try:
            all_subjects.update(json_response["R"][day_name.upper()][lesson_time][week_type]["LESSON"].split("<br>"))
        except:
            pass
    return all_subjects