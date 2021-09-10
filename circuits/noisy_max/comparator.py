import json
from circuits.noisy_max.circuit import Circuit


class Comparator(Circuit):
    def __init__(self, number_of_elements, input_size, top_k):
        super().__init__(number_of_elements, input_size, top_k)

    def comparator(self, alice, bob):
        output = []
        for i in range(self.input_size % 4):
        self.adder2_inputs = output
        self.circuit['out'] = output
        with open('adder1.json', 'w') as file:
            json.dump(self.dictionary, file)

    def four_bit_comparator(self, alice, bob):
        start = self.circuit['gates'][-1]['id']
        # First bit block
        self.circuit['gates'].append({"id": start + 1, "type": "XNOR", "in": [bob[0], alice[0]]})
        self.circuit['gates'].append({"id": start + 2, "type": "NOTAND", "in": [bob[0], alice[0]]})

        # Second bit block
        self.circuit['gates'].append({"id": start + 3, "type": "XNOR", "in": [bob[1], alice[1]]})
        self.circuit['gates'].append({"id": start + 4, "type": "NOTAND", "in": [bob[1], alice[1]]})
        self.circuit['gates'].append({"id": start + 5, "type": "AND", "in": [start + 4, start + 1]})

        # Third bit block
        self.circuit['gates'].append({"id": start + 6, "type": "XNOR", "in": [bob[2], alice[2]]})
        self.circuit['gates'].append({"id": start + 7, "type": "NOTAND", "in": [bob[2], alice[2]]})
        self.circuit['gates'].append({"id": start + 8, "type": "AND", "in": [start + 7, start + 1]})
        self.circuit['gates'].append({"id": start + 9, "type": "AND", "in": [start + 8, start + 3]})

        # Fourth bit block
        self.circuit['gates'].append({"id": start + 10, "type": "XNOR", "in": [bob[3], alice[3]]})
        self.circuit['gates'].append({"id": start + 11, "type": "NOTAND", "in": [bob[3], alice[3]]})
        self.circuit['gates'].append({"id": start + 12, "type": "AND", "in": [start + 11, start + 1]})
        self.circuit['gates'].append({"id": start + 13, "type": "AND", "in": [start + 12, start + 3]})
        self.circuit['gates'].append({"id": start + 14, "type": "AND", "in": [start + 13, start + 6]})

        # OR gate for Alice > Bob output gate
        self.circuit['gates'].append({"id": start + 15, "type": "OR", "in": [start + 2, start + 5]})
        self.circuit['gates'].append({"id": start + 16, "type": "OR", "in": [start + 15, start + 9]})
        self.circuit['gates'].append({"id": start + 17, "type": "OR", "in": [start + 16, start + 14]})

        # AND gate for Alice = Bob output gate
        self.circuit['gates'].append({"id": start + 18, "type": "AND", "in": [start + 1, start + 3]})
        self.circuit['gates'].append({"id": start + 19, "type": "AND", "in": [start + 18, start + 6]})
        self.circuit['gates'].append({"id": start + 20, "type": "AND", "in": [start + 19, start + 10]})

        # NOR gate for Alice < Bob output gate
        self.circuit['gates'].append({"id": start + 21, "type": "NOR", "in": [start + 17, start + 20]})

        self.carry = [start + 17, start + 20, start + 21]
        return self.carry


c = Comparator(5, 32, 2)
c.four_bit_comparator([1, 2, 3, 4], [5, 6, 7, 8])
