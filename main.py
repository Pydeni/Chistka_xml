import xml.etree.ElementTree as ET
from openpyxl import load_workbook

# Парсим хмл
tree = ET.parse('Выписка из реестра 50_04_0000000_13956.xml')
root = tree.getroot()



for i in root.iter('individual'):
    for y in i:
        print(y.tag)
# Удаляем
for i in range(4):
    root[4][0][2][0][0].remove(root[4][0][2][0][0][3])


tree.write('Выписка из реестра 50_04_0000000_13956.xml', encoding='utf-8', xml_declaration=True)