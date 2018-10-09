import numpy as np
#TODO: 活動量sをオンボーディングからとるようにする…が、なんて聞けばいいのかわからんし、調べるのめんどいのでfuture work

def _get_C(sex, age):
    # 参考: http://www-tap.scphys.kyoto-u.ac.jp/~keiju/daietto.html
    d = {
        "男性":[
            (15, (20.9, 363)),
            (18, (18.6, 347)),
            (30, (17.3, 336)),
            (50, (16.7, 301)),
            (70, (16.3, 268))
        ],
        "女性":[
            (15, (19.7, 289)),
            (18, (18.3, 272)),
            (30, (16.8, 263)),
            (50, (16.0, 247)),
            (70, (16.1, 224))
        ]
    }
    _C=d[sex][0][1]
    for a,C in d[sex]:
        if age > a:
            _C = C
    return _C

def get_E_in_by_M0_N(sex, age, goal_delta=None, Mf=None, M0=None):
    Mf = 1.71*1.71*22.2 if Mf is None else Mf
    t = 365*2 if goal_delta is None else goal_delta
    s = 1.5
    alpha, beta = _get_C(sex, age)
    R = 7000
    T = R/s/alpha
    T_alpha = np.exp(-t/T)
    A = (Mf - M0*T_alpha) / (1-T_alpha)
    E_in = (A*alpha + beta)*s

    return E_in

def get_terminal_weight(sex, age, E_in):
    alpha, beta = _get_C(sex, age)
    R = 7000
    s = 1.5
    Mf = (E_in - beta*s) / (alpha*s)

    return Mf

def get_ideal_series_with_E_in(sex, age, M0, N, E_in):
    t = np.linspace(1,N,N)

    alpha, beta = _get_C(sex, age)
    s = 1.5 # やや低い
    R = 7000 # kcal/kg
    Mf = (E_in - beta*s) / (s*alpha)
    T = R / (s*alpha)

    w = Mf - (Mf - M0)*np.exp(-t/T)

    return w

# def get_ideal_series_with_Mf(sex, age, M0, N, Mf):
#     t = np.linspace(1,N,N)

#     alpha, beta = _get_C(sex, age)
#     s = 1.5 # やや低い
#     R = 7000 # kcal/kg
#     T = R / (s*alpha)

#     w = Mf - (Mf - M0)*np.exp(-t/T)

#     return w


def get_equilibrium_E_in(sex, age, weight):
    s = 1.5 # やや低い
    alpha, beta = _get_C(sex, age)
    E_in_p = weight*s*alpha + beta*s

    return E_in_p


if __name__ == "__main__":
  sex = "男性"
  age = 28
