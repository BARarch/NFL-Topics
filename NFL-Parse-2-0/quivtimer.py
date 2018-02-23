from datetime import datetime

class ticToc:
    # the timer that never stopes once started
    def __init__(self):
        self.tic()
    
    def tic(self):
        self.start = datetime.now()
    
    def toc(self):
        return self.time_str(datetime.now() - self.start)
        
    def lap(self):
        timeStr = self.time_str(datetime.now() - self.start)
        self.tic()
        return timeStr
        
    def time_str(self, td):
        # td is a datetime.timedelta object 
        # A: 1800ms
        # B: 47.5s
        # C: 4m 12s
        # D: 1:04:27
        

        hours, rem = divmod(td.seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        milisecondsTotal = int(td.total_seconds() * 1000)


        ## Mesured in Seconds
        milisecondsLimit = 2


        if td.total_seconds() < milisecondsLimit:
            return '{}ms'.format(milisecondsTotal)

        if td.total_seconds() < 60:
            tenths = int(10 * (td.total_seconds() - seconds))
            return '{}.{}s'.format(seconds, tenths)

        if minutes < 60:
            return '{}m {}s'.format(minutes, seconds)

        if hours < 24:
            return str(td)

        else:
            return '{}d'.format(td.days)