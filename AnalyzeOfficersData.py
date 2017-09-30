import glob

from bs4 import BeautifulSoup
from IPython.display import HTML, display
from cssutils import parseStyle
import pandas as pd

import re


def get_col_spans(header_row):
    col_spans=[]
    for i in range(0, len(header_row)):
        col_span=header_row.contents[i].get('colspan')
        if (col_span):
            col_spans.append(col_span)
        else:
            col_spans.append(0)
    return col_spans


def get_row_spans(table_row):
    row_spans=[]
    for i in range(0, len(table_row)):
        col_span=table_row.contents[i].get('rowspan')
        if (col_span):
            row_spans.append(col_span)
        else:
            row_spans.append(0)
    return row_spans


def merge_table_cols(table_body, first_cells_col_num, colspan):
    for table_row in table_body:
        if(len(table_row)>first_cells_col_num):
            first_cell = table_row.contents[first_cells_col_num]
            if (not first_cell.has_attr("colspan") or int(first_cell["colspan"]) != colspan):
                # 最初のセルのcolspan書き換え
                first_cell["colspan"] = colspan

                for index_from_first_cell_num in range(1, colspan):
                    # セルの中身を最初のセルにコピペ
                    first_cell.contents.extend(
                        table_row.contents[first_cells_col_num + index_from_first_cell_num].contents
                    )

                for index_from_first_cell_num in range(1, colspan):
                    # セル削除
                    del table_row.contents[first_cells_col_num + 1]


def merge_table_rows(table_body,first_row_num,col_num,rowspan):
    # rowspanを１行に戻す
    table_body[first_row_num].contents[col_num]["rowspan"]=1

    """
    1行目のrowspanを1に戻すと下の行が１つ無いことになってしまう。
    なのでrowspanでまたがってた行には同じ内容をそれらの行の同じカラム番に入れることで連結を解除する
    """
    for row in range(1,rowspan):
        table_body[first_row_num+row].contents.insert(col_num,table_body[first_row_num].contents[col_num])


def search_table(file_name,match):
    element_name = "table"
    with open(file_name,
              "r") as file:
        doc = BeautifulSoup(file, "lxml")
        tables = doc.find_all(element_name)
        if not tables:
            raise ValueError('No tables found')
        result = []
        unique_tables = set()

        for table in tables:
            if (table not in unique_tables and table.find(text=match) is not None):
                result.append(table)
            unique_tables.add(table)

        return result


def get_formatted_table(file_name, match, header=0):
    result = search_table(file_name, match)

    data_frames = []
    for table in result:
        table_head = table.contents[0]
        table_body = table.contents[1:]

        for row_index, row in enumerate(table_body):
            row_spans = get_row_spans(row)

            for col_index, row_span in enumerate(row_spans):
                row_span = int(row_span)
                if (row_span > 0):
                    merge_table_rows(table_body, row_index, col_index, row_span)
        col_spans = list(map(lambda col_span: int(col_span), get_col_spans(table_head)))

        for index, col_span in enumerate(col_spans):
            if (col_span > 0):
                merge_table_cols(table_body, index, col_span)

        import pandas as pd

        df = pd.read_html(str(table), header=header)
        df1 = df[0]
        data_frames.append(df1)
    return data_frames


def save_officers_data(file_name):
    result1 = get_formatted_table(file_name, "略歴", header=0)
    officers_data = pd.DataFrame()
    for result in result1:
        result = result.dropna(subset=["氏名"])
        officers_data = officers_data.append(result, ignore_index=True)
    print(officers_data)

    officers_names_compiled = [re.compile(r"" + officer_name.replace(" ", "")) for officer_name in officers_data["氏名"]]

    stock_data = pd.DataFrame()
    result2 = get_formatted_table(file_name, "氏名又は名称", 0)
    for result in result2:
        if (result.columns.values[0] == "氏名又は名称"):
            for key, row in result.iterrows():
                for name_index, name in enumerate(officers_names_compiled):
                    matchOB = re.search(name, row["氏名又は名称"].replace(" ", ""))
                    if (matchOB is not None):
                        # display(pd.DataFrame(row).T)
                        # display(pd.DataFrame(officers_data.loc[name_index]).T)
                        data = pd.concat([pd.DataFrame(row).T.reset_index(drop=True),
                                          pd.DataFrame(officers_data.loc[name_index]).T.reset_index(drop=True)], axis=1,
                                         join='outer', ignore_index=True)
                        stock_data = stock_data.append(data)

    for key, stock_data_row in stock_data.iterrows():
        stock_data_row[8] = re.sub(r'[０-９ 0-9]+?年[０-９ 0-9]+?月', "", stock_data_row[8])
        stock_data_row[8] = re.sub(r'平成|昭和', "\n", stock_data_row[8])

    file_name = file_name.split("/")[-1].split("（")[0]
    print(file_name)
    text = (file_name + "\n" + stock_data.to_csv() + "\n")
    text = text.encode('cp932', 'ignore')
    with open('officers_data.csv', mode='ab') as f:
        f.write(text)


for file_name in glob.glob('/Users/sonekenichiro/development/EdinetDownload/pdf_html/*.html'):
    save_officers_data(file_name)


"""[('60', '４'), ('11', '９')]
[('２', '４'), ('14', '１'), ('17', '９')]
[('４', '４'), ('17', '２'), ('17', '９')]
[('10', '４'), ('15', '１'), ('15', '12'), ('19', '10'), ('21', '12')]
[('７', '４'), ('９', '８'), ('11', '１'), ('11', '９'), ('12', '９'), ('15', '６'), ('17', '２'), ('19', '10'), ('21', '12')]
[('11', '４'), ('17', '２'), ('19', '10'), ('21', '12')]"""