# py_calendars

### This package show the calendar view on the terminal when  you give the year and month also give the satring position of month and year

---

> After install the package import the module 


```
from py_calendars import calendars

calendar(2005,'jan')
```
---
> In terminal you get the out put 

```

      January 2005 

 sun   mon  tus  wed  thr  fri  sat 

                                01
  02   03   04   05   06   07   08
  09   10   11   12   13   14   15
  16   17   18   19   20   21   22
  23   24   25   26   27   28   29
  30   31

```
----
### About  package

>In this package thir are three main part 
1. Finding the given year starting position
2. Finding the given month starting position 
3. use the two resuelt to create the calendar printing design

----
> if you want the year starting position import the year_start ( ) function

```
from py_calendars import year_start

print('ans= ', year_start(2005))
```
#### output
```
ans= 7
```
> That means the 2005 January start with 7 position saturday 
```
      January 2005 

 sun   mon  tus  wed  thr  fri  sat 

                                01
  02   03   04   05   06   07   08
  09   10   11   12   13   14   15
  16   17   18   19   20   21   22
  23   24   25   26   27   28   29
  30   31 
  ```

 >if you want the starting month position use month_start ( ) function

 ```
 from py_calendars import month_start


print('ans= ' month_start(2005,'nov'))
```
#### output
````
ans= 3
````
>that mean the 2005 November start with 3 position Tuesday

```
      November 2005 

 sun   mon  tus  wed  thr  fri  sat 

            01   02   03   04   05
  06   07   08   09   10   11   12
  13   14   15   16   17   18   19
  20   21   22   23   24   25   26
  27   28   29   30

```