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


from music21 import converter, tempo, chord, note


def extract_emotion_features(file_path):
    score = converter.parse(file_path)

    all_tempos = score.flatten().getElementsByClass(tempo.MetronomeMark)
    bpm = all_tempos[0].number if all_tempos else 120.0

    key_obj = score.analyze('key')
    mode_val = 1.0 if key_obj.mode == 'major' else 0.0

    all_notes = score.flatten().notes
    total_notes = len(all_notes)

    total_duration_ql = score.highestTime
    duration_seconds = (total_duration_ql / (bpm / 60))
    note_density = total_notes / duration_seconds if duration_seconds > 0 else 0

    velocities = [n.volume.velocity for n in all_notes if n.volume.velocity is not None]
    mean_velocity = sum(velocities) / len(velocities) if velocities else 64

    features = {
        'energy': min(bpm / 200.0, 1.0),
        'valence': mode_val,
        'complexity': min(note_density / 10.0, 1.0),
        'brightness': mean_velocity / 127.0
    }

    return features
