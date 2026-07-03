class move:
    def __init__(self,vectors, piece): #vectors is a list of tuples representing the direction and distance of the move
        self.vectors = vectors
        self.piece = piece #pice is an instance of the piece class
    
        