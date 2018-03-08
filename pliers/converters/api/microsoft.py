''' Microsoft Azure API-based Converter classes. '''

from pliers.converters.image import ImageToTextConverter
from pliers.stimuli.text import TextStim
from pliers.transformers import MicrosoftVisionAPITransformer


class MicrosoftAPITextConverter(MicrosoftVisionAPITransformer,
                                ImageToTextConverter):

    ''' Detects text within images using the Microsoft Vision API. '''

    api_method = 'ocr'
    _log_attributes = ('subscription_key', 'api_version', 'language')

    def __init__(self, language='en', subscription_key=None, location=None,
                 api_version='v1.0', rate_limit=None):
        self.language = language
        super(MicrosoftAPITextConverter,
              self).__init__(subscription_key=subscription_key,
                             location=location,
                             api_version=api_version,
                             rate_limit=rate_limit)

    def _convert(self, stim):
        params = {
            'language': self.language,
            'detectOrientation': False
        }
        response = self._query_api(stim, params)

        lines = []
        for r in response['regions']:
            for l in r['lines']:
                lines.append(' '.join([w['text'] for w in l['words']]))

        text = '\n'.join(lines)
        return TextStim(text=text)