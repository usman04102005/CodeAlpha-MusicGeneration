import numpy as np
import pickle
import os
from keras import Sequential
from keras.layers import LSTM, Dropout, Dense
from keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler

class MusicGenerator:
    def __init__(self, sequence_length=64):
        self.sequence_length = sequence_length
        self.model = None
        self.note_to_idx = {}
        self.idx_to_note = {}
        self.scaler = MinMaxScaler(feature_range=(0, 1))
    
    def prepare_sequences(self, notes_data):
        """Prepare sequences for LSTM training"""
        # Get unique notes
        unique_notes = sorted(set(notes_data))
        self.note_to_idx = {note: i for i, note in enumerate(unique_notes)}
        self.idx_to_note = {i: note for note, i in self.note_to_idx.items()}
        
        print(f"Total unique notes: {len(unique_notes)}")
        
        # Convert notes to integers
        notes_int = np.array([self.note_to_idx[note] for note in notes_data])
        
        # Create sequences
        X = []
        y = []
        
        for i in range(len(notes_int) - self.sequence_length):
            X.append(notes_int[i:i + self.sequence_length])
            y.append(notes_int[i + self.sequence_length])
        
        X = np.array(X)
        y = np.array(y)
        
        # Normalize
        X = X / len(unique_notes)
        
        print(f"Training sequences prepared: {len(X)}")
        
        return X, y
    
    def build_model(self, num_notes, sequence_length):
        """Build LSTM model for music generation"""
        model = Sequential([
            LSTM(128, activation='relu', input_shape=(sequence_length, 1)),
            Dropout(0.2),
            Dense(128, activation='relu'),
            Dropout(0.2),
            Dense(128, activation='relu'),
            Dropout(0.2),
            Dense(num_notes, activation='softmax')
        ])
        
        model.compile(
            loss='sparse_categorical_crossentropy',
            optimizer=Adam(learning_rate=0.001),
            metrics=['accuracy']
        )
        
        print("\n✅ Model Architecture:")
        model.summary()
        
        return model
    
    def train(self, notes_data, epochs=50, batch_size=64):
        """Train the music generation model"""
        print("\n🎵 Training Music Generation Model...")
        
        # Prepare sequences
        X, y = self.prepare_sequences(notes_data)
        
        # Reshape for LSTM [samples, time steps, features]
        X = X.reshape((X.shape[0], X.shape[1], 1))
        
        # Build model
        num_notes = len(set(notes_data))
        self.model = self.build_model(num_notes, self.sequence_length)
        
        # Train
        print(f"\nTraining for {epochs} epochs...")
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1,
            validation_split=0.2
        )
        
        # Save model
        self.model.save('music_generator_model.h5')
        
        # Save mapping
        with open('note_mapping.pkl', 'wb') as f:
            pickle.dump({
                'note_to_idx': self.note_to_idx,
                'idx_to_note': self.idx_to_note,
                'sequence_length': self.sequence_length
            }, f)
        
        print("\n✅ Model saved as 'music_generator_model.h5'")
        print("✅ Note mapping saved as 'note_mapping.pkl'")
        
        return history

def train_music_model():
    """Main training function"""
    # Load notes data
    try:
        with open('notes_data_notes.pkl', 'rb') as f:
            notes = pickle.load(f)
    except FileNotFoundError:
        print("❌ notes_data_notes.pkl not found!")
        print("Run prepare_data.py first to extract notes from MIDI files")
        return
    
    print(f"Loaded {len(notes)} notes")
    
    # Create generator and train
    generator = MusicGenerator(sequence_length=64)
    history = generator.train(notes, epochs=50, batch_size=64)
    
    print("\n🎵 Training completed! Model is ready for generation.")

if __name__ == '__main__':
    train_music_model()