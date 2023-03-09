This project contains python selenium code for scraping Overwatch 2 data from https://www.overbuff.com/heroes. 

The code was originally created in Jupyter. Because of this, "*.py* file isn't formatted well - it had no additional processing after downloading it from Jupyter.


Current version 1 capabilities:
- Get season 3 competitive data for each hero and ranks along with the standard statistics (common to each hero as well as information belonging to a specific hero).
- Data cleansing:
  1) Deleted comma separator on thousands (e.g. 1,009 => 1009).
  2) Translated time representation (e.g. '01:23') to seconds (1*60 + 23 => 83).
  3) Lúcio has become Lucio, Torbjörn - Torbjorn.