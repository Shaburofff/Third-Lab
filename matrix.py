def read_matrix(filename="matrix.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        return [list(map(int, line.split())) for line in f if line.strip()]

def print_matrix(M, title):
    print(f"\n{title}:")
    for row in M:
        print(" ".join(f"{x:4}" for x in row))

def transpose(M):
    return [list(row) for row in zip(*M)]

def mul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def scalar_mult(K, M):
    return [[K * val for val in row] for row in M]

def sub(A, B):
    return [[a - b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]

def get_regions(n):
    r1, r2, r3, r4 = [], [], [], []
    for i in range(n):
        for j in range(n):
            if i < j < n - 1 - i:
                r1.append((i, j))
            elif i < j and j > n - 1 - i:
                r2.append((i, j))
            elif i > j > n - 1 - i:
                r3.append((i, j))
            elif i > j and j < n - 1 - i:
                r4.append((i, j))
    return r1, r2, r3, r4

def count_gt_K_even_cols(A, region, K):
    return sum(1 for i, j in region if j % 2 == 0 and A[i][j] > K)

def prod_even_in_odd_rows(A, region):
    prod = 1
    for i, j in region:
        if i % 2 == 1 and A[i][j] % 2 == 0:
            prod *= A[i][j]
    return prod

def build_F(A, K):
    n = len(A)
    F = [row[:] for row in A]
    r1, r2, r3, r4 = get_regions(n)
    cnt2 = count_gt_K_even_cols(A, r2, K)
    prod3 = prod_even_in_odd_rows(A, r3)
    print(f"Количество чисел > K в чётных столбцах области 2: {cnt2}")
    print(f"Произведение чётных чисел в нечётных строках области 3: {prod3}")
    if cnt2 < prod3:
        for i2, j2 in r2:
            i3, j3 = j2, i2
            F[i2][j2], F[i3][j3] = F[i3][j3], F[i2][j2]
    else:
        for (i1, j1), (i3, j3) in zip(r1, r3):
            F[i1][j1], F[i3][j3] = F[i3][j3], F[i1][j1]
    return F

def main():
    K = int(input("Введите K: "))
    A = read_matrix()
    print_matrix(A, "Матрица A")
    F = build_F(A, K)
    print_matrix(F, "Матрица F")
    result = sub(
        scalar_mult(K, mul(A, F)),
        scalar_mult(K, transpose(A))
    )
    print_matrix(result, "Результат (K*A*F – K*A^T)")

if __name__ == "__main__":
    main()
