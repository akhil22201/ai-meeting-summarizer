# AI-Powered Meeting Summarizer

## Overview

The **AI-Powered Meeting Summarizer** is a Gradio-based application that converts meeting audio recordings into transcripts and generates concise summaries using `whisper.cpp` for speech-to-text conversion and `Ollama` for AI-powered summarization. The system helps users quickly extract key discussion points, decisions, and action items from meetings.

---

## Features

- Audio-to-text conversion using `whisper.cpp`
- AI-powered transcript summarization using `Ollama`
- Support for multiple Whisper models (`base`, `small`, `medium`, `large-v3`)
- Translation support for non-English audio
- Interactive Gradio web interface
- Downloadable transcript generation

---

## Technologies Used

**Languages:** Python, HTML5, CSS3, JavaScript  

**Libraries & Frameworks:** Gradio, Whisper.cpp, Ollama, Requests  

**Concepts:** NLP, Speech-to-Text, Audio Processing, Generative AI, Text Summarization

---

## Requirements

- Python 3.x
- FFmpeg
- Whisper.cpp
- Ollama
- Gradio
- Requests

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/akhil22201/ai-meeting-summarizer.git
cd ai-meeting-summarizer
```

---

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 3: Install and Run Ollama

```bash
ollama run llama3.2
```

---

### Step 4: Run the Application

```bash
python main.py
```

---

## Usage

1. Upload an audio meeting recording (`.mp3`, `.wav`, etc.)
2. Select the Whisper model
3. Generate transcript and summary
4. Download the generated transcript

---

## Supported Whisper Models

- base
- small
- medium
- large-v3

---

## Project Workflow

1. Audio Upload
2. Speech-to-Text Conversion
3. Transcript Processing
4. AI-based Summarization
5. Summary Generation

---

## Project Preview

![Project Screenshot](https://github.com/user-attachments/assets/5b93cfed-c853-4ebb-8d90-bbda58354192)

---

## Future Improvements

- Real-time meeting summarization
- Speaker identification
- Cloud deployment support
- Advanced summarization customization

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- Whisper.cpp
- Ollama
- Gradio

---

## Author

Akhil 
