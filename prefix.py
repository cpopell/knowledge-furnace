# def unitrubric(unitstring)
 # unitlist[0] = str(unitstring)
 # unitlist[1] = str(unitstring).lower()
 # for word in unitstring.split(' ')
  # unitstringmod.append
  # if word == 'Per'
   # word = '/'
   # unitlist.append(''.join(unitstring)
import re #Regex
def splitPrefix(unitstring): #Function splitPrefix detects if the unit is in fractional form
    if '/' in unitstring: #If the division symbol is present in the string, indicating a numerator and denominator
        unitstringsplit = unitstring.split('/') #Split the string in half along the '/'
    elif 'per' in unitstring.lower(): #Otherwise, if there is a 'per' present in the strong (1 meter per second)
        unitstringsplit = unitstring.split('per') #Split the string in half along the 'per'
    else: #Otherwise, pass.
        pass
    return unitstringsplit #Return unitstringsplit as a list

def detectPrefix(unitstringsplit): #Function detectPrefix detects the prefixes
    print ("The passed string is %s") % (unitstringsplit) #TEST: What string was passed?
    unitmultiplier = 1 #Default multiplier is 1.
    multiplierlist = [] #<>
    pattern = re.compile("^((?:\d*\.\d+)|\d+)(?:\^((?:\d*\.\d+)|\d+))?") #Regex
    match = pattern.match(unitstringsplit) #Check unitstringsplit for the regex pattern
    if match is not None: #If a match is found
        num, exp = match.groups() #Number and exponential are two groups
        if exp == None: #If there's no exponential
            scalarmultiplier = num #The scalar multiplier is just the number
        else:#If there is an exponential
            scalarmultiplier = num ** exp #The scalar multiplier is the number raised to the exponential, ie 13^2 would be num == 13, exp == 2, scalarmultiplier == 13 ** 2
    #prefixlist = {'milli':.001,'Milli':.001,'m'
    prefixlist = {'centi':.01,'Centi':.01,'c':.01} #Sample dictionary of prefixes to check for in the 1/100s range

    for prefixkey in prefixlist.keys(): #For each prefixkey in the list
        if prefixkey in unitstringsplit and prefixkey[-1] != unitstringsplit[-1]:
            #Check if it's in unitstringsplit AND if the last prefixkey does not match the last unitstringsplit.
            #This is to make sure that if, say, you have a mm^3 value, the second m doesn't trigger the dictionary.
            unitmultiplier *= prefixlist.get(prefixkey) #Multiply the unit multiplier by the return - ie c is .01
            if '^' in unitstringsplit: #If there's a carrot symbol (exponential)
                unitexponential = int(unitstringsplit[unitstringsplit.index('^') + 1]) #Set unitexponential equal to the value of the int next to the exponential symbol.
                print ("The exponential of the unit is %d") %(unitexponential) #TEST: Print out what the exponential is.
                print ("The prefix %s is the multiplier %r") %(prefixkey, unitmultiplier) #TEST: Print out what the multiplier is.
                unitmultiplier **= unitexponential #Raise the multiplier by the exponential. c^3 = .01**3 = .000001.
                #multiplierlist.append(unitmultiplier)
            #else:
                #multiplierlist.append(unitmultiplier)\
    print ("Scalar multiplier is %r. Unit multiplier is %r") %(scalarmultiplier, unitmultiplier) #Print out the scalar multiplier and unit multiplier.
    return float(scalarmultiplier)*unitmultiplier #Return the scalar multiplier times the unit multiplier

def calculatePrefix(ISUstring):
    ISUsplit = splitPrefix(ISUstring)
    print len(ISUsplit)
    if len(ISUsplit) == 2:
        numerator = detectPrefix(ISUsplit[0])
        print ("The numerator of the unit is %s") %(numerator)
        denominator = detectPrefix(ISUsplit[1])
        print ("The denominator of the unit is %d") %(denominator)
        ISUscale = float(numerator)/denominator
        return ISUscale
    else:
        ISUscale = detectPrefix(ISUsplit)
        return ISUscale

ISUstring = '2/13cm^3'
ISUscale = float(calculatePrefix(ISUstring))
print str.format('{0:.6f}', ISUscale)
