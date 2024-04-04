import random
from algs import WeightedQuickUnionUF, QuickFindUF
import statistics as stats
import random
import time
# percolation data type

class Percolation:
    def __init__(self, n: int, fast: bool) -> None:
        if n <= 0:
            raise Exception("IllegalArgumentException")
        self.n = n
        if fast:    
            self.alg = WeightedQuickUnionUF(n**2 + 2) # add virtual sites
        else:
            self.alg = QuickFindUF(n**2 + 2)
        self.grid = [False for i in range(n**2+2)]
        self.top = 0
        self.bottom = n**2 + 1
        self.open_sites = 0
    
    def corner_case_check(self, row, col):
        if row < 1 or col < 1:
            raise  Exception("IllegalArgumentException")
    
    def row_col_to_idx(self, row: int, col: int):
        return row * self.n - 1 - (self.n - col) 
    
    
    def open(self,  row: int, col: int):
        self.corner_case_check(row, col)
        site_idx = self.row_col_to_idx(row, col) # change to index
        
        # open site
        self.grid[site_idx] = True
        self.open_sites += 1
        
        # connecting top and bottom vs if applicable
        if row == 1:
            self.alg.union(site_idx, self.top)
        if row == self.n:
            self.alg.union(site_idx, self.bottom)
        
        # manual neighbour check with bound restriction
        
        # top
        if row > 1 and self.is_open(row - 1, col):
            self.alg.union(site_idx, self.row_col_to_idx(row - 1, col))
        
        # bottom
        if row < self.n and self.is_open(row + 1, col):
            self.alg.union(site_idx, self.row_col_to_idx(row + 1, col))
        
        # left
        if col > 1 and self.is_open(row, col - 1):
            self.alg.union(site_idx, self.row_col_to_idx(row, col - 1))

        # right
        if col < self.n and self.is_open(row, col + 1):
            self.alg.union(site_idx, self.row_col_to_idx(row, col + 1))

            
        
        
            
    def is_open(self, row: int, col: int) -> bool:
        self.corner_case_check(row, col)

        return self.grid[self.row_col_to_idx(row, col)]
        
    def is_full(self, row: int, col: int) -> bool:
        # checks if given site is connected to the virtual top site
        self.corner_case_check(row, col)
        p = self.row_col_to_idx(row, col)
        if not self.is_open(p):
            return False
        else:
            return self.alg.connected(self.row_col_to_idx(row, col), self.top)

    
    def number_of_open_sites(self) -> int:
        return self.open_sites

    def percolates(self) -> bool:
        return self.alg.connected(self.top, self.bottom) 


class MonteCarloSimulation:
    def __init__(self) -> None:        
        self.thresholds = []
        
    def mean(self):
        return stats.mean(self.thresholds)
        
    def stddev(self):
        return stats.stdev(self.thresholds)

    def confidence(self):
        return [self.mean() - (1.96 * self.stddev()) / len(self.thresholds)**0.5, self.mean() + (1.96 * self.stddev()) / len(self.thresholds)**0.5]
    
    def run(self, n, trials, fast: bool):
        if n <= 0 or trials <= 0:
            raise  Exception("IllegalArgumentException")
        for i in range(trials):     
            self.percolation = Percolation(n, fast=fast) # init grid
            while not self.percolation.percolates():
                random_row = random.randint(1, n)
                random_col = random.randint(1, n)
                
                if not self.percolation.is_open(random_row, random_col):
                    self.percolation.open(random_row, random_col)
            
            self.thresholds.append(self.percolation.open_sites / n**2)
        print("\nMean: ", self.mean())
        print("Standard Deviation: ", self.stddev())
        print("95% Confidence Interval: ", self.confidence())
            
        
sim = MonteCarloSimulation()

n = 10
trials = 50000

fast_start = time.time()
sim.run(n, trials, fast=True)
fast_end = time.time()
print(f"\nWeighted Quick Union with Path Compression took: {round(fast_end - fast_start)}s")

slow_start = time.time()
sim.run(n, trials, fast=False)
slow_end = time.time()
print(f"\nQuick Find took: {round(slow_end - slow_start)}s")