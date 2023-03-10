import xml.etree.ElementTree as ET
from openpyxl import load_workbook

# Парсим хмл
tree = ET.parse('Выписка из реестра 50_04_0000000_13956.xml')
root = tree.getroot()



for i in root.iter('individual'):
    for y in i:
        print(y.tag)

root[0][4][0][2][0].remove(root[0][4][0][2][0][3])
