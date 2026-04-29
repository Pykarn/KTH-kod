from decimal import Decimal, getcontext
import matplotlib.pyplot as plt

getcontext().prec = 30

#kod för rörlig sol
def derive(u1, u2, u3, u4, v1, v2, v3, v4, m1, m2):
    #u1,u2,u3,u4 = x,y,vx,vy för kropp 1
    #v1,v2,v3,v4 = x,y,vx,vy för kropp 2
    dx = v1 - u1
    dy = v2 - u2
    r2 = dx*dx + dy*dy
    r = r2.sqrt()
    r3 = r2 * r

    axu =  m2 * dx / r3
    ayu =  m2 * dy / r3

    axv = -m1 * dx / r3
    ayv = -m1 * dy / r3

    return u3, u4, axu, ayu, v3, v4, axv, ayv


def rk4(u1_0, u2_0, u3_0, u4_0, v1_0, v2_0, v3_0, v4_0, m1, m2, t0, t_slut, h):
    u1 = Decimal(u1_0)
    u2 = Decimal(u2_0)
    u3 = Decimal(u3_0)
    u4 = Decimal(u4_0)
    v1 = Decimal(v1_0)
    v2 = Decimal(v2_0)
    v3 = Decimal(v3_0)
    v4 = Decimal(v4_0)
    t = Decimal(t0)
    h = Decimal(h)

    xlista1 = [u1]
    ylista1 = [u2]
    xlista2 = [v1]
    ylista2 = [v2]
    tlista = [t]
    energilista = []
    dx = v1 - u1
    dy = v2 - u2
    r = (dx*dx + dy*dy).sqrt()
    T = Decimal("0.5")*(m1*(u3*u3 + u4*u4) + m2*(v3*v3 + v4*v4))
    V = - (m1*m2) / r
    energilista = [T+V]

    while t < t_slut:
        

        
        #k1
        k1u1, k1u2, k1u3, k1u4, k1v1, k1v2, k1v3, k1v4 = derive(
        u1, u2, u3, u4, 
        v1, v2, v3, v4, 
        m1, m2)

        #k2
        k2u1, k2u2, k2u3, k2u4, k2v1, k2v2, k2v3, k2v4 = derive(
        u1 + h*k1u1/2, u2 + h*k1u2/2, u3 + h*k1u3/2, u4 + h*k1u4/2,
        v1 + h*k1v1/2, v2 + h*k1v2/2, v3 + h*k1v3/2, v4 + h*k1v4/2, 
        m1, m2)

        #k3
        k3u1, k3u2, k3u3, k3u4, k3v1, k3v2, k3v3, k3v4 = derive(
        u1 + h*k2u1/2, u2 + h*k2u2/2, u3 + h*k2u3/2, u4 + h*k2u4/2,
        v1 + h*k2v1/2, v2 + h*k2v2/2, v3 + h*k2v3/2, v4 + h*k2v4/2, 
        m1, m2)

        #k4
        k4u1, k4u2, k4u3, k4u4, k4v1, k4v2, k4v3, k4v4 = derive(
        u1 + h*k3u1, u2 + h*k3u2, u3 + h*k3u3, u4 + h*k3u4,
        v1 + h*k3v1, v2 + h*k3v2, v3 + h*k3v3, v4 + h*k3v4, 
        m1, m2)

        #kropp 1
        u1 = u1 + h*(k1u1 + 2*k2u1 + 2*k3u1 + k4u1)/Decimal(6)
        u2 = u2 + h*(k1u2 + 2*k2u2 + 2*k3u2 + k4u2)/Decimal(6)
        u3 = u3 + h*(k1u3 + 2*k2u3 + 2*k3u3 + k4u3)/Decimal(6)
        u4 = u4 + h*(k1u4 + 2*k2u4 + 2*k3u4 + k4u4)/Decimal(6)

        #kropp 2
        v1 = v1 + h*(k1v1 + 2*k2v1 + 2*k3v1 + k4v1)/Decimal(6)
        v2 = v2 + h*(k1v2 + 2*k2v2 + 2*k3v2 + k4v2)/Decimal(6)
        v3 = v3 + h*(k1v3 + 2*k2v3 + 2*k3v3 + k4v3)/Decimal(6)
        v4 = v4 + h*(k1v4 + 2*k2v4 + 2*k3v4 + k4v4)/Decimal(6)

        t = t + h

        dx = v1 - u1
        dy = v2 - u2
        r = (dx*dx + dy*dy).sqrt()
        T = Decimal("0.5")*(m1*(u3*u3 + u4*u4) + m2*(v3*v3 + v4*v4))
        V = - (m1*m2) / r
        energilista.append(T + V)

        tlista.append(t)
        xlista1.append(u1)
        ylista1.append(u2)
        xlista2.append(v1)
        ylista2.append(v2)

    return xlista1, ylista1, xlista2, ylista2, energilista, tlista

def semi_implicit_euler(u1_0, u2_0, u3_0, u4_0, v1_0, v2_0, v3_0, v4_0, m1, m2, t0, t_slut, h):
    u1 = Decimal(u1_0)
    u2 = Decimal(u2_0)
    u3 = Decimal(u3_0)
    u4 = Decimal(u4_0)
    v1 = Decimal(v1_0)
    v2 = Decimal(v2_0)
    v3 = Decimal(v3_0)
    v4 = Decimal(v4_0)
    t = Decimal(t0)
    h = Decimal(h)

    xlista1 = [u1]
    ylista1 = [u2]
    xlista2 = [v1]
    ylista2 = [v2]
    energilista = []
    tlista = [t]

    dx = v1 - u1
    dy = v2 - u2
    r = (dx*dx + dy*dy).sqrt()
    T = Decimal("0.5")*(m1*(u3*u3 + u4*u4) + m2*(v3*v3 + v4*v4))
    V = - (m1*m2) / r
    energilista = [T+V]

    while t < t_slut:
        # accelerationen beräknas med nuvarande position
        _, _, axu, ayu, _, _, axv, ayv = derive(u1, u2, u3, u4, v1, v2, v3, v4, m1, m2)

        # uppdatera hastigheter först (symplektiskt steg)
        u3 = u3 + h * axu
        u4 = u4 + h * ayu
        v3 = v3 + h * axv
        v4 = v4 + h * ayv

        # sedan positioner
        u1 = u1 + h * u3
        u2 = u2 + h * u4
        v1 = v1 + h * v3
        v2 = v2 + h * v4

        t = t + h

        dx = v1 - u1
        dy = v2 - u2
        r = (dx*dx + dy*dy).sqrt()
        T = Decimal("0.5")*(m1*(u3*u3 + u4*u4) + m2*(v3*v3 + v4*v4))
        V = - (m1*m2) / r
        energilista.append(T + V)

        xlista1.append(u1)
        ylista1.append(u2)
        xlista2.append(v1)
        ylista2.append(v2)
        tlista.append(t)

    return xlista1, ylista1, xlista2, ylista2, energilista, tlista

#beräkna totala energin för systemet
def total_energy(u1, u2, u3, u4, v1, v2, v3, v4, m1, m2):
    dx = v1 - u1
    dy = v2 - u2
    r2 = dx*dx + dy*dy
    r = r2.sqrt()

    T = Decimal('0.5') * m1 * (u3*u3 + u4*u4) \
      + Decimal('0.5') * m2 * (v3*v3 + v4*v4)

    V = -m1 * m2 / r

    return T + V

if __name__ == "__main__":
    m1 = Decimal("1") #solens massa
    m2 = Decimal("0.1") #planetens massa
    #planet
    v1_0 = Decimal("1") #xplanet
    v2_0 = Decimal("0") #yplanet
    v3_0 = Decimal("0") #vxplanet
    v4_0 = Decimal("1") #vyplanet
    #sol, för en gemensamm tyngdpunkt:
    u1_0 = -m2/m1 * v1_0 # xsol
    u2_0 = -m2/m1 * v2_0 # ysol
    u3_0 = -m2/m1 * v3_0 # vxsol
    u4_0 = -m2/m1 * v4_0 # vysol
        

    t0 = Decimal("0")
    t_slut = Decimal("10000")
    h = Decimal("0.1")

    xlista1, ylista1, xlista2, ylista2, energilista, tlista = rk4(
        u1_0, u2_0, u3_0, u4_0,
        v1_0, v2_0, v3_0, v4_0,
        m1, m2, t0, t_slut, h
    )

    xlista1_s, ylista1_s, xlista2_s, ylista2_s, energilista_s, tlista_s = semi_implicit_euler(
        u1_0, u2_0, u3_0, u4_0,
        v1_0, v2_0, v3_0, v4_0,
        m1, m2, t0, t_slut, h
    )


    
    #plotta
    plt.figure()
    plt.axis("equal")
    plt.plot(xlista1_s, ylista1_s, "g--", label="solen (m1)(Symp)")
    plt.plot(xlista2_s, ylista2_s, "r--", label="planeten (m2)(Symp)")
    plt.plot(xlista1, ylista1, label="solen (m1)(RK4)")
    plt.plot(xlista2, ylista2, label="planeten (m2)(RK4)")
    plt.legend(loc="upper left")
    plt.xlabel("x")
    plt.ylabel("y")
    
    plt.grid(True)
    plt.show()

    
    plt.figure()
    plt.plot(tlista_s, energilista_s, label="Symp Euler")
    plt.plot(tlista, energilista, label="RK4")
    plt.xlabel("t")
    plt.ylabel("E")
    plt.grid(True)
    plt.show()


    #felanalys efter fem varv
    t_end = Decimal("200")  #ungefär fem varv
    hs = [h, h/Decimal("2"), h/Decimal("4"), h/Decimal("8"), h/Decimal("16")]

    #referenslösning med mycket litet h
    x_ref, y_ref, _, _, _, _ = semi_implicit_euler(
        u1_0, u2_0, u3_0, u4_0,
        v1_0, v2_0, v3_0, v4_0,
        m1, m2, t0, t_end, Decimal("0.0001")
    )
    fel = []
    for h_val in hs:
        x_num, y_num, _, _, _, _ = semi_implicit_euler(
        u1_0, u2_0, u3_0, u4_0,
        v1_0, v2_0, v3_0, v4_0,
        m1, m2, t0, t_end, h_val
    )
        dx = x_num[-1] - x_ref[-1]
        dy = y_num[-1] - y_ref[-1]
        E_abs = (dx*dx + dy*dy).sqrt()
        fel.append(E_abs)

    fel_ref_1 = [fel[-1] * (hh / hs[-1])**1 for hh in hs]
    fel_ref_4 = [fel[-1] * (hh / hs[-1])**4 for hh in hs]
    plt.figure()
    plt.plot(x_num, y_num)
    plt.show()
    #loglog plot
    plt.figure()
    plt.loglog([hh for hh in hs], [fe for fe in fel], 'o-', label="Semi-implicit euler, fel i position")
    plt.loglog([hh for hh in hs], [fe for fe in fel_ref_1], '--', label='Referens lutning 1')
    plt.loglog([hh for hh in hs], [fe for fe in fel_ref_4], '--', label='Referens lutning 4')
    plt.xlabel('Steglängd h')
    plt.ylabel('Absolut fel E_abs')
    plt.grid(True, which='both', ls='--')
    plt.legend()
    plt.show()