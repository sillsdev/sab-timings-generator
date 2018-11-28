#Name: Menu
#Author: Joy Penner
#Date: 12 October 2018

#Purpose: Provide a menu for clt_to_txt_python.
#Requires: 
#How to use: Runs automatically when running clt_to_txt_python
#Produces: Results of type {verse: bool, book: int, chapter: int}

#!/usr/bin/env python

import os, sys


def menu():

    print('TIMINGS GENERATOR')
    print('='*17)

    print('Before running have you: ')
    print('1. Added cue files to the folder cue_files')
    print('2. Added the Core script to the folder core_script')
    
    while True:
        try:
            check = ({'done': True, 'not done': None}
                    [input('Done / Not Done: ').lower()]
                    ) and os.listdir('cue_files') \
                    and os.listdir('core_script')
            if check:
                break
            else:
                print('Please add the correct files before continuing')
                continue
        except KeyError:
            print('Invalid input')
            continue

    while True:
        try:
            verse = ({'1': True, '2': False}
                    [input(
                        'Create Timings at a [1] Verse or [2] Phrase level: '
                        ).lower()]
                    )
            break
        except KeyError:
            print('Invalid input')
            continue
    
    name = list_name(os.listdir('cue_files')[0])

    print('')
    print('\t'.join(str(i) for i in range(0, len(name))))
    print('\t'.join(str(n) for n in name))

    print('Using the above as reference please give the indices for:')
    #Get indices of book name and chapter number
    while True:
        try:
            book = int(input('Book name: '))
            if book not in range(0, len(name)):
                print(
                    'ERROR: Invalid input. Please try a number between 0 and {}'
                    .format(len(name)-1)
                    )
                continue
            else:
                break
        except ValueError:
            print(
                'ERROR: Invalid input. Please try a number between 0 and {}'
                .format(len(name)-1)
                )

    while True:
        try:
            chapter = int(input('Chapter number: '))
            if chapter not in range(0, len(name)):
                print(
                    'ERROR: Invalid input. Please try a number between 0 and {}'
                    .format(len(name)-1)
                    )
                continue
            else:
                break
        except ValueError:
            print(
                'ERROR: Invalid input. Please try a number between 0 and {}'
                .format(len(name)-1)
                )
    
    return {
        'verse': verse,
        'book': book,
        'chapter': chapter
    }

#Convert file name into a list
def list_name(name):

    return list(filter(
                        None, 
                        name
                            .split('.')[0] #Remove file type
                            .replace('-', '_')  #Convert - to _
                            .replace(' ', '_')  #Convert spaces to _
                            .split('_') #Split title on _
                        ))  #Remove all empty strings
						
