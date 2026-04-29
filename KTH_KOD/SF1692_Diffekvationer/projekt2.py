import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

getcontext().prec = 30

def deriv(y):
    return y**2

def altderiv(y):
    C = Decimal("4e5")
    return (y**2)*C

def rk4(y0, t0, t_slut, h):
    y = Decimal(y0)
    t = Decimal(t0)
    h = Decimal(h)

    y_max = Decimal("1e100") #definiera explodera till 1e12

    tlista = [t]
    ylista = [y]

    while t < t_slut:

        if y >= y_max:
            print(f"det 'smäller' vid taket y = {y_max} vid t = {t} för h = {h}")
            break

        k1 = deriv(y)
        k2 = deriv(y + h*k1/2)
        k3 = deriv(y + h*k2/2)
        k4 = deriv(y + h*k3)

        y = y + h*(k1 + 2*k2 + 2*k3 + k4)/Decimal(6)
        t = t + h

        tlista.append(t)
        ylista.append(y)

    return tlista, ylista
def alt(y0, t0, t_slut, h):
    y = Decimal(y0)
    t = Decimal(t0)
    h = Decimal(h)


    tlista = [t]
    ylista = [y]

    while t < t_slut:

        if y > 0:
            print(f"y(t) = {y} > 0 för t = {t}")
            return tlista, ylista
        k1 = altderiv(y)
        k2 = altderiv(y + h*k1/2)
        k3 = altderiv(y + h*k2/2)
        k4 = altderiv(y + h*k3)

        y = y + h*(k1 + 2*k2 + 2*k3 + k4)/Decimal(6)
        # y = y + h*altderiv(y)
        t = t + h

        tlista.append(t)
        ylista.append(y)
    return tlista, ylista

    

if __name__ == "__main__":
    #y(0) = 35/100
    h = Decimal("0.001")
    hs = [h * (Decimal("0.5") ** Decimal(i)) for i in range(8)]
    for i in hs:
        tlista0, ylista0 = rk4(y0=Decimal("0.35"), t0=Decimal("0"), t_slut=Decimal("100"), h=i)
    
    #för djupt felaktig lösning
    #tlista_alt, ylista_alt = alt(y0=Decimal("-0.001"), t0=Decimal("0"), t_slut=Decimal("0.02"), h=Decimal("0.01"))
    

    # Rita grafer

    # plt.plot(tlista_alt, ylista_alt)
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.grid(True)
    # plt.show()

#analytisk "när det smäller" ca = 2.8571429

