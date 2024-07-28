
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.pyplot import text

def narisi(ovire,  pot, T, narisi_pot=False, w=100, h=100):
    """
    Funkcija narise ovire ter pot podano kot seznam točk.
    ovire: seznam z elementi (x_1, y_1, x_2, y_2)
    pot: seznam z elementi (x, y)
    T: točka (poizvedba) oblike (x, y)
    """
    #define Matplotlib figure and axis
    fig, ax = plt.subplots()
    ax.set(xlim=(0, w), ylim = (0, h))
    for x1,y1,x2,y2 in ovire:
        ax.add_patch(Rectangle((x1, y1), x2-x1, y2-y1))

   
    if narisi_pot:
        plt.plot([T[0]], [T[1]], marker="o",markersize=10,markerfacecolor="green", markeredgecolor="red")
        for i in range(1, len(pot)):
            x, y = pot[i-1]
            z, w = pot[i]
            plt.plot([x, z], [y, w], "r-")

    #display plot
    plt.show()