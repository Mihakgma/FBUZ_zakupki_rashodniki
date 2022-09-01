#from dfs_templates_file import get_df_templates


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

    def __init__(self, dfs_dict_in):
        self.__dfs_dict_in = dfs_dict_in

    def get_dfs_dict_in(self):
        return self.__dfs_dict_in

    def extract_short_filename(self, full_path: str):
        short_name = full_path[full_path.rfind('\\') + 1:-5]
        return short_name

    def transform_dfs(self):
        df_dict = self.get_dfs_dict_in()
        for full_file_path in df_dict:
            # получаем короткие имена файлов
            curr_short_filename = self.extract_short_filename(full_file_path)
            print(curr_short_filename)
            for df_sheet in df_dict[full_file_path]:
                curr_df = df_dict[full_file_path][df_sheet]
                curr_df.columns = self.colnames_right
                print(list(curr_df))

