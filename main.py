import sys

MATH_NAMES = ["+", "-", "*", "/", "//", "%", "=", "!=", ">", "<", "ИЛИ", "И", "!", "СЧИТАТЬ"]
KEY_WORDS = ["ВЫВОД", "ВВОД", "ВЫХОД", "ПЕРЕЙТИК", "ЕСЛИ", "СЧЁТ", "ЦЕЛ",
             "КУРСОР", "СИМВОЛ", "СТРОКА", "ВВОДСТРОКИ", "СИМВОЛЫ", "ТОЧКА", "НЕЦЕЛ",
             "СЧИТАТЬФАЙЛ", "ЗАПИСАТЬФАЙЛ"]



def math_parse(math_string):
    math_stack = []
    for i in range(len(math_string)):
        if math_string[i] not in MATH_NAMES:
            math_stack.append(float(math_string[i]))
        else:
            el1 = math_stack.pop()
            if math_string[i] == "!":
                res = not el1
            elif math_string[i] == "СЧИТАТЬ":
                res = program_memory[int(el1)]
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
            elif program[cursor][i] == "ЦЕЛ":
                program_memory[memory_cursor] = int(program_memory[memory_cursor])
            elif program[cursor][i] == "СЧИТАТЬФАЙЛ":
                if program[cursor][i + 1] not in MATH_NAMES and program[cursor][i + 1] not in KEY_WORDS:
                    read_cursor = int(math_parse(program[cursor][i + 1:]))
                    filename_chars = []
                    while program_memory[read_cursor] != 0:
                        filename_chars.append(chr(program_memory[read_cursor]))
                        read_cursor += 1
                    filename = "".join(filename_chars)

                with open(filename, "rb") as file:
                    byte = file.read(1)
                    write_cursor = memory_cursor
                    while byte != b"":
                        program_memory[write_cursor] = int.from_bytes(byte)
                        byte = file.read(1)
                        write_cursor += 1
                    program_memory[write_cursor] = 0
                break

            elif "СТРОКА" in program[cursor][i]:
                for j in range(len(program[cursor][i + 1])):
                    program_memory[memory_cursor + j] = ord(program[cursor][i + 1][j])
                program_memory[memory_cursor + len(program[cursor][i + 1])] = 0
                break


    elif attachments_count < program[cursor][0].count("_"):
        pass

    elif attachments_count > program[cursor][0].count("_"):
        attachments_count = program[cursor][0].count("_")
        cursor -= 1


if __name__ == "__main__":
    try:
        with open(sys.argv[1], "r", encoding='utf-8') as program_file:
            program = program_file.readlines()
    except Exception:
        print("ОШИБКА!")
        print("файл по указанному пути отсутствует!")
        input("Нажмите ENTER для выхода")
        sys.exit(0)
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
    if len(sys.argv) > 2 and sys.argv[2] == "--memory":
        program_memory = [0 for i in range(int(sys.argv[3]))]
    else:
        program_memory = [0 for i in range(65536)]
    attachments_count = 0
    try:
        while True:
            instruction_parser()
            cursor += 1
    except Exception as x:
        print(f"Работа программы завершена с ошибкй на строке номер {cursor + 1}")
        print(f"Ошибка тут -> {" ".join(program[cursor])}")