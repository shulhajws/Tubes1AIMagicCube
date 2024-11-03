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

def objective_function_new(cube):
    """Calculate the objective function based on mean difference and variance of line sums."""
    alpha=0.5 
    beta=0.5 
    magic_number=315
    line_sums = []
    
    # Calculate row, column, and pillar sums
    for i in range(5):
        for j in range(5):
            # Row (fixed layer in the third dimension)
            row_sum = np.sum(cube[i, j, :])
            line_sums.append(row_sum)
            
            # Column (fixed layer in the second dimension)
            column_sum = np.sum(cube[i, :, j])
            line_sums.append(column_sum)
            
            # Pillar (fixed layer in the first dimension)
            pillar_sum = np.sum(cube[:, i, j])
            line_sums.append(pillar_sum)
    
    # Calculate face diagonals (diagonals on each face)
    for i in range(5):
        # Layer's diagonals (horizontal and vertical on each layer)
        face_diag1_sum = np.sum([cube[i, j, j] for j in range(5)])
        face_diag2_sum = np.sum([cube[i, j, 5 - 1 - j] for j in range(5)])
        line_sums.extend([face_diag1_sum, face_diag2_sum])
        
        # Layer's diagonals (side view)
        face_diag3_sum = np.sum([cube[j, i, j] for j in range(5)])
        face_diag4_sum = np.sum([cube[j, i, 5 - 1 - j] for j in range(5)])
        line_sums.extend([face_diag3_sum, face_diag4_sum])
        
        # Another side view diagonals
        face_diag5_sum = np.sum([cube[j, j, i] for j in range(5)])
        face_diag6_sum = np.sum([cube[j, 5 - 1 - j, i] for j in range(5)])
        line_sums.extend([face_diag5_sum, face_diag6_sum])

    # Calculate space diagonals
    space_diag1_sum = np.sum([cube[i, i, i] for i in range(5)])
    space_diag2_sum = np.sum([cube[i, i, 5 - 1 - i] for i in range(5)])
    space_diag3_sum = np.sum([cube[i, 5 - 1 - i, i] for i in range(5)])
    space_diag4_sum = np.sum([cube[i, 5 - 1 - i, 5 - 1 - i] for i in range(5)])
    line_sums.extend([space_diag1_sum, space_diag2_sum, space_diag3_sum, space_diag4_sum])
    
    # Calculate Mean Difference
    mean_difference = np.mean([calculate_line_sum_deviation(sum_line, magic_number) for sum_line in line_sums])
    
    # Calculate Variance
    avg_sum_line = np.mean(line_sums)
    variance = np.mean([(sum_line - avg_sum_line) ** 2 for sum_line in line_sums])
    
    # Objective function with 50% weighting for both mean difference and variance
    objective_value = alpha * mean_difference + beta * variance
    
    return objective_value

def objective_function_latest(cube):
    """Calculate the objective function based on mean difference and variance of line sums, and track the best and worst lines."""
    alpha, beta = 0.5, 0.5
    magic_number = 315
    line_sums = []
    best_lines = []
    worst_lines = []

    # Helper to update best and worst lines
    def update_best_lines(deviation, indices):
        if len(best_lines) < 3:
            best_lines.append((deviation, indices))
            best_lines.sort()  # Keep best_lines sorted by deviation (smallest first)
        else:
            if deviation < best_lines[-1][0]:
                best_lines[-1] = (deviation, indices)
                best_lines.sort()  # Keep best_lines sorted by deviation

    def update_worst_lines(deviation, indices):
        if len(worst_lines) < 3:
            worst_lines.append((deviation, indices))
            worst_lines.sort(reverse=True)  # Keep worst_lines sorted by deviation (largest first)
        else:
            if deviation > worst_lines[-1][0]:
                worst_lines[-1] = (deviation, indices)
                worst_lines.sort(reverse=True)  # Keep worst_lines sorted by deviation

    # Calculate row, column, and pillar sums
    for i in range(5):
        for j in range(5):
            # Row [i, j, :]
            row_sum = np.sum(cube[i, j, :])
            deviation = calculate_line_sum_deviation(row_sum, magic_number)
            update_best_lines(deviation, [i, j, ':'])
            update_worst_lines(deviation, [i, j, ':'])
            line_sums.append(row_sum)

            # Column [i, :, j]
            column_sum = np.sum(cube[i, :, j])
            deviation = calculate_line_sum_deviation(column_sum, magic_number)
            update_best_lines(deviation, [i, ':', j])
            update_worst_lines(deviation, [i, ':', j])
            line_sums.append(column_sum)

            # Pillar [:, i, j]
            pillar_sum = np.sum(cube[:, i, j])
            deviation = calculate_line_sum_deviation(pillar_sum, magic_number)
            update_best_lines(deviation, [':', i, j])
            update_worst_lines(deviation, [':', i, j])
            line_sums.append(pillar_sum)

    # Calculate Mean Difference
    mean_difference = np.mean([calculate_line_sum_deviation(sum_line, magic_number) for sum_line in line_sums])

    # Calculate Variance
    avg_sum_line = np.mean(line_sums)
    variance = np.mean([(sum_line - avg_sum_line) ** 2 for sum_line in line_sums])

    # Objective function with 50% weighting for both mean difference and variance
    objective_value = alpha * mean_difference + beta * variance

    return objective_value, best_lines, worst_lines