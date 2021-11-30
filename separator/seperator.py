from asteroid.models import BaseModel
import soundfile as sf

def use_model(wavfile_path="female-female-mixture.wav"):
    model = BaseModel.from_pretrained("mpariente/DPRNNTasNet-ks2_WHAM_sepclean")
    model.separate(wavfile_path)