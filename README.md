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

<img width="1919" height="1079" alt="Screenshot 2026-05-17 145855" src="https://github.com/user-attachments/assets/f3b2839b-7ac8-4d07-9ae8-bc6d4b236737" />


### Music Generation

<img width="1919" height="1079" alt="Screenshot 2026-05-17 150004" src="https://github.com/user-attachments/assets/642b58d5-70fb-4e8a-bf43-bf905186e35f" />

### Generated Music

<img width="1919" height="1079" alt="Screenshot 2026-05-17 150021" src="https://github.com/user-attachments/assets/4e9589c5-acd8-45ba-bfff-1d542703d33a" />




## 👨‍💻 Author

Usman Chughtai
