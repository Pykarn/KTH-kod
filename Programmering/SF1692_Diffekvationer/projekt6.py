from decimal import Decimal, getcontext
import matplotlib.pyplot as plt
import math

getcontext().prec = 30


def derive(u1, u2, u3, u4, Jx, Jy, mJ):
     
    #u1 = x
    #u2 = y
    #u3 = vx
    #u4 = vy
    #(jx, jy) = Jupiters position
    #mJ = Jupiters massa
    
    #solens gravitation (dess position (0,0) och massa (1) är konstant)
    r2Sol = u1*u1 + u2*u2
    rSol = r2Sol.sqrt()
    r3Sol = r2Sol * rSol

    axSol = -u1 / r3Sol
    aySol = -u2 / r3Sol

    #jupiters gravitation
    #avståndet mellan rymdskepp och jupiter
    Dx = Jx - u1
    Dy = Jy - u2
    
    r2Jup = Dx*Dx + Dy*Dy
    rJup = r2Jup.sqrt()
    r3Jup = r2Jup * rJup

    axJup = mJ * Dx / r3Jup
    ayJup = mJ * Dy / r3Jup

    #tot ax och ay
    ax = axSol + axJup
    ay = aySol + ayJup

    #returnerar (u1', u2', u3', u4') = (x', y', vx', vy') = (vx, vy, ax, ay)
    return u3, u4, ax, ay

def deriveJ(Jx, Jy, Jvx, Jvy):
    r2J = Jx*Jx + Jy*Jy
    rJ = r2J.sqrt()
    r3J = r2J * rJ
    aJx = -Jx / r3J
    aJy = -Jy / r3J
    #returnerar (Jx', Jy', Jvx', Jvy') = (Jvx, Jvy, Jax, Jay)
    return Jvx, Jvy, aJx, aJy


def rk4(u1_0, u2_0, u3_0, u4_0, Jx_0, Jy_0, Jvx_0, Jvy_0, mJ, t0, t_slut, h):
    #rymdskepp
    u1 = Decimal(u1_0)   
    u2 = Decimal(u2_0)  
    u3 = Decimal(u3_0)  
    u4 = Decimal(u4_0)
    #Jupiter
    Jx = Decimal(Jx_0)  
    Jy = Decimal(Jy_0)  
    Jvx = Decimal(Jvx_0) 
    Jvy = Decimal(Jvy_0)

    t = Decimal(t0)
    h = Decimal(h)

    xlista = [u1]
    ylista = [u2]
    Jxlista = [Jx]
    Jylista = [Jy]

    E_lista = []
    tlista = [t]

    while t < t_slut:
        Dx = Jx - u1
        Dy = Jy - u2
        
        r2Jup = Dx*Dx + Dy*Dy
        rJup = r2Jup.sqrt()
        dist_to_J = rJup  #avstånd mellan rymdskepp och Jupiter

        if dist_to_J < Decimal("0.5"):
            h_eff = h / (Decimal("100"))  #minska steglängden lokalt
        else:
            h_eff = h  

        #Jupiter
        #k1
        k1Jx, k1Jy, k1Jvx, k1Jvy = deriveJ(Jx, Jy, Jvx, Jvy)
        #k2
        k2Jx, k2Jy, k2Jvx, k2Jvy = deriveJ(Jx + h_eff*k1Jx/2, Jy + h_eff*k1Jy/2, Jvx + h_eff*k1Jvx/2, Jvy + h_eff*k1Jvy/2)
        #k3
        k3Jx, k3Jy, k3Jvx, k3Jvy = deriveJ(Jx + h_eff*k2Jx/2, Jy + h_eff*k2Jy/2, Jvx + h_eff*k2Jvx/2, Jvy + h_eff*k2Jvy/2)
        #k4
        k4Jx, k4Jy, k4Jvx, k4Jvy = deriveJ(Jx + h_eff*k3Jx,   Jy + h_eff*k3Jy,   Jvx + h_eff*k3Jvx,   Jvy + h_eff*k3Jvy)

        #uppdatera jupiter
        Jx =  Jx +  h_eff*(k1Jx +  2*k2Jx +  2*k3Jx +  k4Jx)/Decimal(6)
        Jy =  Jy +  h_eff*(k1Jy +  2*k2Jy +  2*k3Jy +  k4Jy)/Decimal(6)
        Jvx = Jvx + h_eff*(k1Jvx + 2*k2Jvx + 2*k3Jvx + k4Jvx)/Decimal(6)
        Jvy = Jvy + h_eff*(k1Jvy + 2*k2Jvy + 2*k3Jvy + k4Jvy)/Decimal(6)


        #rymdskepp
        #k1
        k1u1, k1u2, k1u3, k1u4 = derive(u1, u2, u3, u4, Jx, Jy, mJ)
        #k2
        k2u1, k2u2, k2u3, k2u4 = derive(u1 + h_eff*k1u1/2, u2 + h_eff*k1u2/2, u3 + h_eff*k1u3/2, u4 + h_eff*k1u4/2, Jx + h_eff*Jvx/2, Jy + h_eff*Jvy/2, mJ)
        #k3
        k3u1, k3u2, k3u3, k3u4 = derive(u1 + h_eff*k2u1/2, u2 + h_eff*k2u2/2, u3 + h_eff*k2u3/2, u4 + h_eff*k2u4/2, Jx + h_eff*Jvx/2, Jy + h_eff*Jvy/2, mJ)
        #k4
        k4u1, k4u2, k4u3, k4u4 = derive(u1 + h_eff*k3u1,   u2 + h_eff*k3u2,   u3 + h_eff*k3u3,   u4 + h_eff*k3u4,   Jx + h_eff*Jvx,   Jy + h_eff*Jvy,   mJ)

        #uppdatera rymdskeppet
        u1 = u1 + h_eff*(k1u1 + 2*k2u1 + 2*k3u1 + k4u1)/Decimal(6)
        u2 = u2 + h_eff*(k1u2 + 2*k2u2 + 2*k3u2 + k4u2)/Decimal(6)
        u3 = u3 + h_eff*(k1u3 + 2*k2u3 + 2*k3u3 + k4u3)/Decimal(6)
        u4 = u4 + h_eff*(k1u4 + 2*k2u4 + 2*k3u4 + k4u4)/Decimal(6)

        #beräkna energi relativt solen
        E_now = total_energy(u1, u2, u3, u4)
        E_lista.append(E_now)

        #tid
        t = t + h_eff

        tlista.append(t)
        xlista.append(u1)
        ylista.append(u2)
        Jxlista.append(Jx)
        Jylista.append(Jy)

    return xlista, ylista, Jxlista, Jylista, u3, u4, E_lista, tlista

#beräkna totala energin relativt till solen
def total_energy(u1, u2, u3, u4):
    #G = 1, M_sol = 1.
    #kinetisk energi
    T = (u3*u3 + u4*u4) / Decimal(2)

    #potentiell energi
    r_sol2 = u1*u1 + u2*u2
    r_sol = r_sol2.sqrt()
    V = -Decimal(1) / r_sol

    #Tot
    E_total = T + V
    return E_total


def escape_velocity(r_sol):
    """
    Beräknar flykthastigheten relativt solen.
    G = 1, M_sol = 1.
    E = 0 ⇒ (1/2) v^2 = 1/r_sol
    """
    r_sol = Decimal(r_sol)
    v2 = 2 / r_sol
    v_escape = v2.sqrt()
    return v_escape


if __name__ == "__main__":
    #rymdskepp
    x0, y0 = Decimal("1"), Decimal("0")       
    vx0, vy0 = Decimal("0"), Decimal("1.35")  
    #Jupiter 
   
    r_J = Decimal("5.2")
    #96 för slingshot för vy0 = 1.4
    #99.4 för slingshot in i solen för vy0 = 1.35
    #99.6 för konstig slingshot för vy0 = 1.35
    #99.7 för slingshot för vy0 = 1.35
    theta_deg = 99.7
    theta = math.radians(theta_deg)

    #pos (r = 5.2)
    Jx0 = r_J * Decimal(math.cos(theta))
    Jy0 = r_J * Decimal(math.sin(theta))

    #tangentiell hastighet
    v_J = Decimal(math.sqrt(1 / float(r_J)))
    Jvx0 = -v_J * Decimal(math.sin(theta))
    Jvy0 =  v_J * Decimal(math.cos(theta))  
    mJ = Decimal("0.001")                          

    t0 = Decimal("0")
    t_slut = Decimal("400")
    h = Decimal("0.001")
    
    xlista, ylista, jxlista, jylista, vx_slut, vy_slut, E_lista, tlista = rk4(x0, y0, vx0, vy0, Jx0, Jy0, Jvx0, Jvy0, mJ, t0, t_slut, h)

    E_start = total_energy(xlista[0], ylista[0], vx0, vy0)
    E_slut = total_energy(xlista[-1], ylista[-1], vx_slut, vy_slut)

    print("\n--- Energiresultat ---")
    print(f"Startenergi E_start = {E_start}")
    print(f"Slutenergi  E_slut  = {E_slut}")
    if E_slut > 0:
        print("Rymdskeppet har lämnat solsystemet (E > 0).")
    else:
        print("Rymdskeppet är bundet (E ≤ 0).")

    
    #escape velocity
    r_sol = (x0**2 + y0**2).sqrt()
    r_Jup = ((Jx0-x0)**2 + (Jy0-y0)**2).sqrt()
    v_esc = escape_velocity(r_sol)
    print("escape velocity vid startposition:", v_esc)
    

    #plotta
    plt.plot(xlista, ylista, label="rymdskepp")
    plt.plot(jxlista, jylista, label="Jupiter")
    plt.plot(0, 0, "yo", label="Solen")

    plt.axis("equal")
    plt.gca().set_aspect("equal")
    plt.legend()
    plt.grid(True)
    plt.show()


    


    #Felanalys nära Jupiter
    
    h_lista = [h*(Decimal("0.5")**i) for i in range(5)]
    energi_fel = []


    for h in h_lista:
        #kör simulationen kortare tid nära Jupiter (snabbare körning)
        xlista, ylista, jxlista, jylista, vx_slut, vy_slut, E_lista, tlista = rk4(
            x0, y0, vx0, vy0, Jx0, Jy0, Jvx0, Jvy0, mJ, Decimal("0"), Decimal("400"), h
        )
        dist_list = []
        for i in range(len(xlista)):
            Dx = jxlista[i] - xlista[i]
            Dy = jylista[i] - ylista[i]
            r2Jup = Dx*Dx + Dy*Dy
            rJup = r2Jup.sqrt()
            dist_list.append(rJup)

        min_dist = min(dist_list)
        
        print(f"minsta avståndet till jupiter är {min_dist}")

        plt.figure()
        plt.plot(xlista, ylista, label="rymdskepp")
        plt.plot(jxlista, jylista, label="Jupiter")
        plt.plot(0, 0, "yo", label="Solen")

        plt.axis("equal")
        # plt.xlim(-6, -1)
        # plt.ylim( 0, 5)
        plt.gca().set_aspect("equal")
        plt.legend()
        plt.grid(True)
        plt.show()


        #plotta energi över tiden
        plt.figure()
        plt.plot([t for t in tlista[:-1]], [E for E in E_lista])
        plt.xlabel("Tid")
        plt.ylabel("Total energi (relativt solen)")
        plt.title(f"Energi som funktion av tid")
        plt.grid(True)
        plt.show()






