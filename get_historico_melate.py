import datetime
import urllib.request
import shutil
import os

import pymysql
import pymysql.cursors

from .melate.secrets import my_db, my_secret_key, my_user, my_password


# Conecta a MySQL
connection = pymysql.connect(
    host='localhost',
    user='',
    password='',
    db='melate',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
) 


def convert_csv_to_list(archivo_destino):
    registros = open(archivo_destino, 'r')
    lista_concursos = []    

    for r in reversed(list(registros.readlines())):
        r = r.replace('\n', '').split(',')
        try:
            r[-1] = datetime.datetime.strptime(r[-1], '%d/%m/%Y').date()
            lista_concursos.append(r)
        except ValueError:
            pass

    return lista_concursos


def get_csv_from_url(url, archivo_destino):
    if not os.path.exists(archivo_destino):
        with urllib.request.urlopen(url) as response, open(archivo_destino, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    else:
        return False

    return True


def llenar_tabla_vacia(lista_concursos):
    clave_melate = 40
    for lista in lista_concursos:
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
                # Funcionará si le doy commit en el finally ?
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
                return result
    finally:
        pass


def actualizar_tabla():
    concurso = get_concurso()
    if concurso == True:
        print(concurso)


def main():

    direccion_csv = 'http://pronosticos.gob.mx/Documentos/Historicos/Melate.csv'
    archivo_destino = 'melate_historico.csv'

    if get_concurso() == False:
        print('tabla vacía, se llenará con el último reporte.')
        if get_csv_from_url(direccion_csv, archivo_destino) == True:
            llenar_tabla_vacia(convert_csv_to_list(archivo_destino))
        else:
            print('No se ha podido encontrar un archivo CSV en la locación definida.')
    else:
        actualizar_tabla()
        print(get_concurso())



if __name__ == '__main__':
    main()