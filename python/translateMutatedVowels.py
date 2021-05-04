mappingMutatedVowels = {
    ord(u"ä"): u"ae",
    ord(u"Ä"): u"Ae",
    ord(u"ö"): u"oe",
    ord(u"Ö"): u"Oe",
    ord(u"ü"): u"ue",
    ord(u"Ü"): u"Ue",
    ord(u"ß"): u"ss"}
greetings = "Hällo HÄllo mÜde müde Öhrchen öhrchen"
print(greetings.translate(mappingMutatedVowels))
result = {'exceptions': greetings}
print(('Exception: %s' % (result['exceptions'])).translate(mappingMutatedVowels))
