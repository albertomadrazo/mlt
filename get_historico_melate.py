import datetime
import urllib.request
import shutil
import os

import pymysql
import pymysql.cursors

from secrets import my_db, my_user, my_password


# Conecta a MySQL
connection = pymysql.connect(
    host='localhost',
    db=my_db,
    user=my_user,
    password=my_password,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
) 


def convert_csv_to_list(archivo_destino):
    registros = open(archivo_destino, 'r')
    lista_concursos = []    

    for r in reversed(list(registros.readlines())):
        lista_concursos.append(format_line_to_list(r))

    return lista_concursos


def format_line_to_list(line):
    line = line.replace('\n', '').split(',')
    try:
        line[-1] = datetime.datetime.strptime(line[-1], '%d/%m/%Y').date()
        return line
    except ValueError:
        return False    


def get_csv_from_url(url, archivo_destino):
    """
    Descarga el archivo CSV del sitio de pronósticos
    """
    try:
        with urllib.request.urlopen(url) as response, open(archivo_destino, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return True
    except OSError:
        print('No se pudo abrir el archivo')
        return False


def agregar_records_a_tabla(lista_concursos):
    clave_melate = 40
    for lista in lista_concursos:
        if lista:
            concurso = int(lista[1])
            num1 = int(lista[2])
            num2 = int(lista[3])
            num3 = int(lista[4])
            num4 = int(lista[5])
            num5 = int(lista[6])
            num6 = int(lista[7])
            num7 = int(lista[8])
            bolsa = int(lista[9])
            fecha = lista[10]

            try:
                with connection.cursor() as cursor:
                    query = "INSERT INTO melate2("
                    query += "producto, concurso, num1, num2, num3, num4, num5, num6, num7, bolsa, fecha)"
                    query += " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(query, (clave_melate, concurso, num1, num2, num3, num4, num5, num6, num7, bolsa, fecha))
                    connection.commit()
            finally:
                pass


def get_concurso():
    try:
        with connection.cursor() as cursor:
            query = "SELECT concurso FROM melate2 ORDER BY concurso DESC LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchall()
            if not result:
                return False
            else:
                return result[0]['concurso']
    finally:
        pass


def actualizar_tabla(url, archivo_csv):
    """
    Actualiza la tabla melate2 si el último concurso en el CSV es mayor al
    que está en la tabla.
    """
    concurso_csv = int(checa_ultimo_concurso_de_csv(url, archivo_csv))
    concurso_reciente = get_concurso()

    if concurso_csv == concurso_reciente:
        print("El concurso {} es el más reciente en la base de datos de melate.".format(concurso_csv))
    elif concurso_csv > concurso_reciente:
        lista_concursos = []
        # Iterar el archivo CSV desde el concurso que tenemos en nuestra db
        archivo = open(archivo_csv)
        for i, linea in enumerate(list(archivo.readlines())):
            # Formatear cada linea y meter el contenido en una lista
            tmp = format_line_to_list(linea)
            if int(tmp[1]) > concurso_reciente:
                lista_concursos.insert(0, tmp)
            else:
                break

        agregar_records_a_tabla(lista_concursos)


def checa_ultimo_concurso_de_csv(url, archivo_csv):
    existe = False
    if not os.path.exists(archivo_csv):
        if get_csv_from_url(url, archivo) == True:
            existe = True
        else:
            print('No se puede acceder al archivo CSV.')
    else:
        existe = True

    if existe == True:
        archivo = open(archivo_csv)
        ultimo_concurso = archivo.readlines()[1].split(',')[1]
        return ultimo_concurso

    return existe


def main():

    direccion_csv = 'http://pronosticos.gob.mx/Documentos/Historicos/Melate.csv'
    archivo_destino = 'melate_historico.csv'

    if get_concurso() == False:
        print('tabla vacía, se llenará con el último reporte.')
        if get_csv_from_url(direccion_csv, archivo_destino) == True:
            agregar_records_a_tabla(convert_csv_to_list(archivo_destino))
            print('listo!')
        else:
            print('No se ha podido encontrar un archivo CSV en la locación definida.')
    else:
        actualizar_tabla(direccion_csv, archivo_destino)



if __name__ == '__main__':
    main()