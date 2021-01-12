import argparse
import csv
all_books = []
def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('searchAuthor', metavar='Author', nargs='+', help='author whose books you are searching for')
    parser.add_argument('searchTitle', metavar='Title', nargs='+', help='string you are looking for in book title')
    parser.add_argument('yearRange', '-yr', default='1759-2020', help='the years in which you would like to sort')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def filter_author(one_name):
    global all_books
    after_filter = []
    for row in all_books:
        if one_name.lower() in row[2].lower():
            after_filter.append(row)
    return after_filter

def filter_single_year(a_year):
    global all_books
    after_filter = []
    for row in all_books:
        if int(row[1]) == int(a_year):
            after_filter.append(row)
    return after_filter

def filter_year_range(start_year, end_year):
    global all_books
    after_filter = []
    for row in all_books:
        if int(row[1]) >= int(start_year) and int(row[1]) <= int(end_year):
            after_filter.append(row)
    return after_filter

def main():
    # arguments = get_parsed_arguments()
    # for animal in arguments.animals:
    #     noise = get_animal_noise(arguments.language, animal)
    #     if noise:
    #         print(f'The {animal} says "{noise}"')
    #     else:
    #         print(f'I don\'t know what the {animal} says in {arguments.language}')
    global all_books
    with open('books.csv') as file:
        all_books = (list(csv.reader(file, skipinitialspace=True)))
    
    all_books = filter_author("toni")
    all_books = filter_year_range(0000, 2000)
    print(all_books)
    

if __name__ == '__main__':
    main()
