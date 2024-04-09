def ReadFile(file):
    tuples_list = []

    f = open(file)
    cont = 0

    for line in f:
        if line:
            prefix, value = line.split(' ', 1)

            if prefix == '1':
                tuples_list.append([prefix+' '+value.rstrip(), ""])

            elif prefix == '2':
                tuples_list[cont][1] = prefix+' '+value.rstrip()
                cont +=1

    #print(tuples_list)

    f.close()
    return tuples_list