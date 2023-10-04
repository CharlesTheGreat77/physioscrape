# Physioscrape
Utility for scraping research datasets on physionet.org fast and efficiently

```
      _---~~(~~-_.
    _{        )   )
  ,   ) -~~- ( ,-' )_
 (  `-,_..`., )-- '_,)
( ` _)  (  -~( -_ `,  }
(_-  _  ~_-~~~~`,  ,' )
  `~ -^(    __;-,((()))
        ~~~~ {_ -_(())
               `\  }
                 { }
```

# Prerequisites
```
python3
```

# requirements
```
# optional
python3 -m venv venv
source venv/bin/activate
# required
pip3 install -r requirements.txt
```

# usage
```
usage: scraper.py [-h] -s SEARCH

Query Physionet for datasets to analyze

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH, --search SEARCH
                        search by study name, general search, etc
```

# example
```
python3 scraper.py -s eeg
```
- searches physionet.org for results with eeg

# key note
Still in progress.. if search has 0 results, an error will appear.
- Will work on error handling

# physionet
https://physionet.org

