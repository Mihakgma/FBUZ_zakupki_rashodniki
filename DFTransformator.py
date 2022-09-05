#from dfs_templates_file import get_df_templates
from pandas import merge as pd_merge
from pandas import DataFrame

class DFtransformator():
    """
    Класс для извлечения в правильном порядке ДФ
    (одних и тех же ячеек у разных филиалов) для
    возможности поиска в них аномально больших / маленьких значений
    (или так называемых "выбросов").
    """

    colnames_right = [
        'наименование',
        'ед_измерения',
        'поставщик',
        'потребность_на_месяц',
        'потребность_на_год',
        'факт_наличие',
        'годовая_потребность',
        'примечания']

    def __init__(self, dfs_dict_in,
                 column_indexes_to_process: list = [3, 4, 5]):
        self.__dfs_dict_in = dfs_dict_in
        self.__column_indexes_to_process = column_indexes_to_process

    def get_dfs_dict_in(self):
        return self.__dfs_dict_in

    def get_column_indexes_to_process(self):
        return self.__column_indexes_to_process

    def extract_short_filename(self, full_path: str):
        short_name = full_path[full_path.rfind('\\') + 1:-5]
        return short_name

    def mul_into_one_column(self, df_in):
        pass

    def transform_dfs(self):
        df_dict_out = {}
        df_dict = self.get_dfs_dict_in()
        column_indexes = self.get_column_indexes_to_process()
        column_key_name = 'key_column'
        flag = True
        start_df = True
        for full_file_path in df_dict:
            # получаем короткие имена файлов (названия филиалов)
            curr_short_filename = self.extract_short_filename(full_file_path)
            print(curr_short_filename)
            for df_sheet in df_dict[full_file_path]:
                curr_df: DataFrame = df_dict[full_file_path][df_sheet]
                curr_df.columns = self.colnames_right
                #print(list(curr_df))
                # отбираем только нужные числовые колонки, по которым будем искать выбросы
                df_colnames_process = [self.colnames_right[colname_ind] for colname_ind in column_indexes]
                # формируем подтаблицу для дальнейшей обработки
                df_process = curr_df[df_colnames_process]
                #print(list(df_process))
                #df_stacked = df_process.stack(dropna=False)
                #df_stacked.columns = [].append(curr_short_filename)
                #if flag:
                #    flag = False
                #    print(df_stacked.index)
                #    print(list(df_stacked))
                #series_name = ('number', 'rowname')

                #df_stacked = df_stacked.to_frame()
                #df_stacked.columns = [].append(curr_short_filename)

                # ДЕЛАЕМ (ФОРМИРУЕМ СОСТАКАННЫЙ ДФ) ПО-НОВОМУ!!!
                values_lst = [] # лист значений
                key_column_lst = [] # лист для идентификаторов - наименование позиции + название колонки
                for column_name in df_colnames_process:
                    curr_column_values = df_process[column_name].to_list()
                    values_lst.extend(curr_column_values)
                    key_tmp_lst = curr_df[self.colnames_right[0]].apply(lambda x: x+'***'+column_name).to_list()
                    key_column_lst.extend(key_tmp_lst)

                #print(f'Длина листа для ключевой колонки: <{len(key_column_lst)}>')
                #print(f'Длина листа для колонки со значениями: <{len(values_lst)}>')

                temp_df_dict = {
                    column_key_name: key_column_lst,
                    curr_short_filename: values_lst
                }

                df_stacked = DataFrame(temp_df_dict)
                #print(df_stacked.dtypes)
                #print(df_stacked.head(1))
                #print(df_stacked.shape)

                if start_df:
                    df_dict_out[df_sheet] = df_stacked
                else:
                    df_previous = df_dict_out[df_sheet]
                    #df_updated = pd_merge(df_previous.rename(series_name), df_stacked.rename(series_name),
                    # left_index=True, right_index=True)
                    df_updated = pd_merge(df_previous, df_stacked,
                                          on=[column_key_name])
                    df_dict_out[df_sheet] = df_updated
            start_df = False
        print(f'Ключи словаря: <{[i for i in list(df_dict_out)]}>')
        print('Размерность ДФ итогового словаря по ключам:')
        for key in df_dict_out:
            this_df = df_dict_out[key]
            print(this_df.shape)
        return df_dict_out
