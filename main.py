import sys

MATH_NAMES = ["+", "-", "*", "/", "//", "%", "=", "!=", ">", "<", "ИЛИ", "И", "!"]
KEY_WORDS = ["СЧИТАТЬ", "ВЫВОД", "ВВОД", "ВЫХОД", "ПЕРЕЙТИК", "ЕСЛИ", "СЧЁТ", "ЦЕЛ",
             "КУРСОР", "СИМВОЛ", "СТРОКА", "ВВОДСТРОКИ", "СИМВОЛЫ", "ТОЧКА", "НЕЦЕЛ"]


def read_memory(read_string):
    if len(read_string) == 1:
        return program_memory[int(read_string[0])]
    return math_parse(read_string)


def math_parse(math_string):
    skip_iteration = False
    math_stack = []
    get_from_memory = False
    for i in range(len(math_string)):
        if skip_iteration:
            skip_iteration = False
            continue
        if math_string[i] not in MATH_NAMES:
            if math_string[i] == "СЧИТАТЬ":
                skip_iteration = True
                math_stack.append(read_memory(math_string[i + 1:i + 2]))
            else:
                math_stack.append(float(math_string[i]))
        else:
            el1 = math_stack.pop()
            if math_string[i] == "!":
                res = not el1
            else:
                try:
                    el2 = math_stack.pop()
                    if math_string[i] == "+":
                        res = el2 + el1
                    if math_string[i] == "-":
                        res = el2 - el1
                    if math_string[i] == "*":
                        res = el2 * el1
                    if math_string[i] == "/":
                        res = el2 / el1
                    if math_string[i] == "//":
                        res = el2 // el1
                    if math_string[i] == "%":
                        res = el2 % el1
                    if math_string[i] == "=":
                        res = el2 == el1
                    if math_string[i] == "!=":
                        res = el2 != el1
                    if math_string[i] == ">":
                        res = el2 > el1
                    if math_string[i] == "<":
                        res = el2 < el1
                    if math_string[i] == "ИЛИ":
                        res = el2 or el1
                    if math_string[i] == "И":
                        res = el2 and el1
                except IndexError:
                    res = el1
            math_stack.append(float(res))
    return float(math_stack[0])


def instruction_parser():
    global memory_cursor
    global cursor
    global attachments_count
    global goto_points
    conditions = False
    schet = False
    set_cursor = False
    set_memory_cursor = False
    if program[cursor][0] == "ВЫХОД":
        sys.exit(0)
    if program[cursor][0].count("_") == attachments_count:
        for i in range(len(program[cursor])):
            if program[cursor][i] == "СЧЁТ":
                schet = True
            elif schet:
                program_memory[memory_cursor] = math_parse(program[cursor][i:])
                break
            elif set_cursor:
                if program[cursor][i] in goto_points.keys():
                    cursor = goto_points[program[cursor][i]]
                    break
                cursor = int(program[cursor][i]) - 1
                break
            elif program[cursor][i] == "ПЕРЕЙТИК":
                set_cursor = True
            elif set_memory_cursor:
                memory_cursor = int(math_parse(program[cursor][i:]))
                set_memory_cursor = False
            elif program[cursor][i] == "КУРСОР":
                set_memory_cursor = True
            elif program[cursor][i] == "ВЫВОД":
                if len(program[cursor][i:]) == 1:
                    print(int(program_memory[memory_cursor]), end="")
                elif program[cursor][i + 1] == "НЕЦЕЛ":
                    print(program_memory[memory_cursor], end="")
                elif program[cursor][i + 1] == "СИМВОЛ":
                    if len(program[cursor][i:]) == 2:
                        print(chr(program_memory[memory_cursor]), end="")
                    else:
                        char_count = math_parse([program[cursor][i + 2]])
                        for j in range(char_count):
                            print(chr(program_memory[memory_cursor + j]), end="")
                elif program[cursor][i + 1] == "СИМВОЛЫ":
                    memory_reader = memory_cursor
                    while program_memory[memory_reader] != 0:
                        print(chr(program_memory[memory_reader]), end="")
                        memory_reader += 1
                break

            elif program[cursor][i] == "ВВОД":
                user_input = input()
                user_input = user_input.replace(",", ".")
                if len(program[cursor][i:]) == 2 and program[cursor][i + 1] == "НЕЦЕЛ":
                    program_memory[memory_cursor] = float(user_input)
                    continue
                program_memory[memory_cursor] = int(user_input)
            elif program[cursor][i] == "ВВОДСТРОКИ":
                input_string = input()
                input_len = len(input_string)
                if len(program[cursor][i:]) > 1:
                    input_len = math_parse(program[cursor][i + 1:])
                for j in range(input_len):
                    program_memory[memory_cursor + j] = ord(input_string[j])
                program_memory[memory_cursor + input_len] = 0
                break
            elif program[cursor][i] == "ЕСЛИ":
                conditions = True
            elif conditions:
                if math_parse(program[cursor][i:]):
                    attachments_count += 1
                    conditions = False
                    break
                conditions = False
            elif "СТРОКА" in program[cursor][i]:
                for j in range(len(program[cursor][i + 1])):
                    program_memory[memory_cursor + j] = ord(program[cursor][i + 1][j])
                program_memory[memory_cursor + len(program[cursor][i + 1])] = 0
                break
            elif program[cursor][i] == "ЦЕЛ":
                program_memory[memory_cursor] = int(program_memory[memory_cursor])
    elif attachments_count < program[cursor][0].count("_"):
        pass

    elif attachments_count > program[cursor][0].count("_"):
        attachments_count = program[cursor][0].count("_")
        cursor -= 1


if __name__ == "__main__":
    try:
        if sys.argv[1] == "help" or sys.argv[1] == "-help" or sys.argv[1] == "--help":
            print("""
            крайткий курс программирования на FTPL
            
            -КУРСОР <номер ячейки> функция задающая ячейку памяти с которой производятся действия.

            -ВВОД читает числовое значение из консоли и записывает в текущую ячейку памяти
            
            -СЧЁТ <формула> результат математического выражения записанного после этой инструкции будет записан в текущую ячейку памяти
            
            -ЕСЛИ <формула> - инструкция для ветвления, все выражения на следующих строчках перед которыми (через пробел, это важно!) стоит символ "_" в количестве равном количеству вложенности будут выполнены только в том случае если условие истинно.
            
            -СЧИТАТЬ <номер ячейки> не используется как самостоятельная инструкция, указывает инструкциям СЧЁТ, ЕСЛИ и т.д на то, что необходимо взять значение из ячейки памяти.
            
            -ТОЧКА <любое слово> создаёт именованую точку перехода для инструкции ПЕРЕЙТИК
            
            -ПЕРЕЙТИК <номер строки (счёт строк начинать с 1) или именованая точка перехода> инструкция после выполнения которой программа будет выполняться далее с указанной строки. Крайне рекомендуется указывать переход на пустую строку, если в качестве аргумента использовано числовое значение.
            
            -СТРОКА <сама строка>СТРОКА инструккция записшет по 1 символу (ввиде числового значения кода ascii) указанную строку в память начиная с текущей ячейки. Стоит учесть, что строка займёт число символов равное не длине строки, а длине строки + 1, т.к. в конце записывается символ окончания строки.
            
            -ВВОДСТРОКИ <n, не обязательный аргумент> читает строку из консоли и записывает в память как и СТРОКА. При указании числа в качестве аргумента будут записаны только n + 1 символов строки (+1 т.к. всегда записывается символ окончания строки.
            
            -ВЫВОД без аргументов выводит целое число из текущей ячеки памяти. Возможно указание нескольких аргументов:
            
              -СИМВОЛЫ выводит последовательно все символы из ячеек памяти пока не дойдёт до ячейки со значением 0 (конец строки)
            
              -СИМВОЛ выводит 1 символ записанный в текущей ячейке памяти
            
              -СИМВОЛ <n> выводит n символов из ячеек
            
            -ВЫХОД оператор выхода из программы
            
            пример кода (нахождение n числа последовательности фибоначи):
            
            КУРСОР 0
            СТРОКА введите номер числа: СТРОКА
            ВЫВОД СИМВОЛЫ
            КУРСОР 1
            ВВОД
            СЧЁТ СЧИТАТЬ 1 1 -
            КУРСОР 2
            СЧЁТ 0
            КУРСОР 3
            СЧЁТ 1
            КУРСОР 4
            СЧЁТ 1
            ТОЧКА цикл
            ЕСЛИ СЧИТАТЬ 2 СЧИТАТЬ 1 <
            _ КУРСОР 2
            _ СЧЁТ СЧИТАТЬ 2 1 +
            _ КУРСОР 5
            _ СЧЁТ СЧИТАТЬ 4
            _ КУРСОР 4
            _ СЧЁТ СЧИТАТЬ 4 СЧИТАТЬ 3 +
            _ КУРСОР 3
            _ СЧЁТ СЧИТАТЬ 5
            _ ПЕРЕЙТИК цикл
            КУРСОР 4
            ВЫВОД
            ВЫХОД
                
            \n""")
            input("нажмите Enter чтобы закрыть")
            sys.exit(0)
    except Exception:
        print("ОШИБКА!")
        print("файл по указанному пути отсутствует или его местопложение и/или его имя указано не верно!")
        input("Нажмите ENTER для выхода")
        sys.exit(0)
    with open(sys.argv[1], "r", encoding='utf-8') as program_file:
        program = program_file.readlines()
    goto_points = dict()
    for i in range(len(program)):
        if "ТОЧКА" in program[i].split(" ")[0]:
            point = program[i].rstrip("\n").split(" ")[1]
            goto_points[point] = i
            program[i] = [""]
            continue
        if program[i].count("СТРОКА") != 0:
            program[i] = program[i].rstrip("СТРОКА\n")
            command = program[i][:program[i].index("СТРОКА") + 6]
            post_command = program[i][program[i].index("СТРОКА") + 7:]
            program[i] = [command, post_command]
            continue
        program[i] = program[i].rstrip("\n").split(" ")
    cursor = 0
    memory_cursor = 0
    program_memory = [0 for i in range(65536)]
    attachments_count = 0
    try:
        while True:
            instruction_parser()
            cursor += 1
    except Exception:
        print(f"Работа программы завершена с ошибкй на строке номер {cursor + 1}")
        print(f"Ошибка тут -> {" ".join(program[cursor])}")
