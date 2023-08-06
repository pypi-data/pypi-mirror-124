import re
import csv
import json
from pathlib import Path


class Moe:
    initials = {
      'bpm': 'ㄅㄆㄇㄈㄉㄊㄗㄘㄙㄋㄌㄓㄔㄕㄖㄐㄑㄒㄍㄎㄏ',
      'pinyin': 'b p m f d t z c s n l zh ch sh r j q x g k h',
      'ipa': 'p pʰ m f t tʰ ts tsʰ s n l ʈʂ ʈʂʰ ʂ ʐ tɕ tɕʰ ɕ k kʰ x'.split()
    }

    def __init__(self, lexicon:set=None) -> None:
        self._load()
        if lexicon:
            for w in set(self.data.keys()).difference(lexicon):
                del self.data[w]

        # Reverse index
        self.phon = { 'bpm': {}, 'pinyin': {}, 'ipa': {}, 'tone': {} }
        for w, vs in self.data.items():
            for v in vs:
                bpm, pinyin, ipa, tone = v['bpm'], v['pinyin'], v['ipa'], v['tone']
                self.phon['bpm'].setdefault(bpm, set()).add(w)
                self.phon['pinyin'].setdefault(pinyin, set()).add(w)
                self.phon['ipa'].setdefault(ipa, set()).add(w)
                self.phon['tone'].setdefault(tone, set()).add(w)
        
    
    def find(self, repr:str, tone=None, tp="bpm", exact=False):
        """Find hanzi from a phonetic representation
        """
        if not exact:
            pat = re.compile(repr)
            out = set()
            for k in self.phon[tp]:
                if pat.search(k):
                    out.update(self.phon[tp][k])
        else:
            out = self.phon[tp].get(repr, set())
        if tone:
            t = str(tone)
            return out.intersection(self.phon['tone'][t])
        return out


    def query(self, char:str):
        """Query a hanzi for its phonetic representations
        """
        return self.data.get(char)


    def decompose(self, repr:str, tp="bpm"):
        """Decompose a phonetic representation into an intital and a rhyme
        """
        init = ''
        for i, c in enumerate(repr):
            init += c
            if init not in self.initials[tp]:
                init = init[:-1]
                break
        return init, repr[i:]


    def _load(self):
        data_dir = Path(__file__).parent / "data"
        # Load hanzi data
        with open(data_dir / "moe_char_phon.json", encoding="utf-8") as f:
            self.data = json.load(f)

        # Load bpm/pinyin/ipa transciption data
        self.trans = {
            'ipa_bmp': {},
            'pinyin_bpm': {}
        }
        with open(data_dir / "moe_transcriptions.csv", encoding="utf-8", newline='') as f:
            for r in csv.DictReader(f):
                bpm, pinyin, ipa = r['Zhuyin'], r['Pinyin'], r['IPA']
                self.trans['ipa_bmp'][ipa] = bpm
                self.trans['pinyin_bpm'][pinyin] = bpm
            
            Bs, Is, Ps = self.initials['bpm'], self.initials['ipa'], self.initials['pinyin']
            for bpm, pinyin, ipa in zip(Bs, Ps, Is):
                self.trans['ipa_bmp'][ipa] = bpm
                self.trans['pinyin_bpm'][pinyin] = bpm
