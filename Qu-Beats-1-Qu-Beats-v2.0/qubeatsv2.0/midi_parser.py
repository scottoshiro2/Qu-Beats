#!/usr/bin/env python
# coding: utf-8

from mido import MidiFile
import numpy as np

def get_messages( midi_tracks ):
    for i, track in enumerate(midi_tracks):
        count = 0
        event_list = []; meta_data = []
        #print('Track {}: {}'.format(i, track.name))
        for msg in track:
            if msg.is_meta:
                meta_data.append( msg )
            else:
                count += 1
                event_list.append(msg)
                #print('MIDI_data: ',msg)
    event_list = event_list[3:]
    return event_list, meta_data

#how many notes are being used in an event list
def midi_vals( events ):
    midi_vals = []
    for j, message in enumerate( events ):
        #print(message['note_set'])
        midi_vals.append( events[message]['note_set'] )
    midi_vals = [item for sublist in midi_vals for item in sublist]
    midi_vals = np.unique(midi_vals).tolist()
    return midi_vals, len(midi_vals)

def note_grouping( events: list ) -> dict:
    nxt_evnt = 0
    event_size = len(events)
    # I need to make an event list polyphon list
    note_set = []
    polyphon = {}; poly_data = {}
    start = 0; count = 0
    # includes the exact time on the track instead of the interval time the message was sent
    for i, message in enumerate( events ):
        if i < event_size - 1:
            nxt_evnt = events[ i+1 ]
            # print( message, next_evnt )
            # Looking for if a zero occurs which means on the same subdivision as the prev msg
            if nxt_evnt.time == 0:
                if start == 0:
                    start = 1
                    start_time = message.time
                    note_set.append(message.note)
                    note_set.append(nxt_evnt.note)

                else:
                    #print(i)
                    #print(message.note, nxt_evnt.note, next_evnt.time, 'not 0', i)
                    note_set.append(nxt_evnt.note)
            else:
                end_time = nxt_evnt.time
                poly_data['note_set'] = ( np.unique(note_set).tolist() ) # This needs to be at the end of the looping of it
                poly_data['next_hit'] = end_time
                polyphon[count] = poly_data
                poly_data = {}
                
                count += 1
                if len( note_set ) == 1:
                    note_set = []
                    #note_set.append(nxt_evnt.note)
                else:
                    note_set = []
                    note_set.append(nxt_evnt.note)
                start = 0

    return polyphon #Have this be the automation for for parsing out the state vector for each bar in the loop

#ok parse out into bars from this data

def bar_length( meta_data ):
    # parameters: meta_data, 
    #solve for tempo: 
    # num of bars should be an input parameter for now
    num_bars = 5
    for i, m in enumerate( meta_data ):
        try:
            tempo = meta_data[i].tempo
        except:
            pass
        
        try:
            ts_num = meta_data[i].numerator
            ts_dem = meta_data[i].denominator
            time_signature = 4 * (ts_num / ts_dem)
        except:
            pass
    BPM = round( 60 / (tempo * 10e-7), 3) #convert from microseconds to seconds
    beat_len = round( 60000 / BPM, 3 ) # length of beat in ms
    bar_len = round( time_signature * beat_len ) #length in milliseconds
    loop_len = num_bars * bar_len

    # find the time signature, need to come up more accurate classifications but this is good
    return bar_len

def zero_fill( ls: list, size: int ) -> list:
    ls.insert( 0,0 )
    if (len( ls ) < size):
        num_o_zeros = size - len( ls )
        for i in range(num_o_zeros):
            ls.append( 0 )
        return ls
    else:
        return ls
    
def state_vectors( data: dict, bar_len: int ) -> list:
    total_time = 0
    bar_lines = [];  bars =[]
    for i in data:
        total_time += data[i]['next_hit']

        if total_time < bar_len:
            bar_lines.append( data[i]['note_set'] )
            #print( i, org[i], 'total_time', total_time ) 
        else:
            total_time = 0
            bar_line = [ns for nst in bar_lines for ns in nst]

            bars.append( bar_line )
            bar_lines = []
            #print( i, org[i], 'total_time', total_time, bars )

    drum_sv = {}; sv_bar = []; state_vector = []      
    for b in bars:
        b_keys = np.unique( b ) # these are the keys
        for key in b_keys:
            drum_sv[key] = 0
            for note in b:
                if note == key:
                    drum_sv[key] += 1

        note_occur_tot = sum( drum_sv.values() )
        for nkey in drum_sv.keys():
            sqr_prob = np.sqrt(drum_sv[nkey] / note_occur_tot)
            sv_bar.append( sqr_prob )
        
        #for i,j in enumerate( sv_bar ):
        #    sv_bar[i] = j / sum( sv_bar )
            
        # make the state vectors for the circuit
        state_vector.append( zero_fill(sv_bar, 8) )
        sv_bar = []

    return state_vector
