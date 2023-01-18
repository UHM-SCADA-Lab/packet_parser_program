# I wanted a standardized way to print data but I also wanted any scripts built 
# on top of this library to be able to use the same formatting, thus I 
# created this class with some prebuilt methods that can be used to print data 
# to console in a table format, with any functionality I thought could be useful
# 
# example usage:
# from functions import print_functions
# pf = print_functions.print_functions()
# pf.print_bar()

from PPP.functions import wrap_line
# see /functions/wrap_line.py for more information on what it does (but it 
# basically just takes a long string and breaks it (at space characters) into 
# shorter strings)



class print_functions():
    def __init__(self,console=True, file_path=None,bar_length=150):
        # defaults to printing to console (console=True)
        # defualts to not printing to a file (file_path=None)
        # Note: you can print to both
        # bar_length defaults to 150 - it is the (max) number of characters
        # wide everything prints
        self.console = console
        self.file_path = file_path
        self.bar_length = bar_length

    # prints each line to either the console, a file, or both
    def optional_print(self,line):
        # file option not tested yet, TODO: test this
        if self.file_path != None:
            # 'with' statement closes file after we are finished with it
            with open(self.file_path, 'a') as packet_info_file:
                packet_info_file.write(line+'\n')

        # prints to console
        if self.console == True:
            print(line)


    # ex: '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
    def print_bar(self):
        bar = self.bar_length*'%'
        self.optional_print(bar)

    # ex: '--------------+-------------------+---------------------------------'
    def print_data_bar(self,column_widths):
        # column_widths should be a list of 2 integers, corresponding with the 
        # widths of the first two columns. The third column's width will be 
        # calculated using the bar_length variable passed when calling the class
        # ex = [10,20]
        #
        # third_column_width is how many characters wide the third column is
        # the int 7 represents the spaces and '|' characters used in the 
        # print_data() function - it is one less character for presentation
        third_column_width = self.bar_length - 7 - sum(column_widths)

        # the extra '-' characters (why it is '--+-' instead of '+') are to 
        # account for the forced white space in the print_data() function
        data_bar = column_widths[0]*'-' + '--+-' + \
            column_widths[1]*'-' + '-+-' + third_column_width*'-'
        self.optional_print(data_bar)
            


    # '              VLAN ID | 3                 | SDN Production'
    # '                      |--> VLAN ID: . . 3 | SDN Production'
    # (function combines first 2 columns in event of a passed arrow length)
    def print_data(self, column_widths, entries, arrow_length = 0, just = '<', lead_zero_strip = True, line_case = '.'):
        # column_widths should be a list of 2 integers, corresponding with the 
        # widths of the first two columns. The third column's width will be 
        # calculated using the bar_length variable passed when calling the class
        # ex = [10,20]
        #
        # entries should be a list of 3 strings, corresponding with the entires 
        # of columns 1, 2, and 3. 
        # ex = ['VLAN ID','3','SDN Production']
        #
        # arrow_length creates an arrow in the second column and moves the 
        # string in entries[0] to be combined with entries[1] (this is done 
        # because it looks better imo, (especially with multiple rows))
        # ex if arrow_length = 0
        # '              VLAN ID | 3                 | SDN Production'
        # ex if arrow_length = 3
        # '                      |--> VLAN ID: . . 3 | SDN Production'
        #
        # just is the justification of the second column
        # ex if just = '<' then: 
        # '        Type | MAC Address       | Vendor ID ' 
        # ex if just = '^' then:
        # '        Type |    MAC Address    | Vendor ID '
        #
        # lead_zero_strip, if true, strips the lead zeroes of the second item 
        # of the list entries (entries[1])
        # ex: if entries[1] = 008243, then it will print 8243
        # 
        # line_case is used to create an "eye guide"
        # see the 'match' statement below for more info

        
        if type(entries[1]) == bytes:
            # convert the bytes to a ascii representation, then make all 
            # letters uppercase
            entries[1] = entries[1].hex().upper()

            if lead_zero_strip == True:
                # strip the leading zeros
                entries[1] = entries[1].lstrip('0')
            
            if entries[1] == '':
                entries[1] = '0'


        # at the ends of this function, it calls a custom print function and 
        # passes this string formatted. 
        data_format = ' {first_entry:>{first_column_width}} |{arrow}' + \
            ' {second_entry:{just}{second_column_width}} | {third_entry} '

        # third_column_width is how many characters wide the third column is
        # the int 8 represents the spaces and '|' characters used in the 
        # data_format string
        third_column_width = self.bar_length - 8 - sum(column_widths)

        second_column_width = column_widths[1]

        # if arrow length is passed, creates the arrow and combines entries 1 
        # and 2 into the second column. 
        # (this is done bc I think it looks better)
        if arrow_length == 0:
            arrow = ''

        elif arrow_length > 0:
            # ex: '----->'
            arrow = (arrow_length-1)*'-' + '>'
            
            # arrow length is subtracted from column_widths for (imo) easier 
            # use for the programmer - it keeps the second column the same 
            # total width with or without the arrow
            second_column_width -= arrow_length

            # this is kinda confusing,
            # I wanted to combine the first two columns in the event that an 
            # arrow length is passed as imo, instead of printing:
            # '              VLAN ID |--> 03              | SDN Production'
            # it looks better to print: 
            # '                      |--> VLAN ID:_____03 | SDN Production'
            #
            # so... first we calculate the size of the gap (represented by the 
            # underscores in the VLAN ID comment example three lines up)

            gap_size = second_column_width - len(entries[0] + entries[1]) - 1
            
            # then create the string of width gap_size to be inserted
            match line_case:
                case None:
                    # No gap
                    gap = ' '
                case '.':
                    # alternating spacesa and periods
                    # ex: ' . . . . . . .'
                    gap_size_mult = gap_size // 2
                    if gap_size % 2 == 1:
                        gap = ' '
                    else:
                        gap = '  '
                        gap_size_mult -= 1
                    gap += '. '*gap_size_mult
                case '_':
                    # solid underscores
                    gap = '_' * gap_size
                case ' ':
                    # solid spaces
                    gap = ' ' * gap_size

            # and combine the two columns
            entries[1] = entries[0]+':'+gap+entries[1]
            entries[0] = ''

        # When printing some descriptions that were requested from external csv 
        # files, some descriptions wouldn't fit in the space provided, and 
        # would make the printed information very ugly
        # 
        # so I created wrap_line.py, which will split a string into a list of 
        # strings of a max provided length, but this is the logic that calls
        # that external function
        #
        # if the data of the third column fits in the width provided, then 
        # print on one line
        #
        # ex:
        # '              VLAN ID | 3                 | SDN Production'
        if len(entries[2]) < third_column_width:
            self.optional_print(data_format.format(
                first_entry = entries[0],
                first_column_width = column_widths[0], 
                arrow = arrow,
                second_entry = entries[1],
                just = just,
                second_column_width = second_column_width,
                third_entry = entries[2]
            ))

        # if it doesn't, then call the function wrap_line I created, which 
        # splits up a string at space characters into smaller strings 
        # see /functions/wrap_line.py for more info
        else:  
            # wrap_line() populates this list that is passed
            print_list = list()
            wrap_line.wrap_line(print_list,entries[2],third_column_width)

            # first, print the data that was passed to the start of this 
            # print_data() function and the first string returned from the 
            # wrap_line() function
            #
            # ex:
            # '                |--> VLAN ID: 3     | (pretend this is longer)'
            self.optional_print(data_format.format(
                first_entry = entries[0],
                first_column_width = column_widths[0], 
                arrow = arrow,
                second_entry = entries[1],
                just = just,
                second_column_width = second_column_width,
                third_entry = print_list[0]
            ))


            # then, print the extra strings in the third column, but nothing in 
            # the first two columns
            #
            # ex
            # '                |                   | wrapped around text!'
            # '                |                   | another line wrapped !!!'
            for string in print_list[1:]:
                self.optional_print(data_format.format(
                    first_entry = '',
                    first_column_width = column_widths[0], 
                    arrow = '',
                    second_entry = '',
                    just = '',
                    second_column_width = column_widths[1],
                    third_entry = string
                ))



