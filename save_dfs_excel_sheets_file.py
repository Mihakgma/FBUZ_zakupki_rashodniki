from os import getcwd, makedirs
from DateCheckerFile import DateChecker
from pandas import ExcelWriter as pd_ExcelWriter


class SaveDataFrames():

    def __init__(self,
                 dfs_dict: dict,
                 results_dir_path:str = '\\РЕЗУЛЬТАТЫ\\',
                 need_sheets_formatting:bool = True):
        self.__dfs_dict = dfs_dict
        self.__results_dir_path = results_dir_path
        self.__need_sheets_formatting = need_sheets_formatting

    def get_dfs_dict(self):
        return self.__dfs_dict

    def get_results_dir_path(self):
        return self.__results_dir_path

    def get_need_sheets_formatting(self):
        return self.__need_sheets_formatting

    def get_full_dir_path(self, destination: str = 'result'):
        """
        Если destination == 'result',
        то выдает путь к папке с рещультатами.
        если destination == 'parent',
        тогда выдает полный путь к базовой
        (с местоположением основных файлов)
        """
        results_path = self.get_results_dir_path()
        current_wd = getcwd()
        if destination == 'result':
            results_full_path = current_wd + results_path
            #print(listdir(results_full_path))
            return results_full_path

    def get_today_date(self):
        today_date = DateChecker('').get_today_date('medium')
        today_date = today_date.replace(':', '_').replace(' ', '_')
        return today_date

    def save_excel_file(self):
        today_date_str = self.get_today_date()
        full_res_path = self.get_full_dir_path()
        tables_dict = self.get_dfs_dict()
        need_format = self.get_need_sheets_formatting()
        #basic_wd = getcwd()
        # путь для папки с результатами
        # если такая папка не существует, тогда создаем ее!!!
        try:
            makedirs(full_res_path)
            print('Папка для сохранения Excel-файлов успешно создана!')
        except:
            print('Папка для сохранения Excel-файлов была создана ранее !')
        writer = pd_ExcelWriter(full_res_path
                                +'СВОДНАЯ_Остатки_РМ_'
                                + today_date_str + '.xlsx',
                                engine='xlsxwriter')

        for sheet in tables_dict:
            current_df = tables_dict[sheet]
            current_df_shape = current_df.shape
            nrows, ncols = current_df_shape
            print(sheet)
            print(f'Размерность ДФ: <{current_df_shape}>')
            current_df.to_excel(writer, f'{sheet}', index=False)
            print()
            if need_format:
                # форматирование текущего листа
                # ширина столбцов
                worksheet = writer.sheets[sheet]
                worksheet.set_column(0, 0, 25) # Первый столбец таблицы
                worksheet.set_column(1, ncols, 17) # От второго (включительно) и до последнего столбца таблицы

        writer.save()


if __name__ == "__main__":
    # проверка корректности работы модуля
    SaveDataFrames({}).save_excel_file()
