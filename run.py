import xlrd
import re
from research_item import Research


startIndex = 0.0
endIndex = 401.0


researchList = []


def read_xlsx_data(filename='teachers_research_update.xlsx'):
    # read data
    workbook = xlrd.open_workbook(filename)
    table = workbook.sheets()[0]
    for row in range(1, table.nrows):
        research_item = Research(table.row_values(row)[0], table.row_values(row)[1], table.row_values(row)[2],
                                table.row_values(row)[3], table.row_values(row)[4], table.row_values(row)[5],
                                table.row_values(row)[6], table.row_values(row)[7])
        researchList.append(research_item)


def is_english_journal(research_item):
    journal_name = research_item.pub
    essay_title = research_item.achi
    # 有期刊信息，已期刊信息判断
    if len(journal_name) > 0:
        return len(re.findall(r'[\u4e00-\u9fff]+', journal_name)) == 0 or '英文期刊' in journal_name
    # 根据文章title判断
    if len(essay_title) > 0:
        return len(re.findall(r'[\u4e00-\u9fff]+', essay_title)) == 0
    # 默认中文期刊
    return False


def get_target_names_in():
    info_summary = {}
    for item in researchList:
        if item.author in info_summary.keys():
            info_summary[item.author] += 1
        else:
            info_summary[item.author] = 1
    # 拼接SQL in
    name_list_str = ""
    for key in info_summary.keys():
        name_list_str += "'" + key + "',"

    return name_list_str[:-1]


def generate_sql():
    pass


if __name__=="__main__":
    read_xlsx_data()
    sql_in_para = get_target_names_in()

    print(sql_in_para)

    print('+++++ All Things Done! ++++')
