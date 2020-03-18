# lg4id
#G4 kissing

Paste one sequence of interest into the text area below. The algorithm checks for "GGG" and "CCC" sequences in 1500 bp non-sliding windows. LG4s calls are made if greater than 120 "GGG" OR 120 "CCC" sequences are found in 1500 bp. Overlapping positive calls are merged into longer, single calls then returned to the user. You can access the user interface here http://omnisearch.soc.southalabama.edu:8080/g4search.

The 'driver' method in quadsearch_modified.py needs to be called to obtain the desired result. 
