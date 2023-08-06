from pep_talk.pep_parts import FIRST_PART, SECOND_PART, THIRD_PART, FOURTH_PART
from colored import stylize
import colored
import random


def print_pep():
    message = f'{FIRST_PART[random.randint(0, len(FIRST_PART) - 1)]} ' + \
        f'{SECOND_PART[random.randint(0, len(SECOND_PART) - 1)]} ' + \
        f'{THIRD_PART[random.randint(0, len(THIRD_PART) - 1)]} ' + \
        f'{FOURTH_PART[random.randint(0, len(FOURTH_PART) - 1)]} '
    mark_up = colored.fg('red_1') + colored.attr('bold') + colored.bg('white')
    print(stylize(f'{message}', mark_up))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_pep()
