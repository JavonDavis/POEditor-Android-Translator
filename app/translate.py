import os

import sys, getopt
from parse import compile

STRING_FORMAT_TAG = "<string name=\"{}\">{}</string>"
STRING_ARRAY_FORMAT_TAG = "<string-array name=\"{}\">{}</string-array>"
ITEM_FORMAT_TAG = "<item>{}</item>"

string_compiler = compile(STRING_FORMAT_TAG)
string_array_compiler = compile(STRING_ARRAY_FORMAT_TAG)
item_compiler = compile(ITEM_FORMAT_TAG)

STRING_OPEN_TAG = "<string"
STRING_CLOSE_TAG = "</string>"

STRING_ARRAY_OPEN_TAG = "<string-array"
STRING_ARRAY_CLOSE_TAG = "</string-array>"

ITEM_START_TAG = "<item>"
ITEM_END_TAG = "</item>"

OPENING_XML_TAG = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<resources>"
CLOSING_XML_TAG = "\n</resources>"

ARRAY_NAME_TYPE = "sa({})"
array_name_compiler = compile(ARRAY_NAME_TYPE)


def execute(file_name):
    """
    Outputs 2 files one to be uploade to POEditor and one to be used to build back the xml
    :param file_name: name of xml file to read from
    :return: None
    """
    fo = open(file_name, "rb+")
    file_data = fo.read()
    start_index = 0

    names_file = "names.csv"
    values_file = "values.csv"

    name_data = ''
    values_data = ''
    name_pointer = open(names_file, "wb+")
    values_pointer = open(values_file, "wb+")

    while True:
        start_index_string = file_data.find(STRING_OPEN_TAG, start_index)
        start_index_array = file_data.find(STRING_ARRAY_OPEN_TAG, start_index)

        valid_tag_left = start_index_string > -1 or start_index_array > -1

        if not valid_tag_left:
            break

        start_index = start_index_string + 1
        if start_index_string == start_index_array:
            # Found String array

            end_index_array = file_data.find(STRING_ARRAY_CLOSE_TAG, start_index_array)
            string_data = list(string_array_compiler.search(file_data[start_index_array:]))

            item_start_index = file_data.find(ITEM_START_TAG, start_index_array, end_index_array)

            # How many elements in the array
            count = 0
            while item_start_index < end_index_array and item_start_index != -1:
                item_data = list(item_compiler.search(file_data[item_start_index:end_index_array]))
                values_data += ("{},\n".format(item_data[0]))
                item_start_index = file_data.find(ITEM_START_TAG, item_start_index + 1, end_index_array)
                count += 1

            name_data += ("{} - sa({}),".format(string_data[0], count))
        else:
            # Found String
            string_data = list(string_compiler.search(file_data[start_index_string:]))
            name_data += ("{} - s,".format(string_data[0]))
            values_data += ("{},\n".format(string_data[1]))

    name_data, values_data = name_data[:-1], values_data[:-2]

    name_pointer.write(name_data)
    values_pointer.write(values_data)

    name_pointer.close()
    values_pointer.close()
    fo.close()


def build_xml(names_file_name, file_name):
    """

    :param names_file_name: name of the files with the string names
    :param file_name: translated csv file
    :return:
    """

    np = open(names_file_name, "r")

    output_file = open("output.xml", "wb+")

    output_file.write(OPENING_XML_TAG)

    name_list = np.read().split(",")

    translation_list = []

    with open(file_name, "r") as fp:
        for line in fp:
            translation_list.append(line)

    name_index = 0
    file_index = 0
    while file_index < len(translation_list):
        name, name_type = name_list[name_index].split("-")

        name = name.strip()
        name_type = name_type.strip()
        if name_type == "s":
            # Then it's a string
            output_file.write(
                '\n\t' + STRING_FORMAT_TAG.format(name, translation_list[file_index].split(",", 1)[1].strip()))
            file_index += 1
        else:
            # Then it's a string array
            length = int(list(array_name_compiler.parse(name_type))[0])
            items = ""
            for i in range(0, length):
                item = ITEM_FORMAT_TAG.format(translation_list[file_index + i].split(",", 1)[1].strip())
                items += ("\n\t\t" + item)
            output_file.write('\n\t' + STRING_ARRAY_FORMAT_TAG.format(name, items))
            file_index += length
        name_index += 1
    output_file.write(CLOSING_XML_TAG)
    np.close()
    output_file.close()
    print "Resulting strings stored in output.xml"


def main(argv):
    option = ''
    try:
        opts, args = getopt.getopt(argv, "h:o:", ["option="])
    except getopt.GetoptError:
        print 'test.py -o <option[translate or build]>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -o <option[translate or build]>'
            sys.exit()
        elif opt in ("-o", "--option"):
            option = arg
    if option == 'translate':
        fname = str(raw_input("File name(Or absolute path to file if it is not in this directory):\n"))
        execute(fname)
    elif option == 'build':
        name_fname = str(raw_input("File name for csv containing string names(Or absolute path to file):\n"))
        values_fname = str(raw_input("File name for csv containing translation(Or absolute path to file):\n"))
        build_xml(name_fname, values_fname)
    else:
        print "Invalid option: " + option
        print "Option must be either translate or build"


if __name__ == "__main__":
    main(sys.argv[1:])
