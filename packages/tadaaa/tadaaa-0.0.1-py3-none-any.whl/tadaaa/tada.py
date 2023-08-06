import numpy as np
import simpleaudio as sa


def note(frequency: float, duration: float):
    fs = 44100  # 44100 samples per second

    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, duration, int(duration * fs), False)

    # Generate a 440 Hz sine wave
    note = np.sin(frequency * t * 2 * np.pi)

    # Ensure that highest value is in 16-bit range
    audio = note * (2 ** 15 - 1) / np.max(np.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    # Start playback
    play_obj = sa.play_buffer(audio, 1, 2, fs)

    # Wait for playback to finish before exiting
    play_obj.wait_done()

def tada():
    """Plays happy ta da sound!"""
    note(440, 0.3)
    note(440, 0.1)
    note(440, 0.1)
    note(880, 0.8)


def quaquaquaquauaua():
    """Plays sad sound"""
    note(587.33, 0.3)
    note(554.37, 0.3)
    note(523.25, 0.3)
    note(493.88, 0.8)
