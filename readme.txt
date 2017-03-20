1. Name
Game Fragment Extractor

2. Description
A script and exe file that will extract a game fragment based on
a full chess game records or pgn file and a user specified marker
comment in the main line of the game. The script is created from
an idea of John Smith who searches a tool to output such records.

Example,
1.d4 Nf6 2.Bg5 d5 3.e3 c5 4.Bxf6 gxf6 {[#]} 5.dxc5 ( 5.Nc3 Nc6 6.Qh5 )...
The comment [#] is the marker that would tell the extractor where to
start extracting the game. See included sample.pgn file.

The python script is written under version 2.7.11 and was tested
on python-chess version 0.17.0. For more information see the
beginning part of source file gfe.py.

3. External files required
pgn-extract.exe
This file can be found at:
https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/

4. Usage
gfe.exe -i <your input pgn file> -o <your output pgn file>

or

gfe.exe --input <your input pgn file> --output <your output pgn file>
