import pypianoroll
# import torch
# from torch import nn
import numpy as np
import librosa
import pretty_midi
from pretty_midi import PrettyMIDI
import argparse
import os
import mido
import matplotlib.pyplot as plt
import warnings
from datetime import timedelta
from ec2vae.ec2vae_model import EC2VAE
from bidict import bidict

folder_path = '/home/gariscat/DURF2022/Chinese Traditional Songs Midi/'
parser = argparse.ArgumentParser(description='Single Track MIR Processing Args')
parser.add_argument('--track_name', default="Sai_Ma",
                    help='Name of the MIDI file (default: Sai_Ma)')
args = parser.parse_args()
track_path = os.path.join(folder_path, args.track_name+'.mid')
"""
TODO: Need to determine "chords"
"""
"""
vae = EC2VAE.init_model()
vae.load_model('./ec2vae/ec2vae-v1.pt')
"""
program_id2instrument_name = {}
name2id = {}
with open('Midi ProgramId2InstrumentName Mapping', 'r') as f:
    lines = f.readlines()
    for line in lines:
        a, b = line.split('\t')
        id = int(a.strip().strip('. ')) - 1
        name = b.strip('\n')
        program_id2instrument_name[id] = name


def process_one_clip(st, ed, midi):
    for channel in midi.tracks:
        channel_name = channel.name
        program_id = channel.program
        piano_roll = channel.pianoroll[st:ed]
        note_indices = np.argmax(piano_roll, axis=1)
    # Unfinished...

    return 0


def process_one_track(midi_path, wave_path=None):
    '''
    midi = PrettyMIDI(midi_path, wave_path)
    instruments = midi.instruments
    time_signature = midi.time_signature_changes[0]
    print(time_signature)
    for ins in instruments:
        print(ins)
    '''
    midi = pypianoroll.read(midi_path)
    time_sign = PrettyMIDI(midi_path).time_signature_changes[0]
    tempo = midi.tempo[0][0]  # we assume the track has a consistent tempo
    total_num_of_steps = midi.downbeat.shape[0]
    num_of_quarter_notes = total_num_of_steps // midi.resolution
    num_of_minutes = num_of_quarter_notes / tempo
    time_length = timedelta(minutes=num_of_minutes)
    num_of_steps_per_bar = 4 * midi.resolution
    if time_sign.numerator != 4 or time_sign.denominator != 4:
        warnings.warn(f"Warning! The time signature of this song is not 4/4.")
        # print(f"It is {time_sign.numerator}/{time_sign.denominator} instead!")

    for channel in midi.tracks:
        channel.plot()
        plt.title(channel.name)
        plt.show()
        plt.close()
        piano_roll = channel.pianoroll
        melody_line = np.argmax(piano_roll, axis=1)
        # print(melody_line)
    ''''''
    retrieved_information = []
    for st in range(0, total_num_of_steps, num_of_steps_per_bar):
        ed = st + num_of_steps_per_bar
        retrieved_information += [process_one_clip(st, ed, midi)]

    # print(midi)


process_one_track(track_path)