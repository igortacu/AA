import time
import math


# ==================== Method 1: Recursive ====================
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


# ==================== Method 2: Dynamic Programming ====================
def fibonacci_dp(n):
    if n <= 1:
        return n
    A = [0] * (n + 1)
    A[0] = 0
    A[1] = 1
    for i in range(2, n + 1):
        A[i] = A[i - 1] + A[i - 2]
    return A[n]


# ==================== Method 3: Matrix Power ====================
def matrix_multiply(A, B):
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
    ]


def matrix_power(M, n):
    result = [[1, 0], [0, 1]]  # Identity matrix
    for _ in range(n):
        result = matrix_multiply(result, M)
    return result


def fibonacci_matrix(n):
    if n <= 1:
        return n
    M = [[0, 1], [1, 1]]
    result = matrix_power(M, n)
    vec = [0, 1]
    return result[0][0] * vec[0] + result[0][1] * vec[1]


# ==================== Method 4: Binet Formula ====================
def fibonacci_binet(n):
    phi = (1 + math.sqrt(5)) / 2
    phi1 = (1 - math.sqrt(5)) / 2
    try:
        return round((pow(phi, n) - pow(phi1, n)) / math.sqrt(5))
    except OverflowError:
        return None  # Overflow for large n due to floating-point limits


# ==================== Timing Utility ====================
def measure_time(func, n):
    start = time.time()
    result = func(n)
    end = time.time()
    return result, end - start


# ==================== Empirical Analysis ====================
def run_analysis():
    # First input set (smaller, for recursive method)
    input_set_1 = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45]

    # Second input set (larger, for DP, Matrix, Binet)
    input_set_2 = [501, 631, 794, 1000, 1259, 1585, 1995, 2512,
                   3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]

    methods_all = {
        "Recursive":  fibonacci_recursive,
        "DP":         fibonacci_dp,
        "Matrix":     fibonacci_matrix,
        "Binet":      fibonacci_binet,
    }

    methods_large = {
        "DP":     fibonacci_dp,
        "Matrix": fibonacci_matrix,
        "Binet":  fibonacci_binet,
    }

    # --- Analysis with first input set (all 4 methods) ---
    print("=" * 80)
    print("ANALYSIS 1: All methods with smaller input set")
    print("=" * 80)
    print(f"{'n':>6}", end="")
    for name in methods_all:
        print(f"  {name:>14s}", end="")
    print()
    print("-" * 80)

    for n in input_set_1:
        print(f"{n:>6}", end="")
        for name, func in methods_all.items():
            _, elapsed = measure_time(func, n)
            print(f"  {elapsed:>14.8f}", end="")
        print()

    # --- Analysis with second input set (DP, Matrix, Binet) ---
    print()
    print("=" * 80)
    print("ANALYSIS 2: DP, Matrix, Binet with larger input set")
    print("=" * 80)
    print(f"{'n':>6}", end="")
    for name in methods_large:
        print(f"  {name:>14s}", end="")
    print()
    print("-" * 80)

    for n in input_set_2:
        print(f"{n:>6}", end="")
        for name, func in methods_large.items():
            result, elapsed = measure_time(func, n)
            if result is None:
                print(f"  {'OVERFLOW':>14s}", end="")
            else:
                print(f"  {elapsed:>14.8f}", end="")
        print()

    # --- Correctness check ---
    print()
    print("=" * 80)
    print("CORRECTNESS CHECK (first 20 terms)")
    print("=" * 80)
    print(f"{'n':>4}  {'Recursive':>12}  {'DP':>12}  {'Matrix':>12}  {'Binet':>12}")
    print("-" * 60)
    for n in range(20):
        r = fibonacci_recursive(n)
        d = fibonacci_dp(n)
        m = fibonacci_matrix(n)
        b = fibonacci_binet(n)
        match = "✓" if r == d == m == b else "✗"
        print(f"{n:>4}  {r:>12}  {d:>12}  {m:>12}  {b:>12}  {match}")


if __name__ == "__main__":
    run_analysis()
