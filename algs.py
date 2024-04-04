class WeightedQuickUnionUF:
    def __init__(self, N):
        self.ids = [i for i in range(N)]
        self.szs = [1 for i in range(N)]
    
    def root(self, i: int) -> int: 
        while i != self.ids[i]:# while the current element isn't the root 
            self.ids[i] = self.ids[self.ids[i]] # shortening the process to the root by jumping to grandparent
            i = self.ids[i] # making i the grandparent and checking if process needs to keep happening
        return i # return the root
    
    def union(self, p: int, q: int):
        proot = self.root(p)
        qroot = self.root(q)
        if proot == qroot: # if same root then quit
            return
        if self.szs[proot] < self.szs[qroot]: # check if p root tree is bigger 
            self.ids[proot] = qroot # if it is then chenge p root to q root to join p and q trees
            self.szs[qroot] += self.szs[proot] # add size of p root to size of q root
        else:# if p root tree is bigger than q root tree
            self.ids[qroot] = proot # change q root to p root to join
            self.szs[proot] += self.szs[qroot] # add q root tree size to p root 
            
    def connected(self, p: int, q: int) -> bool:
        return self.root(p) == self.root(q) # check if p root is the same as q root, if true then they are in the same connected component
    
# weighted quick union has log(O) n for union and find
# second improvement is to connected every node in trajectory to root node to root node directly, stops the need of having to traverse the whole tree at each iteration

class QuickFindUF:
    def __init__(self, N: int):
        self.ids = [i for i in range(N)]
    
    def union(self, p: int, q: int):
        pid = self.ids[p]
        qid = self.ids[q]
        for i in range(len(self.ids)):
            if self.ids[i] == pid:
                self.ids[i] = qid
            
    def connected(self, p: int, q: int) -> bool:
        return self.ids[p] == self.ids[q]