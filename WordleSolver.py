import math
class WordleSolver:
    j = []
        
      
class patternMatrix: 
    def __init__(self):
        self.listOfCombos = []
        for i in range (0,3):
            for j in range (0,3):
                for k in range (0,3):
                    for l in range(0,3):
                        for m in range (0,3):
                            self.listOfCombos.append([i,j,k,l,m])
        self.pruneMatrix()
        print(self.listOfCombos)
        print(len(self.listOfCombos))
        


    def pruneMatrix(self):
        #If the sum is nine, that means the pattern is invalid. (i.e. g,g,g,g,y)
        SUM_TO_DELETE = 9
        self.listOfCombos = [combo for combo in self.listOfCombos if sum(combo) != SUM_TO_DELETE]

def main():
    pattern = patternMatrix()

if __name__ == "__main__":
    main()