# DigitalSongShu

The HackMD notes for this project can be found at:

https://hackmd.io/NlDYjUpwROuRR88fIOb5fw?both#

## List of scripts (Jupyter notebooks)
<code>Fagushan_person_authority.ipynb</code>
  - Get list of personal names from the Fagushan authority file (XML) for the dynasties 晉|劉宋|北魏|南梁|南齊|南北朝|南朝
  
<code>CompileNamesFromChineseWebsite.ipynb</code>
  - Compile list of personal names from the Chinese bio website for the same dynasties
  - Combine this list with the list above to create the file <code>BioCombinedSorted.xlsx</code> (note that single-character entries are deleted)

<code>SongShu.tagging.ipynb</code>
  - Tag the SongShu texts from Hanji database using
    - <code>BioCombinedSorted.xlsx</code> from above
    - <code>劉宋地名與官名 2017-11-14.xlsx</code>
