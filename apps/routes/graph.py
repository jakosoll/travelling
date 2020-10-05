from apps.trains.models import Train


def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов
       из одного города в другой. Вариант посещения
       одного и того же города более одного раза,
        не рассматривается.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph():
    qs = Train.objects.values()
    from_city_set = set(i['from_city_id'] for i in qs)
    graph = {}
    for city in from_city_set:
        trains = Train.objects.filter(from_city=city).values('to_city')
        tmp = set(i['to_city'] for i in trains)
        graph[city] = tmp
    return graph


def handle_form_data_and_get_all_ways(data):
    from_city = data['from_city']
    to_city = data['to_city']
    across_cities_form = data['across_cities']
    travel_time = data['travel_time']  # раскладываем данные в переменные
    graph = get_graph()  # получаем граф маршрутов
    all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
