from math import inf, sqrt
import heapq

# Emina Merlak Susman
#27151132

# Za tri kolinearne točke p, q, r, preveri, če  
# točka q leži na daljici 'pr'  
def naDaljici(p, q, r): 
    if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and 
           (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))): 
        return True
    return False

def orientacija(p, q, r):
    
	# Najde oprientacijo  (p,q,r)
	# funkcija vrne naslednje vrednosti: 
	# 0 : Kolinearne točke 
	# 1 : V smeri urinega kazalca 
	# 2 : V nasprotni smeri urinega kazalca
	
	# Vir: https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/ 
    # https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
	val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1])) 
	if (val > 0): 
		
		# Smer urinega kazalca 
		return 1
	elif (val < 0): 
		
		# Nasprotna smer urinega kazalca 
		return 2
	else: 
		
		# Kolinearnost
		return 0


def se_sekata(daljica_1,daljica_2):
    # preveri, če se daljici sekata
    # daljici sta podani kot tuple dveh točk (x, y): ((p1, q1), (p2, q2))
    p1 = daljica_1[0]
    q1 = daljica_1[1]
    p2 = daljica_2[0]
    q2 = daljica_2[1]
    o1 = orientacija(p1, q1, p2) 
    o2 = orientacija(p1, q1, q2) 
    o3 = orientacija(p2, q2, p1) 
    o4 = orientacija(p2, q2, q1)

    if ((o1 != o2) and (o3 != o4)): 
        return True

    return False

def se_sekata_kolinearni(daljica_1, daljica_2):
    # preveri, če se kolinearni daljici sekata
    # (to rabmo sam v edge case-u, da mamo premico od enga oglišča na y=100, do (100,100)
    # in pol mormo prevert če je vmes kaka ovira
    
    p1 = daljica_1[0]
    q1 = daljica_1[1]
    p2 = daljica_2[0]
    q2 = daljica_2[1]
    o1 = orientacija(p1, q1, p2) 
    o2 = orientacija(p1, q1, q2) 
    o3 = orientacija(p2, q2, p1) 
    o4 = orientacija(p2, q2, q1)
  
    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1 
    if ((o1 == 0) and naDaljici(p1, p2, q1)): 
        return True
  
    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1 
    if ((o2 == 0) and naDaljici(p1, q2, q1)): 
        return True
  
    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2 
    if ((o3 == 0) and naDaljici(p2, p1, q2)): 
        return True
  
    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2 
    if ((o4 == 0) and naDaljici(p2, q1, q2)): 
        return True
  
    # If none of the cases 
    return False

def evklidska(voz1, voz2):
    return sqrt((voz2[0] - voz1[0])**2 + (voz2[1] - voz1[1])**2)

def stevilo_sekanj(p1, q1, ovire):
    # Zračuna, kokrat daljica med p1 in q1 seka ovire
    st_sekanj = 0
    for ovira in ovire:
        v_isti_stranici_ovire = (p1, q1) in ovira or (q1, p1) in ovira
        if v_isti_stranici_ovire:
            return 0
        v_isti_oviri = any([p1 in daljica for daljica in ovira]) and any([q1 in daljica for daljica in ovira])
        if v_isti_oviri:
            return 1        
        for daljica in ovira:
            # scenariji:
            # 1. če sta p1 in q1 v isti oviri, pol se sekata sam če nista v isti daljici ovire.
            # -> p1 NOT in daljica and q1 IN daljica, or p1 IN daljica and q1 NOT IN daljica
            # p1 in q1 v različnih ovirah - se zračuna normalno če sekata to daljico
            if (p1 not in daljica) and (q1 not in daljica):
                daljica_1 = (p1[0], q1[0])
                daljica_2 = (daljica[0][0], daljica[1][0])
                if se_sekata(daljica_1, daljica_2):
                    st_sekanj += 1
                    continue # sekamo to oviro, ne rabmo pogledat ostalih daljic v oviri
    return st_sekanj

def st_sekanj_na_robu(p1, q1, ovire):
    # kokrat daljica seka na robu
    # ta funkcija je narobe, kr za daljico med vozliščema ki sta na robu skladišča in ne seka nobene
    # ovire, vrne da se sekajo. Po pregledu izrisov poti so to ble edine
    # napačne rešitve.
    daljica_1 = (p1[0], q1[0])

    st_sekanj = 0
    for ovira in ovire:
        for daljica in ovira:
            daljica_2 = (daljica[0][0], daljica[1][0])
            if se_sekata_kolinearni(daljica_1, daljica_2):
                # se sekata, ampak intersection point ne sme bit lih q1 al pa p1
                if daljica_1[0] not in daljica_2 or daljica_1[1] in daljica_2 or daljica_2[0] in daljica_1 or daljica_2[1] in daljica_1:
                    st_sekanj += 1
        
    return st_sekanj

def sestavi_graf(ovire):
    # dobi seznam koordinat ovir (+ začetek in konc) in jih pretvori v graf, ki je slovar sosednosti:
    # ključi so tupli (kordinate vozlišča), vrednosti pa seznam sosedov.
    # Graf je poln graf vseh vozlišč (assumamo, da ni ovir vmes med vozlišči)
    n = len(ovire)
    graf = {voz: [] for voz in ovire}
    for i in range(n):
        voz = ovire[i]
        for j in range(n):
            if j != i: # ne vzameš njega samga
                koord = ovire[j]
                # ne moremo se premikat po stranicah ovir,
                # ki so na robovih grafa
                y_je_0 = (koord[0][1] == 0 and voz[0][1] == 0) # point1.y = 0 and point2.y = 0
                y_je_100 = (koord[0][1] == 100 and voz[0][1] == 100) # point1.y = 100, point2.y = 100
                x_je_0 = (koord[0][0]==0 and voz[0][0] == 0) # point1.x = 0 and point2.x = 0
                x_je_100 = (koord[0][0]==100 and voz[0][0] == 100) # point1.x = 100 and point2.x = 100
                if not y_je_0 and not y_je_100 and not x_je_0 and not x_je_100:
                    graf[voz].append(koord)
                    
                
                else:
                    if y_je_100:
                        # oba na zgornjem robu skladišča
                        st_sekanj = st_sekanj_na_robu(voz, koord, ovire_daljice)
                        if st_sekanj == 0:
                            graf[voz].append(koord)
                    elif x_je_100:
                        # oba na desnem robu skladišča
                        st_sekanj = st_sekanj_na_robu(voz, koord, ovire_daljice)
                        if st_sekanj == 0:
                            graf[voz].append(koord)
                    elif y_je_0:
                        # oba na spodnjem robu skladišča
                        st_sekanj = st_sekanj_na_robu(voz, koord, ovire_daljice)
                        if st_sekanj == 0:
                            graf[voz].append(koord)
                    elif x_je_0:
                        # oba na desnem robu skladišča
                        st_sekanj = st_sekanj_na_robu(voz, koord, ovire_daljice)
                        if st_sekanj == 0:
                            graf[voz].append(koord)
    return graf

n,p, k = list(map(int, input().split(','))) 

# preberi koordinate ovir
vozlišča = [((0,0), None), ((100, 100), None)]
ovire_daljice = [] # ovire po daljicah
for i in range(n):
    koordinate = list(map(float, input().split(',')))#
    # sestavi 4 vozlišča - vsako ogljišče ovire
    x1 = koordinate[0]
    y1 = koordinate[1]
    x2 = koordinate[2]
    y2 = koordinate[3]
    spodnje_levo = ((x1, y1), i)
    zgornje_desno = ((x2, y2), i)
    spodnje_desno = ((x2, y1), i)
    zgornje_levo = ((x1, y2), i)
    vozlišča = vozlišča + [spodnje_levo, zgornje_desno, spodnje_desno, zgornje_levo]
    # sestavi daljice za potrebe preverjanja, če daljica med dvema vozliščema seka kako od ovir
    daljica_spodaj = (spodnje_levo, spodnje_desno)
    daljica_zgoraj = (zgornje_levo, zgornje_desno)
    daljica_levo = (spodnje_levo, zgornje_levo)
    daljica_desno = (spodnje_desno, zgornje_desno)
    ovira = [daljica_spodaj, 
            daljica_zgoraj,
            daljica_levo, 
            daljica_desno]
    ovire_daljice.append(ovira)

G = sestavi_graf(vozlišča)
line = input()


def dijkstra(G, s, allowed_st_sekanj):
    obiskani = {voz: False for voz in G}
    razdalje = {voz: float("inf") for voz in G}
    heap = [(0, s, 0)] # distance, voz, st_sekanj
    
    while heap:
        d, trenutni, st_sekanj_do_zdaj = heapq.heappop(heap)
        if obiskani[trenutni] : continue
        obiskani[trenutni] = True
        razdalje[trenutni] = d
        for voz in G[trenutni]:
            st_sekanj = stevilo_sekanj(trenutni, voz, ovire_daljice) # koliko ovir daljica med voz in njenim sosedom seka
            updated_st_sekanj = st_sekanj_do_zdaj + st_sekanj
            if updated_st_sekanj <= allowed_st_sekanj: # case, kolkrat lahko gremo čez ovire
                if obiskani[voz]: continue
                heapq.heappush(heap, (d + evklidska(trenutni[0], voz[0]), voz, updated_st_sekanj))
    return razdalje

def v_kateri_oviri(poizvedba, ovire):
    for i in range(len(ovire)):
        ovira = ovire[i]
        for daljica in ovira:
            for koordinata in daljica:
                if koordinata[0] == poizvedba:
                    return i
                
razdalje_od_nic_do_ostalih = {}
razdalje_od_t_do_ostalih = {}
for j in range(0, k + 1):  
    razdalje_od_nic = dijkstra(G, ((0,0), None), j)
    razdalje_od_t = dijkstra(G, ((100,100), None), j)
    # razdalje_od_nic_do_paketa: slovar, ki ima za ključ
    # število prečkanj j. Za value ma
    # slovar razdalj za stevilo preckanj j
    razdalje_od_nic_do_ostalih[j] = razdalje_od_nic
    razdalje_od_t_do_ostalih[j] = razdalje_od_t

for i in range(p):
    poizvedba = (tuple(map(float, input().split(','))))
    indeks_ovire = v_kateri_oviri(poizvedba, ovire_daljice)
    poizvedba_voz = (poizvedba, indeks_ovire)
    najboljsi_score_ever = float('inf')
    
    for allowed_st_preckanj in range(0, k+1):
        s_do_p = razdalje_od_nic_do_ostalih[allowed_st_preckanj][poizvedba_voz]
        p_do_t = razdalje_od_t_do_ostalih[k - allowed_st_preckanj][poizvedba_voz]
        zdej = s_do_p + p_do_t
        if zdej < najboljsi_score_ever:
            najboljsi_score_ever = zdej
    if najboljsi_score_ever < float('inf'):
        print(najboljsi_score_ever)


