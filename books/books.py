'''
book search program books.py
created by Grace de Benedetti and Jimmy Zhong at Carleton College
Under Prof Jeff Ondich: CS 257, Winter 2020

Given a books.csv of a book list with book title, published year, and author
return a list of books that stasifies the given filters

available filters:
--filter_author [author name]
--filter_title [book_title]
--filter_year [year] # book published at this year
--filter_year [start_year] [end_year] # book published between start_year and end_year
'''
import argparse
import csv
import sys

def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='prints out a list of books that satisfy the filter(s) given by a user')
    parser.add_argument('-a', '--filter_author', metavar='author', nargs= 1, help='author whose books you are searching for')
    parser.add_argument('-t', '--filter_title', metavar='title', nargs= 1, help='book title you are searching for')
    parser.add_argument('-y', '--filter_year', metavar='year', nargs = '+', help='the years in which you would like to search')
    parsed_arguments = parser.parse_args()
    return parsed_arguments


def filter_author_or_title(author_or_title, one_name, input_books):
    '''search a title => do filter_author_or_title("title", [your title])
       search an author => do filter_author_or_title("author", [your author])
       return a list of all books with given title/author'''
    after_filter = []
    if author_or_title == "author":
        for row in input_books:
            if one_name.lower() in row[2].lower():
                after_filter.append(row)
    elif author_or_title == "title":
        for row in input_books:
            if one_name.lower() in row[0].lower():
                after_filter.append(row)
    else:
        print("Error! only 'author' and 'title' choice are allowed")
    return after_filter


def filter_year_range(start_year, end_year, input_books):
    '''return a list of all books published between start_year and end_year
       if user only input 1 year => do "filter_year_range([start_year], "no end year"). Literally, the string "no end year"'''
    after_filter = []
    if end_year != "no end year":
        for row in input_books:
            if int(row[1]) >= int(start_year) and int(row[1]) <= int(end_year):
                after_filter.append(row)
    else:
        for row in input_books:
            if int(row[1]) == int(start_year):
                after_filter.append(row)
    return after_filter


def filter_books(arguments, input_books):
    '''parse user inputs and combine different filters
       return the list of books that statisfies all filters'''
    books_after_filter = input_books
    filter_output = []
    if arguments.filter_title:
        user_search = arguments.filter_title[0]
        books_after_filter = filter_author_or_title("title", user_search, books_after_filter)
        filter_output.append("with: " +  arguments.filter_title[0] + " in the title.")
        books_after_filter = sorted(books_after_filter, key=lambda x: (x[0]))
    if arguments.filter_year:
        years = []
        for year in arguments.filter_year:
            years.append(int(year))
        years.sort()
        if len(years) > 1:
            books_after_filter = filter_year_range(years[0], years[1], books_after_filter)
            filter_output.append("published in the year range: " + str(years[0]) + "-" + str(years[1]))
        else:
            books_after_filter = filter_year_range(years[0], "no end year", books_after_filter)
            filter_output.append("published in the year: " + str(years[0]))
        books_after_filter = sorted(books_after_filter, key=lambda x: (x[1]))
    if arguments.filter_author:
        books_after_filter = filter_author_or_title("author", arguments.filter_author[0], books_after_filter)
        filter_output.append("written by an author with: " + arguments.filter_author[0] + " in their name.")
        books_after_filter = sorted(books_after_filter, key=lambda x: (x[2]))
    
    return books_after_filter, filter_output

def organize_output(filter_output, arguments, books_after_filter):
    '''organize the list of output books into a nice-looking table with titles, years, and authors'''
    filter_print = ''
    for each in filter_output:
        filter_print= filter_print + each
    if (len(books_after_filter) == 0):
        print("There are no books " + filter_print)
    else:
        titles = []
        years = []
        authors = []
        for book in books_after_filter:
            titles.append(book[0])
            years.append(book[1])
            authors.append(book[2])

        titles =["titles", "years", "authors"]
        if (not arguments.filter_author) and (not arguments.filter_year) and (not arguments.filter_title):
            print("You must use at least one filter, or type 'python3 books.py --help' for help")
        else:
            data = [titles] + books_after_filter
            for i, d in enumerate(data):
                line = ''
                for j, each in enumerate(d):
                    if j == 0: # for book titles
                        line = line + str(each).ljust(55)
                    if j == 1: # for book publish years
                        line = line + str(each).ljust(10)
                    if j == 2: # for author names
                        line = line + each
                print(line)
                if i == 0:
                    print('-' * len(line))

def main():
    with open('books.csv') as file:
        all_books = (list(csv.reader(file, skipinitialspace=True)))
    arguments = get_parsed_arguments()
    book_list_after_filter, filter_output = filter_books(arguments, all_books)
    organize_output(filter_output, arguments, book_list_after_filter)

if __name__ == '__main__':
    main()
