# Markov
import time
import datetime
import math

class ItemVisit(object):
    def __init__(self, _id, _hour, _weekday):
        self.id = _id
        self.hour = _hour
        self.weekday = _weekday
        
class ItemState(object):
    def __init__(self):
        self.nextVisits = {}
        self.visitNumber = 0
        self.numberOfVisits = 0
        self.timeOfLastVisit = 0
        self.crfWeight = 0.0
        self.rank = 9223372036854775807
    
    # ts = timestamp as string
    def addVisitToItem(self, _id, _maxVisits, _ts):
        _dt = datetime.datetime.fromtimestamp(float(_ts))
        _hour = _dt.hour
        _weekday = _dt.weekday()
        _item = ItemVisit(_id, _hour, _weekday)
        if _id not in self.nextVisits:
            self.nextVisits[_id] = []
        self.nextVisits[_id].append(_item)
    
    def removeVisitsToItem(self, _id):
        _tmp = dict(self.nextVisits)
        del _tmp[_id]
        self.nextVisits = _tmp
        
    def updateVisits(self, _visitNumber):
        self.numberOfVisits +=1
        #timeOfLastVisit = Date().timeIntervalSince1970
        self.crfWeight += pow(2.0, -0.1 * (_visitNumber - self.visitNumber))
        self.visitNumber = _visitNumber
    
    def updateRank(self, _rank):
        self.rank = _rank
    
    def numberOfTransitionsToItem(self, _id):
        return len(self.nextVisits[_id])
    
    def numberOfVisitsToItem(self, _id, _currentHour):
        if _id not in self.nextVisits:
            return 0
        total = 0
        for _item in self.nextVisits[_id]:
            if _item.hour == _currentHour:
                total+=1
        return total
    
    def numberOfVisitsToItemsInCurrentHourSlot(self, _currentHour):
        total = 0
        for _id in self.nextVisits:
            total +=numberOfVisitsToItem(_id, _currentHour)
        return total
    
    def numberOfVisitsToItem(self, _id, _currentWeekday):
        if _id not in self.nextVisits:
            return 0
        total = 0
        for _item in self.nextVisits[_id]:
            if _item.weekday == _currentWeekday:
                total+=1
        return total
    
    def numberOfVisitsToItemsAtCurrentWeekday(self, _currentWeekday):
        total = 0
        for _id in self.nextVisits:
            total +=numberOfVisitsToItem(_id, _currentWeekday)
        return total
    
    def markovDescription(self):
        items = []
        for _id in self.nextVisits:
            items.append(_id[:10]+' '+str(len(self.nextVisits[_id])))
        return ', '.join(items)
    
class ScoredItem(object):
    def __init__(self, _id, _score):
        self.id = _id
        self.score = _score

class AccessRank(object):
    def __init__(self):
        self.l = 1.65 # medium
        self.d = 0.2 # medium
        self.useTimeWeighting = True
        self.initialItem = "<access_rank_nil>"
        self.mostRecentItem = self.initialItem
        self.visitNumber = 0
        self.items = {}
        predictionList = []
        self.maxVisits = 1000
        
    def stateForItem(self, _id):
        return self.items[_id]
    
    def visitItem(self, _id):
        self.visitNumber += 1
        self.visitNumber = min(self.visitNumber, self.maxVisits)
        previousItem = self.mostRecentItemID
        self.mostRecentItemID = _id
        
        previousItemState = stateForItem(previousItem)
        previousItemState.addVisitToItem(self.mostRecentItemID, self.maxVisits)
        self.items[previousItem] = previousItemState
        
        newItemState = stateForItem(self.mostRecentItemID)
        newItemState.updateVisits(self.visitNumber)
        self.items[self.mostRecentItemID] = newItemState
        
        updatePredictionList()
        
    def removeItem(self, _id):
        _tmp = dict(self.items)
        del _tmp[_id]
        self.items = _tmp
        
        _index_to_del = None
        _tmp_pred_list = self.predictionList
        for _item in _tmp_pred_list:
            if _item.id == _id:
                _index_to_del =  _tmp_pred_list.index(_item)
                break
        if _index_to_del:
            del _tmp_pred_list[_index_to_del]
        self.predictionList = _tmp_pred_list
        
    def removeItems(self, _ids_to_remove):
        for _id in _ids_to_remove:
            removeItem(_id)
            
        if self.mostRecentItemID in _ids_to_remove:
            visitItem(None)
        updatePredictionList()
        
    def updatePredictionList(self):
        updateScoredItems()
        sortPredictionList()
        updateItemRanks()
        addItemsToPredictionList()
        
    def updateScoredItems(self):
        print('')
        
    def sortPredictionList(self):
        print('')
        
    def updateItemRanks(self):
        print('')
    
    def addItemsToPredictionList(self):
        item = self.items[self.mostRecentItemID]
        if self.mostRecentItemID != self.initialItem and item.numberOfVisits == 1:
            self.predictionList.append(ScoredItem(self.mostRecentItemID, 0.0))
            _tmp = self.predictionList
            del _tmp[(-1)*self.maxVisits]
            self.predictionList = _tmp
    
    def scoreForItem(self, _id):
        l = self.l
        wm = markovWeightForItem(_id)
        wcrf = crfWeightForItem(_id)
        wt = self.timeWeightForItem(item) if self.useTimeWeighting else 1.0
        return pow(wm, l) * pow(wcrf, 1 / l) * wt
    
    def markovWeightForItem(self, _id):
        xn = numberOfVisitsForMostRecentItem()
        x = numberOfTransitionsFromMostRecentItemToItem(_id)
        return (x + 1) / (xn + 1)
    
    def numberOfVisitsForMostRecentItem(self):
        return self.items[self.mostRecentItemID].numberOfVisits
    
    def numberOfTransitionsFromMostRecentItemToItem(self, _id):
        return self.items[self.mostRecentItemID].numberOfTransitionsToItem(_id)
    
    def crfWeightForItem(self, _id):
        return self.items[_id].crfWeight
    
    def timeWeightForItem(self, _id):
        rh = hourOfDayRatioForItem(_id)
        rd = dayOfWeekRatioForItem(_id)
        return pow(max(0.8, min(1.25, rh * rd)), 0.25)
    
    def hourOfDayRatioForItem(self, _id):
        if numberOfCurrentHourItemVisits() < 10:
            return 1.0
        return numberOfCurrentHourVisitsToItem(_id) / averageNumberOfCurrentHourVisitsToItem(_id)
    
    def numberOfCurrentHourItemVisits(self, _id):
        total = 0
        for item,state in self.items.items():
            total += state.numberOfVisitsToItemsInCurrentHourSlot()
    
    def numberOfCurrentHourVisitsToItem(self, _id, _currentHour):
        return numberOfVisitsToItem(_id, currentHour)
    
        
    def averageNumberOfCurrentHourVisitsToItem(self, _id):
        totalVisits = 0
        hourOfDay = 1
        
        while hourOfDay < 24:
            totalVisits += numberOfVisitsToItem(_id, hourOfDay)
            hourOfDay += 3
            
        return totalVisits/8
    
    def numberOfVisitsToItem(self, _id, hourOfDay):
        total = 0
        for item,state in self.items.items():
            total += state.numberOfVisitsToItem(_id, hourOfDay)
            
    def dayOfWeekRatioForItem(self, _id):
        if (numberOfCurrentWeekdayItemVisits() < 10):
            return 1.0
        return numberOfCurrentWeekdayVisitsToItem(_id) / averageNumberOfWeekdayVisitsToItem(_id)
    
    def numberOfCurrentWeekdayItemVisits(self):
        total = 0
        for item,state in self.items.items():
            total += state.numberOfVisitsToItemsAtCurrentWeekday()
    
    def numberOfCurrentWeekdayVisitsToItem(self, _id, _currentWeekday):
        return numberOfVisitsToItem(_id, _currentWeekday)
    
    def averageNumberOfWeekdayVisitsToItem(self, _id):
        total = 0
        for weekday in range(1,8):
            total += numberOfVisitsToItem(_id, weekday)
        return total / 7
    
    def numberOfVisitsToItem(self, _id, _weekday):
        total = 0
        for item,state in self.items.items():
            total += state.numberOfVisitsToItem(_id, _weekday)
        return total

def takeSecond(elem):
    return elem[1]

def flatRecom(seq):
    seen_bl = set()
    seen_add_bl = seen_bl.add
    return [x for x in seq if not (x[0] in seen_bl or seen_add_bl(x[0]))]
