from pylab import plt, mpl
plt.style.use("seaborn")
mpl.rcParams['font.family'] = 'serif'
import numpy as np
#BS方程解的离散dt
BS_formula = lambda s0, r, sigma, T, M, I, random_seed: s0 * np.exp(\
    (r - 0.5 * sigma ** 2) * T / M + sigma * (T / M) ** 0.5 * random_seed)


class option_pricing():
    def __init__(self):
        self.s0 = None
        self.r = None
        self.sigma = None
        self.T = None
        self.price = None
        self.type = None
        self.basic_density = None

    def set_basic_stock(self, s0, r, sigma, T):
        self.s0 = s0
        self.r = r
        self.sigma = sigma
        self.T = T

    def set_option(self, K, types="Call"):
        self.K = K
        self.types = types
    #基于BS公式和蒙特卡洛模拟的欧式期权定价
    def BS_MC(self, M, I):
        random_seed = np.random.standard_normal((M, I))
        random_seed = (random_seed - random_seed.mean()) / random_seed.std()
        ST = np.zeros((M + 1, I))
        ST[0] = self.s0
        for i in range(1, M + 1):
            args = (ST[i - 1], self.r, self.sigma, self.T, M, I, random_seed[i - 1])
            ST[i] = BS_formula(*args)
        select = int(I / 10)
        plt.plot(ST[:, :select])
        plt.title("BS_MC simulation")
        plt.show()
        basic_data = ST[-1]
        self.basic_density = basic_data

    def pricing(self):
        if self.types == "Call":
            ht = np.maximum((self.basic_density - self.K), 0)
        else:
            ht = np.maximum((self.K - self.basic_density), 0)
        self.price = np.exp(-self.r * self.T) * ht.mean()
        print(self.price)