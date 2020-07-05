```
  Author: Sujayyendhiren Ramarao Srinivasamurthi
  Description: Exteremely simple home network discovery, storage of info and easy lookup
```


### Description
Home network is discovered here with fping and then data is gathered in an on disk
simplekv storage for easy lookup by other scripts/programs.

### Pre-requisites
Ubuntu> sudo apt-get install fping
python3.x -m pip install -r requirements.txt


## Recommendation (optional) - Sample cron schedule to keep the home inventory uptodate
0 * * * *  cd <path to repository> && python3.8 pyfping.py
