import xlrd
import re
import csv
from research_item import Research


startIndex = 0.0
endIndex = 401.0


researchList = []
teacherCNSumDict = {}
teacherENSumDict = {}


def read_csv_data(en_file='teacher_en_research.csv', cn_file='teacher_cn_research.csv'):
    en_csv_reader = csv.reader(open(en_file, encoding='utf-8'))
    for row in en_csv_reader:
        name = row[1]
        employ_id = row[0]
        min_px = row[2]
        teacherENSumDict[name] = [employ_id, min_px]

    cn_csv_reader = csv.reader(open(cn_file, encoding='utf-8'))
    for row in cn_csv_reader:
        name = row[1]
        employ_id = row[0]
        min_px = row[2]
        teacherCNSumDict[name] = [employ_id, min_px]


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


def generate_zwqk_sql(employee_id='', name='', subject='', journal='', year='', px=0):
    sql_str = "INSERT INTO `fudan_research_paper_zwqk` (`ID`, `employee_ID`, `ISI_number`, `name`, `rank`, `subject`, " \
              "`journal`, `year`, `head`, `end`, `hidden`, `px`) " \
              "VALUES (NULL, '{0}', NULL, '{1}', NULL, '{2}', '{3}', '{4}', NULL, NULL, '0', '{5}');"\
        .format(employee_id, name, subject, journal, year, str(px))
    return sql_str


def generate_ywqk_sql(employee_id='', name='', subject='', journal='', year='', px=0):
    sql_str = "INSERT INTO `fudan_research_paper_ywqk` (`ID`, `employee_ID`, `ISI_number`, `name`, `rank`, `subject`, " \
              "`journal`, `year`, `head`, `end`, `hidden`, `px`) " \
              "VALUES (NULL, '{0}', NULL, '{1}', NULL, '{2}', '{3}', '{4}', NULL, NULL, '0', '{5}');"\
        .format(employee_id, name, subject, journal, year, str(px))
    return sql_str


def generate_sql():
    with open('target_script.sql', 'w') as f:
        for item in researchList:
            if item.author not in teacherENSumDict.keys() and item.author not in teacherCNSumDict.keys():
                print("中英文期刊db无作者信息：" + item.author + "，登记号：" + str(item.regNo))
                continue
            if is_english_journal(item):
                if item.author not in teacherENSumDict.keys():
                    print("作者：" + item.author + "第一份英文期刊")
                    employee_id = teacherCNSumDict[item.author][0]
                    px = 2000
                    teacherENSumDict[item.author] = [employee_id, str(1999)]
                    f.write(generate_ywqk_sql(employee_id, item.author, item.achi, item.pub, item.time, px-1) + '\n')
                else:
                    employee_id = teacherENSumDict[item.author][0]
                    px = int(teacherENSumDict[item.author][1])
                    teacherENSumDict[item.author] = [employee_id, str(px-1)]
                    f.write(generate_ywqk_sql(employee_id, item.author, item.achi, item.pub, item.time, px-1) + '\n')
            else:
                if item.author not in teacherCNSumDict.keys():
                    print("作者：" + item.author + "第一份中文期刊")
                    employee_id = teacherENSumDict[item.author][0]
                    px = 2000
                    teacherCNSumDict[item.author] = [employee_id, str(1999)]
                    f.write(generate_ywqk_sql(employee_id, item.author, item.achi, item.pub, item.time, px-1) + '\n')
                else:
                    employee_id = teacherCNSumDict[item.author][0]
                    px = int(teacherCNSumDict[item.author][1])
                    teacherCNSumDict[item.author] = [employee_id, str(px-1)]
                    f.write(generate_zwqk_sql(employee_id, item.author, item.achi, item.pub, item.time, px-1) + '\n')


if __name__=="__main__":
    read_xlsx_data()
    # sql_in_para = get_target_names_in()
    # print(sql_in_para)
    read_csv_data()
    generate_sql()

    print('+++++ All Things Done! ++++')
