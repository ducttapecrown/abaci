import copy

class Abacus:
    BEAD, DOT = "o", "*"
    
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
        for runner in self.abacus[::-1]:
            ret += '|-' + '-'.join(runner) + '\n'
        return ret

# The code below does not give the correct value of chi.  See, for example,
#
# Abacus([2,3,4],3).chi()
#
# The error comes in because the bead removal process is not runner independent.

# OLD CODE for a single runner
    def runner_count(self, runner):
        branches = []
        for i in range(len(runner) - 1):
            if runner[i] == self.DOT and runner[i+1] == self.BEAD:
                newrunner = list(runner)
                newrunner[i] = self.BEAD
                newrunner[i+1] = self.DOT
                branches.append(newrunner)
        if branches == []:
            return 1
        return sum([self.runner_count(branch) for branch in branches])

    def chi(self, abacus=None):
        if abacus is None:
            abacus = self.abacus
        branches = []
        for runner in range(len(abacus)):
            for i in range(len(abacus[runner]) - 1):
                if abacus[runner][i] == self.DOT and abacus[runner][i+1] == self.BEAD:
                    newabacus = copy.deepcopy(abacus)
                    newabacus[runner][i] = self.BEAD
                    newabacus[runner][i+1] = self.DOT
                    branches.append(newabacus)
            if branches == []:
                return 1
        return sum([self.chi(branch) for branch in branches])
