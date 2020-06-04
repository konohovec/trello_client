python trello_client.py

Считывает список карточек на доске.

python trello_client.py move "CardName" "ListName"

Перемещает выбранную карточку с именем CardName в список ListName с предварительным подтверждением и выбором карточек в случае наличия дубликатов.

python trello_client.py create_column "ListName"

Создает список ListName

python trello_client.py create "CardName" "ListName"

Создает карточку CardName в колонке ListName