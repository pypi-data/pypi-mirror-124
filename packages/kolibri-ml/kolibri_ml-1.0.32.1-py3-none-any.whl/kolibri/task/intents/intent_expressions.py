import regex as re
from kolibri.preprocess.text.cleaning.cleaning_scripts import fix_formating
from kolibri.tokenizers import SentenceTokenizer
from kolibri.task.intents import intent_patterns

tokenize=SentenceTokenizer({'multi-line':False})

def get_match(regexes, test_str):
    if test_str is None:
        return None
    intent_analysis={}
    details_intent = {}

    for regex in regexes:
        dict_name=regex.groupindex

        matches = re.finditer(regex, test_str)


        intent_analysis = {}

        for counter,match in enumerate(matches):
            for i in dict_name:
                details_intent[i] = match.group(dict_name[i])


            intent_analysis['full intent'] = test_str
            intent_analysis['details'] = details_intent

            return intent_analysis

    return intent_analysis


def _get_intent(patterns_, sentence):
    if len(patterns_) > 0:
        pattern=next(iter(patterns_))
        intent = get_match(patterns_[pattern], sentence)
        if intent:
            intent['pattern']=pattern
            return intent
        else:
            return _get_intent({k: v  for k, v in list(patterns_.items())[1:]}, sentence)

def get_intent_expression(text, language):
    return __get_intent_expression(text, intent_patterns[language])


def __get_intent_expression(text, regexes):

    sentences=tokenize.tokenize(fix_formating(text))

    core_intent=[]

    for sent in sentences:

        intent=_get_intent(regexes, sent)


        if intent:
            intent["sentence"] = sent

            core_intent.append(intent)

    return core_intent

