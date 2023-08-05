import re
import emoji
import string


class StringFormatter:

    def replace_url(self, text, value=''):
        return re.sub(r'https?://\S+|www\.\S+', value, text)

    def replace_html(self, text, value=''):
        return re.sub(r'(</?\w*\s*/?>)', value, text)

    def replace_emoji(self, text, value=''):
        return ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)

    def replace_flag(self, text, value=''):
        return re.sub(u'[\U0001F1E6-\U0001F1FF]', value, text) 

    def replace_username_twitter(self, text, value=''):
        return re.sub(r'@[a-zA-Z0-9_]+', value,  text)

    def replace_hashtag_twitter(self, text, value=''):
        return re.sub(r'#[a-zA-Z0-9_]+', value, text)

    def remove_punctuation(self, text):
        return text.translate(str.maketrans('', '', string.punctuation))
