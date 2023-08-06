# this is the module to find the every year starting with witch day on jan
# and find the given month starting also


def year_start(year):
    val=0
    if year == 1970: # the year staring with 1970
        return 369%7

    if year < 1970:
        return 'the year equal to 1970 or more than that '
    else:
        n= year-1970
        y=1970
        
        for i in range(n):
           
            if  (y%100)% 4 == 0:
                val=val+366
            elif y == 1970:
                val=val+369 # 370 is the 365 day and extra 4 empty cloumn in the 1970 jan in starting 

            else:
                val=val+365 
            y=y+1
        ans= (val % 7)+1
        return ans
    
def month_start(year,month):   # this section find the month starting day position

        ans = year_start(year)
       
        mm=0
        mont = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
        mont_d = {1:31,2:28,3:31, 4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        if (year%100)%4 == 0:
            mont_d[2]=29
        else:
            mont_d[2]=28    
        key = int(mont[month])
        
        for z in range(1,key):
            mm = mm + mont_d[z]
            
        mm=mm+ans    
        ans1= mm%7
        if ans1 == 0:
            ans1=7
        return ans1    





