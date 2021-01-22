'''
book search program books.py
created by Grace de Benedetti and Jimmy Zhong at Carleton College
revised by Grace and Jimmy
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

class a_book:
    def __init__(self, book_title, publish_year, author):
        self.book_title = str(book_title)
        self.publish_year = int(publish_year)
        self.author = str(author)

def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='prints out a list of books that satisfy the filter(s) given by a user')
    parser.add_argument('-a', '--filter_author', metavar='author', nargs= 1, help='author whose books you are searching for')
    parser.add_argument('-t', '--filter_title', metavar='title', nargs= 1, help='book title you are searching for')
    parser.add_argument('-y', '--filter_year', metavar='year', nargs = '+', help='the years in which you would like to search')
    parsed_arguments = parser.parse_args()
    return parsed_arguments


def filter_author_or_title(author_or_title, search_str, input_books):
    '''search a title => do filter_author_or_title("title", [your title])
       search an author => do filter_author_or_title("author", [your author])
       return a list of all books with given title/author'''
    after_filter = []
    if author_or_title == "author":
        for book in input_books:
            if search_str.lower() in (book.author).lower():
                after_filter.append(book)
    elif author_or_title == "title":
        for book in input_books:
            if search_str.lower() in (book.book_title).lower():
                after_filter.append(book)
    else:
        print("Error! only 'author' and 'title' choice are allowed")
    return after_filter


def filter_year_range(start_year, end_year, input_books):
    '''return a list of all books published between start_year and end_year
       if user only input 1 year => do "filter_year_range([start_year], "no end year"). Literally, the string "no end year"'''
    after_filter = []
    if end_year != "no end year":
        for book in input_books:
            if book.publish_year >= int(start_year) and book.publish_year <= int(end_year):
                after_filter.append(book)
    else:
        for book in input_books:
            if book.publish_year >= int(start_year):
                after_filter.append(book)
    return after_filter


def filter_books_by_argument(arguments, input_books):
    '''parse user inputs and combine different filters
       return the list of books that statisfies all filters'''
    books_after_filter = input_books
    filter_output = []
    if arguments.filter_title:
        user_search = arguments.filter_title[0]
        books_after_filter = filter_author_or_title("title", user_search, books_after_filter)
        filter_output.append("with: '" + user_search + "' in the title.")
        books_after_filter = sorted(books_after_filter, key=lambda x: x.book_title)
    if arguments.filter_year:
        years = []
        for year in arguments.filter_year:
            years.append(int(year))
        start_year, end_year = min(years), max(years)
        if len(years) > 1:
            books_after_filter = filter_year_range(start_year, end_year, books_after_filter)
            filter_output.append("published in the year range: " + str(start_year) + "-" + str(end_year))
        else:
            books_after_filter = filter_year_range(start_year, "no end year", books_after_filter)
            filter_output.append("published after the year: " + str(start_year))
        books_after_filter = sorted(books_after_filter, key=lambda x: x.publish_year)
    if arguments.filter_author:
        user_search = arguments.filter_author[0]
        books_after_filter = filter_author_or_title("author", user_search, books_after_filter)
        filter_output.append("written by an author with: '" + user_search + "' in their name.")
        books_after_filter = sorted(books_after_filter, key=lambda x: x.author)

    return books_after_filter, filter_output

def print_formatting_line(title, year, author):
    '''used in organize_ouput, print a formatted line given 3 inputs objects, return the length of the printed line'''
    str_to_print = str(title).ljust(55) + str(year).ljust(10) + str(author)
    print(str_to_print)
    return len(str_to_print)

def organize_output(filter_output, arguments, books_after_filter):
    '''organize the list of output books into a nice-looking table with titles, years, and authors'''
    filter_print = ''
    for each in filter_output:
        filter_print= filter_print + each
    if (len(books_after_filter) == 0):
        print("There are no books " + filter_print)
    else:
        header_length = print_formatting_line("titles", "years", "authors")
        print('-' * header_length)
        for book in books_after_filter:
            print_formatting_line(book.book_title, book.publish_year, book.author)

def main():
    all_books = []
    with open('books.csv') as file:
        read_in_file = (list(csv.reader(file, skipinitialspace=True)))
    for row in read_in_file:
        if len(row) > 1:
            # create book objects given book_title, publish_year, and author
            all_books.append(a_book(row[0], row[1], row[2]))

    arguments = get_parsed_arguments()
    book_list_after_filter, filter_output = filter_books_by_argument(arguments, all_books)
    organize_output(filter_output, arguments, book_list_after_filter)

if __name__ == '__main__':
    main()
