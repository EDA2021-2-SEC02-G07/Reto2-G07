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
from tabulate import tabulate
from datetime import datetime
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
    print("1- Cargar información en el catálogo")
    print("2- listar cronológicamente loas artistas (Req. 1)")
    print("3- listar cronológicamente las adquisiciones (Req. 2)")
    print("4- clasificar las obras de un artista por técnica (Req. 3)")
    print("5- clasificar las obras por nacionalidad de sus creadores (Req. 4)")
    print("6- transportar obras de un departamento (Req. 5)")
    print("7- proponer una nueva exposición en el museo (Req. 6)")
    print("0- Salir")

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

def printSort2DArtworksByYear(catalog, begin, end, area, sample=5):
    artworks = controller.loadRangeOfYears2DArtworks(catalog, begin, end)
    j = len(artworks)
    if j< sample:
        sample = j  
    n = 0
    finalArea = 0
    for x in artworks:
        if (float(x['Height (cm)'])*float(x['Width (cm)']))/10000 + finalArea <= area:
            finalArea += (float(x['Height (cm)'])*float(x['Width (cm)']))/10000
            n += 1
    print('El MoMA va a exhibir obras entre', begin, 'y', end)
    print('Hay', len(artworks), 'posibles obras para exponer en un área disponible de:', area, 'm²')
    print('La posible exhibición podría tener', n ,'elementos')
    print('Se utilizaron', round(finalArea,3), 'm² de los', area, 'm² disponibles')
    print()
    print("Las primeras y últimas", sample, " obras ordenadas en el rango de años dado son:")
    print()
    
    i=0
    table = [['Title ', 'ArtistNames', 'Medium', 'Date', 'Dimensions', 'Classification']]
    while i < sample and i <= j-1:
        artwork = artworks[i]
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
        table.append([ title,artists,medium,artwork['Date'],dimension,artwork['Classification']])
        i+=1
    i = len(artworks) - 1
    while i >= j-sample and i>= 0:
        artwork = artworks[i]
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
        table.append([ title,artists,medium,artwork['Date'],dimension,artwork['Classification']])
        i-=1
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid')) 

def printBigNation(bigNation, sample =3):
    j = lt.size(bigNation)
    print('El país con más obras es ' + bigNation['nation'] + ' con', j, 'obras ' )
    print("Las primeras y últimas", sample, " obras ordenadas de nacionalidad ", "'",bigNation['nation'],"'"," son:")
    print()
    j = lt.size(bigNation)
    i=1
    table = [['Title ', 'ArtistNames', 'Medium', 'Date', 'Dimensions']]
    while i <= sample:
        artwork = lt.getElement(bigNation,i)
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
        artwork = lt.getElement(bigNation,i)
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

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
   
    inputs = input('Seleccione una opción para continuar\n')
    
    if int(inputs[0]) == 1:
        start_time = time.process_time()
        catalog = initCatalog()
        loadData(catalog)

        print("Cargando información de los archivos ....")
        print('Obras cargadas: ' + str(lt.size(catalog['artworks'])))
        print('Obras que son de dos dimensiones cargadas: ' + str(lt.size(catalog['2DArtworks'])))
        print('Artistas cargados: ' + str(lt.size(catalog['artists'])))
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)
        print('La carga demoró', elapsed_time_mseg, 'segundos')
    elif int(inputs[0]) == 2:
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

    elif int(inputs[0]) == 3:
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
        except ValueError:
            print('Por favor ingrese una fecha válida')
        print('=============== Req No.2 Inputs ===============')
        print('Busca obras entre ', beginDate, ' y ', endDate)
        print()
        print('=============== Req No.2 Answer ===============')
        printSortResults(controller.giveRangeOfDates(catalog, beginDate, endDate))
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('La carga demoró', elapsed_time_mseg, 'milisegundos')
        stop_time = time.process_time()

    elif int(inputs[0]) == 4:
        start_time = time.process_time()
        name = input('Ingrese el nombre del artista: ')


        ID, medium, total, pos1, pos2, size = controller.Artworks_in_a_medium(name, catalog)

        
        print('La cantidad de obras del artista es: ', size)
        print('El medio más empleado es: ', medium) 
        print('En número de técnicas utilizadas es: ', total)
        print('Las obras en las que se utilizó', medium, 'son: ')
        table = [['Título', 'Fecha', 'Medio', 'Dimensiones']]
        while pos1 <= pos2:
            obra = lt.getElement(catalog['artists_mediums'][ID]['Artworks'], pos1)
            Titulo = obra['Title']
            Fecha = obra['Date']
            Medio = obra['Medium']
            Dimensiones = obra['Dimensions']
            table.append([Titulo, Fecha, Medio, Dimensiones])
            pos1 += 1
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('La carga demoró', elapsed_time_mseg, 'milisegundos')

    elif int(inputs[0]) == 5:
        start_time = time.process_time()
        print('=============== Req No.4 Inputs ===============')
        print('Clasificando las obras por la nacionalidad de sus creadores... ')
        print()
        print('=============== Req No.4 Answer ===============')
        print()
        printSortNations(catalog['nations'])
        print()
        printBigNation(catalog['bigNation'])
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('La carga demoró', elapsed_time_mseg, 'milisegundos')

    elif int(inputs[0]) == 6: 
        start_time = time.process_time()
        Department = input('Ingrese el nombre del departamento: ')

        price, weight, size, Oldest, Oldest_prices, expensives, expensive_prices = controller.Department_transport(catalog, Department)

        if weight == 0:
            weight = 'no registra'

        print('El precio estimado del transporte es: ', price)
        print('El peso total de las obras es de: ', weight)
        print('El número de obras a transportar es de:', size)
        print('Las obras más antiguas a transportar son: ')
        table = [['Título', 'Clasificación', 'Fecha', 'Medio', 'Dimensiones', 'Costo']]
        n = 0
        for obra in Oldest:
            if len(str(obra['Title'])) > 30:
                title = str(obra['Title'])[0:30] + '...'
            else: title = str(obra['Title'])
            if len(controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))) > 14:
                artists = controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))[0:30] + '...'
            else: artists = controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))
            if len(obra['Medium']) > 30:
                medium = obra['Medium'][0:30] + '...'
            else: medium = obra['Medium']
            if len(obra['Dimensions']) > 35:
                dimension = obra['Dimensions'][0:35] + '...'
            else: dimension = obra['Dimensions']
            Clasificacion = obra['Classification']
            Fecha = obra['Date']
            Costo = (Oldest_prices[n])
            table.append([title, Clasificacion, Fecha, medium, dimension, Costo])
            n+=1
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', stralign='left'))
        table = [['Título', 'Clasificación', 'Fecha', 'Medio', 'Dimensiones', 'Costo']]
        print('Las obras más caras son: ')
        n = 0
        for obra in expensives:
            if len(str(obra['Title'])) > 30:
                title = str(obra['Title'])[0:30] + '...'
            else: title = str(obra['Title'])
            if len(controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))) > 14:
                artists = controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))[0:30] + '...'
            else: artists = controller.giveAuthorsName(catalog, eval(obra['ConstituentID']))
            if len(obra['Medium']) > 30:
                medium = obra['Medium'][0:30] + '...'
            else: medium = obra['Medium']
            if len(obra['Dimensions']) > 35:
                dimension = obra['Dimensions'][0:35] + '...'
            else: dimension = obra['Dimensions']
            Clasificacion = obra['Classification']
            Fecha = obra['Date']
            Costo = Oldest_prices[n]
            table.append([title, Clasificacion, Fecha, medium, dimension, Costo])
            n+=1
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', stralign='left'))
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('La carga demoró', elapsed_time_mseg, 'milisegundos')

    elif int(inputs[0]) == 7:
        start_time = time.process_time()
        InitialYear = int(input('Escriba el año inicial de las obras: '))
        EndingYear = int(input('Escriba el año final de las obras: '))
        area = float(input('Indique el área disponible en m² para los objetos planos(cuadros y fotos): '))
        print()
        print('=============== Req No.6 Inputs ===============')
        print('Busca obras entre ', InitialYear, ' y ', EndingYear)
        print('Con un área disponible de:', area, 'm²')
        print()
        print('=============== Req No.6 Answer ===============')
        printSort2DArtworksByYear(catalog, InitialYear, EndingYear, area)
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('La carga demoró', elapsed_time_mseg, 'milisegundos')
        
    else:
        sys.exit(0)
sys.exit(0)


