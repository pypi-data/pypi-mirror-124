"""
Модуль для работы с конфигурацией из командной строки
"""
from sys import argv
from os import getenv
from os.path import exists as path_exists, isfile
from json import dumps as json_dump, loads as json_load
import argparse
from config import __version__

new_element = None

# TODO: сделать обработку ref


def __dump_json__(file_path, json):
    with open(file_path, 'w') as file:
        file.write(json_dump(json, indent=4))


def __parse_element__(element, name_parent_element, parent_element):
    global new_element
    if element['type'] == 'object':
        parent_element[name_parent_element] = {}
        parent_element = parent_element[name_parent_element]
        for i in element['required']:
            __parse_element__(element['properties'][i], i, parent_element)
    else:
        parent_element[name_parent_element] = element.get('default')


def __update_add_command__(params, template):
    # TODO: сделать проверку на существование элемента и запрашивать перезапись
    with open(params.config_file, 'r') as config_file:
        config = json_load(config_file.read())
    for i in params.elements:
        if i not in template['properties']:
            print(f'Элемента {i} нет в шаблоне')
            return
        global new_element
        new_element = {}
        __parse_element__(template['properties'][i], i, new_element)
        config[i] = new_element[i]

    __dump_json__(params.config_file, config)
    print(f"{'Элемент добавлен' if len(params.elements) == 1 else 'Элементы добавлены'}")


def __update_delete_command__(params, template):
    with open(params.config_file, 'r') as config_file:
        config = json_load(config_file.read())

    for i in params.elements:
        if i in config.keys():
            del config[i]
            print(f"{i} элемент удален")
        else:
            print(f"{i} элемент отсутсвует в конфиге")

    __dump_json__(params.config_file, config)

    print('Удаление выполнено')


def create_command(params):
    """
    Команда создания конфига из шаблона
    """
    default_config = {
        "logging": {
            "level_logging": "ERROR",
            "format_logging": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "handlers": [
                {
                    "type_handler": "file",
                    "level_logging": "ERROR",
                    "directory_log": "logs",
                    "logging_rotation_type": "TIMED",
                    "backup_count": 1,
                    "logging_interval": "d 1"
                },
                {
                    "enabled_handler": False,
                    "type_handler": "db",
                    "level_logging": "ERROR"
                },
                {
                    "type_handler": "console",
                    "level_logging": "ERROR"
                }
            ],
            "settings_overload": [
                {
                    "name_logger": "General",
                    "settings": {
                        "handlers": [
                            {
                                "enabled_handler": True,
                                "type_handler": "file",
                                "directory_log": "logs",
                                "logging_rotation_type": "TIMED",
                                "backup_count": 1,
                                "logging_interval": "d 1"
                            }
                        ]
                    }
                }
            ]
        }
    }

    if params.list_elements:
        if not getenv('TEMPLATE_CONFIG', default=None):
            print("Не определена переменная окружения TEMPLATE_CONFIG")
            return

        template = json_load(open(getenv("TEMPLATE_CONFIG")).read())

        message = "Список доступных элементов: "
        for i in template['properties']:
            message += f"{i}, "
        print(message[:-2])
        return
    if path_exists(params.config_file):
        print('Файл конфигурации уже существует, перезаписать его? (y/n)')
        answer = input()
        if answer.lower() != "yes" and answer.lower() != 'y':
            return
    if params.elements:
        if not getenv('TEMPLATE_CONFIG', default=None):
            print("Не определена переменная окружения TEMPLATE_CONFIG")
            return

        template = json_load(open(getenv("TEMPLATE_CONFIG")).read())

        for i in params.elements:
            if i not in template['properties']:
                print(f'Элемента {i} нет в шаблоне')
                return
            global new_element
            new_element = {}
            __parse_element__(template['properties'][i], i, new_element)
            default_config[i] = new_element[i]

    __dump_json__(params.config_file, default_config)
    print('Конфигурация создана')


def update_command(params):
    """
    Команда обновления конфига
    """
    if not getenv('TEMPLATE_CONFIG', default=None):
        print("Не определена переменная окружения TEMPLATE_CONFIG")
        return
    if not path_exists(params.config_file) and not isfile(params.config_file):
        print("Указанного файла не существует")
        return

    # TODO: в удаление шаблон не используется исправить
    template = json_load(open(getenv("TEMPLATE_CONFIG")).read())
    update_methods = {
        "add": __update_add_command__,
        "delete": __update_delete_command__
    }
    update_methods[params.update_command](params, template)


methods = {
    "create": create_command,
    "update": update_command
}


def create_parse():
    """
    Команда создания парсинга аргументов
    """
    parser = argparse.ArgumentParser(add_help=False)

    parent_group = parser.add_argument_group(title="Параметры")
    parent_group.add_argument('--version', action='version', help='Вывести номер версии',
                              version='%(prog)s {}'.format(__version__))
    parent_group.add_argument("--help", "-h", action="help", help="Справка")

    subparsers = parser.add_subparsers(dest="command", title="Возможные команды",
                                       description="Команды, которые должны быть в качестве первого параметра %(prog)s")

    create_command_parser = subparsers.add_parser("create", add_help=False)
    create_command_parser.add_argument('config_file')
    create_command_parser.add_argument('-e', '--elements', nargs='+', help="Элементы, которые нужно добавить в конфиг. "
                                                                           "Для работы этого параметра требуется "
                                                                           "указать переменную окружения "
                                                                           "TEMPLATE_CONFIG")
    create_command_parser.add_argument('--list-elements', action='store_true', default=False)
    create_command_parser.add_argument('-h', '--help', action='help', help='Справка')

    update_command_parser = subparsers.add_parser('update', add_help=False)
    update_command_parser.add_argument('config_file')
    update_command_parser.add_argument('update_command', choices=['add', 'delete'])
    update_command_parser.add_argument('elements', nargs='+')
    update_command_parser.add_argument('-h', '--help', action='help', help='Справка')

    return parser


if __name__ == '__main__':
    main_parser = create_parse()
    parsed_params = main_parser.parse_args(argv[1:])

    methods[parsed_params.command](parsed_params)
