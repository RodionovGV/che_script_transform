import sys
import re

# Файлы для отладки
INPUT_FILE = "input"
OUTPUT_FILE = "output"
EXT = ".md"

# Имена файлов через аргументы консоли
if len (sys.argv) > 1:
    INPUT_FILE = sys.argv[1]
    OUTPUT_FILE = INPUT_FILE

INPUT_POST_FILE = INPUT_FILE + "_pred" 

'''
ссылки
Проверка регулярного выражения
https://regex101.com/r/T3Oabh/1/

Примеры:
https://pythonru.com/primery/primery-primeneniya-regulyarnyh-vyrazheniy-v-python
https://habr.com/ru/post/349860/
https://tproger.ru/translations/regular-expression-python/

https://unicode-table.com/ru/2153/
1/2 ½
1/3 ⅓
1/4 ¼
3/4 ¾
'''    

'''
Правила преобразования входного текста

'''
list_rules = [
    (r'(\s{2,})()', r' '), # Убрать пробелы больше 2х и Замена более одного перевода строки на один
    (r'^(\s)', r''), # Убрать пробел в начале строки
    (r'--', r' — '), # -- тире  '--' на ' — '
    (r'(\d) (—) (\d)', r'\1\2\3'), # -- тире между числами на '—'
    (r'(\s{2,})()', r' '), # повтор, так как правило с -- добавляет лишние пробелы
    (r'([[])((?!#|0x).*?)([]])', r'\[\2\]'), # Отформатировать [] в \[\] кроме [# N] и [0x01 ]
    (r'([a-zA-Zа-яА-ЯёЁ"])(\d{1,3})', r'\1[^\2]'), # Оформление ссылок
    (r'([a-zA-Zа-яА-ЯёЁ"])(\*{2,})', r'\1[^\2]'), # Оформление ссылок редактора !Внимание, срабатывает не срабатывает на первой * т.к.
                                                  # конфликтует с выделением *жирным*.
    
    #Повторяющиеся ошибки
    (r'Вас. Петр,', r'Вас. Петр.'), # 
    (r'т.-е.', r'т. е.'), # 
    (r'No', r'№'), # 
    
    #дроби
    (r'1/2', r'½'), # 
    (r'1/3', r'⅓'), # 
    (r'1/4', r'¼'), # 
    (r'3/4', r'¾'), # 
    #(r'(\d[2-9])/(\d[5-9])', r'--->\1 \ \2 <---'), # поиск не стандартных дробей
    
]
ref_rules =[
    (r'\[\^\d{1,}\]', r''), #[0][0] Оформление ссылок
    (r'[(\[^*{2,}\])]', r''), #[1][0] Оформление ссылок редактора !Внимание, срабатывает не срабатывает на первой * т.к.
                                                  # конфликтует с выделением *жирным*.
    ]


regex_num = re.compile(ref_rules[1][0])
list_ref = regex_num.findall("lа question[^**] religieuse[^***]")

print(list_ref)
print('--------------------------------------------------')

in_data = []
out_data = []
list_ref = []
# Чтение из файла 1 
# file.read().splitlines()
with open(INPUT_FILE + EXT, "r", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip()
        in_data.append(line)


# Применение 2х правил к входному файлу        
for line in in_data:
    if (line == '\n'):
        continue
    # пропускаем строку если есть в ней
    # для картинок
    if ('![' in line):
        out_data.append(line)
        continue
        
    # Применение 2x правил из списка list_rules для создания файла
    # более удобного для сравнения
    # re_val[0] - регулярное выражение
    # re_val[1] - подстановка
    for re_val in list_rules[0:2]:
        print(re_val)
        line = re.sub(re_val[0], re_val[1], line)
        
    # Добавление абзацев в выходной файл
    out_data.append(line)
        
## Сохранение в INPUT_POST_FILE
with open(INPUT_POST_FILE + EXT, "w", encoding="utf-8") as f:
    for line in out_data:
        if line == '':
            continue
        f.write(line + "\n\n")   

# Обнуление списков
in_data = []
out_data = []
list_ref = []

## Открытие в INPUT_POST_FILE
with open(INPUT_POST_FILE + EXT, "r", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip()
        in_data.append(line)
        
# Применение правил к входному файлу        
for line in in_data:
    if (line == '\n'):
        continue
    
    # пропускаем строку если есть в ней
    # для картинок
    if ('![' in line):
        out_data.append(line)
        continue
    
    # Применение основных правил из списка list_rules
    # re_val[0] - регулярное выражение
    # re_val[1] - подстановка
    for re_val in list_rules:
        line = re.sub(re_val[0], re_val[1], line)
    
    # вывод обработанных абзацев в консоль
    print(line)
    
    # Добавление абзацев в выходной файл
    out_data.append(line)
    
    # добавление общих сносок после абзаца где они встетились
    regex_num = re.compile(ref_rules[0][0])
    list_ref = regex_num.findall(line)
    for elem in list_ref:
        out_data.append(elem + ': ') 
    

## Сохранение
with open(OUTPUT_FILE + "_done" + EXT, "w", encoding="utf-8") as f:
    for line in out_data:
        if line == '':
            continue
        f.write(line + "\n\n")    