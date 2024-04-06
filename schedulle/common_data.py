# from schedulle.functions import get_groups

TIME_PARA={
  "1": "09:00-10:40",
  "2": "10:45-12:25",
  "3": "12:30-14:10",
  "4": "15:00-16:40",
  "5": "16:45-18:25",
  "6": "18:30-20:10",
  "7": "20:15-21:55"
}
days_translate = {
    'Monday': 'Понедельник',
    'Tuesday': 'Вторник',
    'Wednesday': 'Среда',
    'Thursday': 'Четверг',
    'Friday': 'Пятница',
    'Saturday': 'Суббота',
    'Sunday': 'Воскресенье'
}
data = {
        # "SERACH": search,//
        "FILTER": "GROUPS",
        "GROUP": "",
        "SELECT": "*",
        "ONLY_SESSIA": "N",
    }
week_types = ["числ.", "знам."]
url = "https://rasp.spbgasu.ru/local/components/gasu/raspisanie.csv/ajax.php"
url_rasp="https://rasp.spbgasu.ru/"

