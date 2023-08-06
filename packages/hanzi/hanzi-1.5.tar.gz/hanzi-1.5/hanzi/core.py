import json
import pkg_resources


class Hanzi(object):
    def __init__(self):
        file_name = pkg_resources.resource_filename(__name__,"data/")
        self.bujian_data = json.load(open(file_name+"bujian_data.json", "r", encoding="utf-8"))
        self.pinyin_data = json.load(open(file_name+"pinyin_data.json", "r", encoding="utf-8"))
        self.bihua_data = json.load(open(file_name+"bihua_data.json", "r", encoding="utf-8"))

    def get_bujian(self, input_char):
        if input_char in self.bujian_data:
            bujian = self.bujian_data[input_char]

            return bujian
        else:

            return None

    def get_pinyin(self, input_char):
        if input_char in self.pinyin_data:
            pinyin = self.pinyin_data[input_char]

            return pinyin
        else:

            return None

    def get_bihua(self, input_char):
        if input_char in self.bihua_data:
            bihua = self.bihua_data[input_char]

            return bihua
        else:

            return None

    def get_full_information(self, input_char):
        bujian, pinyin, bihua = self.get_bujian(input_char), self.get_pinyin(input_char), self.get_bihua(input_char)

        return {"部件": bujian, "拼音": pinyin, "笔画": bihua}
