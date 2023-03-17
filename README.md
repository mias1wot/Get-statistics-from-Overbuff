This project contains python selenium code for scraping Overwatch 2 data from [Overbuff](https://www.overbuff.com/heroes). 

The code was originally created in Jupyter. Because of this, "*.py* file isn't formatted well - it had no additional processing after downloading it from Jupyter.

## Current version 2 capabilities:
- Get data for any competitive season as well as for quick play for each hero and ranks along with the standard statistics (common to each hero as well as information belonging to a specific hero).
- Check if hero informaion exists before retrieving it (as new heroes don't have info for previous seasons).
- Data cleansing:
    * Deleted comma separator on thousands (e.g. 1,009 => 1009).
    * Translated time representation (e.g. '01:23') to seconds (1*60 + 23 => 83).
    * Lúcio has become Lucio, Torbjörn - Torbjorn.
- Format for a name of the output file with the table:
    * curDate = datetime.today().strftime("%Y-%m-%d")
    * For quick play:
        * f'ow2\_quickplay\_heroes\_stats\_\_{curDate}.csv'
    * For fninished competitive season:
        * f'ow2\_season\_{OW2\_SEASON with 2 digits}\_FINAL\_heroes\_stats\_\_{curDate}.csv'
    * For continuing competitive season:
        * f'ow2\_season\_{OW2\_SEASON with 2 digits}\_INTERMEDIATE\_heroes\_stats\_\_{curDate}.csv'


## Previous versions


#### Version 2 new capabilities:
- Get data for any competitive season as well as for quick play.
- Check if hero informaion exists before retrieving it (as new heroes don't have info for previous seasons).
- Changed format for a name of the output file with the table:
    * curDate = datetime.today().strftime("%Y-%m-%d")
    * For quick play:
        * f'ow2\_quickplay\_heroes\_stats\_\_{curDate}.csv'
    * For fninished competitive season:
        * f'ow2\_season\_{OW2\_SEASON with 2 digits}\_FINAL\_heroes\_stats\_\_{curDate}.csv'
    * For continuing competitive season:
        * f'ow2\_season\_{OW2\_SEASON with 2 digits}\_INTERMEDIATE\_heroes\_stats\_\_{curDate}.csv'

<hr>


#### Version 1 capabilities:
- Get season 3 competitive data for each hero and ranks along with the standard statistics (common to each hero as well as information belonging to a specific hero).
- Data cleansing:
    * Deleted comma separator on thousands (e.g. 1,009 => 1009).
    * Translated time representation (e.g. '01:23') to seconds (1*60 + 23 => 83).
    * Lúcio has become Lucio, Torbjörn - Torbjorn.
- Format for a name of the output file with the table: f'ow\_heroes\_data\_season3\_{datetime.today().strftime("%Y-%m-%d")}.csv'