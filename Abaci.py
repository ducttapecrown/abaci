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

# chi_with_labels should give all possible edge labelings that we were looking at in my
# office on Tuesday, October 16.
#
# Each element in chi_with_labels gives a labeling of the edges between places on the
# abacus which indicate the order of the moved beads.  From these orders we can construct
# the associated rim hook tableaux.
#
# See below for an example of its use.  Maybe we can associate the labeling, along with
# the powers of q coming from the hook length numbers, to create a permutation of n?

    def chi_with_labels(self, abacus=None, edge_labels=None, move_number=None):
        if abacus is None:
            abacus = self.abacus
            edge_labels = [[[] for x in runner[1:]] for runner in abacus]
            move_number = 0

        branches = []
        
        for runner in range(len(abacus)):
            for i in range(len(abacus[runner]) - 1):
                if abacus[runner][i] == self.DOT and abacus[runner][i+1] == self.BEAD:

                    new_move_number = copy.deepcopy(move_number)
                    new_move_number += 1

                    new_labels = copy.deepcopy(edge_labels)
                    new_labels[runner][i].append(new_move_number)

                    new_abacus = copy.deepcopy(abacus)
                    new_abacus[runner][i] = self.BEAD
                    new_abacus[runner][i+1] = self.DOT

                    branches.append([new_abacus, new_labels, new_move_number])

        if branches == []:
            return [edge_labels]
        
        return [i for a in [self.chi_with_labels(*b) for b in branches] for i in a]

# An example showing chi_with_labels

A = Abacus([2,3,3,4],2)
print(A)

for edge_labels in A.chi_with_labels():
    for runner in edge_labels[::-1]:
        print(runner)
    print()

print(A.chi() == len(A.chi_with_labels()))
