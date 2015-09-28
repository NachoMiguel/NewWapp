import re
import datetime
import json
import operator
from collections import Counter
from django.http import HttpResponse
from django.shortcuts import render, Http404


def index(request):
    """
    :param data: request
    :return: porcentajes de la conversacion
    """
    return render(request, 'wappApp/index.html')


def do_some_work(request):

    if request.is_ajax() and request.method == "POST":
        if len(request.FILES) != 0:

            data = request.FILES['some_file']

            lineas = data.readlines()

            lines = [linea.decode('utf-8')for linea in lineas]

            # Busca todos los dias en la conversacion #
            dates_str_and_literal = search_date(lines)

            # 02/jan/2015
            dates = dates_str_and_literal[0]
            # 02/01/2015
            literal = dates_str_and_literal[1]

            # Saca los dias con mas comentarios #
            dates_people_talk_more = dates_with_more_comments(lines, literal)

            # Obtiene el nombre de los usuarios y el string que representa cuando los usuarios hablan  #
            users_and_when_users_talk = get_users_names(lines)

            # Solo usuarios #
            solo_users = users_and_when_users_talk[1]

            # String que representa cuando los usuarios hablan #
            w_u_t = list(users_and_when_users_talk[0])

            # Numero de veces cuando un usuario habla #
            user_talks_count = get_users_count_talks(lines, w_u_t)

            context = {'dates': dates_people_talk_more, 'users': solo_users,
                                             'talks': user_talks_count}

            # Paso el diccionario a formato Json #
            data = json.dumps(context)

            return HttpResponse(data, content_type="application/json")
        else:
            raise Http404("No File uploaded")
    else:
        raise Http404("No POST data was given.")


def search_date(lines):
    """
    :param data: la conversacion de wapp
    :return: los dias en que produjeron las conversaciones, dia por dia
    """

    # Crea una lista vacia, separa cada linea con "," graba la primera parte en la lista #
    lista = [line.split(",", 1)[0] for line in lines]

    # Crea un regex pattern y lo compila #
    date_pattern = re.compile(r'\b(\d+/\d+/\d{4})\b')

    # match the pattern in the list objects and make sure there are no repetitions with set()#
    dates = set(list(filter(date_pattern.match, lista)))

    # String to datetime #
    dates_str = [datetime.datetime.strptime(d, "%d/%m/%Y") for d in dates]
    fe = list(set([f.strftime("%d/%b/%Y") for f in dates_str]))
    days_sorted = sorted(fe, key=lambda day: datetime.datetime.strptime(day, "%d/%b/%Y"))
    d = [days_sorted, dates]
    return d


def get_users_names(lines):

    """
    :param data: data del file
    :return: lista con string que representan cuando habla cada usuario y los nombres de los usuarios
    """

    not_user_names = [' - https:']

    # First pattern to look for users when they talk #
    users_pattern = re.compile(r"\s- [^:]+:")

    # use the pattern to search for each line #
    match_objects_users = [re.search(users_pattern, m) for m in lines]

    # make sure that there are no stupid things instead of names #
    string_objects_users = set([w.group() for w in match_objects_users if w is not None and w.group() not in not_user_names])

    # new pattern to be more precise with the names #
    just_user_pattern = re.compile(r"([^:]+)")

    # use new pattern #
    just_users_match_objects = [re.search(just_user_pattern, m) for m in string_objects_users]

    # get the strings out of the matched objects #
    just_users = [w.group() for w in just_users_match_objects]




    list_users_and_string_users = [string_objects_users, just_users]

    return list_users_and_string_users


def get_users_count_talks(lines, wut):

    """
    :param data: data del file, list with string that represent the users talking
    :return: lista con string que representan cuando habla cada usuario y los nombres de los usuarios
    """

    # Split text into single lines #
    dict_users = Counter()
    largo = len(wut)
    for user in wut:
        count = 0
        for line in lines:
            if user in line:
                count += 1
        dict_users[user] = count

    return dict_users.most_common(largo)


def dates_with_more_comments(lines, literals):
    dict_days = Counter()
    r = re.compile(r'\b(\d+/\d+/\d{4})\b')
    for line in lines:
        match = r.search(line)
        if match:
            dte = match.group()
            if dte in literals:
                dict_days[dte] += 1
    dias = dict_days.most_common(5)
    fechas_con_mes = numero_a_mes(dias)
    return dias


def numero_a_mes(dias):
    dict_meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                  9: 'Setiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
    dias_lista = {}
    for i in dias:
        lista = list(i)
        numero = lista[1]
        fecha_entera = lista[0]
        dia = fecha_entera.split('/')[1]
        h = dict_meses[int(dia)]
        fecha_entera = fecha_entera.replace("/" + dia + "/" " de " + h + " del ")
        dias_lista[fecha_entera] = numero
        sorted_dias = sorted(dias_lista.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_dias


def strip_numbers(wut):
    good_user = []
    for u in wut:
        if '\u202a' in u:
            u.replace('\u202a', "")
            if '\u202c' in u:
                u.replace('\u202c', "")
                good_user.append(u)
            else:
                good_user.append(u)
        else:
            good_user.append(u)

    return good_user
