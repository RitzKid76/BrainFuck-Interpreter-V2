import sys

bits = 8
cells = 255

symbol_index = 0
pointer = 0
tape = cells*[0]

steps = 0
debug = False

class UnbalancedBrackets(Exception):
    def __init__(self, line):
        print("Unbalanced Brackets on line", line)

# def precompiler(program):
#     newlinesplit = program.split('\n')

#     for line in newlinesplit:
#         contents = line.split(' ')
#         if(len(contents) == 2):
#             variable = contents[0][1:]
#             setting = False if contents[1].lower() == 'false' else True
#             vars = globals()
#             if variable in vars:
#                 vars[variable] = setting

def bracket_index(parsed_program):
    output = len(parsed_program)*[0]
    stack = []

    for i, c in enumerate(parsed_program):
        match c:
            case '[':
                stack.append(i)
            case ']':
                if(len(stack)):
                    return_index = stack.pop()
                    output[i] = return_index
                    output[return_index] = i
                else:
                    raise UnbalancedBrackets(i)
            case _:
                pass
    if(len(stack)):
        raise UnbalancedBrackets(i)
    print(output)
    return output

def remove_whitespace(program):
    output = ""
    validsymbols = '+-<>.,[]#$'
    for c in program:
        if(c not in validsymbols):
            continue
        output += c
    return output

def debug_output():
    console = ""
    for i, t in enumerate(tape):
        if(i == pointer):
            console += '[' + str(t) + ']'
        else:
            console += str(t)
        console += ' '
    print(console)

def interpret(program):
    global steps
    global pointer
    global symbol_index
    global debug

    input_queue = []

    # precompiler(program)
    program = [*remove_whitespace(program)]
    
    symbol = program[symbol_index]
    max = 2**bits - 1

    brackets = bracket_index(program)

    while(True):
        steps += 1
        symbol = program[symbol_index]
        match symbol:
            case '+':
                tape[pointer] = (tape[pointer] + 1) if tape[pointer] < max else 0
            case '-':
                tape[pointer] = (tape[pointer] - 1) if tape[pointer] > 0 else max
            case '>':
                pointer = (pointer + 1) if pointer < cells - 1 else 0
            case '<':
                pointer = (pointer - 1) if pointer > 0 else cells - 1
            case '.':
                print(chr(tape[pointer]), end='')
            case ',':
                if(not len(input_queue)):
                    input_text = []
                    while(not len(input_text)):
                        input_text = [*input()]
                    for c in input_text:
                        input_queue.append(c)
                tape[pointer] = ord(input_queue.pop(0))
            case '[':
                if(tape[pointer] == 0):
                    symbol_index = brackets[symbol_index]
            case ']':
                if(tape[pointer] != 0):
                    symbol_index = brackets[symbol_index]
            case '#':
                debug_output()
            case '$':
                debug = False if debug else True
            case _:
                pass
        if(debug):
            debug_output()
        symbol_index += 1
        if symbol_index >= len(program):
            break
    print("\nExecuted in ", steps, " steps")
def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("File not found.")
        return ""

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    program = read_file(file_name)
    if len(program):
        interpret(program)
else:
    print("Please provide a file name as a command line argument.")