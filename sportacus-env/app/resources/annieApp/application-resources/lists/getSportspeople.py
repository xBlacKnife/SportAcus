import pandas as pd

with open('sports.txt', 'r') as readFile:
    sportLst = readFile.read()
    
sportLst = sportLst.split()

data = pd.read_csv("athlete_events.csv")

for sportName in sportLst:
    dataCleaned = data[["Name", "Sport", "Event"]]
    dataCleaned = dataCleaned.drop_duplicates()


    sport = dataCleaned[dataCleaned.Sport == sportName]

    sportEvents = sport['Event'].drop_duplicates().tolist()

    peopleNames = sport["Name"].drop_duplicates()

    sportName = sportName.lower().strip()
    
    with open(sportName + 'events.lst', 'w') as writeFile:
        for e in sportEvents:
            writeFile.write(e)
            writeFile.write('\n')
            
    with open(sportName + 'people.lst', 'w') as writeFile:
        for e in peopleNames:
            writeFile.write(e)
            writeFile.write('\n')
            for wrd in e.split()[1:]:
                writeFile.write(wrd)
                writeFile.write('\n')