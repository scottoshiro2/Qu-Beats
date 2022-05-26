import numpy as np
from music21 import *
from midi_parser import *

def beat_construction( org_dbl, org_lps, counts ):
    #Let's parse it out:
    beat_matrix = list(counts.keys())
    print('Beat Matrix')
    beat_matrix #x axis is the bar and beat ID, while the y-axis is the subdivision in 8 th notes

    Beats = []
    for sdv in beat_matrix:
        beats_1 = []
        beats_2 = []
        sdv = sdv.split()
        sdv = np.flip( sdv ).tolist()
        for i, j in enumerate( sdv ):
            if i%2 == 0:
                beats_1.append( j )
            else:
                beats_2.append( j )
        Beats.append( [beats_1, beats_2] ) # x-axis -> Bar, y-axis -> subdiv

    beat_pattern1 = []
    beat_pattern2 = []

    setdbl, num_dbl = midi_vals( org_dbl )
    setlps, num_lps = midi_vals( org_lps )

    setdbl_notes = zero_fill( setdbl, len(setdbl) )
    setlps_notes = zero_fill( setlps, len(setlps) )

    index = 0
    New_Beats = {}
    for b1,b2 in Beats:
        index += 1
        decoded_data = {}
        for bar,val in enumerate( b1 ):
            tr1 = int( b1[bar][0] )
            tr2 = int( b2[bar][0] )

            b1_note = setdbl_notes[int(b1[bar][1:],2)] # Note this is the index on the unique midi value record
            b2_note = setlps_notes[int(b2[bar][1:],2)]

            decoded_data['Bar {}'.format(bar)] = [[b1_note, tr1], [b2_note, tr2]] 
        New_Beats['subdiv {}'.format(index)] = decoded_data

    return New_Beats

def gen_midi( new_beat, bid_1 ):
    new_beat1 = stream.Stream()
    new_beat1.append(tempo.MetronomeMark(number=144))

    new_beat2 = stream.Stream()
    new_beat2.append(tempo.MetronomeMark(number=144))

    for entry in new_beat:
        for i, bar in enumerate( new_beat[entry] ):
            #print('check: ', bn[entry][bar])
            for mx, mval in enumerate( new_beat[entry][bar] ):
                drum = note.Note( pitch.Pitch(midi=mval[0]) )

                if mval[1] == 0:
                    drum.quarterLength = 0.5
                else:
                    drum.quarterLength = 0.25

                if mx == 0:
                    new_beat1.append( drum )
                else:
                    new_beat2.append( drum )

    B1 = midi.translate.streamToMidiFile(new_beat1)
    B2 = midi.translate.streamToMidiFile(new_beat2)

    B1.open('new_beat{}.mid'.format(bid_1), 'wb')
    B1.write()
    B1.close()

    B2.open('new_beat{}_2.mid'.format(bid_1), 'wb')
    B2.write()
    B2.close()


