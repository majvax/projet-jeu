from pydub import AudioSegment
from pydub.playback import play
import threading


def play_sound(filename: str, loop: bool):
    if loop:
        def sound_thread():
            sound = AudioSegment.from_wav(filename)
            while True:
                play(sound)
    else:
        def sound_thread():
            sound = AudioSegment.from_wav(filename)
            play(sound)
    
    thread = threading.Thread(target=sound_thread, daemon=True)
    thread.start()
    return thread




