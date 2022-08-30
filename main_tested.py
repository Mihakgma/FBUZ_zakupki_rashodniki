from DirChecker import check_dir_contain
from excel_parser import excel_to_data_frame_parser, printDimensionsOfDF

# файл для тестового запуска модулей программы!
# путь к папке для тестового запуска
#D:\ФБУЗ_ЦГиЭКО\Остатки_расходников\СВОД\ТЕСТОВЫЕ ДАННЫЕ ДЛЯ РАЗРАБОТКИ ПРИЛОЖЕНИЯ!!!\Филиалы

if __name__ == "__main__":
    dir_cont_info = check_dir_contain()
    file_paths = dir_cont_info[0]
    test_df = excel_to_data_frame_parser(file=file_paths[0],
                                         sheet_name='вирус',
                                         rows_to_skip=2)
    printDimensionsOfDF(test_df, 'Исходная подгрузка')
    print(test_df.head())
    print(test_df.tail())
    print(test_df.iloc[:,2:].dtypes)