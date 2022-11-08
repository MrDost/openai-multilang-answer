import openai
import requests


YOUR_OPENAI_API_KEY = '<KEY>'
YOUR_IAM_TOKEN = '<TOKEN>'
YOUR_FOLDER_ID = '<ID>'


class Translate:
    IAM_TOKEN = YOUR_IAM_TOKEN
    FOLDER_ID = YOUR_FOLDER_ID

    def __init__(self, text_to_translate, language_to_translate):
        self.origin_text = text_to_translate
        self.target_language = language_to_translate
        self.origin_language = self.get_json()['translations'][0]['detectedLanguageCode']
        self.translated_text = self.get_json()['translations'][0]['text']

    def get_json(self):
        body = {
            "targetLanguageCode": self.target_language,
            "texts": self.origin_text,
            "folderId": self.FOLDER_ID,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.IAM_TOKEN)
        }
        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                 json=body, headers=headers)

        return response.json()


def openai_multilang(text):
    translated_input = Translate(text, 'en')

    """Your setup"""
    openai.api_key = YOUR_OPENAI_API_KEY
    response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt=translated_input.translated_text,
                    temperature=0.5,
                    max_tokens=60,
                    top_p=1,
                    frequency_penalty=0.5,
                    presence_penalty=0.0,
    )

    response_text = response['choices'][0]['text']
    translated_output = Translate(response_text, translated_input.origin_language)

    return translated_output.translated_text
