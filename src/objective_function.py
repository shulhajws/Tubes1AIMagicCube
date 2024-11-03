import numpy as np

def calculate_line_sum_deviation(line_sum):
    """Calculate the absolute deviation of a line's sum from magic number."""
    return abs(line_sum - 315)

def objective_function(cube):
    """Calculate the objective function based on mean difference and variance of line sums."""
    alpha=0.5 
    beta=0.5 
    magic_number=315
    line_sums = []
    
    for i in range(5):
        for j in range(5):
            row_sum = np.sum(cube[i, j, :])
            line_sums.append(row_sum)
            
            column_sum = np.sum(cube[i, :, j])
            line_sums.append(column_sum)
            
            pillar_sum = np.sum(cube[:, i, j])
            line_sums.append(pillar_sum)
    
    for i in range(5):
        face_diag1_sum = np.sum([cube[i, j, j] for j in range(5)])
        face_diag2_sum = np.sum([cube[i, j, 5 - 1 - j] for j in range(5)])
        line_sums.extend([face_diag1_sum, face_diag2_sum])
        
        face_diag3_sum = np.sum([cube[j, i, j] for j in range(5)])
        face_diag4_sum = np.sum([cube[j, i, 5 - 1 - j] for j in range(5)])
        line_sums.extend([face_diag3_sum, face_diag4_sum])
        
        face_diag5_sum = np.sum([cube[j, j, i] for j in range(5)])
        face_diag6_sum = np.sum([cube[j, 5 - 1 - j, i] for j in range(5)])
        line_sums.extend([face_diag5_sum, face_diag6_sum])

    space_diag1_sum = np.sum([cube[i, i, i] for i in range(5)])
    space_diag2_sum = np.sum([cube[i, i, 5 - 1 - i] for i in range(5)])
    space_diag3_sum = np.sum([cube[i, 5 - 1 - i, i] for i in range(5)])
    space_diag4_sum = np.sum([cube[i, 5 - 1 - i, 5 - 1 - i] for i in range(5)])
    line_sums.extend([space_diag1_sum, space_diag2_sum, space_diag3_sum, space_diag4_sum])
    
    mean_difference = np.mean([calculate_line_sum_deviation(sum_line) for sum_line in line_sums])
    avg_sum_line = np.mean(line_sums)
    variance = np.mean([(sum_line - avg_sum_line) ** 2 for sum_line in line_sums])
    
    objective_value = alpha * mean_difference + beta * variance
    
    return objective_value