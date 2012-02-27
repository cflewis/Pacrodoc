import sys
import json
import re
import urllib

acronyms = {}

def processAcronym(linkData):
    # Links look like this:
    # [[{u'Str': u'Link Name'}], [u'Link URL', 'Link Title']]
    acronym = linkData[0][0]['Str']
    acronymText = linkData[1][0]

    # First we check if there is an acronym being defined
    if re.search('^acro:', linkData[1][0]):
        # An acronym is being defined, so strip off the acro:
        # prefix and unencode the text
        acronyms[acronym] = {'text': urllib.unquote(acronymText[5:]), 'used': False}

        # Strip out this link
        return {'Str': ''}

    # Now we check if its referring to an acronym instead
    if not acronymText and acronym in acronyms:
        if not acronyms[acronym]['used']:
            acronyms[acronym]['used'] = True
            return {'Str': '%s (%s)' % (acronyms[acronym]['text'], acronym)}
        else:
            return {'Str': acronym}

    # It was just a normal link, so return it unchanged
    return {'Link': linkData}

def lookForAcronyms(jsonData):
    if isinstance(jsonData, list):
        return [lookForAcronyms(value) for value in jsonData]

    if isinstance(jsonData, dict):
        if 'Link' in jsonData:
            return processAcronym(jsonData['Link'])
        else:
            return {k: lookForAcronyms(v) for k, v in jsonData.items()}

    return jsonData

print json.dumps(lookForAcronyms(json.loads(sys.stdin.read())))
