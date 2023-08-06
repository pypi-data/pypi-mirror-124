class BWT(object):
    def __init__(self, text):
        t = text + "$"
        self.position_list = [ i for i in range(len(t)) ]
        self.position_list = sorted(self.position_list, key = lambda s: t[s:])
        self.bwt = "".join( [ t[i-1] for i in self.position_list ] )
        self.ranks = {}
        self.cnums = {}
        for c in self.bwt:
            if not c in self.cnums.keys():
                self.cnums[c] = 0
                self.ranks[c] = []
        for c in self.bwt:
            self.cnums[c] = self.cnums[c] + 1
            for e in self.ranks.keys():
                self.ranks[e].append(self.cnums[e] - 1)
    def search(self, pattern):
        if len(pattern) >= len(self.bwt):
            return []
        i = len(pattern) - 1
        c = pattern[i]
        if not c in self.cnums.keys():
            return []
        first = 0
        for e in self.cnums.keys():
            if e < c:
                first = first + self.cnums[e]
        last = first + self.cnums[c] -1
        while not first > last:
            if i == 0:
                return sorted(self.position_list[first:last+1])
            i = i - 1
            c = pattern[i]
            if not c in self.cnums.keys():
                return []
            first = self.ranks[c][first - 1] + 1
            last = self.ranks[c][last]
            for e in self.cnums.keys():
                if e < c:
                    first = first + self.cnums[e]
                    last = last + self.cnums[e]
        return []
    def get_text(self):
        return "".join([ e[1] for e in sorted( zip(self.position_list, self.bwt) ) ])[1:]
    def from_fasta_file(filename):
        text = ""
        first_line = True
        with open(filename, "r") as f:
            for line in f:
                if first_line:
                    seq_name = line.strip()
                    first_line = False
                else:
                    text = text + line.strip().upper()
        return BWT(text)

if __name__ == "__main__":
    text = "AGATA"
    pattern = "AT"
    bwt = BWT(text)
    print("Burrows Wheeler transform", bwt.bwt)
    print("search found", pattern)
    print("at", bwt.search(pattern))
    print("in", bwt.get_text())
    print("and A at", bwt.search("A"))
    
