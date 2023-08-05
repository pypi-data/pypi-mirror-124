import numpy as np


def lagrange_interpolation(arrx, arry):
    n = len(arrx)
    p = MyPolynomial([0.0])
    for j in range(n):
        fj = arry[j]
        pt = MyPolynomial([fj])
        for m in range(n):
            if m == j:
                continue
            den = arrx[j] - arrx[m]
            pt = pt.mul([1.0, -arrx[m]]).div_by_num(den)
        p = p.sum(pt)
    return p


class MyPolynomial:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(self.arr)

    def sum(self, arr2):
        m = len(arr2)
        p = np.zeros(max(self.n, m))
        if self.n < m:
            for i in range(0, m - self.n):
                p[i] = arr2[i]
            for i in range(self.n):
                p[m - self.n + i] = self.arr[i] + arr2[m - self.n + i]
        else:
            for i in range(0, self.n - m):
                p[i] = self.arr[i]
            for i in range(m):
                p[self.n - m + i] = self.arr[self.n - m + i] + arr2[i]

        return MyPolynomial(p)

    def mul(self, arr2):
        m = len(arr2)
        deg = m + self.n - 1
        p = np.zeros(deg)

        for i in range(deg):
            term = 0.0
            for j in range(i + 1):
                if self.n < m:
                    if j >= self.n or i - j >= m:
                        term += 0
                        continue
                    term += self.arr[j] * arr2[i - j]
                else:
                    if i - j >= self.n or j >= m:
                        term += 0
                        continue
                    term += arr2[j] * self.arr[i - j]
            p[i] = term
        return MyPolynomial(p)

    def add_num(self, a):
        p = np.zeros(self.n)
        for i in range(self.n):
            p[i] = self.arr[i] + a
        return MyPolynomial(p)

    def mul_by_name(self, a):
        p = np.zeros(self.n)
        for i in range(self.n):
            p[i] = self.arr[i] * a
        return MyPolynomial(p)

    def div_by_num(self, a):
        return self.mul_by_name(1.0 / a)

    def __len__(self):
        return self.n

    def __getitem__(self, item):
        return self.arr[item]

    def __call__(self, val):
        val_len = len(val)
        if isinstance(val, MyPolynomial):
            y = 0
        else:
            y = np.zeros(val_len)
        for i in range(self.n):
            y = y * val + self.arr[i]
        return y
