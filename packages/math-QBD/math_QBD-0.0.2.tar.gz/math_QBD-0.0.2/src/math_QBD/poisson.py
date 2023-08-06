def poisson__1D(dx, f_0,f_L,g,h):
    
    M = len(h)

    f = [0] * M
    f[0] = f_0
    f[-1] = f_L

    beta = [0] * M
    gamma = [0] * M

    beta[1] = (g[2] - g[0] + 4 * g[1]) / (8 * g[1])
    gamma[1] = ((-g[2] + g[0] + 4 * g[1]) * f_0 - 4 * dx * dx * h[1]) / (8 * g[1])

    for i in range(2, M-2):
        a_i = -g[i+1] + g[i-1] + 4 * g[i]
        denominator = a_i * beta[i-1] + (-8 * g[i])

        beta[i] = -(g[i+1] - g[i-1] + 4 * g[i]) / denominator
        gamma[i] = (4 * dx * dx * h[i] - a_i * gamma[i-1]) / denominator

    a_N = (-g[-1] + g[-3] + 4 * g[-2])
    f[-2] = (-a_N * gamma[-3] + 4 * dx * dx * h[-2] -(g[-1] - g[-3] + 4 * g[-2]) * f_L) / (a_N * beta[-3] + (-8 * g[-2]))

    for i in range(1,M - 2):
        j = M - 2 - i
        f[j] = beta[j] * f[j + 1] + gamma[j]

    return f