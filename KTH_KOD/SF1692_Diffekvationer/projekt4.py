from decimal import Decimal, getcontext
import matplotlib.pyplot as plt

getcontext().prec = 80

def deriv(y1, y2):
    y1prim = y2
    y2prim = -y1
    return y1prim, y2prim

def rk4(y1_0, y2_0, t0, t_slut, h):
    y1 = Decimal(y1_0)
    y2 = Decimal(y2_0)
    t = Decimal(t0)
    h = Decimal(h)

    tlista = [t]
    ylista = [y1]

    while t < t_slut:
        k1y1, k1y2 = deriv(y1, y2)
        k2y1, k2y2 = deriv(y1 + h*k1y1/Decimal("2"), y2 + h*k1y2/Decimal("2"))
        k3y1, k3y2 = deriv(y1 + h*k2y1/Decimal("2"), y2 + h*k2y2/Decimal("2"))
        k4y1, k4y2 = deriv(y1 + h*k3y1,   y2 + h*k3y2)

        y1 = y1 + h*(k1y1 + Decimal("2")*k2y1 + Decimal("2")*k3y1 + k4y1)/Decimal("6")
        y2 = y2 + h*(k1y2 + Decimal("2")*k2y2 + Decimal("2")*k3y2 + k4y2)/Decimal("6")
        t = t + h

        tlista.append(t)
        ylista.append(y1)

    return tlista, ylista

def hitta_nollställe_linjär(tlista, ylista):
    for i in range(1, len(ylista)):
        if ylista[i-1] * ylista[i] < 0:
            t1, t2 = tlista[i-1], tlista[i]
            y1, y2 = ylista[i-1], ylista[i]
            #linjär interpolation mellan punkterna
            return t1 - y1 * (t2 - t1) / (y2 - y1)
    return None





def hitta_nollställe_kvadratisk(tlista, ylista):
    for i in range(1, len(ylista)-1):
        if ylista[i-1] * ylista[i] < 0:
            t0, y0 = tlista[i-1], ylista[i-1]
            t1, y1 = tlista[i],   ylista[i]
            t2, y2 = tlista[i+1], ylista[i+1]

            nämnare = (t0 - t1) * (t0 - t2) * (t1 - t2)
            if nämnare == Decimal("0"):
                continue

            a = (y0*(t1-t2) + y1*(t2-t0) + y2*(t0-t1)) / nämnare
            b = (y0*(t2**Decimal("2") - t1**Decimal("2")) + y1*(t0**Decimal("2") - t2**Decimal("2")) + y2*(t1**Decimal("2") - t0**Decimal("2"))) / nämnare
            c = (y0*t1*t2*(t1-t2) + y1*t2*t0*(t2-t0) + y2*t0*t1*(t0-t1)) / nämnare

            if a == 0:
                continue

            temp = (b/(Decimal("2")*a))**Decimal("2") - c/a
            if temp < 0:
                continue

            rotdelen = temp**Decimal("0.5")

            r1 = -b/(Decimal("2")*a) + rotdelen
            r2 = -b/(Decimal("2")*a) - rotdelen

            if t0 <= r1 <= t2:
                return r1
            elif t0 <= r2 <= t2:
                return r2
    return None

if __name__ == "__main__":
    h = Decimal("25e-4")
    tlista, ylista = rk4(Decimal("1"), Decimal("0"), Decimal("0"), Decimal("2"), h/Decimal("32"))
    nollställe_h = hitta_nollställe_linjär(tlista, ylista)

    pi = Decimal("3.141592653589793238462643383279")
    pi_uppskattning = nollställe_h * Decimal("2")

    print("t(0) ≈", nollställe_h)
    print("pi ≈", pi_uppskattning)

    pistring = str(pi)
    pi_uppskattning_string = str(pi_uppskattning)
    i = 0
    for digit in pistring:
        if i >= len(pi_uppskattning_string):
            break
        if digit == pi_uppskattning_string[i]:
            i += 1
        else:
            break

    print(f"uppskattning ger {i-2} korrekta decimaler")

    pi_felet = abs(pi_uppskattning - pi)
    print(f"absolut felet vid pi/2: {pi_felet}")


    #kör RK4 till t ≈ 1000
    t_slut = Decimal("1010") #köra t till lite mer än 1000
    tlista, ylista = rk4(Decimal("1"), Decimal("0"), Decimal("0"), t_slut, h/Decimal("32"))


    j = 0
    for i in range(1, len(ylista)):
        if ylista[i-1] * ylista[i] < 0:  # korsning
            j += 1
            if j == 319:
                noll = hitta_nollställe_linjär([tlista[i-1], tlista[i]], [ylista[i-1], ylista[i]])
                nollställe_närmast = noll

    #hitta nollställe som är närmast 1000
    #det är det 318:nd som är närmast i teorin
    #pi/2 + npi = 1000
    # n = (1000 - pi/2)/pi = 317,80988618
    # n = 318


    print(f"Nollstället närmast t ≈ 1000: {nollställe_närmast}")

    pi_uppskattning_1000 = (nollställe_närmast)/(Decimal("318.5"))
    pistring = str(pi)
    pi_uppskattning_string_1000= str(pi_uppskattning_1000)
    i = 0
    for digit in pistring:
        if i >= len(pi_uppskattning_string_1000):
            break
        if digit == pi_uppskattning_string_1000[i]:
            i += 1
        else:
            break
    print(f"pi uppskattning närmast 1000 = {pi_uppskattning_1000}")
    print(f"uppskattning ger {i-2} korrekta decimaler")

    pi_felet_1000 = abs(pi_uppskattning_1000 - pi)
    print(f"absolut felet vid pi/2: {pi_felet_1000}")



    n = Decimal("318")
    nollställe_exakt_närmast_1000 = pi/Decimal("2") + n*pi


    #lista med steglängder
    hs = [h * (Decimal("0.5") ** Decimal(i)) for i in range(6)]


    #första nollstället
    fel_första = []
    for hi in hs:
        tlista_hi, ylista_hi = rk4(Decimal("1"), Decimal("0"), Decimal("0"), Decimal("2"), hi)
        nollställe_hi = hitta_nollställe_linjär(tlista_hi, ylista_hi)
        E_abs = abs(nollställe_hi - pi/Decimal("2"))
        fel_första.append(E_abs)

    #referenslinje lutning 3
    fel_ref_3_första = [fel_första[-1] * (hh/hs[-1])**3 for hh in hs]

    #plotta
    plt.figure()
    plt.loglog([float(hh) for hh in hs], [float(fe) for fe in fel_första], 'o-', label="Numeriskt fel")
    plt.loglog([float(hh) for hh in hs], [float(fe) for fe in fel_ref_3_första], '--', label="Referens lutning 3")
    plt.xlabel("Steglängd h")
    plt.ylabel("Absolut fel E_abs")
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.show()

    #nollstället nära 1000
    fel_1000 = []
    t_slut_1000 = Decimal("1100")
    for hi in hs:
        tlista_hi, ylista_hi = rk4(Decimal("1"), Decimal("0"), Decimal("0"), t_slut_1000, hi)
        
        #hitta nollstället
        j = 0
        for i in range(1, len(ylista_hi)):
            if ylista_hi[i-1] * ylista_hi[i] < 0:  # korsning
                j += 1
                if j == 319:
                    noll_hi = hitta_nollställe_linjär([tlista_hi[i-1], tlista_hi[i]], [ylista_hi[i-1], ylista_hi[i]])
                    nollstället_närmast_hi = noll_hi

        #välj nollstället närmast 1000
        #alltså det 318:nd nollstället ska vara närmast
        E_abs = abs(nollstället_närmast_hi - nollställe_exakt_närmast_1000)
        fel_1000.append(E_abs)

    #referenslinje lutning 3
    fel_ref_3_1000 = [fel_1000[-1] * (hh/hs[-1])**3 for hh in hs]

    #plotta
    plt.figure()
    plt.loglog([float(hh) for hh in hs], [float(fe) for fe in fel_1000], 'o-', label="Nollstället nära 1000")
    plt.loglog([float(hh) for hh in hs], [float(fe) for fe in fel_ref_3_1000], '--', label="Referens lutning 3")
    plt.xlabel("Steglängd h")
    plt.ylabel("Absolut fel E_abs")
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.show()
