import os
import sympy
import numpy as np 

def show_homogeneous_matrix():
    print("\nHomogeneous Maxtrix (A)")

    c_theta, s_theta, d, a, c_alpha, s_alpha = sympy.symbols('c_theta s_theta d a c_alpha s_alpha')

    # Homogeneous Matrix (A)
    A_rot_ztheta_i = np.array([[c_theta, -s_theta, 0, 0],
                            [s_theta, c_theta, 0, 0],
                            [0, 0, 1, 0], 
                            [0, 0, 0, 1]], dtype = object)

    A_trans_zd_i = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, d],
                        [0, 0, 0, 1]], dtype = object)

    A_trans_xa_i = np.array([[1, 0, 0, a],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]], dtype = object)

    A_rot_xa_i = np.array([[1, 0, 0, 0],
                        [0, c_alpha, -s_alpha, 0],
                        [0, s_alpha, c_alpha, 0],
                        [0, 0, 0, 1]], dtype = object)

    return np.matmul(np.matmul(np.matmul(A_rot_ztheta_i, A_trans_zd_i), A_trans_xa_i), A_rot_xa_i)

os.system('cls')
print(show_homogeneous_matrix())
