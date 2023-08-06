#! /usr/bin/python3
# -*- coding: utf-8 -*-
# --------------------------------------------
#+ Autor:	Ran#
#+ Creado:	05/07/2021 17:08:25
#+ Editado:	24/07/2021 01:56:48
# --------------------------------------------

import random

# risca o texto proporcionado
def riscar(catex):
    """
    Dado un texto introducido, devolveo riscado.
    Se se introduce unha lista, mira cada elemento e,
    de ser texto, devolveo riscado.

    @entrada:
        catex   -   Requirido  -    Catex
        └ Catex/Lista a modificar.

    @saida:
        Catex/Lista.
        └ Catex de entrada riscado.
    """

    # se mete un catex
    if type(catex) == str:
        return ''.join([u'\u0336{}'.format(ele) for ele in catex])

    # se mete unha lista
    elif type(catex) == list:
        # para cada elemento da lista chamamos á operación de riscado e metemos o novo valor no lugar do vello
        for index, ele in enumerate(catex):
            catex[index] = riscar(ele)
        return catex

    # se non é ningún devolver a entrada tal cal
    else:
        return catex

# converte un texto proporcionado a leetspeak
def leetspeak(catex, espaciado=True):
    """
    Dado un texto introducido, devolveo traducido a leetspeak.
    Se se introduce unha lista, mira cada elemento e,
    de ser texto, devolveo en traducido.

    @entrada:
        catex       -   Requirido   -   Catex
        └ Catex/Lista a modificar.
        espaciado   -   Opcional    -   Booleano
        └ Booleano que indica se se espacian os caracteres de leetspeak para favorecer a lectura.

    @saida:
        Catex/Lista.
        └ Traducción do catex de entrada a leetspeak.
    """

    leetspeak_basico = {
            'a': ['4', '@', '/\\', '/-\\', '?', '^', 'α', 'λ', '(L', 'Д', 'AYE'],
            'b': ['8', '|3', 'ß', 'l³', '13', 'I3', 'J3', '!3', '(3', '/3', ')3', '|-]', 'j3', '6'],
            'c': ['(', '[', '<', '©', '¢', '{'],
            'd': ['|)', '|]', 'Ð', 'đ', '1)' ')', '(|', '[)' 'I>', '|>', '?', 'T)' 'I7', 'cl', '|}'],
            'e': ['3', '€', '&', '£', 'ε', 'ë', '[-', '|=-'],
            'f': ['|=', 'PH', '|*|-|', '|"', 'ƒ', 'l²', '|#', '/=', 'v'],
            'g': ['6', '&', '9', '(_+', 'C-', 'GEE', '(?,', '[,', '{,', '<_', '(.'],
            'h': ['#', '4', '|-|', '}{', ']-[', '/-/', ')-(', '[-]', '(-)', ':-:', '|~|', '|-|', ']~[', '}{', '!-!', '1-1', '\\-/', 'I+I', '/-\\'],
            'i': ['!', '1', '|', '][', 'ỉ', '[]', 'EYE', '3Y3'],
            'j': ['_|', '¿', ',_|', '_|', '._|', '._]', '_]', ',_]', ']', ';', '1'],
            'k': ['|<', '|{', '|(', 'X', '>|', '/<', '1<', '|c', '|(', '|{'],
            'l': ['1', '|_', '£','|', '][_', '7'],
            'm': ['/\/\\', '/v\\', '|V|', ']V[', '|\\/|', 'AA', '[]V[]', '|11', '/|\\', '^^', '(V)', '|Y|', '!\\/!', '/V\\', 'JVI', '[V]', '<V>',
                '{V}', '(v)', 'nn', 'IVI', '|\\|\\', '1^1', 'ITI', 'JTI'],
            'n': ['|\\|', '/\\/', '/V', '|V', '/\\\\/', '|1', '2', '?', '(\\)', '11', 'r', '!\\!', '^/', '[\\]', '<\\>', '{\\}', 'И', '^', 'ท'],
            'o': ['0', '9', '()', '[]', '*', '°', '<>', 'ø', '{[]}', 'q', 'OH', 'p'],
            'p': ['9','|°', '|>', '|*', '[]D', '][D', '|²', '|?', '|D', '|o', '?', '|^', '|"', '|7'],
            'q': ['0_', '0,', '(_,)', '9', '()_', '2', '0_', '<|', '&'],
            'r': ['2', '|2', '1²', '®', '?', 'я', '12', '.-', '|`', '|~', '|?', '/2', '|^', 'lz', '|9', '[z', 'Я', '|-', '2º', '|º', 'Iº', 'Jº'],
            's': ['5', '$', '§', '?', 'ŝ', 'ş', 'z', 'EHS', 'ES', '2'],
            't': ['7', '+', '†', '\'][\'' , '|', '-|-', '\'][\'', '"|"', '~|~'],
            'u': ['|_|', 'µ', '[_]', 'v', '(_)', 'v', 'L|', 'บ'],
            'v': ['\\/' , '|/' , '\\|' , '\\\''],
            'w': ['\\/\\/', 'VV', '\\A/', '\\\\', 'uu', '\\^/', '\\|/', 'uJ', '\\N', '\'//', '\\\\\'', '(n)', '\\V/', '\\X/', '\\|/', '\\_|_/',
                '\\_:_/', 'Ш', 'Щ', 'uu', '2u', '\\\\//\\\\//', 'พ', 'v²'],
            'x': ['><', ')(', '}{', '%', '?', '×', '][', 'Ж', 'ECKS', '×'],
            'y': ['`/', '°/', '¥', 'j', 'Ч', '7', '\\|/', '\\//'],
            'z': ['z', '2', '"/_', '7_', '-/_', '%', '>_', 's', '~/_', '-\\_', '-|_'],
            ' ': ['_', '-', '__', '--', '_-_', '-_-'] 
            }

    ls_catex = ''

    # se mete un catex
    if type(catex) == str:
        ls_catex = ''.join([random.choice(leetspeak_basico[caracter.lower()])+' ' for caracter in catex])

        if espaciado: 
            return ls_catex[:-1]
        else:
            return ls_catex.replace(' ', '')

    # se mete unha lista
    elif type(catex) == list:
        return 'sen facer'

# --------------------------------------------

if __name__ == '__main__':
    print('*> Probas <*')
    print('> riscar')
    print('Riscando "texto": ', end='')
    print(riscar('texto'))
    print('Riscando lista ["texto","lista"]: ', end='')
    print(riscar(['texto', 'lista']))
    print('Riscando lista ["texto", ["lista", "listisima"]]: ', end='')
    print(riscar(['texto', ['lista', 'listisima']]))
    print('Riscando lista ["texto", ["lista", "listisima", ["si", 2]]]: ', end='')
    print(riscar(['texto', ['lista', 'listisima', ['si', 2]]]))
    print()
    print('> leetspeak')
    print('"Proba" convírtese en {}'.format(leetspeak('Proba')))
    print('"Probando o convertidor" convírtese en {}'.format(leetspeak('Probando o convertidor')))
    print('"Probando o convertidor" convírtese en {}'.format(leetspeak('Probando o convertidor', False)))
    print()
    
# --------------------------------------------
