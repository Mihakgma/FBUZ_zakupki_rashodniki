from os import listdir, chdir, getcwd

def check_dir_contain(file_format:str = 'xlsx'):
    """
    Принимает строку - путь к директории.
    Формат искомых файлов
    Проверяет содержимое папки
    В процессе выполнения функции меняется рабочая директория
    После выполнения кода она меняется на исходную

    :return:
    кортеж (его элементы):
     1) список всех файлов (полный путь) в виде списка;
     2) логич значение - все ли файлы в директории имеют данное расширение;
     3) количество всех файлов вне зависимости от формата;
     4) список файлов с некорректным форматом.
    """
    prev_wd = getcwd()
    all_files_right_format = False
    wrong_format_files = []
    #print(prev_wd)
    dir_path = input('Введите полный путь к папке: ')
    chdir(rf'{dir_path}')
    #print(getcwd())
    files = listdir()
    all_files_number = len(files)
    num_files_ends_with_right_format = sum([True for file in files if file.endswith(file_format)])
    wrong_format_files = [file for file in files if not file.endswith(file_format)]
    #print(num_files_ends_with_right_format)
    if num_files_ends_with_right_format == all_files_number:
        print(f'ВСЕ <{all_files_number}> файлов имеют заданный формат: <{file_format}>')
        all_files_right_format = True
    else:
        print(f'НЕ ВСЕ <{all_files_number}> файлов имеют заданный формат: <{file_format}>')
    files_full_paths = ([(dir_path+'\\')+file for file in files])
    chdir(rf'{prev_wd}')
    return(
        files_full_paths,
        all_files_right_format,
        all_files_number,
        wrong_format_files
    )



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = check_dir_contain()
    print(a)

