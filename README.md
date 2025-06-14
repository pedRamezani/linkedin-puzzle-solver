# LinkedIn Puzzle Solver
Scrapes puzzle information for the LinkedIn games Queens, Tango and Zip using bookmarklets, and then solves them using the constraint optimiser [OR Tools](https://developers.google.com/optimization) in Python.

## Scraper
For now, I haven't bothered writing a scraper with login capabilities, so you need to run the bookmarklets with a logged-in user to download the data as a `.json` file.

Instructions:
1. Copy the raw source code one of these depending on the puzzle data you want to download
    + `queens.js`
    + `tango.js`
    + `zip.js`
1. Visit [Make Bookmarklets](https://make-bookmarklets.com/) and paste the code nto the text box.
1. Click on "Create Bookmarklet" and drag the generated bookmarklet to your bookmarks bar
1. Visit the corresponding LinkedIn puzzle page
1. Click on the bookmarklet
1. ???
1. Profit!

## Solver
Instructions:
1. Install Python 3.8 or above
1. Install OR Tools with `python -m pip install ortools` in a new environment
1. Extract puzzle data as `.json` with the scraper
1. Run one of these depending on the puzzle data downloaded
    + `python queens_solve.py`
    + `python tango_solve.py`
    + `python zip_solve.py`

> [!NOTE]
> If you have renamed the JSON file or saved it in a different directory to the script, you must specify the file path as the first argument in the script.

## Output Examples

Queens (ANSI colored regions in terminal)

```txt
🧩 Puzzle Solved:

 x  x  x  ♛  x  x  x  x  x 
 x  x  x  x  x  ♛  x  x  x 
 x  x  ♛  x  x  x  x  x  x 
 x  x  x  x  x  x  x  x  ♛ 
 x  x  x  x  ♛  x  x  x  x 
 x  x  x  x  x  x  x  ♛  x 
 x  ♛  x  x  x  x  x  x  x 
 x  x  x  x  x  x  ♛  x  x 
 ♛  x  x  x  x  x  x  x  x
```

Tango

```txt
🧩 Puzzle Solved:

🟠🌙🟠🟠🌙🌙
🌙🟠🌙🌙🟠🟠
🟠🟠🌙🟠🌙🌙
🟠🌙🟠🌙🌙🟠
🌙🌙🟠🌙🟠🟠
🌙🟠🌙🟠🟠🌙
```

Zip

```txt
🧩 Puzzle Solved:

 ┌─────┐  ┌────────┐ 
 │  o  │  └─────┐  │ 
 │  │  └─────┐  │  │ 
 │  │  ┌─────┘  │  │ 
 │  │  └─────┐  │  │ 
 │  └─────┐  │  x  │ 
 └────────┘  └─────┘
```