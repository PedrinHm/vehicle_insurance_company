import re

def clean_numeric_input(value):
    """ Limpa o input numérico, removendo letras e caracteres não numéricos. """
    return int(re.sub('[^\d]', '', value))

def check_age(value, range_str):
    """ Verifica se a idade está dentro do intervalo especificado. """
    if '+' in range_str:
        start = int(range_str[:-1])
        return value >= start
    return False

def check_experience(value, range_str):
    """ Verifica se a experiência de condução está dentro do intervalo especificado. """
    if '-' in range_str:
        low, high = map(int, range_str.replace('y', '').split('-'))
        return low <= value <= high
    return False

def check_vehicle_year(value, range_str):
    """ Verifica se o ano do veículo está dentro do intervalo especificado. """
    if 'before' in range_str:
        year = int(range_str.split(' ')[1])
        return value < year
    elif 'after' in range_str:
        year = int(range_str.split(' ')[1])
        return value >= year
    return False
