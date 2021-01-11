import argparse

def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('searchAuthor', metavar='Author', nargs='+', help='author whose books you are searching for')
    parser.add_argument('searchTitle', metavar='Title', nargs='+', help='string you are looking for in book title')
    parser.add_argument('yearRange', '-yr', default='1759-2020', help='the years in which you would like to sort')
    parsed_arguments = parser.parse_args()
    return parsed_arguments


def main():
    arguments = get_parsed_arguments()
    for animal in arguments.animals:
        noise = get_animal_noise(arguments.language, animal)
        if noise:
            print(f'The {animal} says "{noise}"')
        else:
            print(f'I don\'t know what the {animal} says in {arguments.language}')

if __name__ == '__main__':
    main()
