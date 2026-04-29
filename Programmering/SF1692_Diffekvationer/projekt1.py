import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

getcontext().prec = 50

def deriv(y):
    if y < 0:
        return (-y).sqrt()
    return y.sqrt()

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

def analytisk(t0, t_slut, t1, t2, h):
    t = Decimal(t0)
    t_slut = Decimal(t_slut)
    t1 = Decimal(t1)
    t2 = Decimal(t2)
    h = Decimal(h)

    tlista = []
    ylista = []

    while t <= t_slut:
        if t <= t1:
            y = Decimal(-((t - t1) ** 2) / 4)
        elif t1 < t < t2:
            y = Decimal(0)
        else:  # t >= t2
            y = Decimal(((t - t2) ** 2) / 4)

        tlista.append(t)
        ylista.append(y)
        t += h

    return tlista, ylista

def tid_fastnar(y0, t0, t_slut, h, tröskel=Decimal("1e-6")):
    tlista, ylista = rk4(y0, t0, t_slut, h)
    t_fastnar = None
    t_loss = None
    fastna = False

    for t, y in zip(tlista, ylista):
        #första gången abs(y) går under tröskeln: fastnar
        if not fastna and abs(y) <= tröskel:
            fastna = True
            t_fastnar = Decimal(t)
        #första gången efter fastnandet som y går över tröskeln: lossnar
        elif fastna and y > tröskel:
            t_loss = Decimal(t)
            break

    if t_fastnar is not None:
        return t_fastnar, t_loss  #t_loss kan vara None om den aldrig lossnar
    else:
        return None



if __name__ == "__main__":
    #y(0) = 0
    tlista0, ylista0 = rk4(y0=Decimal("0"), t0=Decimal("0"), t_slut=Decimal("100"), h=Decimal("0.01"))

    #y(0) = "nära" 0 = 1e-20
    tlista1, ylista1 = rk4(y0=Decimal("1e-20"), t0=Decimal("0"), t_slut=Decimal("100"), h=Decimal("0.01"))

    epsilon = "1e-100"
    t_fastnar, t_loss = tid_fastnar(y0=(Decimal("-1")+Decimal(epsilon)), t0=Decimal("-1"), t_slut=Decimal("10"), h=Decimal("0.0001"))
    print(f"Första gång abs(y) <= 1e-6 vid t = {t_fastnar} och y > 1e-6 vid t = {t_loss}")

    #analytisk lösn
    tlista_analytisk, ylista_analytisk = analytisk(Decimal("-100"), Decimal("100"), Decimal("-20"), Decimal("20"), Decimal("0.001"))

    #plotta
    plt.plot(tlista0, ylista0, label="numerisk (RK4): y(0)=0")
    plt.plot(tlista1, ylista1, label="numerisk (RK4): y(0)=1e-6")
    plt.plot(tlista_analytisk, ylista_analytisk, "y-", label="analytisk: t1 = -20, t2 = 20")


    plt.xlabel("t")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()
