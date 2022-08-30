from datetime import datetime as dt

class DateChecker():
    """
    Данный класс предназначен как для
    "человеческого" отображения даты,
    поданной на вход конструктору в виде строки
    в формате <ДД.ММ.ГГГГ>    !!!
    но и извлечению из даты всего набора полезной информации
    Один из методов (check_date) класса
    возвращает словарь (date_results_dict) с набором параметров
    обнаруженной даты
    """
    def __init__(self, date_to_check: str):
        self.__date_to_check = date_to_check.strip()



    def get_date_to_check(self):
        return self.__date_to_check

    def get_today_date(self, date_format: str = 'short'):
        """"
        Возвращает сегодняшнюю дату
        в формате <ДД.ММ.ГГГГ>    !!!
        Если в качестве аргумента подать 'long',
        то выводит полную дату со временем (24-часовой формат времени)
        'medium' - то же, но без секунд!!!
        """
        current_timestamp = dt.today()
        if date_format == 'short':
            return current_timestamp.strftime('%d.%m.%Y')
        elif date_format == 'long':
            return current_timestamp.strftime('%d.%m.%Y %H:%M:%S')
        elif date_format == 'medium':
            return current_timestamp.strftime('%d.%m.%Y %H:%M')

    def check_date(self, date_format: str = 'short'):
        date_to_check = self.get_date_to_check()

        weekday_lst = ['понедельник',
                       'вторник',
                       'среда',
                       'четверг',
                       'пятница',
                       'суббота',
                       'воскресенье']

        month_dict = {1: 'январь',
                     2: 'февраль',
                     3: 'март',
                     4: 'апрель',
                     5: 'май',
                     6: 'июнь',
                     7: 'июль',
                     8: 'август',
                     9: 'сентябрь',
                     10: 'октябрь',
                     11:'ноябрь',
                     12: 'декабрь'}

        date_results_dict = {
            'date_ok': False,
            'date_num_valid': False,
            'month_num_valid': False,
            'year_num_valid': False,
            'full_date_str': '',
            'day_num': 0,
            'month_str': '',
            'month_num': 0,
            'year_num': 0,
            'weekday_str': '',
            'weekday_num': 0
        }
        hours_num = 0
        minutes_num = 0
        seconds_num = 0

        # участок кода для обработки даты в формате строки!!!

        try:

            if date_format == 'short':
                date_splitted = date_to_check.split('.')
                day_num = date_splitted[0]
                month_num = date_splitted[1]
                year_num = date_splitted[2]
            elif date_format == 'long':
                full_date_splitted = date_to_check.split(' ')
                date_first_part = full_date_splitted[0]
                date_second_part = full_date_splitted[1]
                date_splitted = date_first_part.split('.')
                day_num = date_splitted[0]
                month_num = date_splitted[1]
                year_num = date_splitted[2]
                time_splitted = date_second_part.split(':')
                hours_num = int(time_splitted[0])
                minutes_num = int(time_splitted[1])
                seconds_num = int(time_splitted[2])

            # пробуем преобразовать отдельные части даты в цифры
            day_num = int(day_num)
            date_results_dict['day_num'] = day_num
            month_num = int(month_num)
            date_results_dict['month_num'] = month_num
            year_num = int(year_num)
            date_results_dict['year_num'] = year_num

            if 32 > day_num > 0:
                date_results_dict['date_num_valid'] = True
            if 13 > month_num > 0:
                date_results_dict['month_num_valid'] = True
            if year_num > 0:
                date_results_dict['year_num_valid'] = True
            date_checked =  dt(
                year_num,
                month_num,
                day_num,
                hours_num,
                minutes_num,
                seconds_num) # Дата - ОК!!!
            date_results_dict['date_ok'] = True
            # добавляем в словарь день недели
            weekday_num = dt.weekday(date_checked)
            date_results_dict['weekday_num'] = weekday_num+1 # нумерация дней недели не с 0 !!!
            #print(self.weekday_lst[weekday_num])
            date_results_dict['weekday_str'] = weekday_lst[weekday_num]
            # добавляем в словарь месяц
            month_num = date_checked.month
            date_results_dict['month_num'] = month_num
            date_results_dict['month_str'] = month_dict[month_num]

            print('Дата - ок!')

        except ValueError:
            print(f'Ошибка в строковом представлении даты: <{date_to_check}>')
        except IndexError:
            print('Ошибка при попытке сплитования на лист строки с датой')
            print(f'Ошибка в строковом представлении даты: <{date_to_check}>')
        except TypeError:
            print(f'Ошибка в строковом представлении даты: <{date_to_check}>')


        date_results_dict['full_date_str'] = date_to_check

        return date_results_dict
