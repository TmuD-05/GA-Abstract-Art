"""
midi_processor.py

This module is responsible for reading and parsing MIDI files.
It extracts raw musical information such as tempo, note events,
velocity, and timing using the music21 library.

The output of this module is unprocessed musical data, which is
then passed to the feature extraction module for normalization
and emotion mapping.

This serves as the input stage of the system.
"""