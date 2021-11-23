import sys
import torch
import numpy as np
from pathlib import Path
import torchaudio
from catalyst.dl.core import Callback, MetricCallback
from train import snr, sdr


class SaveWavCallback(MetricCallback):
    """SNR callback.

    Args:
        input_key (str): input key to use for dice calculation;
            specifies our y_true.
        output_key (str): output key to use for dice calculation;
            specifies our y_pred.

    """

    def __init__(
        self,
        input_key: str = "targets",
        output_key: str = "logits",
        prefix: str = "snr",
        mixed_audio_key: str = "input_audio",
    ):
        self.mixed_audio_key = mixed_audio_key
        super().__init__(prefix=prefix, metric_fn=snr, input_key=input_key, output_key=output_key)

    def on_batch_end(self, state):
        output_audios = state.output[self.output_key]

        if hasattr(state.model, "module"):
            num_person = state.model.module.num_person
        else:
            num_person = state.model.num_person



        sample_rate = 16000

        for n in range(num_person):
            output_audio = output_audios[0, n, ...]
            # save audio
            filename =Path("/home/irslab/ws/highlight-image-generator/looking-to-listen/storage_dir/storage/result/person_{}.wav".format(n))
            # print(output_audio.size())
            torchaudio.save(filename, output_audio.cpu(), sample_rate, format="wav")
