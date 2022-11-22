import re
from googletrans import Translator
import cyrtranslit


class Translate:

    def __init__(self, source_lang='auto', result_lang='en'):
        self.translator = Translator()
        self.source_lang = source_lang
        self.result_lang = result_lang

    def get_translate(self, string):
        # remove redundant symbols from rus string
        del_additional_symbol = re.sub(r"[/.,():-]", " ", fr"{string}")
        # del '/n' if type_from_doc written in two lines
        string_after_del_line_break = del_additional_symbol.replace('\n', ' ')
        # del all other mysterious control symbols...
        string_after_del_line_break = string_after_del_line_break.split()
        string_after_del_line_break = " ".join(string_after_del_line_break)
        # get string eng words after translate
        list_translate_words = self.translator.translate(string_after_del_line_break,
                                                         src=self.source_lang, dest=self.result_lang)
        # get list from eng words
        new_list_from_individual_words = list_translate_words.text.split(' ')
        # deleting invisible command symbol
        temp_list = []
        temp_word = []
        # break the word to single letter list, check this if letter or not, add all which letter in word
        for item in new_list_from_individual_words:
            foo = list(item)
            for i in foo:
                if i in {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                         'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', }:
                    temp_word.append(i)
                # if word was not translated - change literal to eng, instead get empty word
                elif i in {'А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё', 'Ж', 'ж', 'З', 'з',
                           'И', 'и', 'Й', 'й', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о', 'П', 'п', 'Р', 'р',
                           'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф', 'Х', 'х', 'Ц', 'ц', 'Ч', 'ч', 'Ш', 'ш', 'Щ', 'щ',
                           'Ъ', 'ъ', 'Ы', 'ы',	'Ь', 'ь', 'Э', 'э', 'Ю', 'ю', 'Я', 'я'}:
                    # en_literal = translit(i, language_code='ru', reversed=True)
                    en_literal = cyrtranslit.to_latin(i, 'ru')
                    temp_word.append(en_literal)

            word = ''.join(temp_word)
            temp_list.append(word)
            temp_word = []

        # unite through "_" in one word
        result = "_".join(temp_list)
        return result
