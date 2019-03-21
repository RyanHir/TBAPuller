from datetime import datetime
import tbapy
import csv

tba         = tbapy.TBA('d5G1n2z376zOHMgjlQkAHSunMUiupMwDzudrQnHo8FtY0VnN7waRApeJwun1gdgr')
events      = tba.events(tba.status()["current_season"], True, True)
date        = datetime.today()

def getEventMatches(e):
    global header, tba
    allMatches = tba.event_matches(e, True, True)
    collectiveGathered = []
    for m in allMatches:
        match = tba.match(m)
        for x in match["alliances"]:
            match["alliances"][x].pop("dq_team_keys")
            match["alliances"][x].pop("surrogate_team_keys")
        alliances = match["alliances"].copy()
        for x in alliances:
            for y in alliances[x]["team_keys"]:
                a = x+"."+str(match["alliances"][x]["team_keys"].index(y))
                match["alliances"][x][a] = y
            z = match["alliances"][x].copy()
            for y in z:
                a = x+"."+str(y)
                b = z[y]
                match[a] = b
        match.pop("blue.team_keys")
        match.pop("red.team_keys")
        match.pop("alliances")
        match.pop("actual_time")
        match.pop("post_result_time")
        match.pop("predicted_time")
        match.pop("time")
        match.pop("videos")
        try:
            scoreBreakdown = match["score_breakdown"].copy()
        except:
            break
        for x in alliances:
            for y in scoreBreakdown[x]:
                a = x+"."+str(y)
                b = scoreBreakdown[x][y]
                match[a] = b
        match.pop("score_breakdown")
        collectiveGathered.append(match)
    return collectiveGathered
def main():
    approvedOne = []
    approvedTwo = []

    print ("Pre Processing")
    for x in events:
        allMatches = tba.event_matches(x, True, True)
        if len(allMatches) > 0:
            approvedOne.append(x)
    for x in approvedOne:
        y = tba.event(x)['end_date'].split('-')
        if(int(y[1]) > date.month):
            continue
        elif((int(y[2]) >= date.day) and (int(y[1]) == date.month)):
            continue
        else:
            approvedTwo.append(x)

    print ("Going to Process "+str(len(approvedTwo))+" Event(s)")
    finalGathered = []
    for x in approvedTwo:
        print ("Pulling "+x)
        for y in getEventMatches(x):
            finalGathered.append(y)
    print ("Finished, Now Writing")
    with open("pull.csv", 'w') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, finalGathered[0])
        w.writeheader()
        for x in finalGathered:
            w.writerow(x)
main()
