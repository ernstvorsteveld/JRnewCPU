def compile(source, address, var, symbols, myASCII):
    ASMfile = []
    file = open(source, "r")
    for line in file:
        ASMfile.append(line.strip())
    file.close()

    newProgram = []
    for line in ASMfile:
        if line == "" or line[0] == "#" or line[0] == ";":
            pass
        else:
            newProgram.append(line)

    print(newProgram)

    labels   = {}
    #symbols = symbols
    pc       = address
    vars     = var
    varcount = 0

    binProgram = []

    for line in newProgram:
        if line[0] == ":":
            if line not in labels.keys():
                labels[line] = pc
            else:
                exit("ERROR Label already used : " + line)
        elif line[0] == "@":
            if line not in symbols.keys():
                symbols[line] = pc
            else:
                exit("ERROR Symbol already used : " + line)
        elif line[0] == ".":
            _line = line.split()
            if _line[1] not in symbols.keys():
                symbols[_line[1]] = (vars + varcount)
                varcount = varcount + int(_line[2])  # +1 if lenght must be stored
            else:
                exit("ERROR address already used : " + _line[1])
        elif line[0] == "%":
            _line = line.split()
            if _line[1] in symbols.keys():
                i = 0
                for char in _line[2]:
                    if char in myASCII.keys():
                        newline = symbols[_line[1]] + i, myASCII[char] 
                    else:
                        newline = symbols[_line[1]] + i, myASCII["#"]
                    binProgram.append(newline)
                    i = i + 1
                newline = symbols[_line[1]] + i, myASCII["null"]
                binProgram.append(newline)

            else:
                exit("ERROR address undefined : " + _line[1])
        else:
            pc = pc +1

    print(symbols)

    pc =address
    for line in newProgram:
        instruction = line.split()
        #print(instruction)

        if instruction[0][0] in ["@", ".", ":", "%"]:
            pass

        elif instruction[0] in [ 'out', 'in']:
            newLine = (pc, (instruction[0], int(instruction[1])))
            binProgram.append(newLine) 
            pc = pc +1

        elif instruction[0] in ['lix', 'iix', 'dix', 'lda', 'ldb', 'stx', 'lxa', 'lxb', 'sto', 'sta', 'stb', 'lma', 'lmb']:
            if instruction[1][0] == "$" or instruction[1][0] == "@":
                newLine = (pc, (instruction[0], int(symbols[instruction[1]])))
            else:
                newLine = (pc, (instruction[0], int(instruction[1])))
            binProgram.append(newLine)
            pc = pc +1

        elif instruction[0] in ['call', 'jmp', 'jmpx', 'jmpt', 'jmpf']:
            if instruction[1] in labels.keys():
                newLine = (pc, (instruction[0], labels[instruction[1]]))
            elif instruction[1] in symbols.keys():
                newLine = (pc, (instruction[0], symbols[instruction[1]]))
            else:
                newLine = (pc, (instruction[0], int(instruction[1])))
            binProgram.append(newLine)
            pc = pc +1
        elif instruction[0] in ['test', 'inc', 'dec']:
            newLine = (pc, (instruction[0], (instruction[1])))
            binProgram.append(newLine)
            pc = pc +1
        elif instruction[0] in ['halt', 'ise', 'isz', 'idx','push', 'pop', 'ret', 'add', 'sub', 'mul', 'div', 'skip']:
            newLine = (pc, (instruction[0], None))
            binProgram.append(newLine)
            pc = pc +1
        else:
            exit("Assembler ERROR: Unkown instruction: " + instruction[0])


    return(binProgram, vars + varcount, symbols)       


