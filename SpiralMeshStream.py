#.dok's ulam spiral mesh network topography lookup. I am sure that there is a better/more efficient way to do this but this works for now.

#Oh dear god this has turned into a monstrosity. Do not hold me accountable for this code. I am so sorry. Whatever it works

import math
import sys

def getLayer(streamNum): #Returns the layer number of a stream
    layer = math.sqrt(streamNum)
    layer = math.ceil(layer)

    if (layer%2==0):
        layer += 1

    layer = (int(layer)/2)
    return layer

def getFinish(layerNum):#Returns the stream number that finishes the layer
    x = 1
    finish = 1
    
    for y in range(0, layerNum):
        x = x + 2
        finish = ((x)**2)
    return finish

def getStart(layerNum): #Returns the stream number that starts the layer
    finish = getFinish(layerNum)

    start = int(math.sqrt(finish))
    start = start - 1
    start = 4*start
    start = finish - start
    start = start + 1
    
    return start
    
def getQuarterLength(finish): #gives you 1/4 the length of the layer
    finish = int(math.sqrt(finish))
    return (finish - 1)

def getCorner(layer,corner): #returns the stream number of that corner
    finish = getFinish(layer)
    quarterLength = getQuarterLength(finish)
    
    corner4 = finish
    corner3 = finish - quarterLength
    corner2 = corner3 - quarterLength
    corner1 = corner2 - quarterLength

    if corner == 1:
        corner = corner1
    elif corner == 2:
        corner = corner2
    elif corner == 3:
        corner = corner3
    elif corner == 4:
        corner = corner4
    
    return corner

def getQuadrant(stream):#returns what quadrant the stream is in. Stream 2 is in q1, 4 is in q2, 6 is in q3, 8 is in q4. This will likely be replaced with different terminology such as "in" "out" "+" and "-" refering to layers and values
    layer = getLayer(stream)
    if (stream == 1):
        quadrant = 0
    elif (stream <= getCorner(layer,1)):
        quadrant = 1
    elif (stream <= getCorner(layer,2)):
        quadrant = 2
    elif (stream <= getCorner(layer,3)):
        quadrant = 3
    elif (stream <= getCorner(layer,4)):
        quadrant = 4

    return quadrant

def follow(stream): #returns the 8 streams surrounding the passed stream. Starts 1 stream higher than the passed stream no matter how you draw it.
    layer = getLayer(stream)

    #get the corners of the layer for future refence
    c1 = getCorner(layer,1)
    c2 = getCorner(layer,2)
    c3 = getCorner(layer,3)
    c4 = getCorner(layer,4)
    
    if (layer == 0):#layer 0 is a special case and all of the values are already known so it is easy
        f1 = 2
        f2 = 3
        f3 = 4
        f4 = 5
        f5 = 6
        f6 = 7
        f7 = 8
        f8 = 9
    elif stream == getStart(layer): #stream is start
        f1 = getStart(layer+1)+1
        f2 = getStart(layer+1)+2
        f3 = stream+1
        f4 = getStart(layer-1)
        f5 = stream-1
        f6 = getFinish(layer)-1
        f7 = getFinish(layer)
        f8 = getStart(layer+1)
    elif stream == getFinish(layer): #stream is finish (also corner 4)
        f1 = getFinish(layer+1)-1 
        f2 = getFinish(layer+1) 
        f3 = stream+1
        f4 = stream+2
        f5 = getStart(layer)
        f6 = getFinish(layer-1)
        f7 = stream-1
        f8 = getFinish(layer+1)-2
    elif (stream == c1) or (stream == c2) or (stream == c3): #stream is corner
        if stream == c1:
            corner = 1
        elif stream == c2:
            corner = 2
        elif stream == c3:
            corner = 3
        else:
            corner = 4 #redundant but now you know!
            
        f1 = getCorner(layer+1,corner)-1
        f2 = getCorner(layer+1,corner)
        f3 = getCorner(layer+1,corner)+1
        f4 = getCorner(layer+1,corner)+2
        f5 = stream+1
        f6 = getCorner(layer-1,corner)
        f7 = stream-1
        f8 = getCorner(layer+1,corner)-2
    elif (stream == c1-1) or (stream == c2-1) or (stream == c3-1) or (stream == c4-1): #stream is -1 from a corner
        if stream == c1-1:
            corner = 1
        elif stream == c2-1:
            corner = 2
        elif stream == c3-1:
            corner = 3
        else:
            corner = 4 #redundant but now you know!
            
        f1 = getCorner(layer+1,corner)-2
        f2 = getCorner(layer+1,corner)-1
        f3 = stream +1
        f4 = getCorner(layer-1,corner)+1
        f5 = getCorner(layer-1,corner)
        f6 = getCorner(layer-1,corner)-1
        f7 = stream -1
        f8 = getCorner(layer+1,corner)-3
    elif(stream == c1+1) or (stream == c2+1) or (stream == c3+1) or (stream == c4+1): #stream is +1 from a corner
        if stream == c1+1:
            corner = 1
        elif stream == c2+1:
            corner = 2
        elif stream == c3+1:
            corner = 3
        else:
            corner = 4 #redundant but now you know!
            
        f1 = getCorner(layer+1,corner)+2 
        f2 = getCorner(layer+1,corner)+3 
        f3 = stream +1
        f4 = getCorner(layer-1,corner)+1
        f5 = getCorner(layer-1,corner)
        f6 = stream -2
        f7 = stream -1
        f8 = getCorner(layer+1,corner)+1
    else: #stream is not any of the above so find the quadrant and position. 
        if (stream < getCorner(layer,1)):
            quadrant = 1
            position = getCorner(layer,1) - stream
        elif (stream < getCorner(layer,2)):
            quadrant = 2
            position = getCorner(layer,2) - stream 
        elif (stream < getCorner(layer,3)):
            quadrant = 3
            position = getCorner(layer,3) - stream 
        else:
            quadrant = 4
            position = getCorner(layer,4) - stream

        f1 = (getCorner(layer+1,quadrant) - (position +1))
        f2 = (getCorner(layer+1,quadrant) - (position +1)+1)
        f3 = (stream +1)
        f4 = (getCorner(layer-1,quadrant) - (position -2))
        f5 = (getCorner(layer-1,quadrant) - (position -1))
        f6 = (getCorner(layer-1,quadrant) - (position))
        f7 = (stream -1)
        f8 = (getCorner(layer+1,quadrant) - (position +1)-1)

    #Special cases
    if (stream == 11):
        f6 = 9
    elif (stream == 2):
        f4 = 4
    elif (stream ==6):
        f6 = 4
        f4 = 8
    elif (stream ==8):
        f4 = 2
        f6 = 6
    elif (stream ==4):
        f4 = 6
        f6 = 2
    #
    return f1,f2,f3,f4,f5,f6,f7,f8

def fLookup(stream,fol): #lookup the follow for the stream
    f1, f2, f3, f4, f5, f6, f7, f8 = follow(stream) #load the follow streams

    if fol == 1:
        fStream = f1
    elif fol == 2:
        fStream = f2
    elif fol == 3:
        fStream = f3
    elif fol == 4:
        fStream = f4
    elif fol == 5:
        fStream = f5
    elif fol == 6:
        fStream = f6
    elif fol == 7:
        fStream = f7
    elif fol == 8:
        fStream = f8
    else:
        print 'uh oh, Fol = ', fol
        fol = 0
    return fStream

def path(fromStream,toStream): #Finds the stream hop path between two streams
    #Begin magic...
    
    fromQuad = getQuadrant(fromStream)
    toQuad = getQuadrant(toStream)
    oQuad = False

    path = [fromStream]
    fol = 1
    inOut = 0
    plusMinus = 0
    
    toCurStream = toStream
    toFol = 1
    toInOut = 0
    toPlusMinus = 0
    
    fromCurStream = fromStream
    fromFol = 1
    fromInOut = 0
    fromPlusMinus = 0
    
    #Begin to stream section
    if (toStream == 1):
        toInOut = 0
        toPlusMinus = 0
        toCurStream = 1
    else:
        streamQuadrant = getQuadrant(toStream)
        for y in range(1, streamQuadrant): #sticks to one of the four sides, does not move at an angle
            toFol = toFol + 2
            
        #print fromStream
        toCurStream = fLookup(1,toFol)#Move 1 into the correct quadrant
        toInOut = toInOut + 1
        #print curStream
        
    toLayer = getLayer(toStream)
    toCurLayer = getLayer(toCurStream)
    
    if (toCurStream != toStream):
        if(toCurLayer < toLayer):
            
            while True: #Get to layer
                toCurStream = fLookup(toCurStream,1)#Move 1 out
                toInOut = toInOut + 1
                if (getLayer(toCurStream) == toLayer):
                    break

        #Now they are on the same layer
        if (toCurStream > toStream):
            while True:
                toCurStream = toCurStream - 1
                toPlusMinus = toPlusMinus - 1
                if (toCurStream == toStream): #Found
                    break
        elif (toCurStream < toStream):
            while True:
                toCurStream = toCurStream + 1
                toPlusMinus = toPlusMinus + 1
                if (toCurStream == toStream): #Found
                    break
        #Else they are the same
    #END to stream section

    #Begin from stream section
    if (fromStream == 1):
        fromInOut = 0
        fromPlusMinus = 0
        fromCurStream = 1
    else:
        streamQuadrant = getQuadrant(fromStream)
        for y in range(1, streamQuadrant): #sticks to one of the four sides, does not move at an angle
            fromFol = fromFol + 2
            
        #print fromStream
        fromCurStream = fLookup(1,fromFol)#Move 1 into the correct quadrant
        fromInOut = fromInOut + 1
        #print curStream
        
    fromLayer = getLayer(fromStream)
    fromCurLayer = getLayer(fromCurStream)
    
    if (fromCurStream != fromStream):
        if(fromCurLayer < fromLayer):
            
            while True: #Get to layer
                fromCurStream = fLookup(fromCurStream,1)#Move 1 out
                fromInOut = fromInOut + 1
                if (getLayer(fromCurStream) == fromLayer):
                    break

        #Now they are on the same layer
        if (fromCurStream > fromStream):
            while True:
                fromCurStream = fromCurStream - 1
                fromPlusMinus = fromPlusMinus - 1
                if (fromCurStream == fromStream): #Found
                    break
        elif (fromCurStream < fromStream):
            while True:
                fromCurStream = fromCurStream + 1
                fromPlusMinus = fromPlusMinus + 1
                if (fromCurStream == fromStream): #Found
                    break
        #Else they are the same
    #END from stream section

    #Begin fromStream toStream movement
    if(fromStream == 1):
        inOut = toInOut
        plusMinus = toPlusMinus
    elif(toStream == 1):
        inOut = fromInOut * -1
        plusMinus = fromPlusMinus * -1
    elif (fromQuad == toQuad): #Same Quadrant
        inOut = (toInOut - fromInOut)
        plusMinus = (toPlusMinus - fromPlusMinus)
    elif(fromQuad == (toQuad - 1) or fromQuad == (toQuad + 3)): #One quadrant higher
        inOut = (fromInOut + toPlusMinus)
        inOut = (inOut * -1)
        plusMinus = (toInOut - fromPlusMinus)
    elif(fromQuad == (toQuad + 1) or fromQuad == (toQuad - 3)): #One quadrant lower
        inOut = (fromInOut - toPlusMinus)
        inOut = (inOut * -1)
        plusMinus = (toInOut + fromPlusMinus)
        plusMinus = (plusMinus * -1)
    elif(fromQuad == (toQuad + 2) or fromQuad == (toQuad - 2)): # Opposite Quadrant
        inOut = (toInOut + fromInOut)
        inOut = (inOut * -1)
        plusMinus = (toPlusMinus + fromPlusMinus)
        plusMinus = (plusMinus * -1)
        oQuad = True
    #End fromStream toStream movement
        
    #curStream = fLookup(fromStream,fol)#Reset for move
    curStream = fromStream
    lowerHalf = plusMinus 
    #path.append(fromStream) not needed
    if (toStream > fromStream):
        print 'Distance Before Optimization: ', (toStream - fromStream)+1
    else:
        print 'Distance Before Optimization: ', (fromStream - toStream)+1
        
    print 'Distance After First Optimization: ', int(math.fabs(inOut) + math.fabs(plusMinus) + 1)
    
    while True: #Optimized path, uses diagonal movement
        oldFol = fol
        if (inOut > 0):
            if (plusMinus > 0):
                if (curStream == 1):
                    if (fol == 8):
                        fol = 1
                    else:
                        fol = fol+1
                else:
                    fol = 2
                plusMinus = plusMinus - 1
            elif (plusMinus < 0):
                if (curStream == 1):
                    if (fol == 1):
                        fol = 8
                    else:
                        fol = fol-1
                else:
                    fol = 8
                plusMinus = plusMinus + 1
            else:
                fol = 1
            inOut = inOut - 1
                
        elif(inOut < 0):
            if (plusMinus > 0):
                fol = 4
                
                plusMinus = plusMinus - 1
            elif (plusMinus < 0):
                fol = 6
                plusMinus = plusMinus + 1
            else:
                fol = 5
            inOut = inOut + 1

        elif (plusMinus > 0):
            fol = 3
            plusMinus = plusMinus - 1
            
        elif (plusMinus < 0):
            fol = 7
            plusMinus = plusMinus + 1

        if (curStream == 1): #If coming from stream one, a direction must be known other than in/out plus/minus
            streamQuadrant = getQuadrant(toStream)
            flw = 1
            for y in range(1, streamQuadrant): #sticks to one of the four sides, does not move at an angle
                flw = flw + 2
                
            if (fol == 1 or fol == 3 or fol == 5 or fol == 7):
                fol = flw
            elif (fol == 2 or fol == 6):
                if (flw == 8):
                    flw = 1
                else:
                    fol = flw + 1
            elif (fol == 4 or fol == 8):
                if (flw == 1):
                    flw = 8
                else:
                    fol = flw - 1

        curQuad = getQuadrant(curStream)
        futQuad = getQuadrant(fLookup(curStream,(fol)))
            
        if (curQuad != futQuad): #Moving from one quadrant to a different quadrant and curstream != 1
            if (curQuad == 0): #Moving from stream 1 and plusMinus <0
                if (oQuad == True):
                    tmpInOut = inOut * -1
                    tmpPlusMinus = plusMinus * -1
                elif(toPlusMinus == 0):
                    tmpInOut = plusMinus * -1
                    tmpPlusMinus = inOut
                    if (fol == 4 or fol == 6 or fol == 8):
                        fol = fol - 2
                    elif (fol == 1 or fol == 3 or fol == 5 or fol == 7) and (fromStream == 1):
                        tmpPlusMinus = 0
                        tmpInOut = inOut
                elif(lowerHalf < 0):
                    tmpInOut = inOut * -1
                    tmpPlusMinus = plusMinus * -1
                    if (fol == 4 or fol == 6 or fol == 8):
                        if (fromStream != 1):
                            fol = fol - 2
                        else:
                            tmpInOut = plusMinus * -1
                            tmpPlusMinus = inOut
                    
                elif(fromStream != 1 and toStream != 1):
                    tmpInOut = inOut * -1
                    tmpPlusMinus = plusMinus
                else:
                    tmpInOut = inOut
                    tmpPlusMinus = plusMinus
            elif (futQuad == 0):
                tmpInOut = inOut
                tmpPlusMinus = plusMinus
            elif(curQuad == (futQuad - 1) or curQuad == (futQuad + 3)): #One quadrant higher
                tmpInOut = plusMinus
                tmpPlusMinus = inOut * -1
            elif(curQuad == (futQuad + 1) or curQuad == (futQuad - 3)): #One quadrant lower
                tmpInOut = plusMinus * -1
                tmpPlusMinus = inOut
            else:
                tmpInOut = inOut
                tmpPlusMinus = plusMinus
            plusMinus = tmpPlusMinus
            inOut = tmpInOut
        
        curStream = fLookup(curStream,(fol))
        path.append(curStream)

        '''
        # Uncomment for debugging
        print ' '
        print 'inOut:', inOut
        print 'PlusMinus:', plusMinus
        print 'fol:',fol
        print 'curStream:',curStream
        blarg = raw_input('Proceed?')
        print '**************'
        '''
        
        if (curStream == toStream):
            print 'Distance After Final Optimization: ', len(path)
            print ' '
            print 'Path', path
            print ''
            break
            
    
def main():

    print '*****************************************************'
    print 'Ulam spiral lookup by .dok. Enter stream "0" to quit.'
    print 'Commands: lookup, path'
    print '*****************************************************'
    print ' '
    action = raw_input('> ')
    print ' '
    
    if (action == 'lookup'):
        Stream = int(raw_input('StreamNumber: ')) #get the stream number from the user
        if (Stream == 0):
            sys.exit()
            
        layer = getLayer(Stream) #get the layer number
        quadrant = getQuadrant(Stream)
        finish = getFinish(layer) #get the finish of the passed layer
        start = getStart(layer) #get the start of the passed layer
        f1, f2, f3, f4, f5, f6, f7, f8 = follow(Stream) #load the follow streams

        print ' '
        print 'Stream Number: ', Stream
        print 'Layer: ' , layer
        print 'Quadrant: ', quadrant
        print 'Layer Start: ', start
        print 'Layer Finish: ', finish
        print 'Follow1: ', f1
        print 'Follow2: ', f2
        print 'Follow3: ', f3
        print 'Follow4: ', f4
        print 'Follow5: ', f5
        print 'Follow6: ', f6
        print 'Follow7: ', f7
        print 'Follow8: ', f8
        print ' '
        
        main() #loop enter the stream "0" to quit
    elif (action == 'path'):

        stream1 = int(raw_input('From Stream: '))
        stream2 = int(raw_input('To Stream: '))
        print ' '
        
        path(stream1,stream2)
        
        main()
    elif (action == '0'):
        sys.exit()
    else:
        print 'Invalid Command'
        main()
      
main()
