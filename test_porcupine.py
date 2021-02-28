import pyaudio
import pvporcupine
import struct

porcupine = None
pa = None
audio_stream = None


try:
    porcupine = pvporcupine.create(keywords=["blueberry", "grapefruit"])
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=porcupine.sample_rate, channels=1,
                        format=pyaudio.paInt16, input=True,
                        frames_per_buffer=porcupine.frame_length)
    while True:
        print('.',end=' ')
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Hotword Detected")
except Exception as e:
    print('-'*35)
    print(e)
    print('-'*35)
finally:
    if porcupine is not None:
        porcupine.delete()

    if audio_stream is not None:
        audio_stream.close()

    if pa is not None:
            pa.terminate()