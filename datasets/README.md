# Speaker diarization datasets

## 1. Add any speaker diarization dataset to the hub

General steps to add a Speaker diarization dataset with <files, annotations> to the hub:  

1. Prepare a folder containing audios and annotations files , which should be organised like this: 

```
    dataset_folder
    ├── audio                   
    │   ├── file_1.mp3          
    │   ├── file_2.mp3          
    │   └── file_3.mp3                 
    ├── annotations          
    │   ├── file_1.rttm          
    │   ├── file_2.rttm          
    │   └── file_3.rttm    
```


2. Get dictionnaries with the following structure:

```
annotations_files = {
    "subset1": [list of annotations_files in subset1],
    "subset2":  [list of annotations_files in subset2],
}
audio_files = {
    "subset1": [list of annotations_files in subset1],
    "subset2":  [list of annotations_files in subset2],   
}
```

Here, each subset will correspond in a Hugging Face dataset subset. 

3. Use SpeakerDiarization module from `diarizers` to obtain your Hugging Face dataset: 

```
from diarizers import SpeakerDiarizationDataset
dataset = SpeakerDiarizationDataset(audio_files, annotations_files).construct_dataset()
```

Note: This module can currently be used on RTTM format annotation files, but may need to be adapted for other formats.

## Current datasets in diarizers-community

We explain the scripts we used to add the various datasets present in the [diarizers-community](https://huggingface.co/diarizers-community): 

#### AMI IHM AND SDM: 

```
git clone https://github.com/pyannote/AMI-diarization-setup.git
cd /AMI-diarization-setup/pyannote/
sh download_ami.sh
sh download_ami_sdm.sh
```

#### CALLHOME: 

Download for each language (example here for Japanese): 

```
wget https://ca.talkbank.org/data/CallHome/jpn.zip
wget -r -np -nH --cut-dirs=2 -R index.html* https://media.talkbank.org/ca/CallHome/jpn/
unzip jpn.zip
```

#### VOXCONVERSE: 

Download the RTTM files: 

```
git clone git@github.com:joonson/voxconverse.git
```

Download the audio files: 

```
wget https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_dev_wav.zip
unzip voxconverse_dev_wav.zip
wget https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_test_wav.zip
unzip voxconverse_test_wav.zip
```

#### SIMSAMU: 

The Simsamu dataset is based on this [Hugging Face dataset](https://huggingface.co/datasets/medkit/simsamu): 

```
git lfs install
git clone git@hf.co:datasets/medkit/simsamu
```

#### Push to hub: 

We pushed each of these datasets using `spd_datasets.py` and the following script: 


```
python3 spd_datasets.py \
    --dataset=callhome \
    --path_to_dataset=/path_to_callhome \
    --push_to_hub=False \
    --hub_repository=diarizers-community/callhome \
```


## 2. Generate a synthetic dataset compatible with diarizers: 

### Installation

To use the synthetic dataset pipeline, first install `diarizers`: 

```sh
git clone https://github.com/huggingface/diarizers.git
cd diarizers
pip install -e .
```

To augment your synthetic datas with noise, you need to use background noise and room impulse response datasets. Here are suggested datasets and how to download them: 

- Background Noise dataset: [WHAM!](http://wham.whisper.ai/). To download: 

```
wget https://my-bucket-a8b4b49c25c811ee9a7e8bba05fa24c7.s3.amazonaws.com/wham_noise.zip
unzip wham_noise.zip
```

- Room Impulse Response dataset: [MIT-ir-survey](https://mcdermottlab.mit.edu/Reverb/IR_Survey.html). To download: 

```
wget https://mcdermottlab.mit.edu/Reverb/IRMAudio/Audio.zip
unzip Audio.zip
```

### How to use? 

To generate synthetic datasets, you will need to specify a few parameters via the `SyntheticDatasetConfig` class. 

You can generate 20 hours of japanese synthetic speaker diarization datas using the following code snippet: 

```python
from diarizers import SyntheticDatasetConfig, SyntheticDataset

synthetic_config = SyntheticDatasetConfig(
        dataset_name="mozilla-foundation/common_voice_17_0",
        subset="validated",
        split="ja",
        speaker_column_name="client_id", 
        audio_column_name="audio", 
        min_samples_per_speaker=10,
        nb_speakers_from_dataset=-1,
        sample_rate=16000, 
        nb_speakers_per_meeting=3,
        num_meetings=1600,  
        segments_per_meeting=16, 
        normalize=True, 
        augment=False, 
        overlap_proba=0.3,
        overlap_length=3, 
        random_gain=False,
        add_silence=True, 
        silence_duration=3,  
        silence_proba=0.7, 
        denoise=False, 
        num_proc=2
)
dataset = SyntheticDataset(synthetic_config).generate()
dataset.push_to_hub('diarizers-community/synthetic-speaker-diarization-dataset')
```

Find more informations on how to use 🤗 Diarizers synthetic speaker diarization pipeline in this notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1kaKv5Qa2dUuEwyLoFeh5mCwgy8O_ZdYA#scrollTo=27RrvTZte4BF). 
