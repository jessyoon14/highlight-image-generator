from asteroid.models import BaseModel
import soundfile as sf

def use_model(wavfile_path="female-female-mixture.wav"):
    model = BaseModel.from_pretrained("mpariente/DPRNNTasNet-ks2_WHAM_sepclean")
    mixture, _ = sf.read(wavfile_path, dtype="float32", always_2d=True)
    mixture = mixture.transpose()
    mixture = mixture.reshape(1, mixture.shape[0], mixture.shape[1])
    out_wavs = model.separate(mixture)
    base_name = wavfile_path[:-4]

    # sf.write(save_name.format(src_idx), est_src, fs)
    print(out_wavs.size)
    

# Or simply a file name:
# model.separate("female-female-mixture.wav")

import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display


def show_magspec(waveform, **kw):
    return librosa.display.specshow(
        librosa.amplitude_to_db(np.abs(librosa.stft(waveform))),
        y_axis="log", x_axis="time",
        **kw
    )


use_model()

