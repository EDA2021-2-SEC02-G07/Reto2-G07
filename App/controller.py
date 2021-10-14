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
    load2DArtworks(catalog)
    loadArtistMediumsTags(catalog)
    loadDptments(catalog)
    catalog['artists'] = sortArtists(catalog, 3)
    fillArtistMediums(catalog)
    fillMostUsedMediums(catalog)
    catalog['artists_tags'] = sortArtistTags(catalog, 3)
    sort_dptments(catalog)

def loadArtworks(catalog):
    """
    Carga las obras del archivo.  
    """
    artfile = cf.data_dir + 'Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(artfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)

def loadArtists(catalog):
    """
    Carga loas artista en el cátalogo y los organiza por su 'ConstituentID'.

    Complejidad:  O(n + nlogn) n es el número de obras.
    """
    artfile = cf.data_dir + 'Artists-utf8-small.csv'
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
    catalog['adquire'] = model.sortAdquires(catalog)

def loadNacionalities(catalog):
    """
        * Carga en el catálogo el la llave 'nations' una lista de listas, cada sub lista contiene todas la obras de una nacionalidad específica
        ** Carga en el catálogo en el la llave 'bigNation' la lista de obras del país que más obras tiene en el MoMA 

        Complejidad:  tilda(2m+nlogm) n es el número de obras y m el número de artistas, en archivo large m igual al 11% de n
    """
    catalog['nationSize'] = {}
    catalog['nationalities'] = {}
    catalog['nationalities']['Unknown'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction= None, key='ConstituentID')
    catalog['nationalities']['Unknown']['nation'] = 'Unknown'
    catalog['nationSize']['Unknown'] =lt.newList(datastructure='ARRAY_LIST', cmpfunction= None, key='ConstituentID')
    catalog['nationSize']['Unknown']['nation'] = 'Unknown'
    for x in lt.iterator(catalog['artists']):
        if str(x['Nationality']) != '':
            if catalog['nationalities'].get(str(x['Nationality'])) == None:
                catalog['nationSize'][str(x['Nationality'])] = lt.newList(datastructure='ARRAY_LIST', cmpfunction= None, key='ConstituentID')
                catalog['nationSize'][str(x['Nationality'])]['nation'] = str(x['Nationality'])
                catalog['nationalities'][str(x['Nationality'])] = lt.newList(datastructure='ARRAY_LIST', cmpfunction= None, key='ConstituentID')
                catalog['nationalities'][str(x['Nationality'])]['nation'] = str(x['Nationality'])
    for y in lt.iterator(catalog['artworks']):
        for z in eval(y['ConstituentID']):
            pos = model.giveElementBinarySearch(catalog['artists']['elements'],'ConstituentID',int(z))
            if pos != -1:
                nationality = str(catalog['artists']['elements'][pos]['Nationality'])
                if nationality != '' and nationality != 'Nationality unknown':
                    lt.addLast(catalog['nationSize'][nationality], y) 
                    if lt.isPresent(catalog['nationalities'][nationality], y) == 0:
                        lt.addLast(catalog['nationalities'][nationality], y) 
                else: 
                    lt.addLast(catalog['nationSize']['Unknown'], y)
                    if lt.isPresent(catalog['nationalities']['Unknown'], y) == 0:
                        lt.addLast(catalog['nationalities']['Unknown'], y)
    for x in catalog['nationalities']:
        lt.addLast(catalog['bigNation'],catalog['nationalities'][x])
    catalog['bigNation'] = model.sortBigNation(catalog)
    catalog['bigNation'] = catalog['bigNation']['elements'][0]
    for x in catalog['nationSize']:
        lt.addLast(catalog['nations'],catalog['nationSize'][x])
    catalog['nations'] = model.sortNationsSize(catalog)
    
def load2DArtworks(catalog):
    """
        Carga en el cátalogo el la llave '2DArtworks' una sublista de las obras que sean de dos dimensiones (cuadros y fotos) 
    """
    for x in lt.iterator(catalog['artworks']):
        if x['Date'] != '' and x['Width (cm)'] != '' and x['Height (cm)'] != '' :
            model.add2DArtworks(catalog, x)

def loadDptments(catalog):
    artworks = catalog['artworks']
    size = model.size(artworks)
    for i in range(0, size + 1):
        artwork = model.getElement1(artworks, i)
        dptment = artwork['Department']

        if dptment in catalog['artworks_dptments']:
            pass

        else: 
            new_dptment = model.newDptment()
            model.addArtworkdptment(catalog, new_dptment, dptment)

        model.addtolist(catalog['artworks_dptments'][dptment]['Artworks'], artwork)
        try:
            weight = float(artwork['Weight (kg)'])
            catalog['artworks_dptments'][dptment]['weight'] += weight
        except: 
            pass

        catalog['artworks_dptments'][dptment]['price'] += model.Transport_Price(artwork)
        model.expensive_artworks(artwork ,catalog['artworks_dptments'][dptment])

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

def loadRangeOfYears2DArtworks(catalog, begin, end):
    """
        Devuelve una lista con las obras de 2 dimensiones en un determinado rango de años

        Complejidad:  tilda(2m) n es el número de obras y m el número de obras de 2 dimensiones, en archivo large m es igual al 80% de n
    """
    Artworks = []
    for x in lt.iterator(catalog['2DArtworks']):
        if int(x['Date']) >= begin and int(x['Date']) <= end:
            Artworks.append(x)

    return Artworks

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
    Artist_medium = me.getValue(mp.get(catalog['artists_mediums'], ID))
    medium = Artist_medium['mediums']['most_used']
    total = Artist_medium['mediums']['total']
    pos1, pos2 = model.Artworks_in_a_medium(medium, Artist_medium)
    size = model.size(Artist_medium['Artworks']) + 1

    return ID, medium, total, pos1, pos2, size


def Department_transport(catalog, Department):
    Artworks = catalog['artworks_dptments'][Department]['Artworks']
    price = catalog['artworks_dptments'][Department]['price']
    weight = catalog['artworks_dptments'][Department]['weight']
    size = model.size(Artworks)
    expensive = catalog['artworks_dptments'][Department]['expensive_artworks']
    Oldest = []
    expensives = []
    expensive_prices = []
    for i in range(0,5):
        Oldest.append(model.lt.getElement(catalog['artworks_dptments'][Department]['Artworks'], i))
    Oldest_prices = []

    for artwork in Oldest:

        Oldest_prices.insert(0, model.Transport_Price(artwork))
    for key in expensive:
        expensives.append(expensive[key])
        expensive_prices.append(key)
    return price, weight, size, Oldest, Oldest_prices, expensives, expensive_prices

def give_artworks_in_a_medium(catalog, medium):
    mediumList = me.getValue(mp.get(catalog['mediums_map'], medium))

    mediumList = model.sortYearsOfaList(mediumList)
    
    return mediumList
# Funciones de ordenamiento

def sortAdquires(catalog):
    """
    Ordena las adquisiciones
    """
    return model.sortAdquires(catalog)

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

    for key in artworks_dptments:
        dptment = artworks_dptments[key]
        dptment['Artworks'] = sortArtworksByYear(dptment, 3)