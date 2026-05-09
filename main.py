import subprocess
import os
import gradio as gr
import requests
import json

OLLAMA_SERVER_URL = "http://localhost:11434"
WHISPER_MODEL_DIR = "./whisper.cpp/models"


def get_available_models() -> list[str]:
    response = requests.get(f"{OLLAMA_SERVER_URL}/api/tags")
    if response.status_code == 200:
        models = response.json()["models"]
        llm_model_names = [model["model"] for model in models]
        return llm_model_names
    else:
        raise Exception(
            f"Failed to retrieve models from Ollama server: {response.text}"
        )


def get_available_whisper_models() -> list[str]:
    valid_models = ["base", "small", "medium", "large", "large-V3"]
    model_files = [f for f in os.listdir(WHISPER_MODEL_DIR) if f.endswith(".bin")]

    whisper_models = [
        os.path.splitext(f)[0].replace("ggml-", "")
        for f in model_files
        if any(valid_model in f for valid_model in valid_models) and "test" not in f
    ]

    whisper_models = list(set(whisper_models))
    return whisper_models


def summarize_with_model(llm_model_name: str, context: str, text: str) -> str:
    prompt = f"""You are given a transcript from a meeting, along with some optional context.
    
    Context: {context if context else 'No additional context provided.'}
    
    The transcript is as follows:
    
    {text}
    
    Please summarize the transcript."""

    headers = {"Content-Type": "application/json"}
    data = {"model": llm_model_name, "prompt": prompt}

    response = requests.post(
        f"{OLLAMA_SERVER_URL}/api/generate", json=data, headers=headers, stream=True
    )

    if response.status_code == 200:
        full_response = ""
        try:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    json_line = json.loads(decoded_line)
                    full_response += json_line.get("response", "")
                    if json_line.get("done", False):
                        break
            return full_response
        except json.JSONDecodeError:
            print("Error: Invalid JSON.")
            return f"Failed to parse server response."
    else:
        raise Exception(
            f"Failed to summarize with model {llm_model_name}: {response.text}"
        )


def preprocess_audio_file(audio_file_path: str) -> str:
    output_wav_file = f"{os.path.splitext(audio_file_path)[0]}_converted.wav"
    cmd = f'ffmpeg -y -i "{audio_file_path}" -ar 16000 -ac 1 "{output_wav_file}"'
    subprocess.run(cmd, shell=True, check=True)
    return output_wav_file


def translate_and_summarize(
    audio_file_path: str, context: str, whisper_model_name: str, llm_model_name: str
) -> tuple[str, str]:

    print("Processing audio file:", audio_file_path)

    audio_file_wav = preprocess_audio_file(audio_file_path)
    print("Audio preprocessed:", audio_file_wav)

    whisper_command = (
    f'"C:\\Users\\akhil\\AI-Powered-Meeting-Summarizer\\whisper.cpp\\whisper-cli.exe" '
    f'-m "C:\\Users\\akhil\\AI-Powered-Meeting-Summarizer\\whisper.cpp\\models\\ggml-{whisper_model_name}.bin" '
    f'-f "{audio_file_wav}" -otxt'
)

    subprocess.run(whisper_command, shell=True, check=True)
    print("Whisper.cpp executed successfully")

    # -------- FIXED PART (WHISPER OUTPUT FILE) ----------
    whisper_output_file = audio_file_wav + ".txt"

    with open(whisper_output_file, "r", encoding="utf-8") as f:
        transcript = f.read()
    # -----------------------------------------------------

    transcript_file = "transcript.txt"
    with open(transcript_file, "w", encoding="utf-8") as transcript_f:
        transcript_f.write(transcript)

    summary = summarize_with_model(llm_model_name, context, transcript)

    os.remove(audio_file_wav)
    os.remove(whisper_output_file)

    return summary, transcript_file


def gradio_app(
    audio, context: str, whisper_model_name: str, llm_model_name: str
) -> tuple[str, str]:
    return translate_and_summarize(audio, context, whisper_model_name, llm_model_name)


if __name__ == "__main__":
    ollama_models = get_available_models()
    whisper_models = get_available_whisper_models()

    iface = gr.Interface(
        fn=gradio_app,
        inputs=[
            gr.Audio(type="filepath", label="Upload an audio file"),
            gr.Textbox(
                label="Context (optional)",
                placeholder="Provide any additional context for the summary",
            ),
            gr.Dropdown(
                choices=whisper_models,
                label="Select a Whisper model",
                value=whisper_models[0],
            ),
            gr.Dropdown(
                choices=ollama_models,
                label="Select a model for summarization",
                value=ollama_models[0] if ollama_models else None,
            ),
        ],
        outputs=[
            gr.Textbox(label="Summary", show_copy_button=True),
            gr.File(label="Download Transcript"),
        ],
        analytics_enabled=False,
        title="Meeting Summarizer",
        description="Upload an audio file of a meeting and get a summary.",
    )

    iface.launch(debug=True, share=True)
