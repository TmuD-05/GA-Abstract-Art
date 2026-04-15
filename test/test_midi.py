from src.midi_processor import extract_emotion_features

midi_file = "/Users/tafadzwa/Genetic Algorithm For Abstract Art/test/pharrell_williams-happy.mid"

features = extract_emotion_features(midi_file)
print(features)