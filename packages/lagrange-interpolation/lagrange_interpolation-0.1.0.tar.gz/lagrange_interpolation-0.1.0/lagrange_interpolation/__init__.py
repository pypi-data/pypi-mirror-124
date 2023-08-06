from numpy.polynomial import Polynomial


def lagrange_interpolation(x_coordinates, y_coordinates) -> Polynomial:
    n = len(x_coordinates)

    lagrange_polynomial = Polynomial([0])
    for i in range(n):
        basis_polynomial = Polynomial([1])
        for j in range(n):
            x = Polynomial([0, 1])
            if i != j:
                pol = (x - x_coordinates[j]) / (x_coordinates[i] - x_coordinates[j])
                basis_polynomial *= pol
        basis_polynomial *= y_coordinates[i]
        lagrange_polynomial += basis_polynomial

    return lagrange_polynomial
