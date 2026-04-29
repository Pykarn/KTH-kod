from decimal import Decimal, getcontext
import matplotlib.pyplot as plt

getcontext().prec = 30

def derive(u1, u2, u3, u4):
    # u1 = x, u2 = y, u3 = vx, u4 = vy
    r2 = u1*u1 + u2*u2
    r = r2.sqrt()
    r3 = r2 * r

    ax = -u1 / r3
    ay = -u2 / r3
 
    #returnerar (u1', u2', u3', u4') = (x', y', vx', vy') = (vx, vy, ax, ay)
    return u3, u4, ax, ay

def euler(u1_0, u2_0, u3_0, u4_0, t0, t_slut, h):

    u1 = Decimal(u1_0)   #x
    u2 = Decimal(u2_0)   #y
    u3 = Decimal(u3_0)   #vx (x')
    u4 = Decimal(u4_0)   #vy (y')
    t = Decimal(t0)
    h = Decimal(h)

    xlista = [u1]
    ylista = [u2]
    tlista = []
    energilista = []

    while t < t_slut:

        r = (u1*u1 + u2*u2).sqrt()
        E = Decimal(0.5)*(u3*u3 + u4*u4) - Decimal(1)/r
        energilista.append(E)

        u3, u4, ax, ay = derive(u1, u2, u3, u4)

        u1 = u1 + h*u3
        u2 = u2 + h*u4
        u3 = u3 + h*ax
        u4 = u4 + h*ay
        t = t + h

        tlista.append(t)
        xlista.append(u1)
        ylista.append(u2)



    return xlista, ylista, energilista, tlista

def rk4(u1_0, u2_0, u3_0, u4_0, t0, t_slut, h):
    u1 = Decimal(u1_0)   #x
    u2 = Decimal(u2_0)   #y
    u3 = Decimal(u3_0)   #vx (x')
    u4 = Decimal(u4_0)   #vy (y')
    t = Decimal(t0)
    h = Decimal(h)

    xlista = [u1]
    ylista = [u2]
    tlista = []
    energilista = []

    while t < t_slut:

        r = (u1*u1 + u2*u2).sqrt()
        E = Decimal(0.5)*(u3*u3 + u4*u4) - Decimal(1)/r
        energilista.append(E)

        #k1
        k1u1, k1u2, k1u3, k1u4 = derive(u1, u2, u3, u4)
        #k2
        k2u1, k2u2, k2u3, k2u4 = derive(u1 + h*k1u1/2, u2 + h*k1u2/2, u3 + h*k1u3/2, u4 + h*k1u4/2)
        #k3
        k3u1, k3u2, k3u3, k3u4 = derive(u1 + h*k2u1/2, u2 + h*k2u2/2, u3 + h*k2u3/2, u4 + h*k2u4/2)
        #k4
        k4u1, k4u2, k4u3, k4u4 = derive(u1 + h*k3u1,   u2 + h*k3u2,   u3 + h*k3u3,   u4 + h*k3u4)

       
        u1 = u1 + h*(k1u1 + 2*k2u1 + 2*k3u1 + k4u1)/Decimal(6)
        u2 = u2 + h*(k1u2 + 2*k2u2 + 2*k3u2 + k4u2)/Decimal(6)
        u3 = u3 + h*(k1u3 + 2*k2u3 + 2*k3u3 + k4u3)/Decimal(6)
        u4 = u4 + h*(k1u4 + 2*k2u4 + 2*k3u4 + k4u4)/Decimal(6)
        t = t + h

        tlista.append(t)
        xlista.append(u1)
        ylista.append(u2)

    return xlista, ylista, energilista, tlista

#semi-implicit Euler
def symplectic_euler(u1_0, u2_0, u3_0, u4_0, t0, t_slut, h):
    u1 = Decimal(u1_0)  
    u2 = Decimal(u2_0)   
    u3 = Decimal(u3_0)   
    u4 = Decimal(u4_0)   
    t = Decimal(t0)
    h = Decimal(h)

    xlista = [u1]
    ylista = [u2]
    tlista = []
    energilista = []

    while t < t_slut:
        r = (u1*u1 + u2*u2).sqrt()
        E = Decimal(0.5)*(u3*u3 + u4*u4) - Decimal(1)/r
        energilista.append(E)
        
        _, _, ax, ay = derive(u1, u2, u3, u4)

        #uppdatera hastighet
        u3 = u3 + h*ax
        u4 = u4 + h*ay

        #uppdatera position
        u1 = u1 + h*u3
        u2 = u2 + h*u4
        
        t = t + h

        tlista.append(t)
        xlista.append(u1)
        ylista.append(u2)

    return xlista, ylista, energilista, tlista


#beräkna totala energin för systemet
def total_energy(u1, u2, u3, u4):
    #G=1, M_sol=1.
    #kinetisk energi
    kinetic = (u3*u3 + u4*u4) / Decimal(2)

    #potentiell energi från solen
    r_sol2 = u1*u1 + u2*u2
    r_sol = r_sol2.sqrt()
    pot_sol = -Decimal(1) / r_sol

    #total energi
    E_total = kinetic + pot_sol
    return E_total

if __name__ == "__main__":
    #startvillkor för position och hastighet och steglängd
    x0, y0 = Decimal("1"), Decimal("0")
    vx0, vy0 = Decimal("0"), Decimal("1.3")
    t0 = Decimal("0")
    t_slut = Decimal("100")
    h = Decimal("0.01")

    xlista_euler, ylista_euler, energilista_euler, tlista_euler = euler(x0, y0, vx0, vy0, t0, t_slut, h)
    xlista, ylista, energilista_rk4, tlista = rk4(x0, y0, vx0, vy0, t0, t_slut, h)
    xlista_symp, ylista_symp, energilista_symp, tlista_symp = symplectic_euler(x0, y0, vx0, vy0, t0, t_slut, h)

    print(f"deltaE för euler = {abs(energilista_euler[0]-energilista_euler[-1])}")
    print(f"deltaE för rk4 = {abs(energilista_rk4[0]-energilista_rk4[-1])}")
    print(f"deltaE för symplectic euler = {abs(energilista_symp[0]-energilista_symp[-1])}")

    #plotta
    plt.figure()
    plt.axis("equal")
    plt.gca().set_aspect("equal")

    plt.plot(xlista_euler, ylista_euler, "-.",label="Bana euler")

    plt.plot(xlista_symp, ylista_symp, "g--", label="Bana symp euler")
    plt.plot(xlista, ylista,"orange",label="Bana rk4")
    plt.plot(0,0,"yo",label="Solen")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()
    
    plt.figure()
    
    plt.plot(tlista_symp, energilista_symp,label="symp euler")
    plt.plot(tlista, energilista_rk4, label="RK4")
    plt.xlabel("t")
    plt.ylabel("E")
    plt.legend()
    
    plt.grid(True)
    plt.show()


    #felanalys efter fem varv
    t_end = Decimal("200")  #ungefär fem varv
    hs = [h, h/Decimal("2"), h/Decimal("4"), h/Decimal("8"), h/Decimal("16")]

    #referenslösning med mycket litet h
    x_ref, y_ref, _, _ = rk4(Decimal("1"), Decimal("0"), Decimal("0"), Decimal("1.3"), Decimal("0"), t_end, Decimal("0.0001"))

    fel = []
    for h_val in hs:
        x_num, y_num, _, _ = rk4(Decimal("1"), Decimal("0"), Decimal("0"), Decimal("1.3"), Decimal("0"), t_end, h_val)
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
    plt.loglog([hh for hh in hs], [fe for fe in fel], 'o-', label="RK4, fel i position")
    plt.loglog([hh for hh in hs], [fe for fe in fel_ref_1], '--', label='Referens lutning 1')
    plt.loglog([hh for hh in hs], [fe for fe in fel_ref_4], '--', label='Referens lutning 4')
    plt.xlabel('Steglängd h')
    plt.ylabel('Absolut fel E_abs')
    plt.grid(True, which='both', ls='--')
    plt.legend()
    plt.show()
