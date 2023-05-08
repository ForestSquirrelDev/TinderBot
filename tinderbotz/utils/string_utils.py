from typing import Optional, List
import re

def string_contains_word_from_list_case_insensitive(severely_unwanted_words: list, string: str) -> (bool, str):
    string = str.lower(string)
    word = find_substring_from_array(string, severely_unwanted_words)
    if word is None:
        return (False, None)
    else:
        return (True, word)

def find_substring_from_array(string_to_search_in: str, search_array_strings: List[str]) -> Optional[str]:
    for search_word in search_array_strings:
        contains_searched_word = string_to_search_in.find(search_word) != -1
        if contains_searched_word:
            return search_word
    return None

def contains(string: str, substring: str) -> bool:
    return string.find(substring) != -1

def remove_emojis(data: str) -> str:
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)