import sqlite3
from ParserXBRL import *


file_url='xbrls2/縲職00040縲鷹未譚ｱ螟ｩ辟ｶ逑ｦ譁ｯ髢狗匱譬ｪ蠑丈ｼ夂､ｾ 譛我ｾ｡險ｼ蛻ｸ蝣ｱ蜻頑嶌 窶・隨ｬ149譛滂ｼ亥ｹｳ謌・2蟷ｴ1譛・譌･ 窶・蟷ｳ謌・2蟷ｴ12譛・1譌･・・xbrl'

conn = sqlite3.connect('xlrd_data.db')
c = conn.cursor()

sql2 = 'SELECT id, parameter_name FROM parameters'
parameters_data = c.execute(sql2).fetchall()


print(parameters_data)