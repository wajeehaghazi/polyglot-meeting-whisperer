# import sounddevice as sd
# import numpy as np
# from transcribe import transcribe_audio
# import threading
# import time

# def get_device_index(name_contains: str, is_input=True):
#     for i, device in enumerate(sd.query_devices()):
#         if name_contains.lower() in device['name'].lower() and (
#             (is_input and device['max_input_channels'] > 0) or
#             (not is_input and device['max_output_channels'] > 0)
#         ):
#             return i
#     raise RuntimeError(f"Device containing '{name_contains}' not found.")


# SAMPLE_RATE = 22050
# CHANNELS = 1
# CHUNK_DURATION = 5  # seconds
# CHUNK_SIZE = SAMPLE_RATE * CHUNK_DURATION

# # Replace these with the correct indices for your setup
# MIC_DEVICE_INDEX = get_device_index("microphone")
# LOOPBACK_DEVICE_INDEX = get_device_index("stereo mix")

# # Control flags
# recording = False
# mic_stream = None
# loopback_stream = None

# # Shared chunk buffers
# mic_chunks = []
# loopback_chunks = []

# def mic_callback(indata, frames, time_info, status):
#     if status:
#         print("⚠️ Mic:", status)
#     mic_chunks.append(indata.copy())

# def loopback_callback(indata, frames, time_info, status):
#     if status:
#         print("⚠️ Loopback:", status)
#     loopback_chunks.append(indata.copy())

# def chunk_processor():
#     while recording:
#         if len(mic_chunks) > 0 and len(loopback_chunks) > 0:
#             mic_chunk = mic_chunks.pop(0)
#             loopback_chunk = loopback_chunks.pop(0)

#             # Mix the chunks (simple average)
#             combined = ((mic_chunk.astype(np.int32) + loopback_chunk.astype(np.int32)) // 2).astype(np.int16)
#             audio_bytes = combined.tobytes()

#             transcript = transcribe_audio(audio_bytes)
#             if transcript.strip():
#                 print("📝 Transcript added.")
#                 with open("transcripts.txt", "a", encoding="utf-8") as f:
#                     f.write(transcript.strip() + "\n")
#             else:
#                 print("🌀 No speech detected.")
#         else:
#             time.sleep(0.1)

# def record_loop():
#     global mic_stream, loopback_stream, recording

#     try:
#         print("🔊 Starting dual recording (mic + loopback)...")

#         mic_stream = sd.InputStream(
#             device=MIC_DEVICE_INDEX,
#             channels=CHANNELS,
#             samplerate=SAMPLE_RATE,
#             dtype='int16',
#             callback=mic_callback,
#             blocksize=CHUNK_SIZE
#         )

#         loopback_stream = sd.InputStream(
#             device=LOOPBACK_DEVICE_INDEX,
#             channels=CHANNELS,
#             samplerate=SAMPLE_RATE,
#             dtype='int16',
#             callback=loopback_callback,
#             blocksize=CHUNK_SIZE
#         )

#         mic_stream.start()
#         loopback_stream.start()

#         print("✅ Streams started.")
#         threading.Thread(target=chunk_processor, daemon=True).start()

#         while recording:
#             time.sleep(0.1)

#         print("🛑 Stopping streams...")
#         mic_stream.stop(); mic_stream.close()
#         loopback_stream.stop(); loopback_stream.close()

#     except Exception as e:
#         print("❌ Error during stream startup:", e)

# def start_loopback():
#     global recording
#     if not recording:
#         recording = True
#         threading.Thread(target=record_loop, daemon=True).start()

# def stop_loopback():
#     global recording
#     recording = False


# import sounddevice as sd
# import numpy as np
# from transcribe import transcribe_audio
# import threading
# import time

# SAMPLE_RATE = 22050
# CHANNELS = 1
# CHUNK_DURATION = 5  # seconds
# CHUNK_SIZE = SAMPLE_RATE * CHUNK_DURATION

# def get_device_index(name_contains: str, is_input=True, limit=10):
#     devices = sd.query_devices()[:limit]  # only consider top N devices
#     for i, device in enumerate(devices):
#         if name_contains.lower() in device['name'].lower() and (
#             (is_input and device['max_input_channels'] > 0) or
#             (not is_input and device['max_output_channels'] > 0)
#         ):
#             print(f"✅ Found '{name_contains}' as device index: {i}")
#             return i
#     print(f"⚠️ Could not find device with name containing: {name_contains} in top {limit} devices.")
#     return None

# # Try detecting devices
# MIC_DEVICE_INDEX = get_device_index("microphone", is_input=True)
# LOOPBACK_DEVICE_INDEX = get_device_index("stereo mix", is_input=True)

# # Control flags
# recording = False
# mic_stream = None
# loopback_stream = None

# # Shared chunk buffers
# mic_chunks = []
# loopback_chunks = []

# def mic_callback(indata, frames, time_info, status):
#     if status:
#         print("⚠️ Mic:", status)
#     mic_chunks.append(indata.copy())

# def loopback_callback(indata, frames, time_info, status):
#     if status:
#         print("⚠️ Loopback:", status)
#     loopback_chunks.append(indata.copy())

# def chunk_processor():
#     while recording:
#         if LOOPBACK_DEVICE_INDEX is not None:
#             if len(mic_chunks) > 0 and len(loopback_chunks) > 0:
#                 mic_chunk = mic_chunks.pop(0)
#                 loopback_chunk = loopback_chunks.pop(0)
#                 combined = ((mic_chunk.astype(np.int32) + loopback_chunk.astype(np.int32)) // 2).astype(np.int16)
#                 audio_bytes = combined.tobytes()
#             else:
#                 time.sleep(0.1)
#                 continue
#         else:
#             if len(mic_chunks) > 0:
#                 mic_chunk = mic_chunks.pop(0)
#                 audio_bytes = mic_chunk.astype(np.int16).tobytes()
#             else:
#                 time.sleep(0.1)
#                 continue

#         transcript = transcribe_audio(audio_bytes)
#         if transcript.strip():
#             print("📝 Transcript added.")
#             with open("transcripts.txt", "a", encoding="utf-8") as f:
#                 f.write(transcript.strip() + "\n")
#         else:
#             print("🌀 No speech detected.")

# def record_loop():
#     global mic_stream, loopback_stream, recording

#     if MIC_DEVICE_INDEX is None:
#         print("❌ No microphone device found. Aborting.")
#         return

#     try:
#         print("🔊 Starting recording...")

#         mic_stream = sd.InputStream(
#             device=MIC_DEVICE_INDEX,
#             channels=CHANNELS,
#             samplerate=SAMPLE_RATE,
#             dtype='int16',
#             callback=mic_callback,
#             blocksize=CHUNK_SIZE
#         )

#         if LOOPBACK_DEVICE_INDEX is not None:
#             loopback_stream = sd.InputStream(
#                 device=LOOPBACK_DEVICE_INDEX,
#                 channels=CHANNELS,
#                 samplerate=SAMPLE_RATE,
#                 dtype='int16',
#                 callback=loopback_callback,
#                 blocksize=CHUNK_SIZE
#             )

#         mic_stream.start()
#         print("🎤 Mic stream started.")

#         if LOOPBACK_DEVICE_INDEX is not None:
#             loopback_stream.start()
#             print("🔁 Loopback stream started.")
#         else:
#             print("⚠️ Loopback device not found. Running in mic-only mode.")

#         threading.Thread(target=chunk_processor, daemon=True).start()

#         while recording:
#             time.sleep(0.1)

#         print("🛑 Stopping streams...")
#         mic_stream.stop(); mic_stream.close()
#         if loopback_stream:
#             loopback_stream.stop(); loopback_stream.close()

#     except Exception as e:
#         print("❌ Error during stream startup:", e)

# def start_loopback():
#     global recording
#     if not recording:
#         recording = True
#         threading.Thread(target=record_loop, daemon=True).start()

# def stop_loopback():
#     global recording
#     recording = False


import sounddevice as sd
import numpy as np
import threading
import subprocess
import time
import tempfile
import os

from agents.transcribe_agent import TranscribeAgent
from agents.translate_agent import TranslateAgent
from agents.summarizer_agent import SummarizerAgent
from agents.question_generator_agent import QuestionGeneratorAgent
from agents.keyword_explainer_agent import KeywordExplainerAgent

SAMPLE_RATE = 22050
CHANNELS = 1
CHUNK_DURATION = 5
CHUNK_SIZE = SAMPLE_RATE * CHUNK_DURATION

MIC_DEVICE_INDEX = None
LOOPBACK_DEVICE_INDEX = None

# Buffers and flags
recording = False
mic_chunks = []
loopback_chunks = []

# Agents
transcribe_agent = TranscribeAgent()
translate_agent = TranslateAgent()
summarizer_agent = SummarizerAgent()
question_generator_agent = QuestionGeneratorAgent()
keyword_agent = KeywordExplainerAgent()

def get_device_index(name_contains: str, is_input=True, limit=10):
    devices = sd.query_devices()[:limit]
    for i, device in enumerate(devices):
        if name_contains.lower() in device['name'].lower() and (
            (is_input and device['max_input_channels'] > 0) or
            (not is_input and device['max_output_channels'] > 0)
        ):
            return i
    return None

def mic_callback(indata, frames, time_info, status):
    if status:
        print("⚠️ Mic:", status)
    mic_chunks.append(indata.copy())

def loopback_callback(indata, frames, time_info, status):
    if status:
        print("⚠️ Loopback:", status)
    loopback_chunks.append(indata.copy())

def save_output(transcript, translated, keywords, summary, questions):
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write("\n=== New Chunk ===\n")
        f.write(f"Transcript:\n{transcript.strip()}\n")
        f.write(f"Translation:\n{translated.strip()}\n")

        if isinstance(keywords, list):
            keyword_lines = [
                f"- {k['keyword']}: {k['definition']}"
                for k in keywords
                if isinstance(k, dict) and 'keyword' in k and 'definition' in k
            ]
            f.write("Keywords:\n" + "\n".join(keyword_lines) + "\n")
        else:
            f.write(f"Keywords:\n{keywords.strip()}\n")

        if summary:
            f.write(f"Summary:\n{summary.strip()}\n")

        if questions:
            if isinstance(questions, list):
                question_lines = [
                    q["question"] if isinstance(q, dict) and "question" in q else str(q)
                    for q in questions
                ]
                f.write("Questions:\n" + "\n".join(question_lines) + "\n")
            else:
                f.write(f"Questions:\n{questions.strip()}\n")

def chunk_processor():
    while recording:
        try:
            if LOOPBACK_DEVICE_INDEX is not None:
                if mic_chunks and loopback_chunks:
                    mic_chunk = mic_chunks.pop(0)
                    loop_chunk = loopback_chunks.pop(0)
                    combined = ((mic_chunk.astype(np.int32) + loop_chunk.astype(np.int32)) // 2).astype(np.int16)
                    audio_bytes = combined.tobytes()
                else:
                    time.sleep(0.1)
                    continue
            else:
                if mic_chunks:
                    mic_chunk = mic_chunks.pop(0)
                    audio_bytes = mic_chunk.astype(np.int16).tobytes()
                else:
                    time.sleep(0.1)
                    continue


            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wav_file:
                wav_path = wav_file.name
                wav_file.write(audio_bytes)

            # Convert raw PCM .wav to .webm using ffmpeg
            webm_path = wav_path.replace(".wav", ".webm")
            ffmpeg_cmd = [
                "ffmpeg",
                "-y",                        # Overwrite output if it exists
                "-f", "s16le",               # PCM 16-bit little endian
                "-ar", str(SAMPLE_RATE),     # Sample rate
                "-ac", str(CHANNELS),        # Mono or Stereo
                "-i", wav_path,              # Input file (raw PCM)
                webm_path                    # Output file
            ]

            subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            try:
                transcript = transcribe_agent.run(webm_path)
                if transcript.strip():
                    translated = translate_agent.run(transcript, target_language="german")
                    keywords = keyword_agent.run(transcript)
                    summary = summarizer_agent.add_chunk(transcript, target_language="german")
                    questions = question_generator_agent.run(summary, target_language="german") if summary else []

                    save_output(transcript, translated, keywords, summary, questions)
                    print("✅ Processed & saved.")
                else:
                    print("🌀 No speech detected.")
            except Exception as e:
                print("❌ Transcription failed:", e)
            finally:
                os.remove(wav_path)
                os.remove(webm_path)
        except Exception as e:
            print("❌ Error in processing:", e)

def record_loop():
    global MIC_DEVICE_INDEX, LOOPBACK_DEVICE_INDEX, recording

    MIC_DEVICE_INDEX = get_device_index("microphone", is_input=True)
    LOOPBACK_DEVICE_INDEX = get_device_index("stereo mix", is_input=True)

    if MIC_DEVICE_INDEX is None:
        print("❌ No microphone found.")
        return

    try:
        mic_stream = sd.InputStream(
            device=MIC_DEVICE_INDEX,
            channels=CHANNELS,
            samplerate=SAMPLE_RATE,
            dtype='int16',
            callback=mic_callback,
            blocksize=CHUNK_SIZE
        )

        loopback_stream = None
        if LOOPBACK_DEVICE_INDEX is not None:
            loopback_stream = sd.InputStream(
                device=LOOPBACK_DEVICE_INDEX,
                channels=CHANNELS,
                samplerate=SAMPLE_RATE,
                dtype='int16',
                callback=loopback_callback,
                blocksize=CHUNK_SIZE
            )

        mic_stream.start()
        if loopback_stream:
            loopback_stream.start()

        print("🎙️ Recording started.")
        threading.Thread(target=chunk_processor, daemon=True).start()

        while recording:
            time.sleep(0.1)

        mic_stream.stop(); mic_stream.close()
        if loopback_stream:
            loopback_stream.stop(); loopback_stream.close()

        print("🛑 Recording stopped.")

    except Exception as e:
        print("❌ Stream error:", e)

def start_loopback():
    global recording
    if not recording:
        recording = True
        threading.Thread(target=record_loop, daemon=True).start()

def stop_loopback():
    global recording
    recording = False
