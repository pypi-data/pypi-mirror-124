# to create the calendar design 
from py_calendars.year_month import month_start, year_start


def calendar(year,month):
    ans = month_start(year,month)
    
    # day arrangement 
    mont = {'jan':31,'feb':28,'mar':31,'apr':30,'may':31,'jun':30,'jul':31,'aug':31,'sep':30,'oct':31,'nov':30,'dec':31}
    
    if (year%100)%4 == 0:
        mont['feb']=29
    else:
        mont['feb']=28
    day = mont[month]
    b=ans-1
    d=7-b
    da=1
    
    m = {'jan':'January','feb':'February','mar':'March','apr':'April','may':'May','jun':'June','jul':'July','aug':'August','sep':'September','oct':'October','nov':'November','dec':'December'}
    print()
    print()
    print('\033[36m','\033[1m','   ',m[month], year,'\033[0m')
    print()
    print('\033[91m','sun','\033[0m','\033[94m','mon  tus  wed  thr  fri  sat','\033[0m')
    print()

    for i in range (6):
        if b != 0:
            for i in range(1,b+1):
                print('   ',' ',end='')
                b=0
                
            
        for z in range (d):
            
                
            print( ' ',"%02d"% da,'', end='')
            
            da=da+1
            if da > day:
                break
        print()
        if da > day:
                break
        d=7
    print()
    




