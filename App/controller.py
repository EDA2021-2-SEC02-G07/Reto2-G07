"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


from DISClib.ADT import list as lt
import config as cf
import model
import time
import csv
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos
def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtworks(catalog)
    loadArtists(catalog)
    loadAdquires(catalog)
    loadNacionalities(catalog)
    loadArtistMediumsTags(catalog)
    fillArtistMediums(catalog)
    fillMostUsedMediums(catalog)
    loadDptments(catalog)
    catalog['artists'] = sortArtists(catalog, 3)
    catalog['artists_tags'] = sortArtistTags(catalog, 3)
    sort_dptments(catalog)

def loadArtworks(catalog):
    """
    Carga las obras del archivo.  
    """
    artfile = cf.data_dir + 'Artworks-utf8-large.csv'
    input_file = csv.DictReader(open(artfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)

def loadArtists(catalog):
    """
    Carga loas artista en el cátalogo y los organiza por su 'ConstituentID'.

    Complejidad:  O(n + nlogn) n es el número de obras.
    """
    artfile = cf.data_dir + 'Artists-utf8-large.csv'
    input_file = csv.DictReader(open(artfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist) 
    catalog['artistsByID'] = catalog['artists']    
    catalog['artistsByID'] = model.sortArtistID(catalog)

def loadAdquires(catalog):
    """
        Carga en el catálogo el la llave 'adquires'una sublista de las obras y la organiza con respecto a su fecha de adquisición

        Complejidad:  O(nlogn) n es el número de obras.
    """
    catalog['adquire'] = lt.subList(catalog['artworks'], 1, lt.size(catalog['artworks']))
    catalog['adquire'] = sortArtworksByAcquires(catalog['adquire'])

def loadNacionalities(catalog):
    """
        * Carga en el catálogo el la llave 'nations' una lista de listas, cada sub lista contiene todas la obras de una nacionalidad específica
        ** Carga en el catálogo en el la llave 'bigNation' la lista de obras del país que más obras tiene en el MoMA 

        Complejidad:  tilda(2m+nlogm) n es el número de obras y m el número de artistas, en archivo large m igual al 11% de n
    """
    artists = catalog['artists']
    sizes = catalog['nationSize']
    nts = catalog['nationalities']

    for y in lt.iterator(catalog['artworks']):
        for z in eval(y['ConstituentID']):
            pos = model.giveElementBinarySearch(artists['elements'],'ConstituentID',int(z))
            if pos != -1:
                lt.addLast(me.getValue(mp.get(catalog['artworksByAnArtist'], str(z))), y) 
                nationality = lt.getElement(artists, pos + 1)['Nationality']
                if nationality != '' and nationality != 'Nationality unknown':
                    nationNtMap = me.getValue(mp.get(nts, nationality))
                    mp.put(nationNtMap, y['ObjectID'], y)
                    lt.addLast(me.getValue(mp.get(sizes, nationality)), y) 
                else: 
                    lt.addLast(me.getValue(mp.get(sizes, 'Unknown')), y) 
                    Unknowns = me.getValue(mp.get(nts, 'Unknown'))
                    mp.put(Unknowns, y['ObjectID'], y)
                    
    for x in lt.iterator(mp.keySet(nts)):
        listnt = lt.newList('ARRAY_LIST')
        nt = mp.get(nts, x)['value']
        listnt['nation'] = nt['nation']
        sz = mp.get(sizes, x)['value']
        
        keys = mp.keySet(nt)
        for y in lt.iterator(keys):
            lt.addLast(listnt,mp.get(nt,y))
        lt.addLast(catalog['nations'],sz)
        lt.addLast(catalog['bigNation'],listnt)
    catalog['bigNation'] = model.sortBigNation(catalog)
    catalog['bigNation'] = catalog['bigNation']['elements'][0]
    catalog['nations'] = model.sortNationsSize(catalog)
    
def loadDptments(catalog):
    artworks = catalog['artworks']
    size = model.size(artworks)
    for i in range(1, size + 1):
        artwork = model.getElement1(artworks, i)
        dptment = artwork['Department']
        
        if mp.get(catalog['artworks_dptments'], dptment) != None:
            pass

        else: 
            new_dptment = model.newDptment()
            model.addArtworkdptment(catalog, new_dptment, dptment)

        model.addtolist(me.getValue(mp.get(catalog['artworks_dptments'], dptment))['Artworks'], artwork)
        try:
            weight = float(artwork['Weight (kg)'])
            me.getValue(mp.get(catalog['artworks_dptments'], dptment))['weight'] += weight
        except: 
            pass
        price = model.Transport_Price(artwork)
        me.getValue(mp.get(catalog['artworks_dptments'], dptment))['price'] += price
        model.expensive_artworks(artwork , me.getValue(mp.get(catalog['artworks_dptments'], dptment)),price)

def loadArtistMediumsTags(catalog):
    artists = catalog['artists']
    size = model.size(artists) 

    for i in range(0, size + 1):
        name = model.getElement(artists, 'DisplayName', i)   
        ID = model.getElement(artists, 'ConstituentID', i) 
        artist_medium, artist_tag = model.newArtistMedium(ID, name)
        model.addArtistMedium(catalog, artist_medium)
        model.addArtistTag(catalog, artist_tag)

def fillArtistMediums(catalog):
    Artworks = catalog['artworks']
    artists_mediums = catalog['artists_mediums']
    size = model.size(Artworks)

    for i in range(0, size + 1):
        artwork = model.getElement1(Artworks, i)
        IDs = model.getElement(Artworks, 'ConstituentID', i)
        IDs = IDs.replace('[','').replace(']','').split(',')
        medium = model.getElement(Artworks, 'Medium', i)
        for ID1 in IDs:
            ID = str(ID1)
            try:
                artist_medium = me.getValue(mp.get(artists_mediums, ID))
                artlist = artist_medium ['Artworks']
                mediums = artist_medium ['mediums']
            except: 
                continue
            
            

            model.fillArtworks(artlist, artwork)
            

            if medium in mediums['mediums_list']:
                mediums['mediums_list'][medium] += 1

            else:
                mediums['mediums_list'][medium] = 1
                mediums['total'] += 1
    
def fillMostUsedMediums(catalog):
    artists_mediums=catalog['artists_mediums']
    keys = mp.keySet(artists_mediums)
    size = lt.size(keys)
    for i in range(0, size + 1):
        key = model.lt.getElement(keys, i)
        artist_medium = me.getValue(mp.get(artists_mediums, key))['mediums']
        artist_medium_list = me.getValue(mp.get(artists_mediums, key))
        mediums_list = artist_medium['mediums_list']
        most_used_medium = model.MostUsedMedium(mediums_list)
        artist_medium['most_used'] = most_used_medium
        artist_medium_list['Artworks'] = sortArworksByMedium(artist_medium_list, 3)


# Funciones de consulta sobre el catálogo

def giveRightPosArtworkstByDateAcquired(catalog, date):
    """
        LLama la función del model 'giveRightDateBinarySearch'
    """
    return model.giveRightDateBinarySearch(catalog['adquire'], date)

def giveLeftPosArtworkstByDateAcquired(catalog, date):
    """
        LLama la función del model 'giveRightDateBinarySearch'
    """
    return model.giveLeftDateBinarySearch(catalog['adquire'], date)

def giveRangeOfDates(catalog, begin, end):
    """
        Dados por parametro el catálogo, una fecha de inicio y una fecha final, devuelve una lista con todos las obras que hayan sido adquiridas n ese rango de fechas
        
        Debido a que llama a dos busquedas binarias y nada más sabemos que su complejidad se aproxima a:

            Complejidad:  O(2logn) n es el número de obras.
    """
    posI = giveLeftPosArtworkstByDateAcquired(catalog, begin)
    posF = giveRightPosArtworkstByDateAcquired(catalog, end)
    return catalog['adquire']['elements'][posI:posF+1]

def giveAuthorsName(catalog, ConstituentsID):
    """
    Dado una lista de Constituent ID devuelve los nombres de los artistas asociados a esos ID
    """
    names = []

    for x in ConstituentsID:
        names.append(' '+model.giveAuthorName(catalog, x))
    return ','.join(names)

def Artist_in_a_range(year1, year2, catalog):
    posiciones = []
    if year1 <= 0:
        year1 = 1
    pos1, pos2 = model.Artist_in_a_range(year1, year2, catalog)
    size = pos2 - pos1 + 1
    if size<=0:
        return size, None
    elif size <= 3:
        while pos1 <= pos2:
            posiciones.append(pos1)
            pos1 += 1
    else:
        posiciones=[pos1, pos1 + 1, pos1 +2, pos2 - 2, pos2 -1, pos2]

    return size, posiciones 

def Artworks_in_a_medium(name, catalog):
    pos1, pos2= model.TagsFromName(name, catalog)
    ID = model.getElement(catalog['artists_tags'], 'ID', pos1)
    name = model.getElement(catalog['artists_tags'], 'name', pos1)
    Artist_medium = me.getValue(mp.get(catalog['artists_mediums'], ID))
    medium = Artist_medium['mediums']['most_used']
    total = Artist_medium['mediums']['total']
    pos1, pos2 = model.Artworks_in_a_medium(medium, Artist_medium)
    size = model.size(Artist_medium['Artworks']) 

    return ID, medium, total, pos1, pos2, size, name


def Department_transport(catalog, Department):
    Artworks = me.getValue(mp.get(catalog['artworks_dptments'], Department))['Artworks']
    price = me.getValue(mp.get(catalog['artworks_dptments'], Department))['price']
    weight = me.getValue(mp.get(catalog['artworks_dptments'], Department))['weight']
    size = model.size(Artworks)
    expensive = me.getValue(mp.get(catalog['artworks_dptments'], Department))['expensive_artworks']
    Oldest = []
    expensives = []
    expensive_prices = []
    for i in range(1,6):
        Oldest.append(model.lt.getElement(me.getValue(mp.get(catalog['artworks_dptments'], Department))['Artworks'], i))
    Oldest_prices = []

    for artwork in Oldest:

        Oldest_prices.append(model.Transport_Price(artwork))
    for key in expensive:
        expensives.append(expensive[key])
        expensive_prices.append(key)
    return price, weight, size, Oldest, Oldest_prices, expensives, expensive_prices

def give_artworks_in_a_medium(catalog, medium):
    mediumList = me.getValue(mp.get(catalog['mediums_map'], medium))

    mediumList = model.sortYearsOfaList(mediumList)
    
    return mediumList

def giveRangeOfArtists(catalog, begin, end):
    """
        Dados por parametro el catálogo, una fecha de inicio y una fecha final, devuelve una lista con todos las obras que hayan sido adquiridas n ese rango de fechas
        
        Debido a que llama a dos busquedas binarias y nada más sabemos que su complejidad se aproxima a:

            Complejidad:  O(2logn) n es el número de obras.
    """
    positions = Artist_in_a_range(begin, end, catalog)[1]
    posI = positions[0]
    posF = positions[-1]
    return catalog['artists']['elements'][posI-1:posF]

def giveTopProlificArtist(artists, artworks, catalog):
    top = lt.newList('ARRAY_LIST')
    for x in artists:
        arts = me.getValue(mp.get(artworks, x['ConstituentID']))
        x['usedMediums'] = 0
        x['mostUsedMedium'] = ''
        x['numberArtworks'] = lt.size(arts)
        mediums = {}
        n = 0
        for y in lt.iterator(arts):
            if y['Medium'] not in mediums:
                mediums[y['Medium']] = 0
                mediums[y['Medium']] += 1
            else: 
                mediums[y['Medium']] += 1
            if mediums[y['Medium']] > n:
                n = mediums[y['Medium']] 
                x['mostUsedMedium'] = y['Medium']
        x['usedMediums'] = len(mediums)
        lt.addLast(top, x)
    model.sortArtistsByArtworks(top, catalog)
    return top
# Funciones de ordenamiento

def sortArtworksByAcquires(list):
    """
    Ordena las adquisiciones
    """
    return model.sortArtworksByAcquires(list)

def sortArtists(catalog, sort):
    """
    Ordena los libros por average_rating
    """
    return model.sort(catalog, sort, 'artists', model.cmpArtistByBeginDate)


def sortArworksByMedium(artistmedium, sort):
    return model.sort(artistmedium, sort, 'Artworks', model.cmpArtworksByMedium)


def sortArtworksByYear(Dptment, sort):
    return model.sort(Dptment, sort, 'Artworks', model.cmpArtworksByYear)


def sortArtistTags(catalog, sort):
    return model.sort(catalog, sort, 'artists_tags', model.cmpArtistByName) 

def sort_dptments(catalog):
    artworks_dptments = catalog['artworks_dptments']
    keys = mp.keySet(artworks_dptments)
    size = lt.size(keys)
    for i in range(0, size+1):
        key = lt.getElement(keys, i)
        dptment = me.getValue(mp.get(artworks_dptments, key))
        dptment['Artworks'] = sortArtworksByYear(dptment, 3)

