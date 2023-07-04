def parse_circuit_file(circuit_file):

    circuit = {}
    with open(circuit_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                node, expression = line.split(' = ')
                operator = expression.split()[1]
                inputs = expression.split()[::2]
                circuit[node] = {'operator': operator, 'inputs': inputs}

    return circuit

def evaluateGate(expression, input):
    operator = expression['operator']
    inputs_list = expression['inputs']
    if operator == '&':
        return input[inputs_list[0]] & input[inputs_list[1]]
    elif operator == '|':
        return input[inputs_list[0]] | input[inputs_list[1]]
    elif operator == '~':
        return ~input[inputs_list[0]]
    elif operator == '^':
        return input[inputs_list[0]] ^ input[inputs_list[1]]
        

def simulate_circuit(circuit_file, fault_node, input):

    circuit = parse_circuit_file(circuit_file)
    for item in circuit:
        circuit[item] = evaluateGate(circuit[item], input)

        fault_node_value = circuit[item] if item == fault_node else 'Error'
    return circuit['Z'], fault_node_value

def identify_fault(circuit_file, fault_node, fault_type):

    # Initialize the input vector
    outputFile = open("output.txt", "w")
    outputFile.close()
    input_combinations = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1],
                          [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1],
                          [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1],
                          [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]]


    for input in input_combinations:

        # Simulate the circuit
        output, fault_node_value = simulate_circuit(circuit_file, fault_node, input)

        if (fault_type == 'SA0' and fault_node_value == 1) or (fault_type == 'SA1' and fault_node_value == 0):
            outputFile = open("output.txt", "a")
            outputFile.write("[A, B, C, D] = ")
            outputFile.write(str(input))
            outputFile.write(", Z = ")
            outputFile.write(str(output) + "\n")
            outputFile.close()


