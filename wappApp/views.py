import re
import datetime

from django.shortcuts import HttpResponse, render


def index(request):
    file = open("wappApp/Forever.txt", encoding="UTF-8")
    data = file.read()
    file.close()

    dates = search_date(data)
    users_and_when_users_talk = get_users_names(data)

    return render(request, 'wappApp/index.html', context={'dates': dates, 'users': users_and_when_users_talk})


def search_date(data):
        """
        :param data: la conversacion de wapp
        :return: los dias en que produjeron las conversaciones, dia por dia
        """
        # Split text into single lines #
        lines = data.split("\n")

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
        return days_sorted


def get_users_names(data):

        """
        :param data: data del file
        :return: lista con string que representan cuando habla cada usuario y los nombres de los usuarios
        """

        not_user_names = [' - https:']

        # Split text into single lines #
        lines = data.split("\n")

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