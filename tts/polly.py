# Standard Library
import os
from contextlib import closing
from tempfile import gettempdir

# Third Party Stuff
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError


voice = {
    'Danish': {
        'Male': 'Mads',
        'Female': 'Naja',
    },
    'Dutch': {
        'Male': 'Ruben',
        'Female': 'Lotte',
    },
    'Australian English': {
        'Male': 'Russell',
        'Female': 'Nicole',
    },
    'British English': {
        'Male': 'Brian',
        'Female': 'Amy',
    },
    'Indian English': {
        'Male': None,
        'Female': 'Aditi',
    },
    'US English': {
        'Male': 'Joey',
        'Female': 'Ivy',
    },
    'Welsh English': {
        'Male': 'Geraint',
        'Female': None,
    },
    'French': {
        'Male': 'Mathieu',
        'Female': 'Celine',
    },
    'Canadian French': {
        'Male': None,
        'Female': 'Chantal',
    },
    'German': {
        'Male': 'Hans',
        'Female': 'Vicki',
    },
    'Icelandic': {
        'Male': 'Karl',
        'Female': 'Dora',
    },
    'Italian': {
        'Male': 'Giorgio',
        'Female': 'Carla',
    },
    'Japanese': {
        'Male': 'Takumi',
        'Female': 'Mizuki',
    },
    'Korean': {
        'Male': None,
        'Female': 'Seoyeon',
    },
    'Norwegian': {
        'Male': None,
        'Female': 'Liv',
    },
    'Polish': {
        'Male': 'Jan',
        'Female': 'Ewa',
    },
}


class Polly():
    """Amazon Polly class to support functionality of Text-To-Speech.
    Read here: http://docs.aws.amazon.com/polly/latest/dg/what-is.html

    Defaults
    --------
    Output Format: mp3
    Text type: text

    Available
    ----------
    Output Formats: json | mp3 | ogg_vorbis | pcm
    Text types: ssml | text
    """

    output_format = 'mp3'
    text_type = 'ssml'
    language = 'US English'
    gender = 'Female'

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        """Initialize Amazon Polly client with the provided credentials
        """
        self.session = Session(aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               region_name=region_name)
        self.client = self.session.client('polly')

    def _get_ssml_text(self, text):
        """Converts plain text to SSML text to keep requests consistent"""
        if not text.startswith('<speak>'):
            text = '{}{}{}'.format('<speak>', text, '</speak>')
        return text

    def _get_synthesized_speech(self, text, voice_id, text_type, output_format):
        """Get audio stream of the specified text using Amazon Polly,
        and return the audiostream itself, without saving it anywhere
        """
        text = self._get_ssml_text(text)
        try:
            # Request speech synthesis
            response = self.client.synthesize_speech(Text=text,
                                                     VoiceId=voice_id,
                                                     TextType=text_type,
                                                     OutputFormat=output_format)
            if 'AudioStream' in response:
                return response['AudioStream']
            raise ValueError('Audio cannot be streamed.')

        except (BotoCoreError, ClientError) as error:
            raise ValueError(error)

    def get_speech(self, text, voice_id, text_type, output_format):
        """Get synthesized speech and return its contents"""
        speech = self._get_synthesized_speech(text, voice_id, text_type, output_format).read()
        return speech

    def get_voice_by_language_and_gender(self, language, gender):
        voice_id = voice[language][gender]
        if voice_id is None:
            gender = 'Female' if gender is 'Male' else 'Male'
            voice_id = voice[language][gender]
        if voice_id is None:
            raise ValueError("No voice to convert text to.")
        return voice_id

    def get_speech_file(self, text, voice_id, filename, text_type, output_format):
        """Write audio stream to a file and return the path to the file"""
        response = self._get_synthesized_speech(text, voice_id, text_type, output_format)
        with closing(response) as stream:
            filename = '{}.{}'.format(filename, output_format)
            filepath = os.path.join(gettempdir(), filename)
            try:
                with open(filepath, "wb") as file:
                    file.write(stream.read())
                return filepath
            except IOError as error:
                raise ValueError(error)

    def remove_speech_file(self, filepath):
        if os.path.exists(filepath) and os.path.isfile(filepath):
            os.remove(filepath)
