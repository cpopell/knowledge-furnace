def splitsource(sourcestring): #Function splitsource detects if the unit is in
                               #fractional form
    if '/' in sourcestring: #If the division symbol is present in the string,
                            #indicating a numerator and denominator
        sourcestringsplit = sourcestring.split('/') #Split the string in half
                                                    #along the '/'
    elif 'per' in sourcestring.lower(): #Otherwise, if there is a 'per' present
                                        #in the strong (1 meter per second)
        sourcestringsplit = sourcestring.split('per') #Split the string in half
                                                      #along the 'per'
    else: #Otherwise, pass.
        sourcestringsplit = sourcestring
    return sourcestringsplit #Return sourcestringsplit as a list

def detectprefix(sourcestringsplit): #Function detectPrefix detects the prefixes
    import re
    print ("The passed string is %s") % (sourcestringsplit) #TEST: What string was passed?
    scalarmultiplier = 1 #Default multiplier is 1.
    startpoint = 0
    scalarstring = None
    pattern = re.compile("^((?:\d*\.\d+)|\d+)(?:\^((?:\d*\.\d+)|\d+))?") #Regex
    match = pattern.match(sourcestringsplit) #Check unitstringsplit for the regex pattern
    if match is not None: #If a match is found
        num, exp = match.groups() #Number and exponential are two groups
        if exp == None: #If there's no exponential
            scalarmultiplier = num #The scalar multiplier is just the number
        else:#If there is an exponential
            scalarmultiplier = int(num) ** int(exp) #The scalar multiplier is the number raised to the exponential, ie 13^2 would be num == 13, exp == 2, scalarmultiplier == 13 ** 2
            startpoint = len(num) + len(exp) + 1
            scalarstring = str(num) + '^' + str(exp)
    return scalarmultiplier, startpoint, scalarstring

def listcheck(list, startpoint, inputstring):
    for key in list:
        if key in inputstring and inputstring.index(key) == 0:
            startpoint += len(key)
            return True, key, startpoint
    return False, None, startpoint
    
def printstate(parsedunit, startpoint):
    print 'The list of sorted substrings is ' + str([x[0] for x in parsedunit])
    print 'The interpretation of sorted substrings is ' + str([x[1] for x in parsedunit])
    print 'The index of types of sorted substrings is ' + str([x[2] for x in parsedunit])
    print 'The starting point for the next search is ' + str(startpoint)
    return

def dictimport(filename):
    importdict = {}
    importlist = []
    with open(filename, "r") as txt:
        for line in txt:
            if '\n' in line:
                line = line.replace("\n", "")
            definition = line.split(',')
            key = definition[0]
            value = definition[1]
            importdict[key] = value
            importlist.append(key)
        importlist.sort()
        importlist.sort(key=len, reverse = True)
    return importdict, importlist

    
def updateparsedunit(parsedunit,key,value,currenttype):
    import collections
    parsedsubstring = collections.namedtuple('parsedsubstring',
                                             ['subin','subout','subtype'])
    parsedtuple = parsedsubstring(subin=key,subout=value,subtype=currenttype)
    parsedunit.append(parsedtuple)
    return parsedunit
    
def init():
    import collections
    import re #Regex
    #parsedsubstring = collections.namedtuple('parsedsubstring',['subin','subout','subtype'])
    parsedunit = []
    sourcestring = '13^2mmkPa'
    doublelist = []
    
    prefixdict, prefixlist = dictimport('prefix.txt')
    unitdict, unitlist = dictimport('unit.txt')
    for unit in unitlist:
        if unit in prefixlist:
            doublelist.append(unit)
    
    sourcestringsplit = splitsource(sourcestring)
    print sourcestringsplit
    if len(sourcestringsplit) == 2:
        left = sourcestringsplit[0]
        right = sourcestringsplit[1]
    else:
        parsedunit = stringparse(parsedunit, sourcestring, doublelist,
                                 prefixdict, prefixlist, unitdict, unitlist)

def stringparse(parsedunit, sourcestring, doublelist, prefixdict, prefixlist,
                unitdict, unitlist):
    startpoint = 0
    currenttype = 0
    scalarmultiplier, startpoint, scalarstring = detectprefix(sourcestring)
    print scalarmultiplier
    while int(startpoint+1) <= len(sourcestring):
        print len(parsedunit)+1
        inputstring = sourcestring[startpoint:]
        print 'Remaining string to be parsed is ' + inputstring
        checkflag, key, tempstartpoint = listcheck(prefixlist, startpoint,
                                                  inputstring)
        if checkflag == False:
            #print 'prefixlistcheck false at ' + str(startpoint)
            checkflag, key, tempstartpoint = listcheck(unitlist, startpoint,
                                                      inputstring)
            if checkflag == False:
                print 'No units from either dictionary have been found in the rest of your input string'
            elif checkflag == True:
                currenttype = 2
                updateparsedunit(parsedunit,key,unitdict[key],currenttype)
                startpoint = tempstartpoint
                printstate(parsedunit,startpoint)
        elif checkflag == True:
            if key in doublelist: # If this is one of the annoying keys that is
                                  # both a prefix and a unit, such as milli and
                                  # meter, check further
                print 'Checking if detected substring is a prefix or unit, as it represents both.'
                doublecheckflag, doublekey, doublestartpoint = listcheck(unitlist, tempstartpoint, inputstring[len(key):])
                print doublecheckflag
                if doublecheckflag == True: #Pattern is [p/u]->u
                    if currenttype == 0: #This means this is the first substring
                        currenttype = 1 #It's -probably- a prefix. Pattern
                                        #locked as p->u
                        updateparsedunit(parsedunit,key,prefixdict[key],
                                         currenttype)
                        startpoint = tempstartpoint
                    elif currenttype == 1:#This checks to see if the last time
                                          #around the update was a
                                          #prefix. Pattern is p->[p/u]->u
                        currenttype = 2 #Pattern confirmed as p->u->u
                        updateparsedunit(parsedunit,key,unitdict[key],
                                         currenttype)
                        startpoint = tempstartpoint #Instead of updating twice
                                                    #at once, incrementing
                                                    #properly so next eval can
                                                    #be done as well.
                    elif currenttype == 2: #Pattern is u->[p/u]->u
                        currenttype = 1 #Pattern locked as u->p->u
                        updateparsedunit(parsedunit,key,prefixdict[key],
                                         currenttype)
                        startpoint = tempstartpoint
                elif doublecheckflag == False: #Pattern is [p/u]->p
                    currenttype = 2 #It's absolutely a unit. p->p not allowed.
                    updateparsedunit(parsedunit,key,unitdict[key],currenttype)
                    startpoint = tempstartpoint
            else:#Otherwise, update
                currenttype = 1
                updateparsedunit(parsedunit,key,prefixdict[key],currenttype)
                startpoint = tempstartpoint
                printstate(parsedunit,startpoint)
    return parsedunit

init()
