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

# bead_labels_with_pass gives all possible bead labels along with their associated "pass
# numbers" and "position sequence". These correspond to rim hook tableaux.

    def bead_labels_with_pass(self,
                              abacus = None,
                              bead_labels = None,
                              move_number = None,
                              pass_numbers = None,
                              pos_sequence = None):

        if abacus is None:
            abacus = self.abacus
            bead_labels = [[[] for x in runner if x is self.BEAD] for runner in abacus]
            move_number, pass_numbers, pos_sequence = 0, [], []

        branches = []

        for runner in range(len(abacus)):
            for i in range(len(abacus[runner]) - 1):
                if abacus[runner][i] == self.DOT and abacus[runner][i+1] == self.BEAD:

                    new_pos_sequence = copy.deepcopy(pos_sequence)
                    new_pos_sequence.append(i * self.k + runner + 1)

                    new_pass_numbers = copy.deepcopy(pass_numbers)
                    if new_pass_numbers == []:
                        new_pass_numbers.append(1)
                    else:
                        if new_pos_sequence[-1] < pos_sequence[-1]:
                            new_pass_numbers.append(pass_numbers[-1])
                        else:
                            new_pass_numbers.append(pass_numbers[-1] + 1)

                    new_move_number = move_number + 1

                    new_bead_labels = copy.deepcopy(bead_labels)
                    new_bead_labels[runner][abacus[runner][:i].count(self.BEAD)].append(new_move_number)

                    new_abacus = copy.deepcopy(abacus)
                    new_abacus[runner][i] = self.BEAD
                    new_abacus[runner][i+1] = self.DOT

                    branches.append([new_abacus,
                                     new_bead_labels,
                                     new_move_number,
                                     new_pass_numbers,
                                     new_pos_sequence])

        if branches == []:
            return [([[[pass_numbers[i-1] for i in j] for j in row] for row in bead_labels[::-1]],
                     [max(self.partition) + len(self.partition) - a for a in pos_sequence])]

        return [i for a in [self.bead_labels_with_pass(*b) for b in branches] for i in a]

class Perm:
    def __init__(self, perm):
        self.perm = perm
        self.n = len(perm)
        self.maj = sum([i+1 for i in range(self.n - 1) if perm[i] > perm[i+1]])
        self.inv = sum([sum([perm[j] > i for i in perm[j:]]) for j in range(self.n)])

# The RSK algorithm

# Insert the integer j into P.  Returns new P and the insert row.
def row_insert(j, P=None, row=None):
    if P is None:
        return ([[j]], 0)
    if row is None:
        row = 0

    newP = copy.deepcopy(P)

    if row == len(P):
        newP.append([j])
        return (newP, row)

    if P[row][-1] <= j:
        newP[row].append(j)
        return (newP, row)

    a = len([n for n in P[row] if n <= j])
    newP[row][a] = j

    return row_insert(P[row][a], newP, row + 1)

# The RSK algorithm for a word of integers.
def RSK(word, P=None, Q=None, i=None):
    if i is None:
        i = 0
    if i == len(word):
        return (P,Q)

    newP, r = row_insert(word[i], P)
    if Q is None:
        newQ = [[1]]
    else:
        newQ = copy.deepcopy(Q)
        if r == len(newQ):
            newQ.append([i+1])
        else:
            newQ[r].append(i+1)

    return RSK(word, newP, newQ, i+1)

def major_index_tableau(Q):
    pairs = [i for a in [[(n, row) for n in Q[row]] for row in range(len(Q))] for i in a]
    maj = 0
    for (n,row) in pairs:
        next = [(j,r) for (j,r) in pairs if j == n+1]
        if next != [] and next[0][1] > row:
            maj += n
    return maj

# Examples below.

L = [1,2,3]
k = 1

for p in sorted(L): print("x"*p)
print()

A = Abacus(L,k)
print(A)

BWP = sorted([(Perm(s).maj, p, s) for (p,s) in A.bead_labels_with_pass()])
BWP = [(p,s) for (m,p,s) in BWP]

print("There are", len(BWP), "rim hook tableaux.")
print()

# Prints the major index of the position sequence (giving the q weight), the
# pass sequence, the position sequence, and the P and Q tableaux from RSK
# applied to the position sequence.

for p,s in BWP:
    print(Perm(s).maj, " ",
          p, " ",
          ''.join([str(n) for n in s]), " ",
          RSK(s)[0], " ",
          RSK(s)[1])
