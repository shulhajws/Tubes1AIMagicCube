import numpy as np

def calculate_line_sum_deviation(line_sum):
    """Calculate the absolute deviation of a line's sum from magic number."""
    return abs(line_sum - 315)

def objective_function(cube):
    """Calculate the objective function"""
    total_deviation = 0
    
    # Sum deviations for rows, columns, and pillars
    for i in range(5):
        for j in range(5):
            # Row (fixed layer in the third dimension)
            row_sum = np.sum(cube[i, j, :])
            total_deviation += calculate_line_sum_deviation(row_sum)
            
            # Column (fixed layer in the second dimension)
            column_sum = np.sum(cube[i, :, j])
            total_deviation += calculate_line_sum_deviation(column_sum)
            
            # Pillar (fixed layer in the first dimension)
            pillar_sum = np.sum(cube[:, i, j])
            total_deviation += calculate_line_sum_deviation(pillar_sum)
    
    # Sum deviations for face diagonals (diagonals on each face)
    for i in range(5):
        # Layer's diagonals (layer's here is stack layer from low to top)
        face_diag1_sum = np.sum([cube[i, j, j] for j in range(5)]) 
        face_diag2_sum = np.sum([cube[i, j, 5 - 1 - j] for j in range(5)]) 
        total_deviation += calculate_line_sum_deviation(face_diag1_sum)
        total_deviation += calculate_line_sum_deviation(face_diag2_sum)
        
        # Layer's diagonals (layer's here is standing layer)
        face_diag3_sum = np.sum([cube[j, i, j] for j in range(5)]) 
        face_diag4_sum = np.sum([cube[j, i, 5 - 1 - j] for j in range(5)]) 
        total_deviation += calculate_line_sum_deviation(face_diag3_sum)
        total_deviation += calculate_line_sum_deviation(face_diag4_sum)
        
        # Layer's diagonals (layer's here is standing layer - another side view)
        face_diag5_sum = np.sum([cube[j, j, i] for j in range(5)])  
        face_diag6_sum = np.sum([cube[j, 5 - 1 - j, i] for j in range(5)])
        total_deviation += calculate_line_sum_deviation(face_diag5_sum)
        total_deviation += calculate_line_sum_deviation(face_diag6_sum)

    # Sum deviations for space diagonals
    space_diag1_sum = np.sum([cube[i, i, i] for i in range(5)])
    space_diag2_sum = np.sum([cube[i, i, 5 - 1 - i] for i in range(5)])
    space_diag3_sum = np.sum([cube[i, 5 - 1 - i, i] for i in range(5)])
    space_diag4_sum = np.sum([cube[i, 5 - 1 - i, 5 - 1 - i] for i in range(5)])
    
    total_deviation += calculate_line_sum_deviation(space_diag1_sum)
    total_deviation += calculate_line_sum_deviation(space_diag2_sum)
    total_deviation += calculate_line_sum_deviation(space_diag3_sum)
    total_deviation += calculate_line_sum_deviation(space_diag4_sum)
    
    return total_deviation

if __name__ == "__main__":
    cube = np.random.permutation(np.arange(1, 125+1)).reshape(5,5,5)
    
    deviation = objective_function(cube)
    print("Total deviation from magic constant:", deviation)