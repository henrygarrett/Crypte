import pickle
import random
from cryptography.fernet import Fernet


def encrypt(key, data):
    """Encrypt a message.

    Args:
        key: The encryption key.
        data: The message to encrypt.

    Returns:
        The encrypted message as a byte stream.
    """
    f = Fernet(key)
    return f.encrypt(data)


def decrypt(key, data):
    """Decrypt a message.

    Args:
        key: The decryption key.
        data: The message to decrypt.

    Returns:
        The decrypted message as a byte stream.
    """
    f = Fernet(key)
    return f.decrypt(data)


def evaluate(circuit, g_tables, pbits_out, a_inputs, b_inputs):
    """Evaluate yao circuit with given inputs.

    Args:
        circuit: A dict containing circuit spec.
        g_tables: The yao circuit garbled tables.
        pbits_out: The pbits of outputs.
        a_inputs: A dict mapping Alice's wires to (key, encr_bit) inputs.
        b_inputs: A dict mapping Bob's wires to (key, encr_bit) inputs.

    Returns:
        A dict mapping output wires with their result bit.
    """
    gates = circuit["gates"]  # dict containing circuit gates
    wire_outputs = circuit["out"]  # list of output wires
    wire_inputs = {}  # dict containing Alice and Bob inputs
    evaluation = {}  # dict containing result of evaluation

    wire_inputs.update(a_inputs)
    wire_inputs.update(b_inputs)

    # Iterate over all gates
    for gate in sorted(gates, key=lambda g: g["id"]):
        gate_id, gate_in, msg = gate["id"], gate["in"], None
        # Special case if it's a NOT gate
        if (len(gate_in) < 2) and (gate_in[0] in wire_inputs):
            # Fetch input key associated with the gate's input wire
            key_in, encr_bit_in = wire_inputs[gate_in[0]]
            # Fetch the encrypted message in the gate's garbled table
            encr_msg = g_tables[gate_id][(encr_bit_in, )]
            # Decrypt message
            msg = decrypt(key_in, encr_msg)
        # Else the gate has two input wires (same model)
        elif (gate_in[0] in wire_inputs) and (gate_in[1] in wire_inputs):
            key_a, encr_bit_a = wire_inputs[gate_in[0]]
            key_b, encr_bit_b = wire_inputs[gate_in[1]]
            encr_msg = g_tables[gate_id][(encr_bit_a, encr_bit_b)]
            msg = decrypt(key_b, decrypt(key_a, encr_msg))
        if msg:
            wire_inputs[gate_id] = pickle.loads(msg)

    # After all gates have been evaluated, we populate the dict of results
    for out in wire_outputs:
        evaluation[out] = wire_inputs[out][1] ^ pbits_out[out]

    return evaluation
