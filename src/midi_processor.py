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

from music21 import converter, tempo, chord, note, instrument
from collections import defaultdict
import statistics


def extract_emotion_features(file_path, use_average_tempo=True):
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
    try:
        score = converter.parse(file_path)
    except Exception as e:
        raise ValueError(f"Failed to parse MIDI: {e}")

    # ===== 1. TEMPO (Energy) =====
    all_tempos = score.flatten().getElementsByClass(tempo.MetronomeMark)

    if all_tempos:
        bpm_values = [t.number for t in all_tempos]
        if use_average_tempo:
            bpm = statistics.median(bpm_values)  # More robust than mean
        else:
            bpm = bpm_values[0]
    else:
        bpm = 120.0

    # Normalize with realistic BPM range (40–220)
    energy = (bpm - 40) / (220 - 40)
    energy = max(0.0, min(energy, 1.0))  # Clamp to [0, 1]

    # ===== 2. MODE + HARMONIC BRIGHTNESS (Valence) =====
    try:
        key_obj = score.analyze('key')
        confidence = key_obj.correlationCoefficient if hasattr(key_obj, 'correlationCoefficient') else 0.5
    except:
        # Fallback if key analysis fails
        key_obj = None
        confidence = 0.0

    if key_obj and confidence > 0.3:
        # Base valence from mode
        mode_val = 1.0 if key_obj.mode == 'major' else 0.0

        # Harmonic brightness: sharps = brighter, flats = darker
        # C=0, G=1 (sharp), F=-1 (flat), etc.
        key_shift = (key_obj.tonic.pitchClass % 12)
        # Map to [-1, 1] where sharps are positive
        harmonic_brightness = ((key_shift - 6) % 12 - 6) / 6  # Range -1 to 1

        # Blend mode (binary) with harmonic brightness (continuous)
        valence = mode_val * 0.8 + (harmonic_brightness + 1) / 2 * 0.2
        valence = max(0.0, min(valence, 1.0))
        valence_confidence = confidence
    else:
        # Neutral valence if key can't be determined
        valence = 0.5
        valence_confidence = 0.0

    # ===== 3. NOTE DENSITY (Complexity) =====
    all_notes = score.flatten().notes
    total_duration_ql = score.highestTime

    if total_duration_ql > 0:
        duration_seconds = (total_duration_ql / (bpm / 60)) if bpm > 0 else 1.0
    else:
        duration_seconds = 1.0

    # Count unique note onset times (not total notes)
    # This prevents chords from inflating density
    unique_onsets = len(set(n.offset for n in all_notes))

    # Complexity: notes per second (normalized to 0–1 with 15 notes/sec as max)
    note_density = unique_onsets / duration_seconds if duration_seconds > 0 else 0
    complexity = (note_density / 15.0)  # 15 notes/sec = max complexity
    complexity = max(0.0, min(complexity, 1.0))

    # ===== 4. NORMALIZED VELOCITY (Brightness) =====
    # Group velocities by instrument to normalize fairly
    velocities_by_instrument = defaultdict(list)

    for n in all_notes:
        try:
            instr = n.getContextByClass(instrument.Instrument)
            instr_name = instr.instrumentName if instr else 'unknown'
        except:
            instr_name = 'unknown'

        vel = n.volume.velocity if n.volume.velocity is not None else 64
        velocities_by_instrument[instr_name].append(vel)

    # Normalize each instrument independently, then average
    normalized_velocities = []
    for instr_name, vels in velocities_by_instrument.items():
        if not vels:
            continue

        v_min, v_max = min(vels), max(vels)
        v_range = max(v_max - v_min, 1)  # Avoid division by zero

        for v in vels:
            normalized = (v - v_min) / v_range
            normalized_velocities.append(normalized)

    brightness = (
        sum(normalized_velocities) / len(normalized_velocities)
        if normalized_velocities
        else 0.5
    )

    # ===== RETURN FEATURES =====
    features = {
        'energy': round(energy, 3),
        'valence': round(valence, 3),
        'complexity': round(complexity, 3),
        'brightness': round(brightness, 3),

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


# ===== EXAMPLE USAGE & TESTING =====
if __name__ == '__main__':
    # Test with a sample file
    test_files = [
        'sad_ballad.mid',
        'upbeat_dance.mid',
        'ambient.mid'
    ]

    for file_path in test_files:
        try:
            result = extract_emotion_features(file_path)
            print(f"\n{file_path}")
            print(f"  Energy: {result['energy']} (BPM: {result['metadata']['bpm']})")
            print(
                f"  Valence: {result['valence']} (Mode: {result['metadata']['mode']}, Confidence: {result['metadata']['key_confidence']})")
            print(
                f"  Complexity: {result['complexity']} ({result['metadata']['unique_onsets']} onsets in {result['metadata']['duration_seconds']}s)")
            print(f"  Brightness: {result['brightness']}")
        except FileNotFoundError:
            print(f"\n{file_path} - not found (skipped)")