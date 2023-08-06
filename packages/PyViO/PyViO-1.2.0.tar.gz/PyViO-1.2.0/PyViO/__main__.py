"""
View outliers in data.

****Methods:****
- Hample Method
- Z-Score Method
- IQR Method

****For reading more on these topics:****
- Enter 1 - Interquartile range
- Enter 2 - Standard score
- Enter 3 - Median filter

Since this library produces graphical output which can be best enjoyed in a notebook, we request you to run it in a notebook.

The reading articles have been referenced from Wikipedia.

****Contact:****
team.pyvio@gmail.com
"""

import sys
import wikipedia

def main() -> None:
    input_arg = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    input_option = [opt for opt in sys.argv[1:] if opt.startswith("-")]

    # Show help message
    if "-h" in input_option or "-help" in input_option:
        print(__doc__)
        raise SystemExit()

    if input_arg:
        for id in input_arg:
            art = show_wiki_art(id)
            print(art)   
    else:
        print("Not a valid input. Please refer to the -help section to learn more.")

def show_wiki_art(id):
    art_list = ["Interquartile range","Standard score","Median filter"]
    id = int(id)
    if ((id > 0) and (id <= len(art_list))):
        return(art_list[id-1]," ::::::::::: ",wikipedia.summary(art_list[id-1], sentences = 4))
    else:
        return("Not a valid input. Please choose 1 or 2 or 3.")

if __name__ == "__main__":
    main()
