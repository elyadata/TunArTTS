class DerjaNinjaConstants:
    DERJA_NINJA_LINK = ["https://derja.ninja/search?search=", "&script=arabic"]
    RESULT_ELEMENT_CLASS_VALUE = "search-result__row"
    AUDIO_ELEMENT_TAG = "audio"
    AUDIO_ELEMENT_ATTRIBUTE = "src"
    TERM_CLASS_VALUE = "search-result__term_in_arabic"
    SENTENCE_CLASS_VALUE = "search_result__example_sentence_in_arabic"
    EXAMPLE_SENTENCE_CLASS_VALUE = "example-sentence"
    JS_SCRIPT_TAG = "script"
    JS_SCRIPT_ATTRIBUTE = "innerHTML"
    TERM = "term"
    SENTENCE = "sentence"
    START_TIME = "start"
    END_TIME = "end"


class DrejjaToEnglishDatasetConstants:
    METADATA_FILE = "tunsi_english_data.csv"
    TUNISIAN_SENTENCES_COLUMN_NAME = "tn"


class ScrappedDatasetConstants:
    TEXT_FILE_NAME = "scrapped_tunisian_dataset.txt"
    TEXT_FILE_SEP = "|"
    COLUMN_NAMES = ["audio", "term", "sentence", "term_start", "term_end", "sen_start", "sen_end"]
    TERM_START_TIME = "term_start"
    TERM_END_TIME = "term_end"
    SENTENCE_START_TIME = "sen_start"
    SENTENCE_END_TIME = "sen_end"


class MetaDataConstants:
    SPEAKER = "SP1"
    AUDIO_PATH_COLUMN_NAME = "audio"
    DURATION_COLUMN_NAME = "duration"
    SEGMENT_ID_COLUMN_NAME = "id"
    SAMPLE_RATE_COLUMN_NAME = "sample_rate"
    TARGET_TEXT_COLUMN_NAME = "tgt_text"
    SPEAKER_COLUMN_NAME = "speaker"
    FILE_SEPARATOR = '\t'
    TEST_TSV_FILENAME = "test.tsv"
    VALIDATION_TSV_FILENAME = "dev.tsv"
    TRAIN_TSV_FILENAME = "train.tsv"
    TSV_FILE_NAME_AR = "complete_text_dataset.tsv"
    TERM_COLUMN_NAME = "term"
    SENTENCE_COLUMN_NAME = "sentence"
    TSV_FILE_NAME_BW = "complete_text_dataset_buckwalter.tsv"
    TSV_FILE_NAME_WITH_DIACRITICS = "complete_text_with_diac_dataset.tsv"
    TSV_FILE_NAME_PHN = "complete_text_dataset_phonemes.tsv"
    CHAR_TO_REPLACE = {'.': '', ',': '', '+': '', '،': '',
                       '-': '', '!': '', '?': '', '\\': '', '%': ''}

class AudioConstants:
    SAMPLE_RATE = 44100
    THRESHOLD_IN_DB = 45


class TunisianDatasetConstants:
    TEST_TOTAL_DURATION = 420
    VALIDATION_TOTAL_DURATION = 600
    LIST_OF_AUDIOS_TO_REMOVE = [21319, 700, 15806, 709, 19527, 14915, 19478, 14917, 403, 368, 15936, 18450, 349, 343,
                                19434, 19491, 517, 390, 391, 14555, 15806, 19431, 635, 19130, 14996, 15691, 14555,
                                14824, 9, 56, 10, 19405, 24, 17447, 15039, 55, 54, 11, 26, 15038]
    LIST_OF_AUDIOS_TO_KEEP = [range(1, 816), range(14502, 20757), range(20913, 21746)]
    TERM_SEN_SEN_TEXT = [1, 3, 13, 14, 15, 17, 18, 19, 21, 22, 24, 32, 33, 35, 38, 41, 42, 43, 45, 46, 47, 48, 49, 50,
                         51, 52, 54, 55, 56, 58, 60, 61, 62, 63, 65, 68, 69, 70, 71, 72, 77, 78, 79, 80, 290, 298, 296]
    TERM_TERM_SEN_SEN_TEXT = [5, 288, 289, 293, 338, 489, 15638, 18136, 18392, 19888, 19889, 20120, 20547]
    TERM_TERM_TERM_TEXT = 584
    SEN_SEN_TEXT = 467
    TERM_TERM_TERM_SEN_SEN_SEN_TEXT = [18244, 19584]


class BuckwalterMapping:
    BUCKWALTER = {
        u'\u0628': u'b', u'\u0630': u'*', u'\u0637': u'T', u'\u0645': u'm',
        u'\u062a': u't', u'\u0631': u'r', u'\u0638': u'Z', u'\u0646': u'n',
        u'\u062b': u'^', u'\u0632': u'z', u'\u0639': u'E', u'\u0647': u'h',
        u'\u062c': u'j', u'\u0633': u's', u'\u063a': u'g', u'\u062d': u'H',
        u'\u0642': u'q', u'\u0641': u'f', u'\u062e': u'x', u'\u0635': u'S',
        u'\u0634': u'$', u'\u062f': u'd', u'\u0636': u'D', u'\u0643': u'k',
        u'\u0623': u'>', u'\u0621': u'\'', u'\u0626': u'}', u'\u0624': u'&',
        u'\u0625': u'<', u'\u0622': u'|', u'\u0627': u'A', u'\u0649': u'Y',
        u'\u0629': u'p', u'\u064a': u'y', u'\u0644': u'l', u'\u0648': u'w',
        u'\u064b': u'F', u'\u064c': u'N', u'\u064d': u'K', u'\u064e': u'a',
        u'\u064f': u'u', u'\u0650': u'i', u'\u0651': u'~', u'\u0652': u'o'
    }
