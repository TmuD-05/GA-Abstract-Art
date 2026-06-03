from music21 import converter, tempo
import statistics

"""
midi_processor.py

Parses a MIDI file and extracts three musical features:
- Energy:  derived from tempo (BPM)
- Valence: derived from average pitch
- Density: derived from how many notes are played over time

All three features are normalized to a 0-1 range.
"""

def extract_emotion_features(file_path, use_average_tempo=True):
    try:
        score = converter.parse(file_path)
    except Exception as e:
        raise ValueError(f"Failed to parse MIDI: {e}")

    all_tempos = score.flatten().getElementsByClass(tempo.MetronomeMark)
    all_notes = score.flatten().notes
    total_duration_ql = score.highestTime

    bpm = get_bpm(all_tempos,use_average_tempo)

    valence = get_valence(all_notes)

    density = get_density(all_notes,total_duration_ql,bpm)

    energy = (bpm - 40) / (220 - 40)
    energy = max(0.0, min(energy, 1.0))

    features = {
        'energy': round(energy, 3),
        'valence': round(valence, 3),
        'density': round(density, 3),
        # Metadata for debugging
        'metadata': {
            'bpm': round(bpm, 1),
            'total_notes': len(all_notes),
        }
    }
    return features

def get_valence(all_notes):
    if not all_notes:
        valence = 0.5

    pitches = []
    for n in all_notes:
        if hasattr(n, 'pitch'):
            pitch_value = n.pitch.ps
            pitches.append(pitch_value)


    avg_pitch = sum(pitches) / len(pitches)

    valence = (avg_pitch - 40) / (80 - 40)

    valence = max(0.0, min(valence, 1.0))

    return valence

def get_density(all_notes,total_duration_ql,bpm):

    if total_duration_ql > 0:
         if bpm > 0 :
             duration_seconds = (total_duration_ql / (bpm / 60))
         else:
            duration_seconds =  1.0
    else:
        duration_seconds = 1.0

    unique_onsets = len(set(n.offset for n in all_notes))

    if duration_seconds > 0:
        note_density = unique_onsets / duration_seconds
    else:
        note_density = 0

    density = (note_density / 15.0)
    density = max(0.0, min(density, 1.0))
    return density

def get_bpm(all_tempos,use_average_tempo=True):

    if all_tempos:
        bpm_values = []
        for t in all_tempos:
            bpm_values.append(t.number)
        if use_average_tempo:
            bpm = statistics.median(bpm_values)
        else:
            bpm = bpm_values[0]
    else:
        bpm = 120.0
    return bpm