import xml.etree.ElementTree as ET
from openpyxl import load_workbook
import os

sp = ['surname','name','patronymic']
# функция удаления тэгов
def delit(elem, sp):
    for el in elem:
        if el.tag in sp:
            continue
        else:
            elem.remove(el)

#прочитать содержимое
for f in os.scandir(r'C:\\Users\\Denis\\PycharmProjects\\Chistka_xml\\1'):
    tree = ET.parse(f.name)
    root = tree.getroot()
    # Удаляем координаты
    for i in root[2]:
        if i.tag == "contours":
            root[2].remove(i)
    # Удаляем личные данные
    for elem in root.iter('individual'):
        while True:
            if len(elem) == len(sp):
                break
            else:
                delit(elem, sp)

    # Перезаписываем xml
    tree.write(f.name, encoding='utf-8', xml_declaration=True)




