

import datetime

def calculateDuration(startTim, endTim):
    duration = endTim - startTim
    hours = duration.seconds / 3600
    minutes = (duration.seconds % 3600) / 60
    seconds = (duration.seconds % 3600) % 60
    if duration.days > 0:
        return '%d天%d时%d分%d秒' % (duration.days,hours, minutes, seconds)
    else:
        return '%d时%d分%d秒' % (hours, minutes, seconds)