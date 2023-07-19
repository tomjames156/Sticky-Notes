import re

special_chars = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '*': '\*',
    '$': '\$',
    '?': '\?',
    '+': '\+',
    '.': '\.',
    '^': '\^',
    '(': '\(',
    ')': '\)',
    '[': '\[',
    ']': '\]',
    '|': '\|',
    '{': '\{',
    '}': '\}',
    '\\': '\\',
    ' ': '\s'
}

def create_regex_pattern(search_query):
    pattern = ''
    words = search_query.split()
    if(len(words) == 0):
        return None
    elif(len(words) == 1):
        word  = words[0]
        pattern += f"[^</>]((<\w+>)*"
        for character in word:
            if character in special_chars:
                character = special_chars[character]
            pattern += f"{character}(</?\w+>|&\w+;)*"
        pattern += f")"
    elif(len(words) > 1):
        for index, word in enumerate(words):
            if(index == 0):
                pattern += f"((</?\w+>|&\w+;)*"
                for character in word:
                    if character in special_chars:
                        character = special_chars[character]
                    pattern += f"{character}(</?\w+>|&\w+;)*"
            elif(index > 0):
                pattern += "\s*(</?\w+>|&\w+;)*\s*"
                for character in word:
                    if character in special_chars:
                        character = special_chars[character]
                    pattern += f"{character}(</?\w+>|&\w+;)*"

        pattern += ")"

    return pattern

def find_matches(search_query, text):
    text = text[3:]
    pattern = ''
    words = search_query.split()
    if(len(words) == 0):
        return text
    elif(len(words) == 1):
        word  = words[0]
        pattern += f"((<\w+>)*"
        for character in word:
            if character in special_chars:
                character = special_chars[character]
            pattern += f"{character}(</?\w+>|&\w+;)*"
        pattern += f")"
    elif(len(words) > 1):
        for index, word in enumerate(words):
            if(index == 0):
                pattern += f"((</?\w+>|&\w+;)*"
                for character in word:
                    if character in special_chars:
                        character = special_chars[character]
                    pattern += f"{character}(</?\w+>|&\w+;)*"
            elif(index > 0):
                pattern += "\s*(</?\w+>|&\w+;)*\s*"
                for character in word:
                    if character in special_chars:
                        character = special_chars[character]
                    pattern += f"{character}(</?\w+>|&\w+;)*"

        pattern += ")"

    searchRegex = re.compile(pattern, re.I)
    return searchRegex.sub(r"<span class='highlight'>\1</span>", text ), searchRegex.findall(text)

def remove_wrong_highlight(text):
    removed = []
    wrongHighlightRegexHTMLTags = re.compile(r"(</?\w*)<span class='highlight'>(\w)</span>(\w*>)")

    wrongHighlightRegexHTMLTags2 = re.compile(r"(</?)<span class='highlight'>(\w+)</span>(>)")

    # wrongly highlighted the alphabetic characters of a html entity
    wrongHighlightRegexHTMLEntities = re.compile(r"(&\w*)<span class='highlight'>(\w*)</span>(\w*;)")

    # wrongly highlighted the "&" of a html entity
    wrongHighlightRegexHTMLEntities2 = re.compile(r"<span class='highlight'>(&)</span>(\w*)(;)")

    # wrongly highlighted the ";" of a html entity
    wrongHighlightRegexHTMLEntities3 = re.compile(r"(&)(\w*)<span class='highlight'>(;)</span>")

    doubleHightRegex = re.compile(r"((</?span(\sclass='highlight')?>)(</?span(\sclass='highlight')?>))")

    strongTagsRegex = re.compile(r"(</?\w*)<span class='highlight'>(\w*)</span>(\w*>)")

    removed += wrongHighlightRegexHTMLTags.findall(text)
    fixedHTMLTags = wrongHighlightRegexHTMLTags.sub(r"\1\2\3", text)
    removed += wrongHighlightRegexHTMLTags2.findall(fixedHTMLTags)
    fixedHTMLTags2 = wrongHighlightRegexHTMLTags2.sub(r"\1\2\3", fixedHTMLTags)
    removed += wrongHighlightRegexHTMLEntities.findall(fixedHTMLTags2)
    fixedHTMLEntities = wrongHighlightRegexHTMLEntities.sub(r"\1\2\3", fixedHTMLTags2)
    removed += wrongHighlightRegexHTMLEntities2.findall(fixedHTMLEntities)
    fixedHTMLEntities2 = wrongHighlightRegexHTMLEntities2.sub(r"\1\2\3", fixedHTMLEntities)
    removed += wrongHighlightRegexHTMLEntities3.findall(fixedHTMLEntities2)
    fixedHTMLEntities3 = wrongHighlightRegexHTMLEntities3.sub(r"\1\2\3", fixedHTMLEntities2)
    fixedDoubleHighlight = doubleHightRegex.sub(r"\2", fixedHTMLEntities3)
    fixedStrongTags = strongTagsRegex.sub(r"\1\2\3", fixedDoubleHighlight)

    result = "<p>" + fixedStrongTags

    return result, removed

def is_search_result(text):
    """Checks if a search result was found by checking for span text"""
    spanRegex = re.compile(r"<span class='highlight'>.*?</span>")

    if spanRegex.findall(text) == []:
        return False
    else:
        return True

def search_note(search_query, text):
    search_result = find_matches(search_query, text)
    formatted_result = remove_wrong_highlight(search_result[0])

    return formatted_result[0]