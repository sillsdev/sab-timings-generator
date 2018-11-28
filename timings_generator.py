#Name: Timings Generator
#Author: Joy Penner
#Date: 5 October 2018

#Purpose: Generate timing files from a core script and cue files.
#Requires: pandas, xlrd
#How to use: From command line run .\clt_to_txt_python.py
#Produces: Timing files split at the phrase or verse level,
#depending on user input.

#!/usr/bin/env python3

import os
import sys
import pandas as pd
import math
from menu import menu, list_name
from progress_bar import printProgressBar

#Run menu and converter
def main():
    response = menu()

    # response = {
    #     'verse': True,
    #     'book': 1,
    #     'chapter': 2
    # }

    converter(response)

#Check if core script is present and run
def converter(res):
    
    path_core = 'core_script'
    
    try:
        #Check for core
        core = os.listdir(path_core)[0]
        #Get phrase markers from core script
        phrase_markers = retrieve_phrase_markers(
                                                os.path.join(path_core,
                                                core)
                                                )

        #Run converter
        clt_to_txt(phrase_markers, res)

        print('\nDone! Check the timings folder for your files')
    except IndexError:
        print('ERROR: Please check core script is in core_script')

def clt_to_txt(phrase_markers, res):

    path_cue = 'cue_files'
    path_timings = 'timings'
    files = os.listdir(path_cue)

    #Run for every cue file in cue_files
    for filename in files:

        printProgressBar(files.index(filename), len(files)-1, prefix='Converting: {}'.format(filename), suffix='Completed')

        #Extract book title and chapter from filename
        name, origname = get_titles(filename, res)

        with open(os.path.join(path_cue, filename)) as fi:

            #Get the time stamps from the cue files
            results = extract_numbers(fi)

            #Create a new timing file
            timing_file = open(os.path.join(path_timings, name + '.txt'), 'w')

            for num in results:
                
                if len(phrase_markers[origname]) > 0:
                    count = phrase_markers[origname].pop(0)
                else:
                    count = ''
                
                #If split at phrase level add all time stamps
                #If split at verse level only add verse time stamps
                if count and res['verse']:
                    timing_file.write('{}\t{}\t{}\n'.format(num, num, count))
                elif not res['verse']:
                    timing_file.write('{}\t{}\t{}\n'.format(num, num, count))

            timing_file.close()

#Extract book and chapter from filename
def get_titles(filename, res):
    
    #Convert filename into list
    brkdwn = list_name(filename)

    book = brkdwn[res['book']]
    origbook = book
    # FCBH and SAB use different names for Titus and James
    if book == "TTS":
        book = "TIT"
    if book == "JMS":
        book = "JAS"

    chapter = brkdwn[res['chapter']]
    name = book + '_' + chapter
    origname = origbook + '_' + chapter

    return name, origname

#Extract time stamps from cue file and add to list
#Cue file format:
# Prefix=
# 44100                 <--- Divisor for time stamps
# 0                     <--- Beginning time stamp
# 343826                <--- Duration of clip
# N2_NOD_WBT_0001.wav   <--- Name of wave file (Sound effects begin with F)
#Result is list of time stamps
def extract_numbers(fi):

    nums = []
    set_div = False
    div = 0

    for line in fi:

        if set_div:                 #Get time divisor
            div = line
            set_div = False

        elif line == 'Prefix=\n':   #Indicates next line is time divisor
            set_div = True

        elif is_number(line):       #Grab time stamp or duration, divide by divisor
            nums.append(float(line) / float(div))

        elif line.startswith("F"):  #Remove timings for sound effects
            nums.pop()
            nums.pop()

    #For each time stamp and duration, add to produce result
    results = [round(nums[i] + nums[i-1], 6) for i in range (1, len(nums), 2)]

    return results

#Check if string is number or not
def is_number(s):

    try:
        float(s)
        return True
    except ValueError:
        return False

#Retreives phrase level breakdown from core script
#Result is dict books = { BOOK: [PHRASE MARKERS]}
def retrieve_phrase_markers(path):
    print('Retreiving phrase markers from: ' + path)

    with pd.ExcelFile(path) as xlsx:
        #Use columns for Book Title, Chapter, Verse, and Recording Index
        df = pd.read_excel(xlsx, usecols=[1,2,3,8], skiprows=56, header = None)
    
        books = {}
        last = 0

        for index, row in df.iterrows():
            printProgressBar(index, len(df)-1, prefix='Processing:', suffix='Completed')

            #If the row is not a repeat or the beginning of a book
            if not str(row[3]).endswith('r') and row[2] != '<<':
                #Title becomes BOOK_## where ## is the chapter #
                title = "{}_{}".format(row[0], str(row[1]).zfill(2))

                #Add chapter # to BOOK
                if title not in books:
                    books[title] = []
                if row[2] == last: #Check if verse is divided into phrases
                    books[title].append('')
                else:
                    books[title].append(row[2])
                
                #Track verse number last used
                last = row[2]

    return books

if __name__ == "__main__":
    main()

