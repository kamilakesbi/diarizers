import argparse
import copy
import glob
import os

from moviepy.editor import AudioFileClip
from pydub import AudioSegment

from diarizers import SpeakerDiarizationDataset


def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()


def get_ami_files(path_to_ami, setup="only_words", hm_type="ihm"):

    """_summary_

    Returns:
        _type_: _description_
    """
    assert setup in ["only_words", "mini"]
    assert hm_type in ["ihm", "sdm"]

    rttm_files = {
        "train": glob.glob(path_to_ami + "/AMI-diarization-setup/{}/rttms/{}/*.rttm".format(setup, "train")),
        "validation": glob.glob(path_to_ami + "/AMI-diarization-setup/{}/rttms/{}/*.rttm".format(setup, "dev")),
        "test": glob.glob(path_to_ami + "/AMI-diarization-setup/{}/rttms/{}/*.rttm".format(setup, "test")),
    }

    audio_files = {
        "train": [],
        "validation": [],
        "test": [],
    }

    for subset in rttm_files:

        rttm_list = copy.deepcopy(rttm_files[subset])

        for rttm in rttm_list:
            meeting = rttm.split("/")[-1].split(".")[0]
            if hm_type == "ihm":
                path = path_to_ami + "/AMI-diarization-setup/pyannote/amicorpus/{}/audio/{}.Mix-Headset.wav".format(
                    meeting, meeting
                )
                if os.path.exists(path):
                    audio_files[subset].append(path)
                else:
                    rttm_files[subset].remove(rttm)
            if hm_type == "sdm":
                path = path_to_ami + "/AMI-diarization-setup/pyannote/amicorpus/{}/audio/{}.Array1-01.wav".format(
                    meeting, meeting
                )
                if os.path.exists(path):
                    audio_files[subset].append(path)
                else:
                    rttm_files[subset].remove(rttm)

    return audio_files, rttm_files


def get_callhome_files(path_to_callhome, langage="jpn"):

    audio_files = glob.glob(path_to_callhome + "/callhome/{}/*.mp3".format(langage))

    audio_files = {
        "data": audio_files,
    }
    cha_files = {
        "data": [],
    }

    for subset in audio_files:
        for cha_path in audio_files[subset]:
            file = cha_path.split("/")[-1].split(".")[0]
            cha_files[subset].append(path_to_callhome + "/callhome/{}/{}.cha".format(langage, file))

    return audio_files, cha_files


def get_callfriends_files(path_to_callfriend, langage="jpn"):

    audio_files = glob.glob(path_to_callfriend + "/callfriend/{}/audio/*.mp3".format(langage))

    audio_files = {
        "data": audio_files,
    }
    cha_files = {
        "data": [],
    }

    for subset in audio_files:
        for cha_path in audio_files[subset]:
            file = cha_path.split("/")[-1].split(".")[0]
            cha_files[subset].append(path_to_callfriend + "/callfriend/{}/cha/{}.cha".format(langage, file))

    return audio_files, cha_files


def get_sakura_files(path_to_sakura, convert_mp4_to_mp3=False):

    if convert_mp4_to_mp3:
        audio_files = glob.glob(path_to_sakura + "/sakura/audio/*.mp4")

        for mp4_path in audio_files:

            mp3_path = mp4_path.split(".")[0] + ".mp3"

            MP4ToMP3(mp4_path, mp3_path)

    audio_files = glob.glob(path_to_sakura + "/sakura/audio/*.mp3")

    audio_files = {
        "data": audio_files,
    }
    cha_files = {
        "data": [],
    }

    for subset in audio_files:
        for cha_path in audio_files[subset]:
            file = cha_path.split("/")[-1].split(".")[0]
            cha_files[subset].append(path_to_sakura + "/sakura/cha/{}.cha".format(file))

    return audio_files, cha_files


def get_simsamu_files(path_to_simsamu):

    rttm_files = glob.glob(path_to_simsamu + "/simsamu/*/*.rttm")
    audio_files = glob.glob(path_to_simsamu + "/simsamu/*/*.m4a")

    for file in audio_files:
        sound = AudioSegment.from_file(file, format="m4a")
        file.split("/")
        file_hanlde = sound.export(file.split(".")[0] + ".wav", format="wav")

    audio_files = glob.glob(path_to_simsamu + "/simsamu/*/*.wav")

    audio_files = {"data": audio_files}

    rttm_files = {"data": rttm_files}

    return audio_files, rttm_files


def get_voxconverse_files(path_to_voxconverse):

    audio_files = {
        "dev": glob.glob(path_to_voxconverse + "/voxconverse/audio/*.wav"),
        "test": glob.glob(path_to_voxconverse + "/voxconverse/voxconverse_test_wav/*.wav"),
    }

    rttm_files = {
        "dev": [],
        "test": [],
    }

    for subset in audio_files:
        for file in audio_files[subset]:
            file = file.split("/")[-1].split(".")[0]
            rttm_files[subset].append(path_to_voxconverse + "/voxconverse/{}/{}.rttm".format(subset,file))

    return audio_files, rttm_files


def get_sakura_files(path_to_sakura, convert_mp4_to_mp3=False):

    if convert_mp4_to_mp3:
        audio_files = glob.glob(path_to_sakura + "/sakura/audio/*.mp4")

        for mp4_path in audio_files:

            mp3_path = mp4_path.split(".")[0] + ".mp3"

            MP4ToMP3(mp4_path, mp3_path)

    audio_files = glob.glob(path_to_sakura + "/sakura/audio/*.mp3")

    audio_files = {
        "data": audio_files,
    }
    cha_files = {
        "data": [],
    }

    for subset in audio_files:
        for cha_path in audio_files[subset]:
            file = cha_path.split("/")[-1].split(".")[0]
            cha_files[subset].append(path_to_sakura + "/sakura/cha/{}.cha".format(file))

    return audio_files, cha_files


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--path_to_dataset", required=True)
    parser.add_argument("--setup", required=False, default="only_words")
    parser.add_argument("--push_to_hub", required=False, default=False)

    parser.add_argument("--hub_repository", required=False)
    args = parser.parse_args()

    if args.dataset == "ami":

        audio_files, rttm_files = get_ami_files(path_to_ami=args.path_to_dataset, setup=args.setup, hm_type="ihm")
        ami_dataset_ihm = SpeakerDiarizationDataset(audio_files, rttm_files).construct_dataset()
        if args.push_to_hub == "True":
            ami_dataset_ihm.push_to_hub(args.hub_repository, "ihm")
        audio_files, rttm_files = get_ami_files(path_to_ami=args.path_to_dataset, setup=args.setup, hm_type="sdm")
        ami_dataset_sdm = SpeakerDiarizationDataset(audio_files, rttm_files).construct_dataset()
        if args.push_to_hub == "True":
            ami_dataset_sdm.push_to_hub(args.hub_repository, "sdm")

    if args.dataset == "callhome":

        langages = ["eng", "jpn", "spa", "zho", "deu"]

        for langage in langages:
            audio_files, cha_files = get_callhome_files(args.path_to_dataset, langage=langage)
            dataset = SpeakerDiarizationDataset(
                audio_files, cha_files, annotations_type="cha", crop_unannotated_regions=True
            ).construct_dataset()

            if args.push_to_hub == "True":
                dataset.push_to_hub(args.hub_repository, str(langage))

    if args.dataset == "simsamu":
        audio_files, rttm_files = get_simsamu_files(args.path_to_dataset)
        dataset = SpeakerDiarizationDataset(audio_files, rttm_files).construct_dataset()

        if args.push_to_hub == "True":
            dataset.push_to_hub(args.hub_repository)

    if args.dataset == "voxconverse":
        audio_files, rttm_files = get_voxconverse_files(args.path_to_dataset)
        dataset = SpeakerDiarizationDataset(audio_files, rttm_files).construct_dataset()

        if args.push_to_hub == "True":
            dataset.push_to_hub(args.hub_repository)

    if args.dataset == "sakura":

        audio_files, cha_files = get_sakura_files(args.path_to_dataset)
        sakura_dataset = SpeakerDiarizationDataset(
            audio_files, cha_files, annotations_type="cha", crop_unannotated_regions=True
        ).construct_dataset()

        if args.push_to_hub == "True":
            dataset.push_to_hub(args.hub_repository)

    if args.dataset == "callfriend":

        langages = ["eng-s", "eng-s", "fra-q", "jpn", "spa", "spa-c", "zho-m"]

        for langage in langages:
            audio_files, cha_files = get_callfriends_files(args.path_to_dataset, langage=langage)
            dataset = SpeakerDiarizationDataset(
                audio_files, cha_files, annotations_type="cha", crop_unannotated_regions=True
            ).construct_dataset()

        if args.push_to_hub == "True":
            dataset.push_to_hub(args.hub_repository, str(langage))
