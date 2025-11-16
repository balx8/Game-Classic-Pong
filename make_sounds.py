import os
import math
import wave
import struct

SAMPLE_RATE = 44100  # Hz


def generate_tone(filename, freq_hz, duration_ms, volume=0.5):
    """
    Tạo file WAV đơn giản: 1 tone sine.
    filename: đường dẫn file .wav
    freq_hz: tần số (Hz), ví dụ 440
    duration_ms: thời lượng (ms), ví dụ 200
    volume: 0.0 -> 1.0
    """
    num_samples = int(SAMPLE_RATE * (duration_ms / 1000.0))

    # mở file wav
    with wave.open(filename, "w") as wav_file:
        n_channels = 1   # mono
        sampwidth = 2    # 2 bytes = 16-bit
        framerate = SAMPLE_RATE
        n_frames = num_samples
        comptype = "NONE"
        compname = "not compressed"

        wav_file.setparams((n_channels, sampwidth, framerate, n_frames, comptype, compname))

        max_amplitude = 32767 * volume

        for i in range(num_samples):
            t = float(i) / SAMPLE_RATE
            sample = max_amplitude * math.sin(2 * math.pi * freq_hz * t)
            # 16-bit signed
            wav_file.writeframes(struct.pack("<h", int(sample)))


def main():
    os.makedirs("sounds", exist_ok=True)

    hit_path = os.path.join("sounds", "hit.wav")
    score_path = os.path.join("sounds", "score.wav")

    # hit: tiếng ngắn, cao
    print(f"Tao {hit_path} ...")
    generate_tone(hit_path, freq_hz=800, duration_ms=120, volume=0.8)

    # score: tiếng dài hơn, trầm hơn
    print(f"Tao {score_path} ...")
    generate_tone(score_path, freq_hz=500, duration_ms=250, volume=0.8)

    print("Xong! Da tao 2 file WAV trong thu muc 'sounds/'.")


if __name__ == "__main__":
    main()
