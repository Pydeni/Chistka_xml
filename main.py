import xml.etree.ElementTree as ET
import pandas as pd
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')



# Получаем путь, можешь посмотреть work_path через принт
work_path = Path.cwd()

path = Path(work_path, 'ВЧ.xlsx')
path1 = Path(work_path, 'РФ.xlsx')

vch = pd.read_excel(path)
rf = pd.read_excel(path1)

# # Удаляем файлы, которые есть в ВЧ и РФ
# def ydalit(vch,rf):
#     count = 0
#     spispok_xml = os.listdir(r'C:\Users\denis.osipov\PycharmProjects\Chistka_xml\Общая')
#     for xml in spispok_xml:
#         if xml.split()[3][:-4] in vch['Кад. № ОКС'].unique():
#             os.remove(fr'C:\Users\denis.osipov\PycharmProjects\Chistka_xml\Общая\{xml}')
#             print(f'Удален {xml}')
#             count += 1
#     print(f"Закончили удалять из ВЧ, удалено {count}")
#     spispok_xml = os.listdir(r'C:\Users\denis.osipov\PycharmProjects\Chistka_xml\Общая')
#     for xml_1 in spispok_xml:
#         if xml_1.split()[3][:-4] in rf['Кад. № ОКС'].unique():
#             os.remove(fr'C:\Users\denis.osipov\PycharmProjects\Chistka_xml\Общая\{xml_1}')
#             count += 1
#     return count

# print(f'Всего удалено {ydalit(vch,rf)} файлов (из вч и рф)')

# Создаем  скелет датафрейма
shapka = {'Кадастровый № ОКС':[],'Вид ОКС':[],'Назначение':[],'Адрес ОКС':[],'Площадь':[],'Вид права':[],'ФИО':[],'Номер рег. записи':[]}
df = pd.DataFrame(shapka)

# Список тегов, личных данных, которые надо удалить
sp = ['surname','name','patronymic']

# функция удаления тэгов
def delit(elem, sp):
    for el in elem:
        if el.tag in sp:
            continue
        else:
            elem.remove(el)

# Функция получения словаря с данными из xml. Для добавления в пандас фрейм.
def data_from_xml(root):
    # Словарь для добавления строк с данными экселей, в датафрейм
    stroka = dict()
    # Список для фио
    sp = list()
    reg_zap = list()
    # Добавляем данные
    stroka['Кадастровый № ОКС'] = root[2][1][0][0].text
    stroka['Вид ОКС'] = "Здание"
    for znachenie_tag in root.iter('purpose'):
        for znach in znachenie_tag:
            if znach.tag == 'value':
                stroka['Назначение'] = znach.text
    for adress_tag in root.iter('address'):
        for adress in adress_tag:
            if adress.tag == 'readable_address':
                stroka['Адрес ОКС'] = adress.text
    for area_tag in root.iter('params'):
        for area in area_tag:
            if area.tag == 'area':
                stroka['Площадь'] = area.text

    for right_tag in root.iter('right_type'):
        for right in right_tag:
            if right.tag == 'value':
                stroka['Вид права'] = right.text

    for sobstsvennik_tag in root.iter('right_holder'):
        if len(sp) > 0:
            break
        for sobstsvennik in sobstsvennik_tag:
            if sobstsvennik.tag == 'individual':
                for fio_tag in root.iter('individual'):
                    for fio in fio_tag:
                        if fio.tag == 'surname':
                            sp.append(fio.text)
                        elif fio.tag == 'name':
                            sp.append(fio.text)
                        elif fio.tag == 'patronymic':
                            sp.append(fio.text)
                stroka['ФИО'] = '  '.join(sp)
                break
            if sobstsvennik.tag == 'public_formation':
                for municipal_tag in root.iter('municipality'):
                    for municipal in municipal_tag:
                        if municipal.tag == 'name':
                            stroka['ФИО'] = municipal.text
            if sobstsvennik.tag == 'legal_entity':
                for municipal_tag in root.iter('resident'):
                    for municipal in municipal_tag:
                        if municipal.tag == 'name':
                            stroka['ФИО'] = municipal.text

    for right_pravo_tag in root.iter('right_data'):
        for right_pravo in right_pravo_tag:
            if right_pravo.tag == 'right_number':
                reg_zap.append(right_pravo.text)
    stroka['Номер рег. записи'] = '    '.join(reg_zap)
    return stroka

# Читаем содержимое в папке
for f in os.scandir(r'C:\Users\denis.osipov\PycharmProjects\Chistka_xml\Общая'):
    print(f'В работе {f}')
    tree = ET.parse(f)
    root = tree.getroot()
    proverka = False
    #Удаляем хмл, если в ней больше 4 комнат и где в адрессе есть СНТ
    adress = [i.text.split() for i in root.iter('readable_address')]
    for text in adress:
        for snt in text:
            if snt == "СНТ" or snt == 'казарма':
                os.remove(fr'C:\Users\denis.osipov\PycharmProjects\Chistka_xml\Общая\{f.name}')
                print(f'Удален файл {f.name}, тут был СНТ')
                break
        else:
            if len([i for i in root.iter('room_record')]) > 4:
                os.remove(fr'C:\Users\denis.osipov\PycharmProjects\Chistka_xml\Общая\{f.name}')
                print(f'Удален файл {f.name}, комнат больше 4')
                proverka = True
            if proverka == False:
                # Удаляем координаты
                for i in root[2]:
                    if i.tag == "contours":
                        root[2].remove(i)
                for i in root:
                    if i.tag == "restrict_records":
                        root.remove(i)
                # Удаляем личные данные
                for elem in root.iter('individual'):
                    for el in elem:
                        if el.tag != 'surname' or el.tag != 'name' or el.tag != 'patronymic':
                            delit(elem, sp)
                df = df.append(data_from_xml(root), ignore_index=True)

                # # # Перезаписываем xml
                print(f'Перезаписан {f}')
                tree.write(f, encoding='utf-8', xml_declaration=True)




# Обработка книги (ExcelWriter - класс для записи объектов DataFrame в листы Excel). файл эксель создавать не надо, достаточно датафрейма.
# файл создастся сам, когда создаем экземпляр класса writer. Как будет называеться файл и его путь, указать при создание экземпляра writer
# writer = pd.ExcelWriter(r'C:\Users\denis.osipov\PycharmProjects\Chistka_xml\Данные из xml.xlsx')
# df.to_excel(writer, index=False)
# # Автоматическое выравнивание ячеек (выравнивает ячейки исходя из текста внутри)
# for column in df:
#     column_width = max(df[column].astype(str).map(len).max(), len(column))
#     col_idx = df.columns.get_loc(column)
#     writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)
# writer.save()

# print(f'Еще раз проходимся и удаляем из вч и рф, удалено {ydalit(vch,rf)}')

# Для просто записи датафрейма в эксель, без обработки листов
df.to_excel(r'C:\Users\denis.osipov\PycharmProjects\Chistka_xml\Данные из xml.xlsx', index= False)
