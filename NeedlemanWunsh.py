# function for creating 0 matrices
def create_matrix(rows, cols):
    matrix = []
    for _ in range(rows):
        row = [0] * cols
        matrix.append(row)
    return matrix


# take input for file name
file1 = input("Enter file 1 name: ")
file2 = input("Enter file 2 name")

# function to read file name


def read_file(file_name):
    file_name = file_name + ".txt"
    with open(file_name, 'r') as file:
        sequence = file.readline().strip()  # Read the first line and remove any leading/trailing spaces
        return sequence


sequence_1 = read_file(file1)
sequence_2 = read_file(file2)

# make both matrices: one for actually keeping the score and one for keeping the penalties/rewards
# for mismatches/matches.

main_matrix = create_matrix(len(sequence_1)+1, len(sequence_2)+1)
match_checker_matrix = create_matrix(len(sequence_1), len(sequence_2))

# Providing the scores for match ,mismatch and gap
match_reward = 1
mismatch_penalty = -1
gap_penalty = -2

# Fill the match checker matrix so that when letters in seq match - reward, else penalty
for i in range(len(sequence_1)):
    for j in range(len(sequence_2)):
        if sequence_1[i] == sequence_2[j]:
            match_checker_matrix[i][j] = match_reward
        else:
            match_checker_matrix[i][j] = mismatch_penalty


# Needleman_Wunsch algorithm
# fill in the gap penalties for first row and column
for i in range(len(sequence_1)+1):
    main_matrix[i][0] = i*gap_penalty
for j in range(len(sequence_2)+1):
    main_matrix[0][j] = j * gap_penalty

# start filling the matrix
for i in range(1, len(sequence_1)+1):
    for j in range(1, len(sequence_2)+1):
        main_matrix[i][j] = max(main_matrix[i-1][j-1]+match_checker_matrix[i-1][j-1],
                                main_matrix[i-1][j]+gap_penalty,
                                main_matrix[i][j-1] + gap_penalty)


# Start Traceback

aligned_1 = ""
aligned_2 = ""

ti = len(sequence_1)
tj = len(sequence_2)

# start from bottom right end and move up/left/diagonally
while ti > 0 and tj > 0:

    # case where we are moving diagonally
    if ti > 0 and tj > 0 and main_matrix[ti][tj] == main_matrix[ti-1][tj-1] + match_checker_matrix[ti-1][tj-1]:

        aligned_1 = sequence_1[ti-1] + aligned_1
        aligned_2 = sequence_2[tj-1] + aligned_2

        ti = ti - 1
        tj = tj - 1

    # moving to left
    elif ti > 0 and main_matrix[ti][tj] == main_matrix[ti-1][tj] + gap_penalty:
        aligned_1 = sequence_1[ti-1] + aligned_1
        aligned_2 = "-" + aligned_2

        ti = ti - 1

    # moving up
    else:
        aligned_1 = "-" + aligned_1
        aligned_2 = sequence_2[tj-1] + aligned_2

        tj = tj - 1
