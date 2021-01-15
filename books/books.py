import argparse
import csv
import sys

all_books = []
def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='prints out a list of books that satisfy the filter(s) given by a user')
    parser.add_argument('-a', '--filter_author', metavar='author', nargs= '1', help='author whose books you are searching for')
    parser.add_argument('-t', '--filter_title', metavar='title', nargs= '1', help='book title you are searching for')
    parser.add_argument('-y', '--filter_year', metavar='year', nargs = '+', help='the years in which you would like to search')
    #parser.add_argument('-h', '--help', nargs = 0, help = 'usage.txt')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

#if you want to search title, do filter_author_or_title("title", [your title])
#if you want to search author, do filter_author_or_title("author", [your author])
def filter_author_or_title(author_or_title, one_name):
    global all_books
    after_filter = []
    if author_or_title == "author":
        for row in all_books:
            if one_name.lower() in row[2].lower():
                after_filter.append(row)
    elif author_or_title == "title":
        for row in all_books:
            if one_name.lower() in row[0].lower():
                after_filter.append(row)
    else:
        print("Error! only 'author' and 'title' choice are allowed")

    return after_filter

#if user only input 1 year, use "filter_year_range([start_year], "no end year"). Literally, the string "no end year"
def filter_year_range(start_year, end_year):
    global all_books
    after_filter = []
    if end_year != "no end year":
        for row in all_books:
            if int(row[1]) >= int(start_year) and int(row[1]) <= int(end_year):
                after_filter.append(row)
    else:
        for row in all_books:
            if int(row[1]) == int(start_year):
                after_filter.append(row)
    return after_filter

def main():
    global all_books
    with open('books.csv') as file:
        all_books = (list(csv.reader(file, skipinitialspace=True)))
    original_copy = all_books.copy()

    arguments = get_parsed_arguments()
    #filter_output = filter_books(arguments):
    #organize_output(filter_output):

#def filer_books(arguments):
    filter_output = []

    #if arguments.help:
    #    with open('usage.txt') as file:
    #        print(file)

    # if len(list(arguments.filter_title)) > 1:
    #     print("You can only search for 1 title at a time \n, if there is a space in your input, put them into a pair of quotation sign")
    # if len(list(arguments.filter_author)) > 1:
    #     print("You can only search for 1 author at a time \n, if there is a space in your input, put them into a pair of quotation sign")


    if arguments.filter_title:
        all_books = filter_author_or_title("title", arguments.filter_title[0])
        filter_output.append("with the title: " + arguments.filter_title[0])
        all_books = sorted(all_books,key=lambda x: (x[0]))
    if arguments.filter_year:
        years = []
        for year in arguments.filter_year:
            years.append(int(year))
        years.sort()
        if len(years) > 1:
            all_books = filter_year_range(years[0], years[1])
            filter_output.append("published in the year range: " + str(years[0]) + "-" + str(years[1]))
        else:
            all_books = filter_year_range(years[0], "no end year")
            filter_output.append("published in: " + str(years[0]))
        all_books = sorted(all_books,key=lambda x: (x[1]))
    if arguments.filter_author:
        all_books = filter_author_or_title("author", arguments.filter_author[0])
        filter_output.append("written by: " + arguments.filter_author[0])
        all_books = sorted(all_books,key=lambda x: (x[2]))
    #return (filter_output)

#def organize_output(filter_output, arguments):
#organize output of of books into a table with titles, years, and authors
    filter_print = ''
    for each in filter_output:
        filter_print= filter_print + each
    if (len(all_books) == 0):
        print("There are no books " + filter_print)
    else:
        titles = []
        years = []
        authors = []
        for book in all_books:
            titles.append(book[0])
            years.append(book[1])
            authors.append(book[2])


        titles =["titles", "years", "authors"]
        #data = [titles] + list(zip(titles, authors, years))


        if (not arguments.filter_author) and (not arguments.filter_year) and (not arguments.filter_title):
            print("You must use at least one filter, or type 'python3 books.py --help' for help")
        else:
            data = [titles] + all_books
            for i, d in enumerate(data):
                #line = '|'.join(str(x).ljust(30) for x in d)
                line = ''
                for j, each in enumerate(d):
                    if j == 0:
                        line = line + str(each).ljust(55)
                    if j == 1:
                        line = line + str(each).ljust(10)
                    if j == 2:
                        line = line + each
                print(line)
                if i == 0:
                    print('-' * len(line))
        #print(filter_print)
        #for each in all_books:
        #    print("title: " + each[0] + " \t year: "+ each[1] + "\t author:" + each[2])


if __name__ == '__main__':
    main()
