from nlp_cleaner.string_formatter import StringFormatter


class NlpCleaner:

    def __init__(self):
        self.string_formatter = StringFormatter()

    def remove_all_twitter(self, text: str) -> str:
        print(text)
        new_text = self.string_formatter.replace_html(text)
        print(new_text)
        new_text = self.string_formatter.replace_url(new_text)
        print(new_text)
        new_text = self.string_formatter.replace_username_twitter(new_text)
        print(new_text)
        new_text = self.string_formatter.replace_emoji(new_text)
        print(new_text)
        new_text = self.string_formatter.replace_flag(new_text)
        print(new_text)
        new_text = self.string_formatter.replace_hashtag_twitter(new_text)
        print(new_text)
        return self.string_formatter.remove_punctuation(new_text)