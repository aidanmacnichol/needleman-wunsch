from tabulate import tabulate

class NeedlemanWunsch:
    
    MATCH_SCORE = 1
    MISMATCH_PENALTY = -1
    GAP_PENALTY = -2
    seq1 = ""
    seq2 = ""
    
    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2
    
    def print_matrix(self, matrix):
        """
        Helper function to print matrix nicely.

        Args:
            matrix (arr[][]): matrix to print
        """
        header = [" "] + list(self.seq2)
        table = []

        for i in range(len(matrix)):
            if i == 0:
                row = [" "] + matrix[i]
            else:
                row = [self.seq1[i-1]] + matrix[i]
            table.append(row)
        print(tabulate(table, headers=header, tablefmt="grid"))

        
    def init_matrix(self):
        """
        Initialize the matrix to the seq length + 1
        Initialize first row and column to gap penalty * i (-2, -4, -6...)

        Returns:
            matrix[][]: Empty matrix with first row/col initialized
        """
        # get length of rows/cols
        rows = len(self.seq1) + 1
        cols = len(self.seq2) + 1
        # Initialize empty matrix with all 0's
        matrix = [[0 for col in range(cols)] for row in range(rows)]
        
        # Initialize first row/col to gap penalty
        for i in range(1, rows):
            matrix[i][0] = i * self.GAP_PENALTY
        for j in range(1, cols):
            matrix[0][j] = j * self.GAP_PENALTY
            
        return matrix
    
    def forward_pass(self, matrix): 
        """
        
         0 -2
        -2  
        
        (deletion) top = 0 + -2 = -2
        (insertion) left = 0 + -2 = -2
        (match) diag = 0 + (check match)
        Args:
            matrix (_type_): _description_
        """
        
        for i in range(1, len(self.seq1) + 1):
            for j in range(1, len(self.seq2) + 1):
                # Calculate match score (diag) - diagonal cell + match_score if sequence letters match else + mismatch_penalty
                diag = matrix[i-1][j-1] + (self.MATCH_SCORE if self.seq1[i-1] == self.seq2[j-1] else self.MISMATCH_PENALTY)
                top = matrix[i-1][j] + self.GAP_PENALTY
                left = matrix[i][j-1] + self.GAP_PENALTY
                matrix[i][j] = max(diag, top, left)
    
    def backtrack(self, matrix):
        """
        1. Start bottom right corner (end of allignment)
        2. Determine move: diag (match/mismatch), left (gap in seq1), up (gap in second seq2)
            - if sequence letters match move diagonal
            - if left number bigger than top go left
            - if top number bigger than left go up
        3. Record allignment: diag (add letters from both sequences), up (add letter from seq1 and a gap "-" to seq2), left (add gap "-" to seq1 and add letter from seq2)
        4. Move to next cell depending on result from step 2. 
        5. Repeat steps 1-4 until top left cell is reached
        6. Final allignment is backwards to reverse the order.

        Args:
            matrix (_type_): _description_
        """

        alignment1 = []
        alignment2 = []
        i, j = len(self.seq1), len(self.seq2)

        while i > 0 and j > 0:
            # 
            up_score = matrix[i-1][j]
            left_score = matrix[i][j-1]
  
            # check diagonal move
            if self.seq1[i-1] == self.seq2[j-1]:
                alignment1.append(self.seq1[i-1])
                alignment2.append(self.seq2[j-1])
                i -= 1
                j -= 1
            elif up_score >= left_score:
                alignment1.append(self.seq1[i-1])
                alignment2.append("-")
                i -= 1
            else:
                alignment1.append("-")
                alignment2.append(self.seq2[j-1])
                j -= 1
        
        while i > 0:
            alignment1.append(self.seq1[i-1])
            alignment2.append("-")
            i -= 1
        
        while j > 0:
            alignment1.append("-")
            alignment2.append(self.seq2[j-1])
            j -= 1

        alignment1.reverse()
        alignment2.reverse() 

        print(f"alignment1: {alignment1}")
        print(f"alignment2: {alignment2}")



test = NeedlemanWunsch("GAAC", "GAAGAC")
mat = test.init_matrix()
test.forward_pass(mat)
test.print_matrix(mat) 
test.backtrack(mat)

