import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

getcontext().prec = 50

def deriv(y):
    return y

def rk4(y0, t0, t_slut, h):
    y = Decimal(y0)
    t = Decimal(t0)
    h = Decimal(h)

    tlista = [t]
    ylista = [y]

    while t < t_slut:
        k1 = deriv(y)
        k2 = deriv(y + h*k1/2)
        k3 = deriv(y + h*k2/2)
        k4 = deriv(y + h*k3)

        y = y + h*(k1 + 2*k2 + 2*k3 + k4)/Decimal(6)
        t = t + h
        tlista.append(t)
        ylista.append(y)

    return tlista, ylista

if __name__ == "__main__":
    h = Decimal("1e-5")
    #y(0) = 35
    N = Decimal("35")
    k = Decimal("5")

    tlista0, ylista0 = rk4(y0=N, t0=Decimal("0"), t_slut=Decimal("2")**k, h=h)
    
    hs = [Decimal(h), Decimal(h/2), Decimal(h/4), Decimal(h/8), Decimal(h/16)]
    ks = [1, 2, 3]

    for k in ks:
        t_slut = Decimal(2) ** k
        fel = []

        for h in hs:
            _, ylista = rk4(y0=N, t0=Decimal(0), t_slut=t_slut, h=h)
            teori = N * t_slut.exp()
            E_abs = abs(teori - ylista[-1])
            fel.append(E_abs)
            print(f"k={k}, h={h}, E_abs={E_abs}")

        plt.figure()
        plt.loglog([h for h in hs], [e for e in fel], 'o-', label=f"k={k}")
        plt.xlabel("Steglängd h")
        plt.ylabel("Absolutfel E_abs")
        plt.title(f"Loglog-plot av fel för y(2^{k})")
        plt.grid(True, which="both")

        #referenslinje med lutning 4
        h0 = float(hs[-1])
        E0 = float(fel[-1])
        h_ref = [float(hs[0]), float(hs[-1])]
        E_ref = [E0 * (float(hs[0])/h0)**4, E0 * (float(hs[-1])/h0)**4]
        plt.loglog(h_ref, E_ref, '--', label="Referenslinje lutning 4")

        plt.legend()
        plt.show()




"""  
y(2^1) = 258.61696346257275795302185865207019898413918109018
teoretiska svaret = 258.61696346257275795306496112012527346131104496931
absolut fel = 4.310246805507447717186387913E-20

y(2^2) = 1910.9352511600483677332221689912081209235147096341
teoretiska svaret = 1910.9352511600483677338591421001307440976757963515
absolut fel = 6.369731089226231741610867174E-19

y(2^3) = 104333.52954646048961595616837411503216652932600559
teoretiska svaret = 104333.52954646048961602572348085110358145887786965
absolut fel = 6.955510673607141492955186406E-17

y(2^4) = 311013868.21777554228629114922542189827821464932678
teoretiska svaret = 311013868.21777554228670583092735076227809519376498
absolut fel = 4.1468170192886399988054443820E-13

y(2^5) = 2763703606393824.3306268609773604434713577441920166
teoretiska svaret = 2763703606393824.3306342307922287878476984668290373
absolut fel = 0.0000073698148683443763407226370207

y(2^6) = 218230217828406590900659470016.49083075195168574518
teoretiska svaret = 218230217828406590901823354812.49644106909871461825
absolut fel = 1163884796.00561031714702887307


Dessa numeriska uppskattningar har minst två decimalers noggranhet

Numeriska värden
h = 0.00001

k=1, y(2^1) = 258.61696346257275795302185865207019898413918109018
k=2, y(2^2) = 1910.9352511600483677332221689912081209235147096341
k=3, y(2^3) = 104333.52954646048961595616837411503216652932600559
k=4, y(2^4) = 311013868.21777554228629114922542189827821464932678
k=5, y(2^5) = 2763703606393824.3306268609773604434713577441920166
k=6, y(2^6) = 218230217828406590900659470016.49083075195168574518

teoretiska värden
y(t) = Ne^t , N = 35
k=1, y(2^1) = 258.61696346257275795306496112012527346131104496931
k=2, y(2^2) = 1910.9352511600483677338591421001307440976757963515
k=3, y(2^3) = 104333.52954646048961602572348085110358145887786965
k=4, y(2^4) = 311013868.21777554228670583092735076227809519376498
k=5, y(2^5) = 2763703606393824.3306342307922287878476984668290373
k=6, y(2^6) = 218230217828406590901823354812.49644106909871461825

"""