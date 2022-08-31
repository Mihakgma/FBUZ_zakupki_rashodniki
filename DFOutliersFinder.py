from pandas import DataFrame as pd_DataFrame
from pandas import Series as pd_Series
from search_Outliers_testing import df_outliers_test
from numbers import Number


class OutliersSearcher():

    """
    Данный класс принимает на вход в качестве аргументов:
    1) ДатаФрейм (далее - ДФ) в котором содержится как минимум 1 столбец с числовыми значениями;
    2) Список названий колонок по которым необходимо проитерироваться;
    3) искать нижние выбросы (bool);
    4) искать верхние выбросы (bool).

    В процессе итерации спеицально созданный метод класса определяет выбросы
    (как нижние, так и верхние - по умолчанию)
    """

    def __init__(self, df_in: pd_DataFrame,
                 column_names: list,
                 lower_outliers: bool = True,
                 higher_outliers: bool = True):
        self.__df_in = df_in
        self.__column_names = column_names
        self.__lower_outliers = lower_outliers
        self.__higher_outliers = higher_outliers

    def get_df_in(self):
        return self.__df_in

    def get_column_names(self):
        return self.__column_names

    def get_lower_outliers(self):
        return self.__lower_outliers

    def get_higher_outliers(self):
        return self.__higher_outliers

    def check_values_type(self):
        """
        метод
        проверяет значения всех столбцов
        ДФ содержали численные значения (integer or float)
        :return:
        True - все столбцы содержать инфрмацию правильного формата
        False - предыдущее утверждение неверно
        """
        everything_ok = True
        df: pd_DataFrame = self.get_df_in()
        colnames_to_process = self.get_column_names()
        subtable = df[colnames_to_process]
        for colname in list(subtable):
            current_column = subtable[colname]
            are_values_digits = current_column.apply(lambda x: isinstance(x, Number))
            if are_values_digits.sum() == current_column.shape[0]:
                print(f'все строки колонки <{colname}> - цифры')
            else:
                print(f'Не все значения колонки <{colname}> - цифры')
                everything_ok = False
        return everything_ok

    def check_searched_colnames(self):
        """
        Показывает общую инфу по ДФ,
        ищет имена колонок в ДФ,
        :return:
        True - все искомые имена присутствуют, все ОК
        False - хотя бы одно из имен отсутвует в ДФ
        """
        everything_ok = True
        df = self.get_df_in()
        colnames_to_process = self.get_column_names()
        df_nrows = df.shape[0]
        df_ncols = df.shape[1]
        colnames_df = list(df)
        print('Размерность ДФ составляет:')
        print(f'<{df_nrows}> строк на <{df_ncols}> столбцов')
        searched_cols_in_df = []
        absent_colnames = []
        for colname_searched in colnames_to_process:
            if colname_searched in colnames_df:
                searched_cols_in_df.append(True)
            else:
                searched_cols_in_df.append(False)
                absent_colnames.append(colname_searched)
        yes_no = ['Нет', 'Да']
        all_colnames_present = sum(searched_cols_in_df) == len(colnames_to_process)
        print(f'Все искомые имена колонок присутствуют в ДФ: <{yes_no[all_colnames_present]}>')
        if all_colnames_present == False:
            everything_ok = False
            print('Перечень отсутствующих в ДФ названий столбцов:')
            prepared_absent_colnames = '\n'.join([i for i in absent_colnames])
            print(f'{prepared_absent_colnames}')
        return everything_ok

    def detect_outliers_IQR_method(self, column_values: list):
        """
        метод принимает на вход лист
        :param column_values: значения столбца
        :return: словарь с результатами
        ключ - выброс (верхний / нижний - low/high)
        значение - список [(индекс элемента, значение самого элемента)]
        """
        need_lower_outliers = self.get_lower_outliers()
        need_higher_outliers = self.get_higher_outliers()
        result_dict = {'low': [], 'high': []}
        column_values_series = pd_Series(column_values)
        q_low = column_values_series.quantile(0.25)
        q_high = column_values_series.quantile(0.75)
        iqr = q_high - q_low # IQR  - межквартильный размах
        fence_low = q_low - 1.5 * iqr
        fence_high = q_high + 1.5 * iqr
        for elem_index in range(len(column_values)):
            curr_element = column_values[elem_index]
            if need_lower_outliers:
                if curr_element < fence_low:
                    result_dict['low'].append((elem_index, curr_element))
                    continue
            if need_higher_outliers:
                if curr_element > fence_high:
                    result_dict['high'].append((elem_index, curr_element))
        print(result_dict)
        return result_dict

    def save_found_outliers(self):
        """
        Сохраняет в виде текстового документа (?)
        Результаты поиска выбросов в данных (result_dict)...
        :return: ?
        """
        pass



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df_tested = pd_DataFrame(df_outliers_test)
    column_names_tested = ['digits_int_positive', 'digits_int_negatives_here', 'dotted_digits']
    test_object = OutliersSearcher(
        df_in=df_tested,
        column_names=column_names_tested)
    colnames_there = test_object.check_searched_colnames()
    print(colnames_there) # выводим на печать результат проверки наличия всех столбцов в ДФ
    types_ok = test_object.check_values_type() # проверяем типы данных во всех колонках - цифровые или нет
    print(types_ok)
    if colnames_there and types_ok:
        for column_name in column_names_tested:
            column_values = list(df_tested[column_name])
            print(column_name)
            test_object.detect_outliers_IQR_method(column_values)
