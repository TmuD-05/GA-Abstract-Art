from music21 import converter, tempo, chord, note, instrument
from collections import defaultdict
import statistics

"""
Extract 4D emotion features from MIDI with robustness improvements.

Features:
- energy: Arousal from tempo (0–1)
- valence: Positivity from mode + key brightness (0–1)
- complexity: Busyness from note event density (0–1)
- brightness: Attack/sharpness from normalized velocity (0–1)

Args:
    file_path: Path to MIDI file
    use_average_tempo: Use median tempo instead of first (handles accelerandos)

Returns:
    Dictionary with emotion features and confidence scores
"""
def extract_emotion_features(file_path, use_average_tempo=True):
    try:
        score = converter.parse(file_path)
    except Exception as e:
        raise ValueError(f"Failed to parse MIDI: {e}")

    all_tempos = score.flatten().getElementsByClass(tempo.MetronomeMark)

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
    energy = (bpm - 40) / (220 - 40)
    energy = max(0.0, min(energy, 1.0))

    try:
        key_obj = score.analyze('key')
        if hasattr(key_obj, 'correlationCoefficient'):
            confidence = key_obj.correlationCoefficient
        else:
           confidence =  0.5
    except:

        key_obj = None
        confidence = 0.0

    if key_obj and confidence > 0.3:

        if key_obj.mode == 'major':
            valence = 1.0
            valence_confidence = confidence
        else:
            valence = 0.0
            valence_confidence = 0.0
    else:

        valence = 0.5
        valence_confidence = 0.0

    all_notes = score.flatten().notes
    total_duration_ql = score.highestTime

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

    velocities_by_instrument = defaultdict(list)

    for n in all_notes:
        try:
            instr = n.getContextByClass(instrument.Instrument)
            if instr:
                instr_name = instr.instrumentName
            else:
                instr_name = 'unknown'
        except:
            instr_name = 'unknown'

        if n.volume.velocity is not None:
            vel = n.volume.velocity
        else:
           vel = 64
        velocities_by_instrument[instr_name].append(vel)


    normalized_velocities = []
    for instr_name, vels in velocities_by_instrument.items():
        if not vels:
            continue

        v_min, v_max = min(vels), max(vels)
        v_range = max(v_max - v_min, 1)

        for v in vels:
            normalized = (v - v_min) / v_range
            normalized_velocities.append(normalized)

    """
    brightness = (
        sum(normalized_velocities) / len(normalized_velocities)
        if normalized_velocities
        else 0.5
    )
    """


    features = {
        'energy': round(energy, 3),
        'valence': round(valence, 3),
        'density': round(density, 3),
        #'brightness': round(brightness, 3),

        # Metadata for debugging
        'metadata': {
            'bpm': round(bpm, 1),
            'mode': key_obj.mode if key_obj else 'unknown',
            'key_confidence': round(valence_confidence, 2),
            'total_notes': len(all_notes),
            'unique_onsets': unique_onsets,
            'duration_seconds': round(duration_seconds, 1),
            'instruments': list(velocities_by_instrument.keys())
        }
    }

    return features
