import json

class MagicDeck:
    def __init__(self, name, format, path, importDeck=False):
        if not importDeck:
            self._new_deck(name, format, path)
        else:
            self._import_deck(name, format, path)

    def _new_deck(self, name, format, path):
        self.deckDict = {
            "name" : name,
            "format" : format,
            "zones" : {
                "maindeck": {},
                "ideasdeck": {}
            }
        }
        if format == "commander" :
            self.deckDict["commander"] = ""

        self.save_deck(path)

    def _import_deck(self, name, format, path):
        with open(path) as jsonFile:
            self.deckDict = json.load(jsonFile)
            self.deckDict["name"] = name
            if self.deckDict['format'] != format:
                raise ValueError("Expected import deck", format, "got", self.deckDict['format'])

    def save_deck(self, path):
        with open(path, 'w') as outfile:
            json.dump(self.deckDict, outfile)

    def get_quantity(self, cardname, zone):
        if cardname in self.deckDict["zones"][zone].keys():
            return self.deckDict["zones"][zone][cardname]
        else:
            return 0

    def add_card(self, cardname, zone, quantity=1):
        if cardname in self.deckDict["zones"][zone].keys():
            self.deckDict["zones"][zone][cardname] += quantity
        else:
            self.deckDict["zones"][zone][cardname] = quantity

    def remove_card(self, cardname, zone):
        if cardname in self.deckDict["zones"][zone].keys():
            self.deckDict["zones"][zone][cardname] -= 1
        else:
            raise ValueError("No card", cardname, "found in", zone)

    def remove_card_all_copies(self, cardname, zone):
        if cardname in self.deckDict["zones"][zone].keys():
            nCopies = self.deckDict["zones"][zone][cardname]
            del self.deckDict["zones"][zone][cardname]
            return nCopies
        else:
            raise ValueError("No card", cardname, "found in", zone)

    def move_card(self, cardname, zoneOld, zoneNew):
        self.remove_card(cardname, zoneOld)
        self.add_card(cardname, zoneNew)

    def move_card_all_copies(self, cardname, zoneOld, zoneNew):
        nCopies = self.remove_card_all_copies(cardname, zoneOld)
        self.add_card(self, cardname, zoneNew, quantity=nCopies)

