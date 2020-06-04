import requests
import sys

# Данные авторизации в API Trello
auth_params = {
    'key': 'b717a045473f5823da1dbaa1d7172452',
    'token':
        'cc7492ccba486dcc9b78c2f66660c72c15561275ac754f7c7876127e9d55684b', }

# Адрес, на котором расположен API Trello
# Именно туда мы будем отправлять HTTP запросы.
base_url = 'https://api.trello.com/1/{}'
board_id = 'wZdbadJw'


def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(
        base_url.format('boards') + '/' + board_id + '/lists',
        params=auth_params).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней
    # относятся:
    for column in column_data:
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(
            base_url.format('lists') + '/' + column['id'] + '/cards',
            params=auth_params).json()
        print(column['name'], '({} задача(и))'.format(len(task_data)))
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(
        base_url.format('boards') + '/' + board_id + '/lists',
        params=auth_params).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая
    # нам нужна
    for column in column_data:
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'),
                          data={'name': name, 'idList': column['id'],
                                **auth_params})
            break


def create_column(name):
    # Создаем новую доску
    requests.post(base_url.format('boards/' + board_id + '/lists'),
                  data={'name': name, 'idBoard': board_id,
                        **auth_params})


def move(name, column_name):
    tasks_names = {}
    column_names = {}
    column_data = requests.get(base_url.format('boards') + '/'
                               + board_id + '/lists',
                               params=auth_params).json()
    for column in column_data:
        column_names[column['id']] = column['name']
        column = requests.get(
            base_url.format('lists') + '/' + column['id'] + '/cards',
            params=auth_params).json()
        for card in column:
            if card['name'] == name:
                tasks_names[len(tasks_names) + 1] = card
                print('{}.'.format(len(tasks_names)),
                      '{}'.format(card['name']),
                      'in {}.'.format(column_names[card['idList']]),
                      'Description: {}.'.format(card['desc']))
            else:
                break
    num = int(input('Choose a card to move: '))
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая
    # нам нужна
    for column in column_data:
        if column['name'] == column_name:
            requests.put(base_url.format('cards') +
                         '/' + tasks_names[num]['id'],
                         data={'idList': column['id'], **auth_params})
    print('Card moved!')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        read()
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])