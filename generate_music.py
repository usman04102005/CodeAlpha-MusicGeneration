import numpy as np
import pickle
from keras.models import load_model
from music21 import note, chord, stream, instrument, tempo
import random

class MusicSequenceGenerator:
    def __init__(self, model_path='music_generator_model.h5', 
                 mapping_path='note_mapping.pkl'):
        """Load pre-trained model"""
        self.model = load_model(model_path)
        
        with open(mapping_path, 'rb') as f:
            mapping = pickle.load(f)
            self.note_to_idx = mapping['note_to_idx']
            self.idx_to_note = mapping['idx_to_note']
            self.sequence_length = mapping['sequence_length']
        
        print(f"✅ Model loaded with {len(self.idx_to_note)} unique notes")
    
    def generate(self, seed_sequence, length=100, temperature=0.8):
        """
        Generate new music sequence
        
        Args:
            seed_sequence: Initial sequence of notes
            length: Number of notes to generate
            temperature: Randomness (0=deterministic, 1=random)
        """
        # Convert seed to integers and pad if seed is shorter than sequence_length
        current_sequence = [self.note_to_idx.get(note, 0) for note in seed_sequence]
        if len(current_sequence) < self.sequence_length:
            pad_len = self.sequence_length - len(current_sequence)
            current_sequence = [0] * pad_len + current_sequence
        
        generated_notes = seed_sequence.copy()
        
        print(f"\n🎵 Generating {length} notes...")
        
        for i in range(length):
            # Prepare input
            input_sequence = np.array(current_sequence[-self.sequence_length:])
            input_sequence = input_sequence / len(self.idx_to_note)
            input_sequence = input_sequence.reshape((1, self.sequence_length, 1))
            
            # Predict next note
            prediction = self.model.predict(input_sequence, verbose=0)[0]
            
            # Apply temperature
            prediction = np.log(prediction + 1e-10) / temperature
            prediction = np.exp(prediction) / np.sum(np.exp(prediction))
            
            # Sample next note
            next_note_idx = np.random.choice(len(prediction), p=prediction)
            next_note = self.idx_to_note[next_note_idx]
            
            generated_notes.append(next_note)
            current_sequence.append(next_note_idx)
            
            if (i + 1) % 20 == 0:
                print(f"   Generated {i + 1}/{length} notes")
        
        return generated_notes
    
    def save_to_midi(self, notes_sequence, filename='generated_music.mid', 
                     bpm=120):
        """Convert generated notes to MIDI file"""
        score = stream.Stream()
        score.append(instrument.Piano())
        score.append(tempo.MetronomeMark(number=bpm))
        
        current_offset = 0.0
        
        for note_name in notes_sequence:
            if note_name == 'rest':
                current_offset += 0.5
            elif '.' in note_name:
                # Chord
                chord_notes = note_name.split('.')
                c = chord.Chord(chord_notes)
                c.duration.quarterLength = 0.5
                c.offset = current_offset
                score.append(c)
                current_offset += 0.5
            else:
                # Single note
                n = note.Note(note_name)
                n.duration.quarterLength = 0.5
                n.offset = current_offset
                score.append(n)
                current_offset += 0.5
        
        score.write('midi', fp=filename)
        print(f"✅ MIDI file saved: {filename}")
        return filename

def generate_music():
    """Main generation function"""
    try:
        # Load generator
        generator = MusicSequenceGenerator()
        
        # Create seed sequence
        seed = list(generator.idx_to_note.values())[:10]
        
        # Generate 100 notes
        generated = generator.generate(
            seed_sequence=seed,
            length=100,
            temperature=0.8
        )
        
        # Save to MIDI
        generator.save_to_midi(generated)
        
        print("\n✅ Music generation complete!")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure you've trained the model first by running: python train_model.py")

if __name__ == '__main__':
    generate_music()