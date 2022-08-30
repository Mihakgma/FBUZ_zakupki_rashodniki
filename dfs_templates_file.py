from pandas import DataFrame as pd_DataFrame
from sheeet_names import sheets_dict

def get_df_templates(temp_dict=sheets_dict):
    sheets = [i for i in temp_dict]
    colnames_dict = {
        'наименование':'',
        'ед_измерения':'',
        'поставщик':'str',
        'потребность_на_месяц': 'int',
        'потребность_на_год': 'int',
        'факт_наличие': 'int',
        'годовая_потребность': 'int',
        'примечания':'str'}
    df_templates = {}
    for sheet in sheets:
        print(sheet)
        curr_nrows = temp_dict[sheet][0]
        empty_str_lst = [''] * curr_nrows
        empty_num_lst = [0] * curr_nrows
        template = {}

        for colname in colnames_dict:
            column_type = colnames_dict[colname]
            if column_type == 'str':
                template[colname] = empty_str_lst
            elif column_type == 'int':
                template[colname] = empty_num_lst

        df_temp = pd_DataFrame(template)
        print(df_temp.shape)
        df_templates[sheet] = df_temp
    return df_templates


if __name__ == "__main__":
    sheet = list(sheets_dict)[0]
    templates_dict = get_df_templates()
    #print(templates_dict)
    print(templates_dict[sheet].head())
    print(templates_dict[sheet].dtypes)
    #print(list(templates_dict[sheet])[0,-1])
    print(list(templates_dict[sheet])[1:-1])