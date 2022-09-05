from DirChecker import check_dir_contain
from sheeet_names import sheets_dict
from dfs_templates_file import get_df_templates
from save_dfs_excel_sheets_file import SaveDataFrames
from DFProcessing import extract_dfs, summarize_dfs
#from DFTransformator import DFtransformator


# файл для процессинга всех файлов
# путь к папке для тестового запуска
#D:\ФБУЗ_ЦГиЭКО\Остатки_расходников\СВОД\ТЕСТОВЫЕ ДАННЫЕ ДЛЯ РАЗРАБОТКИ ПРИЛОЖЕНИЯ!!!\Филиалы
#D:\ФБУЗ_ЦГиЭКО\Остатки_расходников\СВОД\ТЕСТОВЫЕ ДАННЫЕ ДЛЯ РАЗРАБОТКИ ПРИЛОЖЕНИЯ!!!\ИЛЦ

sheets = [i for i in sheets_dict]


if __name__ == "__main__":
    dir_cont_info = check_dir_contain()
    file_paths = dir_cont_info[0]
    files_format_ok = dir_cont_info[1]
    wrong_files = dir_cont_info[3]
    if files_format_ok:
        extracted_dfs = extract_dfs(files_lst=file_paths,
                                    sheet_names=sheets)
        #print(list(extracted_dfs))

        # Трансформация ДФ для поиска выбросов
        # Начало участка

        # ЗАКОММЕНТИРОВАТЬ!!! - для работы в штатном режиме
        #transformed_dfs = DFtransformator(extracted_dfs).transform_dfs()
        #SaveDataFrames(dfs_dict=transformed_dfs).save_excel_file()

        # Конец участка

        templates = get_df_templates()

        result_df_dict = summarize_dfs(extracted_dfs, sheets, templates)
        # РАЗКОММЕНТИРОВАТЬ!!! - для работы в штатном режиме
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
