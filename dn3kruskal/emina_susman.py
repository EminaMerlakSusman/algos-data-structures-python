# Emina Merlak Susman
# 27151132

class Graf:
    def __init__(self, vozlisca, povezave, utezi_vozlisc):
        self.graf = []
        self.vozlisca = vozlisca
        self.povezave = povezave
        self.utezi_vozlisc = utezi_vozlisc
        self.st_povezav_v_mst = 0
    
    def dodaj_povezavo(self, u, v, w):
        self.graf.append([u, v, w])
            
    def najdi(self, stars, i):
        if stars[i] != i:
            stars[i] = self.najdi(stars, stars[i])
        return stars[i]

    def unija(self, stars, rang, x, y):
        # insertaj drevo z manjsim rangom pod koren drevesa z višjim rangom
        if rang[x] < rang[y]:
            stars[x] = y
        elif rang[x] > rang[y]:
            stars[y] = x
        else:
            stars[y] = x
            rang[x] += 1
        
    def kruskal(self):
        drevo = []
        i = 0 # indeks, za sortirane edge
        e = 0 # indeks za rezultat
        
        self.graf = sorted(self.graf, key=lambda x: x[2])
        
        stars = []
        rang = []
        for voz in range(self.vozlisca):
            stars.append(voz)
            rang.append(0)
        
        limit = self.vozlisca - 1 if self.povezave >= self.vozlisca - 1 else self.povezave
        while e < limit and i < limit:
            # izberi najmanjso povezavo
            # in inkrementiraj indeks
            u, v, w = self.graf[i]
            i = i + 1
            x = self.najdi(stars, u)
            y = self.najdi(stars, v)
            
            # če vključevanje te povezave ne ustvari cikla,
            # jo daj v graf in inkrementiraj e
            if x != y:
                e = e + 1
                drevo.append((u, v, w))
                self.unija(stars, rang, x, y)
                
        self.st_povezav_v_mst = e
        return drevo
    
    def st_za_odstranit(self, k):
        # Izračuna, koliko povezav moramo odstraniti iz MST, da ga razbijemo na k komponent.
        
        # V povezanem MST bi mogl bit n - 1 vozlišč. Če jih je manj, mormo odstranit tok povezav,
        # kolkr jih še manjka da dobimo k povezanih komponent
        d = (self.vozlisca - 1) - self.st_povezav_v_mst
        trenutno_st_komponent = d + 1
        return k - trenutno_st_komponent
        
    def sestavi_seznam_sosednosti(self, seznam_povezav, st_povezav):
        # dobi seznam povezav in sestavi seznam sosednosti dolzine n
        povezave = [[] for _ in range(self.vozlisca)]
        for i in range(st_povezav):
            povezava = seznam_povezav[i]
            u = povezava[0]
            v = povezava[1]
            povezave[u].append(v)
            povezave[v].append(u)
        return povezave
    
    def dfs_pomozna(self, v, obiskane, seznam_sosednosti):
        obiskane[v] = True
        vsota_kvadratov = self.utezi_vozlisc[v]**2
        vsota = self.utezi_vozlisc[v]
        velikost_komponente = 1
        for u in seznam_sosednosti[v]:
            if not obiskane[u]:
                vk, v, c = self.dfs_pomozna(u, obiskane, seznam_sosednosti)
                vsota_kvadratov += vk
                vsota += v
                velikost_komponente += c
        
        return vsota_kvadratov, vsota, velikost_komponente
    
    def zmnozi_po_komponentah(self, seznam_sosednosti):
        zmnozki_in_velikosti_komponent = []
        obiskane = [False for i in range(self.vozlisca)]
        
        for v in range(self.vozlisca):
            if obiskane[v] == False:
                vsota_kv, vsota, velikost = self.dfs_pomozna(v, obiskane, seznam_sosednosti)
                # če je velikost komponente 1,
                # je ta vsota 0
                rezultat = (vsota ** 2 - vsota_kv) / 2
                
                zmnozki_in_velikosti_komponent.append((velikost, rezultat))
        
        return zmnozki_in_velikosti_komponent

# Branje inputa
n, m, k = map(int, input().split(','))
utezi_vozlisc = list(map(float, input().split(',')))
graf = Graf(n, m, utezi_vozlisc)
for i in range(m):
    u, v, w =  input().split(',')
    u = int(u)
    v = int(v)
    w = float(w)
    graf.dodaj_povezavo(u, v, w)           

    
# Najdi MST s Kruskalom
drevo = graf.kruskal()
st_za_odstranit = graf.st_za_odstranit(k) #k - trenutno_st_komponent
if st_za_odstranit < 0: # to pomen da mamo preveč komponent
    print('-1')
    graf = graf.sestavi_seznam_sosednosti(drevo, graf.st_povezav_v_mst)
    print(graf)
   
else:
    # odstranimo potrebno stevilo povezav
    for i in range(st_za_odstranit): 
        drevo.pop(graf.st_povezav_v_mst - i - 1)

    # sestavimo seznam sosednosti za nastalo drevo (z odstranjenimi povezavami)
    # za potrebe DFS-ja pri iteriranju po komponentah
    seznam_sosednosti = graf.sestavi_seznam_sosednosti(drevo, graf.st_povezav_v_mst - st_za_odstranit)
    zmnozki_in_velikosti = graf.zmnozi_po_komponentah(seznam_sosednosti)
    for c, f in sorted(zmnozki_in_velikosti, reverse=True):
        print(f'{c},{f:.4f}')
