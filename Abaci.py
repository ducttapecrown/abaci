class Abacus:
    BEAD, DOT = "⚫", "·"
    
    def __init__(self, partition, k):
        self.partition = sorted(partition)
        self.n = sum(partition)
        self.k = k
        
        self.abacus = [[] for i in range(k)]
        dots, part, index = 0, 0, 0
        while part < len(self.partition):
            if dots < self.partition[part]:
                self.abacus[index % k].append(self.DOT)
                dots += 1
            elif dots == self.partition[part]:
                self.abacus[index % k].append(self.BEAD)
                part += 1
            index += 1
            
    def __repr__(self):
        return str(self.partition) + " divided by " + str(self.k) + "\n" + str(self.abacus)
    
    def __str__(self):
        ret = str(self.partition) + '\n\n'
        for string in self.abacus[::-1]:
            ret += '├' + '–'.join(string) + '\n'
        return ret

# The code below does not give the correct value of chi.  See, for example,
#
# Abacus([2,3,4],3).chi()
#
# The error comes in because the bead removal process is not runner independent.

    def string_count(self, string):
        branches = []
        for i in range(len(string) - 1):
            if string[i] == self.DOT and string[i+1] == self.BEAD:
                newstring = list(string)
                newstring[i] = self.BEAD
                newstring[i+1] = self.DOT
                branches.append(newstring)
        if branches == []:
            return 1
        return sum([self.string_count(branch) for branch in branches])
    
    def chi(self):
        product = 1
        for string in self.abacus:
            product *= self.string_count(string)
        return product
