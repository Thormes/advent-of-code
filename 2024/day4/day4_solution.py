with open("day4.input") as text_input:
    lines = [x.strip() for x in text_input.readlines()]


def find_word(words: dict, word: str):
    found = set()
    word = word.upper()
    for coord, search in words.items():
        if search.upper() == word or search.upper() == word[::-1]:
            found.add(coord)
    return len(found)


def search_word_in_matrix(matrix: list[str], size: int):
    length = len(matrix)
    width = len(matrix[0])
    if len(matrix[0]) < size:
        raise ValueError("The searched word doesn't fit the matrix size")
    count = 0
    found_index = []
    words = {}
    for i in range(length):
        for j in range(width):
            #se puder pegar diagonal (palavras internas) pega todas as palavras possíveis
            if i + size <= length and j + size <= width:
                horizontal = ''
                vertical = ''
                diagonal1 = ''
                diagonal2 = ''
                for n in range(size):
                    diagonal1 += matrix[i + n][j + n]
                    diagonal2 += matrix[i + n][j + (size - 1) - n]
                    vertical += matrix[i + n][j]
                horizontal = matrix[i][j:j + size]
                words[f"({i},{j})-({i + size - 1},{j + size - 1})"] = diagonal1
                words[f"({i},{j + size - 1})-({i + size - 1},{j})"] = diagonal2
                words[f"({i},{j})-({i},{j + size - 1})"] = horizontal
                words[f"({i},{j})-({i + size - 1},{j})"] = vertical

            #get last lines
            elif j + size <= width:
                horizontal = matrix[i][j:j + size]
                words[f"({i},{j})-({i},{j + size - 1})"] = horizontal
            #get last columns
            elif i + size <= length:
                vertical = ''
                for n in range(size):
                    vertical += matrix[i + n][j]
                words[f"({i},{j})-({i + size - 1},{j})"] = vertical

    return words


def get_matrices(matrix, size):
    result = []
    for i in range(len(matrix) - size + 1):
        for j in range(len(matrix[0]) - size + 1):
            mat = []
            for n in range(size):
                mat.append(matrix[i + n][j:j + size])
            result.append(mat)
    return result


def has_x_word(matrix, word: str):
    size = len(word)
    word = word.upper()
    diagonal1 = ''
    diagonal2 = ''
    for n in range(size):
        diagonal1 += matrix[n][n]
        diagonal2 += matrix[n][size - 1 - n]

    if (diagonal1.upper() == word or diagonal1.upper() == word[::-1]) and (
            diagonal2.upper() == word or diagonal2.upper() == word[::-1]):
        return True

    return False


#words = search_word_in_matrix(lines, 3, True)
#total = find_word(words, 'MAS')
matrices = get_matrices(lines, 3)
count = 0
for matrix in matrices:
    if has_x_word(matrix, 'MAS'):
        count += 1

print(count)
