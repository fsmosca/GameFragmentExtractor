"""
A. Program name
Game Fragment Extractor


B. Program description
Creates a new game record based on PGN file (containing full game
records) and a specified marker in the main line of the game.


C. License notice

This program is free software, you can redistribute it and/or modify
it under the terms of the GPLv3 License as published by the
Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License (LICENSE)
along with this program, if not visit https://www.gnu.org/licenses/gpl.html


D. Application references and dependencies

1. Developed under python 2.7.11
   https://www.python.org/download/releases/2.7/
2. Using python-chess library version 0.17.0
   https://pypi.python.org/pypi/python-chess
3. pgn-extract
   https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/
4. py2exe
   https://pypi.python.org/pypi/py2exe/
   

E. Tests
1. The script is tested under Windows 7


F. Release notes

1. Release date: 2017-03-25
2. Version no.:  1.1
3. Files: 
   a. gfe.py
   b. gfe.exe
   c. run_gfe.bat
   d. sample.pgn
   e. LICENSE

"""

import os
import sys
import getopt
import subprocess
import chess
from chess import pgn


APP_NAME = 'Game Fragment Extractor'
APP_VER = '1.1'


def write_node(fen, game_pos, game, pgn_out_fn):
    """ Writes main line and variations """

    # Set fmvn to 1 for pgn-extract since game fragment
    # starting move nb will be renumbered to 1
    new_fen = ' '.join(fen.split()[0:4]) + ' 0 1'

    # Print all headers of the original game
    for k, v in game.headers.items():
        if k == 'SetUp' or k == 'FEN':
            continue
        with open(pgn_out_fn, 'a') as f:
            f.write('[%s \"%s\"]\n' %(k, v))
            
    # Print the revised FEN
    with open(pgn_out_fn, 'a') as f:
        f.write('[SetUp "1"]\n')
        f.write('[FEN \"%s\"]\n\n' %(new_fen)) 

    # (1) Process main line
    game_node = game_pos
    while game_node.variations:
        next_node = game_node.variation(0)   
        mv = next_node.move
        com = next_node.comment

        with open(pgn_out_fn, 'a') as f:
            if com != '' and com != '[#]':
                f.write('%s {%s} ' %(str(mv), com))
            else:
                f.write('%s ' %(str(mv)))

        # (2) Process 1st level variations, these are variations of main line
        for var1 in range(1, 100):
            try:    
                var_node1 = game_node.variation(var1)
                if var_node1.starts_variation():

                    # Print also the starting comment of a variation if there is
                    scom1 = var_node1.starting_comment

                    with open(pgn_out_fn, 'a') as f:
                        if scom1 != '':
                            f.write('({%s}' %(scom1))
                        else:
                            f.write('(')

                        f.write('%s ' %(str(var_node1.move)))
                    
                    # If this is the only move in this var then print its comment
                    # now because we will not be visiting this node again
                    if not var_node1.variations:
                        com1 = var_node1.comment
                        if com1 != '':
                            with open(pgn_out_fn, 'a') as f:
                                f.write('{%s}' %(com1))
                            
                    while var_node1.variations:
                        next_node1 = var_node1.variation(0)
                        mv1 = next_node1.move

                        # Print also the starting comment of a variation if there is
                        com1 = next_node1.comment
                        with open(pgn_out_fn, 'a') as f:                            
                            if com1 != '':
                                f.write('%s {%s}' %(str(mv1), com1))
                            else:
                                f.write('%s ' %(str(mv1)))

                        # (3) Process 2nd level variations, these are sub-variations of 1st level variations
                        for var2 in range(1, 100):
                            try:
                                var_node2 = var_node1.variation(var2)
                                if var_node2.starts_variation():

                                    # Print also the starting comment of a variation if there is
                                    scom2 = var_node2.starting_comment
                                    with open(pgn_out_fn, 'a') as f:
                                        if scom2 != '':
                                            f.write('({%s}' %(scom2))
                                        else:
                                            f.write('(')
                                        
                                        f.write('%s ' %(str(var_node2.move)))
                                    
                                    # If this is the only move in this var then print its comment
                                    # now because we will not be visiting this node again
                                    if not var_node2.variations:
                                        com2 = var_node2.comment
                                        if com2 != '':
                                            with open(pgn_out_fn, 'a') as f:
                                                f.write('{%s}' %(com2))
                            
                                    while var_node2.variations:
                                        next_node2 = var_node2.variation(0)
                                        mv2 = next_node2.move

                                        # Print also the starting comment of a variation if there is
                                        com2 = next_node2.comment
                                        with open(pgn_out_fn, 'a') as f:
                                            if com2 != '':
                                                f.write('%s {%s}' %(str(mv2), com2))
                                            else:
                                                f.write('%s ' %(str(mv2)))

                                        # (4) Process 3rd level variations, these are sub-variations of 2nd level variations
                                        for var3 in range(1, 100):
                                            try:
                                                var_node3 = var_node2.variation(var3)
                                                if var_node3.starts_variation():

                                                    # Print also the starting comment of a variation if there is
                                                    scom3 = var_node3.starting_comment
                                                    with open(pgn_out_fn, 'a') as f:
                                                        if scom3 != '':
                                                            f.write('({%s}' %(scom3))
                                                        else:
                                                            f.write('(')
                                                            
                                                        f.write('%s ' %(str(var_node3.move)))
                                                    
                                                   # If this is the only move in this var then print its comment
                                                   # now because we will not be visiting this node again
                                                    if not var_node3.variations:
                                                        com3 = var_node3.comment
                                                        if com3 != '':
                                                            with open(pgn_out_fn, 'a') as f:
                                                                f.write('{%s}' %(com3))
                            
                                                    while var_node3.variations:
                                                        next_node3 = var_node3.variation(0)
                                                        mv3 = next_node3.move
                                                        com3 = next_node3.comment
                                                        with open(pgn_out_fn, 'a') as f:
                                                            if com3 != '':
                                                                f.write('%s {%s}' %(str(mv3), com3))
                                                            else:
                                                                f.write('%s ' %(str(mv3)))

                                                            var_node3 = next_node3

                                                    with open(pgn_out_fn, 'a') as f:
                                                        f.write(') ')
                                            except:
                                                pass
                                            
                                        var_node2 = next_node2

                                    with open(pgn_out_fn, 'a') as f:
                                        f.write(') ')
                            except:
                                pass
                            
                        var_node1 = next_node1

                    with open(pgn_out_fn, 'a') as f:
                        f.write(') ')
            except:
                pass

        game_node = next_node

    with open(pgn_out_fn, 'a') as f:
        f.write(' %s\n\n' %(game.headers['Result']))


def delete_file(fn):
    """ Delete fn file """
    if os.path.isfile(fn):
        os.remove(fn)


def usage():
    print('Usage:')
    print('program_name -i <input pgn file> -o <output pgn file>')
    print('program_name --input <input pgn file> --output <output pgn file>\n')

        
def main(argv):
   
   print('%s v%s\n' %(APP_NAME, APP_VER))
    
    pgn_in_fn = None
    pgn_out_fn = None
    temp_pgn_fn = None
    pgn_extract_fn = 'pgn-extract.exe'

    # Read command line options
    try:
        opts, args = getopt.getopt(argv, "i:o:", ["input=", "output="])
    except getopt.GetoptError as err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--input"):
            pgn_in_fn = arg
        elif opt in ("-o", "--output"):
            pgn_out_fn = arg

    # Check presence of input pgn file
    if not os.path.isfile(pgn_in_fn):
        print('Error, the file %s is missing!!\n' %(pgn_in_fn))
        return

    # Check if input pgn filename is the same to that of output pgn filename
    if pgn_in_fn == pgn_out_fn:
        print('Error, input %s and output %s is the same!!\n' %(pgn_in_fn, pgn_out_fn))
        return

    # Exit if output file is the same as the script filename
    if pgn_out_fn == os.path.basename(sys.argv[0]):
        print('Error, program name is the same as output filename!!')
        return

    # Check presence of pgn-extract
    if not os.path.isfile(pgn_extract_fn):
        print('Error, %s is missing!!\n' %(pgn_extract_fn))
        return

    temp_pgn_fn = 'temp_out_' + pgn_in_fn

    # Delete existing output file
    delete_file(pgn_out_fn)

    # Read the input pgn file
    pgnh = open(pgn_in_fn, 'r')
    game = chess.pgn.read_game(pgnh)
    
    while game:
        game_node = game
        while game_node.variations:
            fen = game_node.board().fen()            
            next_node = game_node.variation(0)
            com = game_node.comment

            # Write game fragment when this kind of comment is encountered in the main line
            if com == '[#]':
                write_node(fen, game_node, game, temp_pgn_fn)
            game_node = next_node
        game = chess.pgn.read_game(pgnh)
    pgnh.close()

    # Run pgn-extract
    if os.path.isfile(temp_pgn_fn):
        cmdLine = 'pgn-extract -s -o' + pgn_out_fn + ' ' + temp_pgn_fn
        p = subprocess.Popen(cmdLine, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.communicate()
    else:
        print('Warning temp pgn file is not created by the tool!!')

    # Delete temp file
    delete_file(temp_pgn_fn)


if __name__ == "__main__":
    main(sys.argv[1:])
