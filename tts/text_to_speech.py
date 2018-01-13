from .polly import Polly


def get_polly_client():
    '''
    Description
    -----------
    Read: https://aws.amazon.com/polly/
     Get Polly client to create applications that talk.

    Return value
    ------------
    Object of Polly class. See polly.py
    '''
    aws_access_key_id = AWS_ACCESS_KEY_ID
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    region_name = AWS_REGION_NAME
    polly = Polly(aws_access_key_id, aws_secret_access_key, region_name)

    return polly


def get_voice_id(language=None, gender=None):
    '''
    Description
    -----------
    Read: https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
    Get voice ID understood by AWS Polly based on the language and gender.

    Example
    -------
    >> get_voice_id(language='US English', 'Male')
    'Joey'

    Return value
    ------------
    voice ID evaluated as per the voice dictionary. See polly.py

    Cases
    =====
    1. Voice for a particular gender does not exist.
        returns:: the voice ID of other gender.
    2. Voice does not exist at all.
        raises:: ValueError
    '''
    polly = get_polly_client()
    if language is None:
        language = Polly.language
    if gender is None:
        gender = Polly.gender
    voice_id = polly.get_voice_by_language_and_gender(language, gender)
    return voice_id


def get_audio(text, voice_id, text_type=None, output_format=None):
    '''
    Description
    -----------
    Gets TTS for the provided text and voice_id.

    Arguments
    ---------
    text
    ====
    Type:: str
    Description:: Text that is to be converted to speech.

    voice_id
    ========
    Type:: str
    Description:: Voice in which the speech needs to be.

    text_type
    =========
    Type:: str
    Values:: ssml | text
    Description:: Read: https://docs.aws.amazon.com/polly/latest/dg/ssml.html
                  Type of text that is being provided to Polly.

    output_format
    =============
    Type:: str
    Values:: json | mp3 | ogg_vorbis | pcm
    Description:: Format in which speech output should be.


    Return value
    ------------
    Audio object returned after TTS from Polly.
    '''
    polly = get_polly_client()
    if text_type is None:
        text_type = Polly.text_type
    if output_format is None:
        output_format = Polly.output_format
    audio = polly.get_speech(text, voice_id, text_type, output_format)
    return audio


def get_audio_file(text, voice_id, filename, text_type=None, output_format=None):
    '''
    Description
    -----------
    Gets TTS for the provided text and voice_id.

    Arguments
    ---------
    text
    ====
    Type:: str
    Description:: Text that is to be converted to speech.

    voice_id
    ========
    Type:: str
    Description:: Voice in which the speech needs to be.

    filename
    ========
    Type:: str
    Description:: Name of the file in which the audio output is to be saved.

    text_type
    =========
    Type:: str
    Values:: ssml | text
    Description:: Read: https://docs.aws.amazon.com/polly/latest/dg/ssml.html
                  Type of text that is being provided to Polly.

    output_format
    =============
    Type:: str
    Values:: json | mp3 | ogg_vorbis | pcm
    Description:: Format in which speech output should be.


    Return value
    ------------
    Path to file containing audio object returned after TTS from Polly.
    '''
    polly = get_polly_client()
    if text_type is None:
        text_type = Polly.text_type
    if output_format is None:
        output_format = Polly.output_format
    audio_file = polly.get_speech_file(text, voice_id, filename, text_type, output_format)
    return audio_file


def remove_audio_file(filepath):
    '''
    Description
    -----------
    Remove the audio file as per path specified.

    Arguments
    ---------
    filepath
    ====
    Type:: str
    Description:: Path to the file that is to be deleted.

    Return value
    ------------
    -
    '''
    polly = get_polly_client()
    polly.remove_speech_file(filepath)
