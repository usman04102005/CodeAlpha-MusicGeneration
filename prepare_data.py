import os
import numpy as np
import pickle
from music21 import converter, instrument, note, chord, stream
import glob

def is_midi_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            return f.read(4) == b'MThd'
    except Exception:
        return False


def prepare_training_data(midi_folder='midi_data', output_file='notes_data'):
    """
    Extract notes from MIDI files and prepare for training
    Expects midi_folder to contain .mid or .midi files
    """
    notes = []
    durations = []
    
    # Find all MIDI files recursively in midi_folder
    midi_files = glob.glob(os.path.join(midi_folder, '**', '*.mid'), recursive=True) + \
                 glob.glob(os.path.join(midi_folder, '**', '*.midi'), recursive=True)
    
    if not midi_files:
        print(f"⚠️ No MIDI files found in {midi_folder} or its subfolders")
        print("📝 Instructions to get MIDI files:")
        print("   1. Visit: https://www.kaggle.com/datasets/ngyewching/classical-music-dataset")
        print("   2. Or: https://www.classicforkids.com/download.html")
        print("   3. Place .mid files in 'midi_data/' or its subfolders")
        return False
    
    print(f"Found {len(midi_files)} MIDI files")
    
    for i, midi_file in enumerate(midi_files):
        print(f"Processing {i+1}/{len(midi_files)}: {os.path.basename(midi_file)}")
        
        if not is_midi_file(midi_file):
            print(f"   ⚠️ Skipping invalid MIDI file: {os.path.basename(midi_file)}")
            continue
        
        try:
            # Parse MIDI file
            score = converter.parse(midi_file)
            
            # Extract notes and chords
            parts = score.parts if hasattr(score, 'parts') else [score]
            
            for part in parts:
                for element in part.flatten().notesAndRests:
                    if isinstance(element, note.Note):
                        # Single note
                        notes.append(str(element.pitch))
                        durations.append(element.duration.quarterLength)
                    elif isinstance(element, chord.Chord):
                        # Chord (multiple notes)
                        notes.append('.'.join(str(n) for n in element.pitches))
                        durations.append(element.duration.quarterLength)
                    elif isinstance(element, note.Rest):
                        # Rest
                        notes.append('rest')
                        durations.append(element.duration.quarterLength)
        
        except Exception as e:
            print(f"   ❌ Error processing file: {str(e)}")
            continue
    
    if not notes:
        print("❌ No notes extracted from MIDI files")
        return False
    
    print(f"\n✅ Extracted {len(notes)} notes from {len(midi_files)} files")
    
    # Save notes and durations
    with open(f'{output_file}_notes.pkl', 'wb') as f:
        pickle.dump(notes, f)
    
    with open(f'{output_file}_durations.pkl', 'wb') as f:
        pickle.dump(durations, f)
    
    print(f"✅ Data saved to {output_file}_notes.pkl and {output_file}_durations.pkl")
    return True

if __name__ == '__main__':
    prepare_training_data()