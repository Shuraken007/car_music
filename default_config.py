from pydub import AudioSegment
AudioSegment.converter = "/usr/bin/ffmpeg"
AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
AUDIO_SEGMENT = AudioSegment

DOWNLOAD_PATH = "./download"
CONVERT_PATH = "./convert"

MUSIC_EXT = (".mp3", ".wav", ".flac")
SUPPORTED_MUSIC_EXT = (".mp3", ".wav", ".flac")
EXTRA_EXT = (".cue", ".jpg")
MUSIC_CONVERT = [".flac"]