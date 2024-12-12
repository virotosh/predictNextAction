# Combined Frequency and Recency
import time
import datetime
import math

class CFR_ItemVisit(object):
    def __init__(self, item_id, second, visitNumber):
        self.id = item_id
        self.second = second
        self.visitNumber = visitNumber
        
class CFR_ItemState(object):
    def __init__(self, item_id):
        self.item_id = item_id
        self.nextVisits = []
        self.crfWeight = 0.0
        
    def updateVisits(self, visitTime, visitNumber):
        curr_visitNumber = visitNumber
        crfWeight = 0.0
        for idx in range(len(self.nextVisits)):
            prev_visitNumber = self.nextVisits[idx].visitNumber
            crfWeight +=(math.pow(2.0, -0.1 * (curr_visitNumber - prev_visitNumber)))
        self.crfWeight = crfWeight
        
    def addVisitToItem(self, visitTime, visitNumber):
        x = time.strptime(visitTime,'%H:%M:%S')
        second = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
        _itemVisit = CFR_ItemVisit(self.item_id, second, visitNumber)
        self.nextVisits.append(_itemVisit)
        
class ItemFactory(object):
    def __init__(self):
        self.items = {}
        self.numberOfVisits = 0
        
    def update(self, item_id, visitTime):
        self.numberOfVisits +=1
        if item_id not in self.items:
            self.items[item_id] = CFR_ItemState(item_id)
        self.items[item_id].addVisitToItem(visitTime, self.numberOfVisits)
        for it in self.items:
            self.items[it].updateVisits(visitTime, self.numberOfVisits)