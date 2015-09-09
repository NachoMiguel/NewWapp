import re
import datetime
import heapq


from django.shortcuts import render


def index(request):
    """
    :param data: request
    :return: porcentajes de la conversacion
    """
    file = open("wappApp/Forever.txt", encoding="UTF-8")
    data = file.read()
    file.close()

    lines = data.split("\n")

    # Search for all the days in the conversation #
    dates_str_and_literal = search_date(lines)

    # 02/jan/2015
    dates = dates_str_and_literal[0]
    # 02/01/2015
    literal = dates_str_and_literal[1]

    dates_people_talk_more = dates_with_more_comments(lines, literal)

    # Get the name of the users and the string that represents when a user talks  #
    users_and_when_users_talk = get_users_names(lines)

    # String that represents when users talks #
    w_u_t = list(users_and_when_users_talk[0])

    # number of times each user talks #
    user_talks_count = get_users_count_talks(lines, w_u_t)

    return render(request, 'wappApp/index.html', context={'dates': dates, 'users': users_and_when_users_talk,
                                                          'talks': user_talks_count})


def search_date(lines):
    """
    :param data: la conversacion de wapp
    :return: los dias en que produjeron las conversaciones, dia por dia
    """

    # Create empty list, split each line with "," and save the first part into the list #
    lista = [line.split(",", 1)[0] for line in lines]

    # Create regex pattern and compile it #
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
    users_pattern = re.compile(r"\s- [a-zA-Z]+:")

    # use the pattern to search for each line #
    match_objects_users = [re.search(users_pattern, m) for m in lines]

    # make sure that there are no stupid things instead of names #
    string_objects_users = set([w.group() for w in match_objects_users if w is not None and w.group() not in not_user_names])

    # new pattern to be more precise with the names #
    just_user_pattern = re.compile(r"[a-zA-Z]+")

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
    dict_users = {}
    for user in wut:
        count = 0
        for line in lines:
            if user in line:
                count += 1
        dict_users[user] = count

    return dict_users


def dates_with_more_comments(lines, literals):
    dict_days = {}
    for day in literals:
        count = 0
        for line in lines:
            if day in line:
                count += 1
        dict_days[day] = count

    newA = heapq.nlargest(5, dict_days, key=dict_days.get)

    return newA
