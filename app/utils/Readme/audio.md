# Audio Utilities

## 1. Overview

The `audio.py` module provides microphone-based audio recording functionality for Nevark AI.

It uses the `sounddevice` library to capture audio from the system's microphone, NumPy to convert the recorded samples into 16-bit integer values, and SciPy to save the recording as a WAV file.

The module exposes one primary function:

- `record_audio()` – Records audio for a configurable duration, saves it to a WAV file, and returns the output file path.

This utility provides a local audio-capture mechanism that can supply audio files to the speech-processing pipeline.

## 2. Dependencies

```python
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
```

| Dependency | Purpose |
|---|---|
| `sounddevice` | Captures audio from the system's audio input device |
| `numpy` | Handles recorded audio samples and converts their data type |
| `scipy.io.wavfile` | Writes recorded audio data into a WAV file |

## 3. Audio Configuration

```python
SAMPLE_RATE = 16000
```

The module defines a sample rate of 16,000 Hz.

This means the recording captures 16,000 audio samples per second.

| Property | Configuration |
|---|---|
| Sample rate | 16,000 Hz |
| Channels | 1 |
| Recording format | `float32` during capture |
| Saved sample format | `int16` |
| Output container | WAV |

The recording uses a single audio channel, producing mono audio.

## 4. Core Function: `record_audio()`

```python
def record_audio(
    duration: int = 5,
    output_file: str = "temp.wav"
):
```

The `record_audio()` function captures audio through the system microphone and saves the recording to a WAV file.

### Input parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `duration` | `int` | `5` | Recording duration in seconds |
| `output_file` | `str` | `"temp.wav"` | Destination path for the recorded WAV file |

### Return value

The function returns:

- `output_file` – The path supplied for the saved recording.

## 5. Recording Process

### Step 1: Display recording status

```python
print("🎤 Recording Audio...")
```

A message is printed to indicate that audio recording is starting.

### Step 2: Capture microphone audio

```python
audio = sd.rec(
    int(duration * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32"
)
```

The `sounddevice.rec()` function starts recording audio from the system's default input device.

The recording configuration includes:

| Parameter | Value | Purpose |
|---|---|---|
| Number of frames | `duration * SAMPLE_RATE` | Determines how many samples to record |
| `samplerate` | `16000` | Sets the recording sample rate |
| `channels` | `1` | Records mono audio |
| `dtype` | `float32` | Stores captured samples as 32-bit floating-point values |

### Calculating the number of samples

```python
int(duration * SAMPLE_RATE)
```

The total number of samples is calculated by multiplying the recording duration by the sample rate.

For the default five-second recording:

\[
5 \times 16000 = 80000
\]

Therefore, the recording captures 80,000 audio frames.

### Step 3: Wait for recording completion

```python
sd.wait()
```

The function waits until the recording operation finishes.

This ensures that the recorded audio data is available before the module attempts to save it.

### Step 4: Convert audio samples and save the WAV file

```python
wav.write(
    output_file,
    SAMPLE_RATE,
    (audio * 32767).astype(np.int16)
)
```

This step converts the recorded audio samples into a format suitable for saving as a 16-bit PCM-style WAV recording.

The conversion happens in two stages.

**A. Scale the audio samples**

```python
audio * 32767
```

The recorded samples are represented as floating-point values.

They are multiplied by 32,767 to scale them into the approximate range used by signed 16-bit integer audio samples.

**B. Convert the sample data type**

```python
.astype(np.int16)
```

NumPy converts the scaled samples into signed 16-bit integers.

**C. Write the WAV file**

```python
wav.write(
    output_file,
    SAMPLE_RATE,
    ...
)
```

SciPy writes the audio data to the specified output path using the configured 16,000 Hz sample rate.

### Step 5: Display completion status

```python
print("✅ Recording Complete")
```

A completion message is printed after the WAV file has been written successfully.

### Step 6: Return the output path

```python
return output_file
```

The function returns the path of the generated audio file.

The calling component can use this path for subsequent audio processing.

## 6. Complete Execution Flow

The recording pipeline follows this sequence:

1. A component calls `record_audio()`.
2. The function uses the supplied duration and output path.
3. `sounddevice` captures microphone audio.
4. Audio is recorded as mono `float32` samples at 16 kHz.
5. `sd.wait()` waits for the recording to finish.
6. NumPy scales and converts the samples to `int16`.
7. SciPy writes the samples into a WAV file.
8. A completion message is printed.
9. The generated file path is returned.

## 7. Example Usage

### Default recording

```python
audio_path = record_audio()
```

This records five seconds of microphone audio and saves it as:

`temp.wav`

### Custom recording duration

```python
audio_path = record_audio(
    duration=10
)
```

This records ten seconds of audio and saves it using the default output filename.

### Custom output file

```python
audio_path = record_audio(
    duration=5,
    output_file="recording.wav"
)
```

This records five seconds of audio and saves it as `recording.wav`.

These examples illustrate the function's supported parameters.

## 8. Integration with Speech Processing

The generated WAV file path can be passed to the Faster-Whisper transcription function:

```python
audio_path = record_audio(
    duration=5
)

transcript = transcribe_audio(
    audio_path
)
```

This is an illustrative integration based on the interfaces exposed by:

- `app/utils/audio.py`
- `app/core/whisper_engine.py`

The audio utility handles microphone recording, while the Whisper engine handles speech recognition.

The `record_audio()` function itself does not invoke Whisper or send the recording to the chat service.

## 9. Current Implementation Scope

The module currently provides:

- Local microphone recording.
- Configurable recording duration.
- Configurable output filename.
- Mono audio capture.
- 16 kHz sample rate.
- Floating-point audio capture.
- Conversion to 16-bit integer samples.
- WAV file generation.
- Recording status messages.
- Output file path return.

The module does not currently implement:

- Continuous microphone streaming.
- Real-time transcription.
- Automatic silence detection.
- Voice activity detection during recording.
- Noise cancellation.
- Audio enhancement.
- Microphone-device selection.
- Automatic recording retries.
- Recording-file cleanup.
- Direct integration with the chat service.

## 10. Important Implementation Considerations

### 10.1 Default recording duration

The default duration is five seconds.

Longer recordings can be requested by supplying a different `duration` value.

### 10.2 Default microphone selection

The implementation does not explicitly select an input device.

It relies on the default audio input device configured in the environment.

### 10.3 Blocking recording operation

The function is synchronous.

`sd.wait()` blocks execution until the requested recording completes.

### 10.4 Output-file handling

The WAV file is written to the supplied path.

If a file already exists at that path, the write operation can replace its contents.

### 10.5 Audio conversion

The recording is captured as `float32` and converted to `int16` before being written.

The module does not perform additional audio normalization, filtering, or noise reduction.

## 11. Summary

The `audio.py` module provides the local microphone-recording utility for Nevark AI.

It captures mono audio at 16 kHz using SoundDevice, converts the recorded samples into 16-bit integer format using NumPy, and saves the result as a WAV file through SciPy.

The returned audio path can then be supplied to the Whisper engine for speech-to-text processing.

This module provides the audio-capture foundation for workflows that begin with locally recorded microphone input.