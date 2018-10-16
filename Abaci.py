
# coding: utf-8

# In[4]:


class Abacus:
    BEAD = 'o'
    DOT = '*'
    
    def __init__(self, partition, k):
        self.partition = sorted(partition)
        self.n = sum(partition)
        self.k = k
        if self.n % self.k != 0:
            raise ValueError(str(k) + ' does not divide ' + str(self.n))
        
        self.abacus = [[] for i in range(k)]
        self.string = []
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
        ret = str(self.partition) + '\n'
        for string in self.abacus[::-1]:
            ret += '|-' + '-'.join(string) + '\n'
        return ret
        
    def string_count(self, string):
        branches = []
        for i in range(len(string) - 1):
            if string[i] == self.DOT and string[i+1] == self.BEAD:
                newstring = list(string)
                newstring[i] = self.BEAD
                newstring[i+1] = self.DOT
                branches.append(newstring)
                #print('ns',newstring)
        if branches == []:
            return 1
        return sum([self.string_count(branch) for branch in branches])
    
    def chi(self):
        product = 1
        for string in self.abacus:
            product *= self.string_count(string)
        return product
    
                
                
                

