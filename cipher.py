#!/usr/bin/env python3
import sys

def create_square_matrix(text):
    size = int(len(text) ** 0.5) + (1 if int(len(text) ** 0.5) ** 2 < len(text) else 0)
    numbers = [ord(c) for c in text]
    while len(numbers) < size * size:
        numbers.append(0)
    return [numbers[i:i + size] for i in range(0, len(numbers), size)]


def create_message_matrix(numbers, key_size):
    while len(numbers) % key_size != 0:
        numbers.append(0)
    return [numbers[i:i + key_size] for i in range(0, len(numbers), key_size)]


def matrix_multiply(mat1, mat2):
    result = [[0] * len(mat2[0]) for _ in range(len(mat1))]
    for i in range(len(mat1)):
        for j in range(len(mat2[0])):
            for k in range(len(mat2)):
                result[i][j] += mat1[i][k] * mat2[k][j]
    return result


def determinant(matrix):
    size = len(matrix)
    if size == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0
    for c in range(size):
        submatrix = [
            [matrix[i][j] for j in range(size) if j != c]
            for i in range(1, size)
        ]
        det += ((-1) ** c) * matrix[0][c] * determinant(submatrix)
    return det


def invert_matrix(matrix):
    size = len(matrix)
    det = determinant(matrix)
    if det == 0:
        raise ValueError("Matrix inversion is not possible due to zero determinant.")
    if size == 2:
        return [[matrix[1][1] / det, -matrix[0][1] / det],
                [-matrix[1][0] / det, matrix[0][0] / det]]
    cofactor_matrix = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            submatrix = [
                [matrix[x][y] for y in range(size) if y != j]
                for x in range(size) if x != i
            ]
            cofactor_matrix[i][j] = ((-1) ** (i + j)) * determinant(submatrix)
    return [[cofactor_matrix[j][i] / det for j in range(size)] for i in range(size)]


def encrypt(message, key_matrix):
    key_size = len(key_matrix)
    message_matrix = create_message_matrix([ord(c) for c in message], key_size)
    encrypted_matrix = matrix_multiply(message_matrix, key_matrix)
    return [item for row in encrypted_matrix for item in row]


def decrypt(encrypted_message, key_matrix):
    encrypted_numbers = list(map(int, encrypted_message.split()))
    encrypted_matrix = create_message_matrix(encrypted_numbers, len(key_matrix))
    inverted_key = invert_matrix(key_matrix)
    decrypted_matrix = matrix_multiply(encrypted_matrix, inverted_key)
    characters = []
    for row in decrypted_matrix:
        for item in row:
            char = chr(round(item))
            if char != '\x00':
                characters.append(char)
    return ''.join(characters)


def print_matrix(matrix):
    for row in matrix:
        print('\t'.join(map(str, row)))


def print_help():
    print("USAGE:\n\t./103cipher.py message key flag\n\n")
    print("DESCRIPTION:")
    print("\tmessage: The message to encrypt or decrypt.")
    print("\tkey: The key to use for encryption or decryption.")
    print("\tflag: 0 for encryption, 1 for decryption.")
    sys.exit(84)


def main():
    if len(sys.argv) != 4:
        print_help()
        sys.exit(84)
    try:
        message, key, flag = sys.argv[1], sys.argv[2], int(sys.argv[3])
        key_matrix = create_square_matrix(key)

        if determinant(key_matrix) == 0:
            print("Error: Key matrix is singular (non-invertible).")
            sys.exit(84)

        if flag == 0:
            print("Key matrix:")
            print_matrix(key_matrix)
            encrypted = encrypt(message, key_matrix)
            print("\nEncrypted message:")
            print(' '.join(map(str, encrypted)))
        elif flag == 1: 
            print("Key matrix:")
            print_matrix(key_matrix)
            decrypted = decrypt(message, key_matrix)
            print("\nDecrypted message:")
            print(decrypted)
        else:
            print_help()
            sys.exit(84)
    except:
        print_help()
        sys.exit(84)
