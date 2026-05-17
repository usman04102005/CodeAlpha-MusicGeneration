# 🎵 AI Music Generator

An AI-powered music generation web application built using Flask, TensorFlow, LSTM neural networks, and MIDI processing.

## 🚀 Features

- AI-generated music using deep learning
- LSTM neural network architecture
- MIDI file generation
- Interactive Flask web interface
- Download generated music
- Adjustable creativity (temperature)

## 🛠 Technologies Used

- Python
- Flask
- TensorFlow / Keras
- Music21
- NumPy
- HTML/CSS/JavaScript

## 📂 Project Structure

```bash
CodeAlpha_MusicGeneration/
│
├── app.py
├── train_model.py
├── prepare_data.py
├── generate_music.py
├── requirements.txt
├── templates/
│   └── index.html
```

## ▶️ Setup Instructions

### Create Virtual Environment (Windows)

```powershell
py -3.10 -m venv venv
.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Prepare Dataset

Place MIDI files inside:

```bash
midi_data/
```

Then run:

```bash
python prepare_data.py
```

### Train Model

```bash
python train_model.py
```

### Run Application

```bash
python app.py
```

Open in browser:

```bash
http://127.0.0.1:5002
```

## 📸 Screenshots

### Main Interface

![Home](screenshots/home.png)

### Music Generation

![Generation](screenshots/generation.png)

## 👨‍💻 Author

Usman Chughtai
