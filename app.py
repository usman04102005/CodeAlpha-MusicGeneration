from flask import Flask, jsonify, send_file, render_template
from flask_cors import CORS
import os
from generate_music import MusicSequenceGenerator

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

# Load generator once
try:
    generator = MusicSequenceGenerator()
    generator_ready = True
except Exception as e:
    print(f"Warning: {e}")
    generator_ready = False

@app.route('/api/generate-music', methods=['POST'])
def generate():
    """Generate new music sequence"""
    if not generator_ready:
        return jsonify({'error': 'Model not ready. Please train first.'}), 500
    
    try:
        # Create seed from the mapping and pad to sequence length if needed
        seed = list(generator.idx_to_note.values())[:generator.sequence_length]
        
        # Generate
        generated = generator.generate(seed, length=100, temperature=0.8)
        
        # Save MIDI
        filename = 'generated_music.mid'
        generator.save_to_midi(generated, filename)
        
        return jsonify({
            'success': True,
            'message': 'Music generated successfully',
            'notes_count': len(generated),
            'file': filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-music', methods=['GET'])
def download():
    """Download generated MIDI file"""
    try:
        return send_file('generated_music.mid', 
                        as_attachment=True,
                        download_name='generated_music.mid')
    except FileNotFoundError:
        return jsonify({'error': 'No generated music file found'}), 404

@app.route('/api/status', methods=['GET'])
def status():
    """Check generator status"""
    return jsonify({
        'ready': generator_ready,
        'notes_count': len(generator.idx_to_note) if generator_ready else 0
    })

if __name__ == '__main__':
    app.run(debug=True, port=5002)