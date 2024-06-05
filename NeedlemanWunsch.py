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
            
        print(tabulate(matrix, tablefmt="grid"))
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
                diag = matrix[i-1][j-1] + (self.MATCH_SCORE if self.seq1[i-1] == self.seq2[i-1] else self.MISMATCH_PENALTY)
                top = matrix[i-1][j-1] + matrix[i-1][j]
                left = matrix[i-1][j-1] + matrix[i][j-1]
                matrix[i][j] = max(diag, top, left)
    
        print(tabulate(matrix, tablefmt="grid"))
  
test = NeedlemanWunsch("TACGA", "TATGC" )
mat = test.init_matrix()
test.forward_pass(mat)

