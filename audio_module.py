import numpy as np

try:
    import sounddevice as sd
except ImportError:
    sd = None


class ClassroomAudioAnalyzer:
    """Analyzes classroom microphone or simulated audio chunks for activity level."""

    def __init__(self, sample_rate: int = 16000, duration: float = 0.5):
        self.sample_rate = sample_rate
        self.duration = duration

    def capture_and_analyze(self, simulate_if_unavailable: bool = True) -> dict:
        samples = None

        if sd is not None:
            try:
                recording = sd.rec(
                    int(self.duration * self.sample_rate),
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype="float32",
                )
                sd.wait()
                samples = np.squeeze(recording)
            except Exception:
                samples = None

        if samples is None:
            if not simulate_if_unavailable:
                return {
                    "rms_energy": 0.0,
                    "audio_activity": "Unavailable",
                    "audio_engagement": 0.0,
                    "source": "none",
                }
            # Offline fallback signal when no microphone is accessible
            t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))
            samples = 0.025 * np.sin(2 * np.pi * 220 * t)
            source = "simulated_offline"
        else:
            source = "microphone"

        rms_energy = float(np.sqrt(np.mean(np.square(samples))))

        if rms_energy < 0.008:
            audio_activity = "Silent / Low Activity"
            audio_engagement = 35.0
        elif rms_energy <= 0.08:
            audio_activity = "Moderate Discussion / Q&A"
            audio_engagement = 85.0
        else:
            audio_activity = "High Noise / Overlapping Talk"
            audio_engagement = 55.0

        return {
            "rms_energy": round(rms_energy, 5),
            "audio_activity": audio_activity,
            "audio_engagement": audio_engagement,
            "source": source,
        }


if __name__ == "__main__":
    audio = ClassroomAudioAnalyzer(duration=1.0)
    output = audio.capture_and_analyze()
    print("Audio Test Result:", output)