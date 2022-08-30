from DirChecker import check_dir_contain
from excel_parser import excel_to_data_frame_parser
from sheeet_names import sheets_dict
from dfs_templates_file import get_df_templates
from save_dfs_excel_sheets_file import SaveDataFrames


# файл для процессинга всех файлов
# путь к папке для тестового запуска
#D:\ФБУЗ_ЦГиЭКО\Остатки_расходников\СВОД\ТЕСТОВЫЕ ДАННЫЕ ДЛЯ РАЗРАБОТКИ ПРИЛОЖЕНИЯ!!!\Филиалы
#D:\ФБУЗ_ЦГиЭКО\Остатки_расходников\СВОД\ТЕСТОВЫЕ ДАННЫЕ ДЛЯ РАЗРАБОТКИ ПРИЛОЖЕНИЯ!!!\ИЛЦ

sheets = [i for i in sheets_dict]

def extract_dfs(files_lst:list,
                sheet_names:list):
    """

    :param files_lst: список полных путей к файлам для парсинга в виде строк
           sheet_names: список названий листов в шаблоне
    :return: словарь словарей по названию файла (ключ) - название листа (ключ) - ДФ
    """
    dfs_dict = {}
    ###
    # Начало основной части кода функции
    for curr_file_path in files_lst:
        dfs_dict[curr_file_path] = {}
        print(curr_file_path)
        #short_filename = curr_file_path[curr_file_path.rfind('\\')+1:-5]
        #print(short_filename)
        for sheet in sheet_names:
            temp_df = excel_to_data_frame_parser(file=curr_file_path,
                                                 sheet_name=sheet,
                                                 rows_to_skip=2)
            dfs_dict[curr_file_path][sheet] = temp_df
            #printDimensionsOfDF(temp_df, sheet)
    # Конец основного кода функции
    ###
    return dfs_dict

def smart_fillna(df, str_cols_lst, num_col_lst):
    """
    в исходном ДФ заменяет заданные пропущенные значения по заданным
    колонкам (строковые и численные) на пустую строку и ноли соответственно
    :param df:
    :return:
    измененный ДФ с заполненными пустыми значениями согласно заданию
    """

    str_values = {}
    digit_values = {}
    for current_colname in str_cols_lst:
        str_values[current_colname] = ''
    for current_colname in num_col_lst:
        digit_values[current_colname] = 0
    df.fillna(value=str_values, inplace=True)
    df.fillna(value=digit_values, inplace=True)
    #df[[num_col_lst]] = df[[num_col_lst]].fillna(0)

    return df

def add_file_name_to_str(text:str, filename:str, divider:str=';'):
    text = text.replace('/=', '')
    text_refined = str(text).strip()
    out_text = text
    if len(text_refined) > 0:
        out_text = divider + ' <' + filename + '>: ' + text_refined
    return out_text

def replace_str_cont(df, str_colnames: list, file_name: str):
    #print(str_colnames)
    column_names_df = list(df)
    for colname_index in range(len(str_colnames)):
        colname = str_colnames[colname_index]
        #colname_in_df = ['НЕТ', 'ДА'][colname in column_names_df]
        #print(f'Столбец с названием <{colname}> присутствует в ДФ: <{colname_in_df}>')
        #print(colname)
        #print(f'Типы данных по колонкам: {df.dtypes}')
        df[colname] = df[colname].apply(lambda x: add_file_name_to_str(text=x,
                                                                       filename=file_name))
    return df


def summarize_dfs(dfs_dict:dict, sheet_names:list, df_templates:dict):
    """
    суммирует ДФ с одинаковыми названиями листов
    :param dfs_dict: словарь с названиями файлов и вложенными словарями,
    где в свою очередь ключами являются названия листов
    :param sheet_names: собственно сами названия листов
    :param df_templates - словарь с шаблонами ДФ, где ключ - это имя листа (универсальное!)
    значенение - сам шаблон ДФ с правильным (корректным наименованием колонок)
    :return:
    словарь с ДФ с ключами по названиям листов (уже не словарь словарей!!!)
    """

    dfs_summarized = {}
    df_verify = {}
    ###
    # Начало основной части кода функции

    # создаем пустые ДФ на каждое название листа
    # в них по мере итериации по словарю будет накапливаться сумма

    start_flag = True
    colnames = list(df_templates[sheet_names[0]])
    str_cont_columns = []
    str_cont_columns.append(colnames[0])
    str_cont_columns.append(colnames[-1])
    #str_cont_columns = ['поставщик', 'примечания']
    #str_cont_columns = ['примечания']
    print(f'Строковые колонки: <{str_cont_columns}>')
    digit_cont_columns = colnames[1:-1]
    print(f'Числовые колонки: <{digit_cont_columns}>')

    for file in dfs_dict:
        short_filename = file[file.rfind('\\') + 1:-5]
        print(short_filename)
        if start_flag:
            start_flag = False
            for sheet in sheet_names:
                basic_df = dfs_dict[file][sheet]
                rownames_values = basic_df.iloc[:,:2]
                df_verify[sheet] = rownames_values
                #print(rownames_values)
                basic_df = basic_df.iloc[:,2:]
                basic_df.columns = colnames
                #print(list(basic_df))
                # выборочная замена пропущенных значений
                basic_df = smart_fillna(df=basic_df,
                                        str_cols_lst=str_cont_columns,
                                        num_col_lst=digit_cont_columns)
                basic_df = replace_str_cont(basic_df,
                                            str_cont_columns,
                                            short_filename)
                dfs_summarized[sheet] = basic_df
        else:
            for sheet in sheet_names:
                print(sheet)
                basic_df = dfs_summarized[sheet]
                new_df = dfs_dict[file][sheet]
                rownames_values_etalon = df_verify[sheet]
                rownames_values_for_check = new_df.iloc[:, :2]

                # сравниваем "эталон" (1-ый спарсенный файл) с данным ДФ (первые столбцы)
                #if rownames_values_etalon == rownames_values_for_check:
                #    dfs_are_equal = True
                #else:
                #    dfs_are_equal = False
                no_yes = ['НЕТ', 'ДА'][rownames_values_etalon.equals(rownames_values_for_check)]
                print(f'Строки в данном ДФ идиентичны эталону: <{no_yes}>')
                new_df = new_df.iloc[:, 2:]
                new_df.columns = colnames
                #print(list(new_df))
                # выборочная замена пропущенных значений
                new_df = smart_fillna(df=new_df,
                                        str_cols_lst=str_cont_columns,
                                        num_col_lst=digit_cont_columns)
                new_df = replace_str_cont(new_df,
                                          str_cont_columns,
                                          short_filename)
                dfs_summarized[sheet] = basic_df + new_df

    # Конец основного кода функции
    ###
    return dfs_summarized

if __name__ == "__main__":
    dir_cont_info = check_dir_contain()
    file_paths = dir_cont_info[0]
    files_format_ok = dir_cont_info[1]
    wrong_files = dir_cont_info[3]
    if files_format_ok:
        extracted_dfs = extract_dfs(files_lst=file_paths,
                                    sheet_names=sheets)
        templates = get_df_templates()

        result_df_dict = summarize_dfs(extracted_dfs, sheets, templates)
        SaveDataFrames(dfs_dict=result_df_dict).save_excel_file()
        #print(result_df_dict[sheets[0]].head(15))
        #print(result_df_dict[sheets[1]].head(15))
        #print(result_df_dict[sheets[2]].head(15))
        # выводим на печать ключи словаря
        #print([i for i in extracted_dfs])
    else: # формат хотя бы одного из файлов не соответствует заданному!!!
        print('Проверьте файлы в указанной директории! В частности следующие файлы:')
        print([file for file in wrong_files], sep='\n')
    input('Для завершения нажми клавишу Enter')