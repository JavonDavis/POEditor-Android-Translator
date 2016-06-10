from parse import compile

STRING_FORMAT_TAG = "<string name=\"{}\">{}</string>"
STRING_ARRAY_FORMAT_TAG = "<string-array name=\"{}\">{}</string-array>"
ITEM_FORMAT_TAG = "<item>{}</item"

string_compiler = compile(STRING_FORMAT_TAG)
string_array_compiler = compile(STRING_ARRAY_FORMAT_TAG)
item_compiler = compile(ITEM_FORMAT_TAG)

STRING_OPEN_TAG = "<string"
STRING_CLOSE_TAG = "</string>"

STRING_ARRAY_OPEN_TAG = "<string-array"
STRING_ARRAY_CLOSE_TAG = "</string-array>"

ITEM_START_TAG = "<item>"
ITEM_END_TAG = "</item>"


def execute(file_name):
    fo = open(file_name, "r")
    file_data = fo.read()
    start_index = 0

    element_list = []

    names_file = "names.csv"
    values_file = "values.csv"

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
                values_pointer.write("{},\n".format(item_data[0]))
                item_start_index = file_data.find(ITEM_START_TAG, item_start_index + 1, end_index_array)
                count += 1

            name_pointer.write("{} - sa({}),\n".format(string_data[0], count))
        else:
            # Found String
            string_data = list(string_compiler.search(file_data[start_index_string:]))
            name_pointer.write("{} - s,\n".format(string_data[0]))
            values_pointer.write("{},\n".format(string_data[1]))


if __name__ == "__main__":
    fname = str(raw_input("Enter File name\n"))

    print fname

    execute(fname)


# print "Name of the file: ", fo.name
# print "Closed or not : ", fo.closed
# print "Opening mode : ", fo.mode
# print "Softspace flag : ", fo.softspace
