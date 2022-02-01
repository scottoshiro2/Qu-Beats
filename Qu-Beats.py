#!/usr/bin/env python
# coding: utf-8
from typing import List, Callable

import numpy as np

from mido import Message, MidiFile, MidiTrack

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute

from qiskit.tools.visualization import plot_histogram


#~~~~~~~ Circuit Transformations ~~~~~~~#

def add_bell_state(qc: QuantumCircuit) -> None:
    """This transformation modifies the input circuit by preparing a Bell State."""
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])


def add_teleportation(qc: QuantumCircuit) -> None:
    """This transformation modifies the input circuit by implementing the teleportation
    protocol.
    """
    qc.z(0)
    qc.h(0)
    qc.h(1)
    qc.cx(1, 2)
    qc.cx(0,1)
    
    qc.measure(1, 1)
    qc.cx(1,2)
    qc.h(0)
    qc.measure(0, 0)
    qc.cz(0,2)
    
    qc.h(2)
    qc.z(2)
    qc.measure([0, 1, 2], [0, 1, 2])


def add_grover(qc: QuantumCircuit) -> None:
    """This transformation modifies the input circuit by implementing Grover's algorithm."""
    qc.h(0)
    qc.h(1)

    qc.x(0)
    qc.x(1)
    
    qc.cz(0, 1)
    qc.x(0)
    qc.x(1)
    
    qc.h(0)
    qc.h(1)
    
    qc.cz(0, 1)
    qc.h(0)
    qc.h(1)
    qc.measure([0, 1], [0, 1])


def bertstein_vazirani(qc: QuantumCircuit) -> None:
    """This transformation modifies the input circuit by implementing Bertstein-Vazirani."""
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.h(3)
    qc.z(0)
    qc.z(1)
    qc.z(2)
    qc.z(3)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.h(3)
    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])

#~~~~~~~ Input arrays, representing beats over time ~~~~~~~#

beat1 = [0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
beat2 = [1, 1, 0, 1, 1, 0, 1, 1, 1, 1]
beat3 = [0, 0, 0, 1, 1, 1, 1, 0, 0, 1]
beat4 = [1, 0, 0, 0, 1, 1, 0, 0, 0, 1]


#~~~~~~~ Conversion to MIDI ~~~~~~~#

def save_to_midi(beat_array: List[int],
                 filename: str,
                 note: int = 32,
                 time: int = 100) -> None:
    """Save the input to a new midi file."""
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    for bt in beat_array:
        message = 'note_{}'.format('on' if bt == 1 else 'off')
        track.append(Message(message, note=note, time=time))

    mid.save(filename)

save_to_midi(beat1, '/Users/lauren@ibm.com/Documents/pBeat1.mid')
save_to_midi(beat2, '/Users/lauren@ibm.com/Documents/pBeat2.mid')
save_to_midi(beat3, '/Users/lauren@ibm.com/Documents/pBeat3.mid')
save_to_midi(beat4, '/Users/lauren@ibm.com/Documents/pBeat4.mid')


#~~~~~~~ Build QuantumCircuits ~~~~~~~#

def build_circuits(transformation: Callable,
                   beat1: List[int], *beats: List[List[int]]) -> List[QuantumCircuit]:
    circuits = []
    for i in range(len(beats[0])):
        qr = QuantumRegister(4)
        cr = ClassicalRegister(4)
        qc = QuantumCircuit(qr, cr)
        for j, beat in enumerate(beats):
            if beat[i] == 1:
                qc.x(j)

        qc.barrier()
        # Add transformation (and measurement)
        transformation(qc)

        circuits.append(qc)

    return circuits


#~~~~~~~ BELL STATE ~~~~~~~#

circuits = build_circuits(add_bell_state, beat1, beat2)
circuits[0].draw(output='mpl')

## Executing code

simulator = Aer.get_backend('qasm_simulator')
result = execute(circuits, backend=simulator, shots=1).result()

cir_array = []
for c in circuits:
    cir_array.append([k for k in result.get_counts(c).keys()][0])

new_track1 = []
new_track2 = []
for b in cir_array:
    new_track1.append(int(b[0]))
    new_track2.append(int(b[1]))

## New Midi Rhythms
save_to_midi(new_track1, '/Users/lauren@ibm.com/Documents/Bell_Circ.mid')
save_to_midi(new_track2, '/Users/lauren@ibm.com/Documents/Bell_Circ2.mid')


#~~~~~~~ TELEPORTATION ~~~~~~~#

circuits = build_circuits(add_teleportation, beat1, beat2, beat3)
circuits[0].draw(output='mpl')

# Executing code

simulator = Aer.get_backend('qasm_simulator')
result = execute(circuits, backend = simulator, shots=1).result()

cir_array = []
for c in circuits:
    cir_array.append([k for k in result.get_counts(c).keys()][0])

new_track1 = []
new_track2 = []
new_track3 = []
for b in cir_array:
    new_track1.append(int(b[0]))
    new_track2.append(int(b[1]))
    new_track3.append(int(b[2]))

#~~~~~~~ BERNSTEIN VAZIRANI ~~~~~~~#

circuits = build_circuits(bertstein_vazirani, beat1, beat2, beat2, beat2)
circuits[0].draw(output='mpl')

## Executing code
simulator = Aer.get_backend('qasm_simulator')
result = execute(circuits, backend = simulator, shots=1024).result()
plot_histogram(result.get_counts(circuits[4]))

cir_array = []
for c in circuits:
    cir_array.append([k for k in result.get_counts(c).keys()][0])

new_track1 = []
new_track2 = []
new_track3 = []
for b in cir_array:
    new_track1.append(int(b[0]))
    new_track2.append(int(b[1]))
    new_track3.append(int(b[2]))

save_to_midi(new_track1, '/Users/lauren@ibm.com/Documents/new_teleport1.mid')
save_to_midi(new_track2, '/Users/lauren@ibm.com/Documents/new_teleport2.mid')
save_to_midi(new_track3, '/Users/lauren@ibm.com/Documents/new_teleport3.mid')
