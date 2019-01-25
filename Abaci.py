import copy

class Abacus:
    BEAD, DOT = "O", "⋆"

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
        ret = ''
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

    def chi_with_labels(self, abacus=None, edge_labels=None, move_number=None):
        if abacus is None:
            abacus = self.abacus
            edge_labels = [[[] for x in runner[1:]] for runner in abacus]
            move_number = 0

        branches = []

        for runner in range(len(abacus)):
            for i in range(len(abacus[runner]) - 1):
                if abacus[runner][i] == self.DOT and abacus[runner][i+1] == self.BEAD:

                    new_move_number = move_number + 1

                    new_labels = copy.deepcopy(edge_labels)
                    new_labels[runner][i].append(new_move_number)

                    new_abacus = copy.deepcopy(abacus)
                    new_abacus[runner][i] = self.BEAD
                    new_abacus[runner][i+1] = self.DOT

                    branches.append([new_abacus, new_labels, new_move_number])

        if branches == []:
            return [edge_labels]

        return [i for a in [self.chi_with_labels(*b) for b in branches] for i in a]

# bead_labels_with_pass gives all possible bead labels along with their associated "pass
# numbers".  These correspond to rim hook tableaux.

    def bead_labels_with_pass(self, abacus=None, bead_labels=None, move_number=None, pass_numbers=None, last_move=None):
        if abacus is None:
            abacus = self.abacus
            bead_labels = [[[] for x in runner if x is self.BEAD] for runner in abacus]
            move_number, pass_numbers, last_move = 0, [], [0,0]

        branches = []

        for runner in range(len(abacus)):
            for i in range(len(abacus[runner]) - 1):
                if abacus[runner][i] == self.DOT and abacus[runner][i+1] == self.BEAD:

                    new_last_move = copy.deepcopy(last_move)
                    new_last_move = [runner,i]

                    new_pass_numbers = copy.deepcopy(pass_numbers)
                    if new_pass_numbers == []:
                        new_pass_numbers.append(1)
                    else:
                        if i * self.k + runner < last_move[1] * self.k + last_move[0]:
                            new_pass_numbers.append(pass_numbers[-1])
                        else:
                            new_pass_numbers.append(pass_numbers[-1] + 1)

                    new_move_number = move_number + 1

                    new_bead_labels = copy.deepcopy(bead_labels)
                    new_bead_labels[runner][abacus[runner][:i].count(self.BEAD)].append(new_move_number)

                    new_abacus = copy.deepcopy(abacus)
                    new_abacus[runner][i] = self.BEAD
                    new_abacus[runner][i+1] = self.DOT

                    branches.append([new_abacus, new_bead_labels, new_move_number, new_pass_numbers, new_last_move])

        if branches == []:
            return [(bead_labels, pass_numbers)]

        return [i for a in [self.bead_labels_with_pass(*b) for b in branches] for i in a]

L = [2,3]
k = 1

for p in sorted(L): print("x"*p)
print()

A = Abacus(L,k)
print(A)

BWP = A.bead_labels_with_pass()

print("There are", len(BWP), "rim hook tableaux.")

for s, p, a in sorted([[sum(p),p,a] for [a,p] in BWP]):
    for row in a[::-1]:
        print('-'.join([''.join([str(p[i-1]) for i in j]) for j in row]))
    print("with sum", sum(p), "\n")
