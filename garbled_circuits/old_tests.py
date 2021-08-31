# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 18:34:48 2021

@author: Garret_H
"""


#DONT TOUCH, IT WORKS
def test_subtractor(how_many, input_size, verbose=True):
    base_in = '{:0' + str(input_size) + 'b}'
    
    a_input = [random.randint(2**(input_size-2),2**(input_size-1)) for i in range(how_many)]
    b_input = [random.randint(0,2**(input_size-2)) for i in range(how_many)]
    values = str(a_input) + str(b_input)
    true_result = [int(x) for i in range(how_many) for x in base_in.format(a_input[i]-b_input[i])]
    a_input = [int(x) for a in a_input for x in base_in.format(a)]
    add = [0 for _ in range(input_size + 1)]
    add.extend(a_input)
    a_input = add
    b_input = [int(x) for b in b_input for x in base_in.format(b)]
    
    subtractor = Subtractor_circuit(how_many, input_size)
    subtractor.subtractor()
    circuit = "subtractor.json"
    
    res = main(circuit, a_input, b_input)
    view('subtractor', values, true_result, list(res.values())[::-1], verbose)

#DONT TOUCH, IT WORKS
def test_sieve(how_many, input_size, verbose=True):
    base_in = '{:0' + str(input_size) + 'b}'
    
    a_input = [random.randint(0,1)*random.randint(0,9) for i in range(how_many)]
    values = a_input
    true_result = [0 if x == 0 else 1 for x in a_input]
    a_input = [int(x) for a in a_input for x in base_in.format(a)]
    add = [0 for _ in range(input_size + 1)]
    add.extend(a_input)
    a_input = add
    
    sieve = Sieve_circuit(how_many, input_size)
    sieve.sieve()
    circuit = "sieve.json"
    
    b_input = [random.randint(0,2**(input_size-2)) for i in range(how_many)]
    b_input = [int(x) for b in b_input for x in base_in.format(b)]
    
    res = main(circuit, a_input, b_input)
    view('sieve', values, true_result, list(res.values()), verbose)

def test_adder1(how_many, input_size, verbose=True):
    base_out = '{:0' + str(math.ceil(math.log(how_many + 0.1,2))) + 'b}'
    base_in = '{:0' + str(input_size) + 'b}'
    
    a_input = [random.randint(0,9) for i in range(how_many)]
    
    a_input = [int(x) for a in a_input for x in base_in.format(a)]
    add = [0 for _ in range(input_size + 1)]
    add.extend(a_input)
    a_input = add
    
    
    b_input = [random.randint(0,2**(input_size) -1) for i in range(how_many)]
    b_input = [int(x) for b in b_input for x in base_in.format(b)]
    values = b_input[:how_many]
    true_result = [int(x) for i in base_out.format(sum([1 if i != 0 else 0 for i in values])) for x in i]
    
    adder = Adder1(how_many, input_size)
    adder.adder1()
    circuit = "adder1.json"
    
    res = main(circuit, a_input, b_input)
    view('adder1', values, true_result, list(res.values())[::-1], verbose)

def test_adder2(how_many, input_size, verbose=True):
    base_in = '{:0' + str(input_size) + 'b}'
    
    a_input = [random.randint(0,9) for i in range(how_many)]
    
    a_input = [int(x) for a in a_input for x in base_in.format(a)]
    add = [0 for _ in range(input_size + 1)]
    add.extend(a_input)
    a_input = add
    
    
    b_input = [random.randint(0,2**(input_size) -1) for i in range(how_many)]
    b_input = [int(x) for b in b_input for x in base_in.format(b)]
    box = b_input[:math.ceil(math.log(how_many + 0.1, 2))]
    values = int(''.join(str(e) for e in box),2)
    true_result = box
    
    
    adder = Adder2(how_many, input_size)
    adder.adder2()
    circuit = "adder2.json"
    
    res = main(circuit, a_input, b_input)
    view('adder2', values, true_result, list(res.values()), verbose)

def test_complete1(how_many, input_size, verbose=True):
    base_in = '{:0' + str(input_size) + 'b}'
    base_out = '{:0' + str(math.ceil(math.log(how_many + 0.1,2))) + 'b}'
    
    for _ in range(100):
        input = [random.randint(0,1) for _ in range(how_many)]
        values = input
        true_result = [int(x) for i in base_out.format(sum(copy.deepcopy(input))) for x in i]
        input = [int(x) for a in input for x in base_in.format(a)]
        input.insert(0,0)
        
        counter = Adder1_circuit(how_many, input_size)
        counter.counter()
        counter.adder()
        circuit = "adder2.json"
        
        res = main(circuit, input, [0])
        view('counter',values, true_result, list(res.values())[::-1], verbose)

def test_complete2(how_many, input_size, verbose=True):
    base_in = '{:0' + str(input_size) + 'b}'
    base_out = '{:0' + str(math.ceil(math.log(how_many,2))) + 'b}'
    
    a_input = [random.randint(2**(input_size-2),2**(input_size-1)) for i in range(how_many)]
    b_input = [a_input[i] - random.randint(0,1)*random.randint(0,2**(input_size-2)) for i in range(how_many)]
    values = str(a_input) + str(b_input)
    
    true_result = base_out.format(sum([0 if a_input[i]-b_input[i] == 0 else 1 for i in range(how_many)]))
    true_result = [int(x) for x in true_result]
    

    a_input = [int(x) for a in a_input for x in base_in.format(a)]
    add = [0 for _ in range(input_size + 1)]
    add.extend(a_input)
    a_input = add
    b_input = [int(x) for b in b_input for x in base_in.format(b)]
    counter = Complete_circuit(how_many, input_size)
    counter.subtractor(lonely=True)
    counter.filter()
    counter.adder1()
    circuit = "adder2.json"
    
    res = main(circuit, a_input, b_input)
    view('filter', values, true_result, list(res.values())[::-1], verbose)

def test_complete3(how_many, input_size, verbose=True):
    base_in = '{:0' + str(input_size) + 'b}'
    base_out = '{:0' + str(math.ceil(math.log(how_many+0.1,2))) + 'b}'
    print(base_out)
    r = random.randint(0,2**math.ceil(math.log(how_many,2)-1)-1)
    print(r)
    a_input = [random.randint(2**(input_size-2),2**(input_size-1)) for i in range(how_many)]
    b_input = [a_input[i] - random.randint(0,1)*random.randint(0,2**(input_size-2)) for i in range(how_many)]
    values = str(a_input) + str(b_input)
    
    true_result = base_out.format(sum([0 if a_input[i]-b_input[i] == 0 else 1 for i in range(how_many)])+r )
    true_result = [int(x) for x in true_result]
    

    a_input = [int(x) for a in a_input for x in base_in.format(a)]
    add = [int(x) for x in base_out.format(r)]
    add.extend(a_input)
    a_input = add
    a_input.insert(0,0)
    b_input = [int(x) for b in b_input for x in base_in.format(b)]
    
    counter = Complete_circuit(how_many, input_size)
    counter.subtractor()
    counter.sieve()
    counter.adder1()
    counter.adder2()
    circuit = "adder2.json"
    
    res = main(circuit, a_input, b_input)
    view('filter', values, true_result, list(res.values())[::-1], verbose)

def view(test, values, true_result, output, verbose):
    if verbose:
        print('TEST: ', test)
        print('Values:        ', values)
        print('True Result:   ', true_result)
        print('Circuit Output:', output)
    assert output == true_result
    print('Test ran successfully')
    print('\n')
