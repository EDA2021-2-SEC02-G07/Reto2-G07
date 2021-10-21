"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from tabulate import tabulate
import sys
import time
from datetime import datetime
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- listar cronológicamente loas artistas (Req. 1)")
    print("2- listar cronológicamente las adquisiciones (Req. 2)")
    print("3- clasificar las obras de un artista por técnica (Req. 3)")
    print("4- clasificar las obras por nacionalidad de sus creadores (Req. 4)")
    print("5- transportar obras de un departamento (Req. 5)")
    print("6- proponer una nueva exposición en el museo (Req. 6)")
    print("7- Salir")

def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()
    
def loadData(catalog):
    """
    Carga los libros en la estructura de datos
    """
    controller.loadData(catalog)

def printSortResults(ord_artworks, sample=3):
    n = 0
    for x in ord_artworks:
        if x['CreditLine'] == 'Purchase':
            n += 1
    size = len(ord_artworks)
 
    i=0
    if size < sample:
        sample = size
    print("En este rango de años el MoMA adquirió", size, "obras únicas.")
    print()
    print("De estas", size,",", n, "fueron compradas por el MoMA" )
    print()
    if size > sample:
        print("Las primeras y últimas ", sample, " obras ordenados son:")
        print()
    table = [['Title ', 'ArtistNames', 'Medium', 'Date', 'Dimensions', 'DateAcquired']]
    while i < sample and i <= size-1:
        artwork = ord_artworks[i]
        if len(str(artwork['Title'])) > 30:
            title = str(artwork['Title'])[0:30] + '...'
        else: title = str(artwork['Title'])
        if len(controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))) > 14:
            artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))[0:30] + '...'
        else: artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))
        if len(artwork['Medium']) > 30:
            medium = artwork['Medium'][0:30] + '...'
        else: medium = artwork['Medium']
        if len(artwork['Dimensions']) > 35:
            dimension = artwork['Dimensions'][0:35] + '...'
        else: dimension = artwork['Dimensions']
        table.append([ title,artists,medium,artwork['Date'],dimension, artwork['DateAcquired']])
        i+=1
    i = size - sample
    while i >= size-sample and i< size:
        artwork = ord_artworks[i]
        if len(str(artwork['Title'])) > 30:
            title = str(artwork['Title'])[0:30] + '...'
        else: title = str(artwork['Title'])
        if len(controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))) > 14:
            artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))[0:30] + '...'
        else: artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))
        if len(artwork['Medium']) > 30:
            medium = artwork['Medium'][0:30] + '...'
        else: medium = artwork['Medium']
        if len(artwork['Dimensions']) > 35:
            dimension = artwork['Dimensions'][0:35] + '...'
        else: dimension = artwork['Dimensions']
        table.append([ title,artists,medium,artwork['Date'],dimension, artwork['DateAcquired']])
        i+=1
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid')) 

def trydepartment():
    Department = input('Ingrese el nombre del departamento: ')
    try:
        return controller.Department_transport(catalog, Department)
    except:
        print('Por favor ingrese un departamento valido')
        return trydepartment()


    
        
    
    table = [['Title ', 'ArtistNames', 'Medium', 'Date', 'Dimensions']]
    while i < sample and i <= size-1:
        artwork = ord_artworks[i]
        if len(str(artwork['Title'])) > 30:
            title = str(artwork['Title'])[0:30] + '...'
        else: title = str(artwork['Title'])
        if len(controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))) > 14:
            artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))[0:30] + '...'
        else: artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))
        if len(artwork['Medium']) > 30:
            medium = artwork['Medium'][0:30] + '...'
        else: medium = artwork['Medium']
        if len(artwork['Dimensions']) > 35:
            dimension = artwork['Dimensions'][0:35] + '...'
        else: dimension = artwork['Dimensions']
        table.append([ title,artists,medium,artwork['Date'],dimension])
        i+=1
    i = len(ord_artworks) - 1
    while i >= size-sample and i>= 0:
        artwork = ord_artworks[i]
        if len(str(artwork['Title'])) > 30:
            title = str(artwork['Title'])[0:30] + '...'
        else: title = str(artwork['Title'])
        if len(controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))) > 14:
            artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))[0:30] + '...'
        else: artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))
        if len(artwork['Medium']) > 30:
            medium = artwork['Medium'][0:30] + '...'
        else: medium = artwork['Medium']
        if len(artwork['Dimensions']) > 35:
            dimension = artwork['Dimensions'][0:35] + '...'
        else: dimension = artwork['Dimensions']
        table.append([ title,artists,medium,artwork['Date'],dimension])
        i-=1
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid')) 

def printReq6(catalog, begin, end, n):
    artists = controller.giveRangeOfArtists(catalog, begin, end)
    artworks = catalog['artworksByAnArtist']
    print('Hay', len(artists), 'artistas entre', begin, 'y', end)
    print()
    print('El TOP', n ,'artistas más prolíficos en este rango de años son:')
    top = controller.giveTopProlificArtist(artists,artworks,catalog)
    i=1
    table = [['ConstituentID', 'DisplayName', 'BeginDate', 'Gender', 'Artworks', 'Used Mediums', 'Top Medium']]
    if lt.size(top) < n:
        n = lt.size(top)
    while i <= n:
        artwork = lt.getElement(top, i)
        if len(str(artwork['DisplayName'])) > 30:
            DisplayName = str(artwork['DisplayName'])[0:30] + '...'
        else: DisplayName = str(artwork['DisplayName'])
        if len(artwork['mostUsedMedium']) > 30:
            mostUsedMedium = artwork['mostUsedMedium'][0:30] + '...'
        else: mostUsedMedium = artwork['mostUsedMedium']
        table.append([ artwork['ConstituentID'],DisplayName,artwork['BeginDate'],artwork['Gender'],artwork['numberArtworks'], artwork['usedMediums'],mostUsedMedium])
        i+=1
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid')) 
    
    topID = lt.getElement(top, 1)['ConstituentID']
    top1Name = lt.getElement(top, 1)['DisplayName']
    top1num = lt.getElement(top, 1)['numberArtworks']
    top1 = me.getValue(mp.get(artworks, topID))
    top1 = controller.sortArtworksByAcquires(top1)
    table = [['Title ', 'Medium', 'Date', 'Dimensions' ,'DateAcquired', 'Department', 'Classification']]
    print()
    print(top1Name + ' con el MoMA ID', topID, 'tiene', top1num, 'piezas a su nombre.')
    print('Las primeras 5 organizadas por fecha de adquisición son:')
    i = 1
    sample = 5
    if lt.size(top1) < sample:
        sample = lt.size(top1)
    while i <= sample:
        artwork = lt.getElement(top1, i)
        if len(str(artwork['Title'])) > 30:
            title = str(artwork['Title'])[0:30] + '...'
        else: title = str(artwork['Title'])
        if len(controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))) > 14:
            artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))[0:30] + '...'
        else: artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))
        if len(artwork['Medium']) > 30:
            medium = artwork['Medium'][0:30] + '...'
        else: medium = artwork['Medium']
        if len(artwork['Dimensions']) > 35:
            dimension = artwork['Dimensions'][0:35] + '...'
        else: dimension = artwork['Dimensions']
        table.append([ title,medium,artwork['Date'],dimension, artwork['DateAcquired'], artwork['Department'], artwork['Classification']])
        i+=1
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid')) 

def printBigNation(bigNation, sample =3):
    j = lt.size(bigNation)
    print('El país con más obras es ' + bigNation['nation'] + ' con', j, 'obras ' )
    print("Las primeras y últimas", sample, " obras ordenadas de nacionalidad ", "'",bigNation['nation'],"'"," son:")
    print()
    i=1
    table = [['Title ', 'ArtistNames', 'Medium', 'Date', 'Dimensions']]
    while i <= sample:
        artwork = lt.getElement(bigNation,i)['value']
        if len(str(artwork['Title'])) > 30:
            title = str(artwork['Title'])[0:30] + '...'
        else: title = str(artwork['Title'])
        if len(controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))) > 14:
            artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))[0:30] + '...'
        else: artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))
        if len(artwork['Medium']) > 30:
            medium = artwork['Medium'][0:30] + '...'
        else: medium = artwork['Medium']
        if len(artwork['Dimensions']) > 35:
            dimension = artwork['Dimensions'][0:35] + '...'
        else: dimension = artwork['Dimensions']
        table.append([ title,artists,medium,artwork['Date'],dimension])
        i+=1
    i = lt.size(bigNation) - 1
    while i >= j-sample:
        artwork = lt.getElement(bigNation,i)['value']
        if len(str(artwork['Title'])) > 30:
            title = str(artwork['Title'])[0:30] + '...'
        else: title = str(artwork['Title'])
        if len(controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))) > 14:
            artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))[0:30] + '...'
        else: artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))
        if len(artwork['Medium']) > 30:
            medium = artwork['Medium'][0:30] + '...'
        else: medium = artwork['Medium']
        if len(artwork['Dimensions']) > 35:
            dimension = artwork['Dimensions'][0:35] + '...'
        else: dimension = artwork['Dimensions']
        table.append([ title,artists,medium,artwork['Date'],dimension])
        i-=1
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', stralign="left")) 

def printSortNations(nations, sample=10):

    size = lt.size(nations)
    if size > sample:
        print("Las primeras ", sample, " naciones ordenados son:")
    i=1
    table = [['Nationality', 'Number of artists']]
    while i <= sample:
        artwork = lt.getElement(nations,i)
        table.append([artwork['nation'], str(lt.size(artwork))])
        i+=1
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))    

def printMediumList(medio, MediumList, sample =3):
    j = lt.size(MediumList)
    if j < sample:
        sample = j
    print('Hay ',j, 'obras hechas en el medio' + medio)
    print("Las", sample, " más antiguas son:")
    print()
    j = lt.size(MediumList)
    i=1
    table = [['Title ', 'ArtistNames', 'Medium', 'Date', 'Dimensions']]
    while i <= sample:
        artwork = lt.getElement(MediumList,i)
        if len(str(artwork['Title'])) > 30:
            title = str(artwork['Title'])[0:30] + '...'
        else: title = str(artwork['Title'])
        if len(controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))) > 14:
            artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))[0:30] + '...'
        else: artists = controller.giveAuthorsName(catalog, eval(artwork['ConstituentID']))
        if len(artwork['Medium']) > 30:
            medium = artwork['Medium'][0:30] + '...'
        else: medium = artwork['Medium']
        if len(artwork['Dimensions']) > 35:
            dimension = artwork['Dimensions'][0:35] + '...'
        else: dimension = artwork['Dimensions']
        table.append([ title,artists,medium,artwork['Date'],dimension])
        i+=1
    
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', stralign="left")) 
catalog = None

"""
Menu principal
"""
while True:
    printMenu()
   
    inputs = input('Seleccione una opción para continuar\n')
    
    if int(inputs[0]) == 0:
        start_time = time.process_time()
        catalog = initCatalog()
        loadData(catalog)

        print("Cargando información de los archivos ....")
        print('Obras cargadas: ' + str(lt.size(catalog['artworks'])))
        print('Artistas cargados: ' + str(lt.size(catalog['artists'])))
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)
        print('La carga demoró', elapsed_time_mseg, 'segundos')
    elif int(inputs[0]) == 1:
        start_time = time.process_time()
        try:
            year1=int(input('Ingrese el año inicial: '))
            year2=int(input('Ingrese el año final: '))
        except:
            print('Por favor ingrese un año válido')
        size, positions = controller.Artist_in_a_range(year1, year2, catalog)
        
        if positions == None:
            print('No hay artistas en el rango')
        
        else:
            print('Hay', size, 'Artista(s) entre los años ingresados')
            print('Los primeros y los últimos 3 artistas (si los hay) son:')
            table = [['Nombre', 'Año de nacimiento', 'Año de fallecimiento', 'Nacionalidad', 'Género']]
            for i in positions:
                artista = lt.getElement(catalog['artists'], i)
                Nombre = artista['DisplayName']
                Nacimiento = artista['BeginDate']
                Fallecimiento = artista['EndDate']
                Nacionalidad = artista['Nationality']
                Genero = artista['Gender']
                table.append([Nombre, Nacimiento, Fallecimiento, Nacionalidad, Genero])
            print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('La carga demoró', elapsed_time_mseg, 'milisegundos')

    elif int(inputs[0]) == 2:
        start_time = time.process_time()
        try:
            InitialYear = int(input('Escriba el año inicial de las obras (AAAA): '))
            InitialMonth = int(input('Escriba el mes inicial de las obras (MM): '))
            InitialDay = int(input('Escriba el día inicial de las obras (DD): '))
            FinalYear = int(input('Escriba el año final de las obras (AAAA): ')) 
            FinalMonth = int(input('Escriba el mes inicial de las obras (MM): '))
            FinallDay = int(input('Escriba el día inicial de las obras (DD): '))
            beginDate = str(InitialYear) +'-' + str(InitialMonth) +'-' + str(InitialDay) 
            endDate = str(FinalYear) + '-' + str(FinalMonth) + '-' + str(FinallDay)
            date_object1 = datetime.strptime(beginDate, '%Y-%m-%d').date()
            date_object2 = datetime.strptime(endDate, '%Y-%m-%d').date()
        
            
            print('=============== Req No.2 Inputs ===============')
            print('Busca obras entre ', beginDate, ' y ', endDate)
            print()
            print('=============== Req No.2 Answer ===============')
            printSortResults(controller.giveRangeOfDates(catalog, beginDate, endDate))
            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            print('La carga demoró', elapsed_time_mseg, 'milisegundos')
            
        except:
            print('Por favor ingrese una fecha válida')
            print()

    elif int(inputs[0]) == 3:
        start_time = time.process_time()
        name = input('Ingrese el nombre del artista: ')


        ID, medium, total, pos1, pos2, size, name_1 = controller.Artworks_in_a_medium(name, catalog)

        if name == name_1:
            print('La cantidad de obras de', name_1, 'es: ', size)
            print('El medio más empleado es: ', medium) 
            print('En número de técnicas utilizadas es: ', total)
            print('Las obras en las que se utilizó', medium, 'son: ')
            try:
                table = [['Título', 'Fecha', 'Medio', 'Dimensiones']]
                while pos1 <= pos2:
                    obra = lt.getElement(controller.me.getValue(controller.mp.get(catalog['artists_mediums'], ID))['Artworks'], pos1)
                    Titulo = obra['Title']
                    Fecha = obra['Date']
                    Medio = obra['Medium']
                    Dimensiones = obra['Dimensions']

                    if len(Titulo) > 30:
                        Titulo = str(Titulo)[0:30] + '...'
                    else: Titulo = str(Titulo)
                    if len(Medio) > 30:
                        Medio = str(Medio)[0:30] + '...'
                    else: Medio = str(Medio)
                    if len(Dimensiones) > 35:
                        Dimensiones = str(Dimensiones)[0:35] + '...'
                    else: Dimensiones = str(Dimensiones)

                    table.append([Titulo, Fecha, Medio, Dimensiones])
                    pos1 += 1
            except:
                table=[['No hay obras registradas para el artista']]
            print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            print('La carga demoró', elapsed_time_mseg, 'milisegundos')
        else:
            print('El nombre ingresado no registra')

    elif int(inputs[0]) == 4:
        start_time = time.process_time()
        print('=============== Req No.4 Inputs ===============')
        print('Clasificando las obras por la nacionalidad de sus creadores... ')
        print()
        print('=============== Req No.4 Answer ===============')
        print()
        printSortNations(catalog['nations'])
        print()
        printBigNation(catalog['bigNation'])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('La carga demoró', elapsed_time_mseg, 'milisegundos')
    elif int(inputs[0]) == 5: 
        start_time = time.process_time()
        price, weight, size, Oldest, Oldest_prices, expensives, expensive_prices = trydepartment()

        if weight == 0:
            weight = 'no registra'

        print('El precio estimado del transporte es: ', price)
        print('El peso total de las obras es de: ', weight)
        print('El número de obras a transportar es de:', size)
        print('Las obras más antiguas a transportar son: ')
        table = [['Título', 'Clasificación', 'Fecha', 'Medio', 'Dimensiones', 'Costo', 'Artistas', 'Department']]
        n = 0
        for obra in Oldest:
            if len(str(obra['Title'])) > 20:
                title = str(obra['Title'])[0:20] + '...'
            else: title = str(obra['Title'])
            try:
                if len(controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))) > 14:
                    artists = controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))[0:30] + '...'
                else: artists = controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))
            except:
                artists = 'no registra'
            if len(obra['Medium']) > 20:
                medium = obra['Medium'][0:20] + '...'
            else: medium = obra['Medium']
            if len(obra['Dimensions']) > 20:
                dimension = obra['Dimensions'][0:20] + '...'
            else: dimension = obra['Dimensions']
            Clasificacion = obra['Classification']
            Fecha = obra['Date']
            Costo = (Oldest_prices[n])
            Department = obra['Department']
            table.append([title, Clasificacion, Fecha, medium, dimension, Costo, artists, Department])
            n+=1
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', stralign='left'))
        table = [['Título', 'Clasificación', 'Fecha', 'Medio', 'Dimensiones', 'Costo', 'Artistas']]
        print('Las obras más caras son: ')
        n = 0
        for obra in expensives:
            if len(str(obra['Title'])) > 20:
                title = str(obra['Title'])[0:20] + '...'
            else: title = str(obra['Title'])
            try:
                if len(controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))) > 14:
                    artists = controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))[0:30] + '...'
                else: artists = controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))
            except:
                artists = 'no registra'
            if len(obra['Medium']) > 20:
                medium = obra['Medium'][0:20] + '...'
            else: medium = obra['Medium']
            if len(obra['Dimensions']) > 20:
                dimension = obra['Dimensions'][0:20] + '...'
            else: dimension = obra['Dimensions']
            Clasificacion = obra['Classification']
            Fecha = obra['Date']
            Costo = expensive_prices[n]
            table.append([title, Clasificacion, Fecha, medium, dimension, Costo, artists])
            n+=1
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', stralign='left'))
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('La carga demoró', elapsed_time_mseg, 'milisegundos')

    elif int(inputs[0]) == 6:
        try:
            start_time = time.process_time()
            InitialYear = int(input('Escriba el año inicial de las obras: '))
            EndingYear = int(input('Escriba el año final de las obras: '))
            n = int(input('Indique el número de artistas a consultar: '))
            print()
            print('=============== Req No.6 Inputs ===============')
            print('Buscando los', n, 'más prolíficos entre ', InitialYear, ' y ', EndingYear)
            print()
            print('=============== Req No.6 Answer ===============')
            printReq6(catalog, InitialYear, EndingYear, n)
            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            print('La carga demoró', elapsed_time_mseg, 'milisegundos')
        except:
            print()
            print('ERROR: Ingrese un número válido')
            print()
    
    else:
        sys.exit(0)
sys.exit(0)


