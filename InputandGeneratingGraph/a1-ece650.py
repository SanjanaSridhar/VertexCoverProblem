#!/usr/bin/python
import re
import math
import sys
class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = []

    def addNeighbor(self, nbr):
        self.connectedTo.append(nbr)
    
    def removeNeighbor(self,nbr):
        self.connectedTo.remove(nbr)

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo

    def getId(self):
        return self.id


class Graph:
    def __init__(self):
        self.vertList = {}
        self.vertexCoordinate = {}
        self.numVertices = 0
        self.vertexID = 0
    '''Creates a map between vertex id and it's co-ordinate'''
    def createVertexCoordinate(self, coordinate):
        self.vertexID = self.vertexID+1
        self.vertexCoordinate[coordinate] = self.vertexID

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex
    
    def deleteVertex(self,key):
        self.numVertices = self.numVertices - 1
        self.vertList.pop(key,None)
        #deleted vertex is key
        connectionsToBeDeleted = []
        for x in self.vertList.keys():
            v = self.getVertex(x)
            for nbr in v.connectedTo:
                if key == nbr.id:
                    connectionsToBeDeleted = v
        return connectionsToBeDeleted

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t):
        if f in self.vertList and t in self.vertList:
            self.vertList[f].addNeighbor(self.vertList[t])
            
    def deleteEdge(self,f,t):
        if f in self.vertList and t in self.vertList:
            self.vertList[f].removeNeighbor(self.vertList[t])
            
    def edgdeExists(self,f,t):
        adjList1 = self.vertList[f].connectedTo
        adjList2 = self.vertList[t].connectedTo
        if(self.vertList[t] in adjList1):
            return True
        elif (self.vertList[f] in adjList1):
            return True
        else:
            return False
            
    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())


class VertexCoverGraph(Graph):
    def __init__(self):
        Graph.__init__(self)
        '''This is a map from street name to its GPS coordinates '''
        self.streetPointsMap = {}
        '''This is a map of intersection points to the list of street ids '''
        self.intersection = {} 
        '''Map between street name and id'''   
        self.streetIdMap = {}
        self.streetId = 0
    '''This function parses the input by splitting it according to the delimiters ""/'' and space '''
    def inputParsing(self, inputString):
        finalInput = []
        pos = 0
        # (['"]?) - matches optional single or double quote
        #(,*?) - matches the string itself.  - non greedy match - assigned to result
        #\1 back reference, to match the single or double quote arrived at earlier
        #( |$) -matches space separating entry or end of line - assigned to separator
#         PATTERN = re.compile(r"""(['"]?)(.*?)\1( |$)""")
        PATTERN = re.compile(r"""(['"]?)(.*?)\1( |$)""")
        while True:
            m = PATTERN.search(inputString, pos)
            result = m.group(2)
            separator = m.group(3)
            finalInput.append(result)
            if not separator:
                break
            pos = m.end(0)
        return finalInput

    '''This function reads the input from the user through command line '''
    def readInput(self):
        userInput = raw_input()
        inputList = self.inputParsing(userInput)
        return inputList
    
    def isBetween(self,a, b, c):
        epsilon = 2.220446049250313e-16
        crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
        if abs(crossproduct) > epsilon : 
            return False   # (or != 0 if using integers)
        dotproduct = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1])*(b[1] - a[1])
        if dotproduct < 0 : 
            return False
        squaredlengthba = (b[0] - a[0])*(b[0] - a[0]) + (b[1] - a[1])*(b[1] - a[1])
        if dotproduct > squaredlengthba:
            return False

        return True
    
    '''This functions calculates the intersection point between 2 line segments represented by 4 points'''
    def lineIntersection(self, line1, line2):
        #line 1 points - A,B | line 2 points - C,D
        #(A.x - B.x) ,   (C.x - D.x)
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        #(A.y - B.y)  ,  (C.y - D.y)
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
        '''Finding the determinant'''
        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]
    
        div = det(xdiff, ydiff)
        if div == 0:
            return False
            #raise Exception('lines do not intersect') # Lines are parallel
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        if self.isBetween(line1[0], line1[1], [x,y]) and self.isBetween(line2[0], line2[1], [x,y]):
                return [(x, y), line1, line2]
        else:
            return False
    
    def addStreet(self, inputList):
        if (inputList[1] in self.streetPointsMap):
            sys.stderr.write('Error: This street already exists. Please use c to change the street')
        else:
            for i in range(2,len(inputList)):
                self.streetPointsMap.setdefault(inputList[1], []).append(inputList[i])
            self.streetId = self.streetId + 1
            self.streetIdMap[inputList[1]] = self.streetId
            
    def changeStreet(self, inputList):
            if (inputList[1] in self.streetPointsMap):
                coordinateList = self.streetPointsMap[inputList[1]]
                del self.streetPointsMap[inputList[1]]
                for coordinate in coordinateList:
                    if (eval(coordinate) in self.vertexCoordinate.keys()):
                        id = self.vertexCoordinate[eval(coordinate)]
                        vertexObj = self.getVertex(id)
                        tobedeleted = self.deleteVertex(id)
                        if vertexObj in tobedeleted.connectedTo:
                            tobedeleted.connectedTo.remove(vertexObj)
                        del self.vertexCoordinate[eval(coordinate)]
                        
                streetIdToDelete = self.streetIdMap[inputList[1]]
                
                intersectionToBeDeleted = 0 #random value
                
                for key in self.intersection:
                    if streetIdToDelete in self.intersection[key]:
                        listOfStreets = self.intersection[key]
                        if len(listOfStreets) == 2:
                            intersectionToBeDeleted = key
                            del self.vertexCoordinate[key]                       
                        elif len(listOfStreets) > 2:
                            self.intersection[key].remove(streetIdToDelete)
                            
                if intersectionToBeDeleted!=0:
                    del self.intersection[intersectionToBeDeleted]       
                self.vertList.clear()
                
                for i in range(2,len(inputList)):
                    self.streetPointsMap.setdefault(inputList[1], []).append(inputList[i]) 
            else:
                sys.stderr.write('Error: This street does not exist. Please add the street before trying to change it')
        
    def removeStreet(self, inputList):
        if (inputList[1] in self.streetPointsMap):
            coordinateList = self.streetPointsMap[inputList[1]]
            del self.streetPointsMap[inputList[1]]
            for coordinate in coordinateList:
                if (eval(coordinate) in self.vertexCoordinate.keys()):
                    id = self.vertexCoordinate[eval(coordinate)]
                    vertexObj = self.getVertex(id)
                    tobedeleted = self.deleteVertex(id)
                    if vertexObj in tobedeleted.connectedTo:
                        tobedeleted.connectedTo.remove(vertexObj)
                    del self.vertexCoordinate[eval(coordinate)]
            
            streetIdToDelete = self.streetIdMap[inputList[1]]
            intersectionToBeDeleted = 0 #random value
            
            for key in self.intersection:
                if streetIdToDelete in self.intersection[key]:
                    listOfStreets = self.intersection[key]
                    if len(listOfStreets) == 2:
                        intersectionToBeDeleted = key
                        del self.vertexCoordinate[key]                       
                    elif len(listOfStreets) > 2:
                        self.intersection[key].remove(streetIdToDelete)
             
            if intersectionToBeDeleted!=0: 
                del self.intersection[intersectionToBeDeleted]  
            self.vertList.clear()        
            del self.streetIdMap[inputList[1]]
            
            if len(self.streetIdMap) == 1:
                self.vertexCoordinate.clear()
                
            
            
        else:
            sys.stderr.write( 'Error: This street does not exist')
        
    def combinations(self,keyList):
        for i, value in enumerate(keyList):
            for j in range(i+1, len(keyList)):
                    yield [value, keyList[j]]

    def displayGraph(self):
        keyList = self.streetPointsMap.keys()
        combinationOfStreets = list(self.combinations(keyList))
        points = []
        
        if len(self.vertexCoordinate) <5:
            self.vertexCoordinate.clear()
            
        
        for namePair in combinationOfStreets:
            street1 = self.streetPointsMap[namePair[0]]
            street2 = self.streetPointsMap[namePair[1]]
            street1Pairs = []
            for x in range(0,len(street1)):
                if((x+1) < len(street1)):
                    street1Pairs.append([eval(street1[x]), eval(street1[x+1])])
                    
            street2Pairs = []
            for y in range(0,len(street2)):
                if((y+1) < len(street2)):
                    street2Pairs.append([eval(street2[y]), eval(street2[y+1])])

            points =[(self.lineIntersection(a,b)) for a in street1Pairs for b in street2Pairs]

            for i in range(0, len(points)):
                if (points[i] != False):
                    
                    if points[i][0] not in self.intersection:
                        self.intersection.setdefault(points[i][0], []).append(self.streetIdMap[namePair[0]])
                        self.intersection.setdefault(points[i][0], []).append(self.streetIdMap[namePair[1]])
                    
                    else:
                        intersectionStreetList = self.intersection[points[i][0]]
                        if  self.streetIdMap[namePair[0]] not in intersectionStreetList:
                            self.intersection.setdefault(points[i][0], []).append(self.streetIdMap[namePair[0]])
                        if  self.streetIdMap[namePair[1]] not in intersectionStreetList:
                            self.intersection.setdefault(points[i][0], []).append(self.streetIdMap[namePair[1]]) 
                            
                        
                    if (points[i][0] not in self.vertexCoordinate.keys()):
                        self.createVertexCoordinate(points[i][0])
                        
                            
                    if (points[i][1][0] not in self.vertexCoordinate.keys()):
                        self.createVertexCoordinate(points[i][1][0])
                    if (points[i][1][1] not in self.vertexCoordinate.keys()):
                        self.createVertexCoordinate(points[i][1][1])
                    if (points[i][2][0] not in self.vertexCoordinate.keys()):
                        self.createVertexCoordinate(points[i][2][0])
                    if (points[i][2][1] not in self.vertexCoordinate.keys()):
                        self.createVertexCoordinate(points[i][2][1])
                    '''adding the vertices'''
                    self.addVertex(self.vertexCoordinate[points[i][0]])
                    self.addVertex(self.vertexCoordinate[points[i][1][0]])
                    self.addVertex(self.vertexCoordinate[points[i][1][1]])
                    self.addVertex(self.vertexCoordinate[points[i][2][0]])
                    self.addVertex(self.vertexCoordinate[points[i][2][1]])
                    '''adding the edges'''
                    for key in self.vertexCoordinate:
                        
                        if(points[i][0]!= key) and (points[i][1][0]!=key):
                            if (self.isBetween(points[i][0], points[i][1][0], key)):
                                if(self.edgdeExists(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][1][0]])==True):
                                    self.deleteEdge(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][1][0]])
                                if (points[i][0]!=key):
                                    if(self.edgdeExists(self.vertexCoordinate[points[i][0]],self.vertexCoordinate[key])!=True):
                                        self.addEdge(self.vertexCoordinate[points[i][0]],self.vertexCoordinate[key])
                                if points[i][1][0] in self.intersection or key in self.intersection:
                                    if(self.edgdeExists(self.vertexCoordinate[key], self.vertexCoordinate[points[i][1][0]])!=True):
                                        self.addEdge(self.vertexCoordinate[key], self.vertexCoordinate[points[i][1][0]])    
                            else:
                                if(self.edgdeExists(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][1][0]])!=True):
                                    self.addEdge(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][1][0]])
                                
                        if(points[i][0]!= key) and (points[i][1][1]!=key):           
                            if(self.isBetween(points[i][0], points[i][1][1], key)):
                                
                                if(self.edgdeExists(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][1][1]])==True):

                                    self.deleteEdge(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][1][1]])
                                if (points[i][0]!=key):
                                    if(self.edgdeExists(self.vertexCoordinate[points[i][0]],self.vertexCoordinate[key])!=True):
                                        self.addEdge(self.vertexCoordinate[points[i][0]],self.vertexCoordinate[key])
                                if points[i][1][1] in self.intersection or key in self.intersection:
                                    if(self.edgdeExists(self.vertexCoordinate[key], self.vertexCoordinate[points[i][1][1]])!=True):
                                        self.addEdge(self.vertexCoordinate[key], self.vertexCoordinate[points[i][1][1]])
                            else:
                                if(self.edgdeExists(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][1][1]])!=True):  
                                    self.addEdge(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][1][1]])
                                
                        if(points[i][0]!= key) and (points[i][2][0]!=key):
                            if(self.isBetween(points[i][0], points[i][2][0], key)):

                                if(self.edgdeExists(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][2][0]])==True):

                                    self.deleteEdge(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][2][0]])
                                if (points[i][0]!=key):
                                    if(self.edgdeExists(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[key])!= True):
                                        self.addEdge(self.vertexCoordinate[points[i][0]],self.vertexCoordinate[key])
                                if points[i][2][0] in self.intersection or key in self.intersection:
                                    if(self.edgdeExists(self.vertexCoordinate[key], self.vertexCoordinate[points[i][2][0]])!= True):
                                        self.addEdge(self.vertexCoordinate[key], self.vertexCoordinate[points[i][2][0]])
                            else:
                                if(self.edgdeExists(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][2][0]])!=True):
                                    self.addEdge(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][2][0]])
                                
                        if(points[i][0]!= key) and (points[i][2][1]!=key):
                            if(self.isBetween(points[i][0], points[i][2][1], key)):

                                if(self.edgdeExists(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][2][1]])==True):

                                    self.deleteEdge(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][2][1]])
                                if (points[i][0]!=key):
                                    if(self.edgdeExists(self.vertexCoordinate[points[i][0]],self.vertexCoordinate[key])!=True):
                                        self.addEdge(self.vertexCoordinate[points[i][0]],self.vertexCoordinate[key])
                                if points[i][2][1] in self.intersection or key in self.intersection:
                                    if(self.edgdeExists(self.vertexCoordinate[key], self.vertexCoordinate[points[i][2][1]] )!=True):
                                        self.addEdge(self.vertexCoordinate[key], self.vertexCoordinate[points[i][2][1]])
                            else:
                                if(self.edgdeExists(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][2][1]])!=True):
                                    self.addEdge(self.vertexCoordinate[points[i][0]], self.vertexCoordinate[points[i][2][1]])

vcg = VertexCoverGraph()
while True:
    try:
        inputList = vcg.readInput()  # input string split according to space delimiter
        lengthOfInput = len(inputList)
        choice = inputList[0]  # this will represent the flags a, c, r, g
        if (choice == 'a') and (lengthOfInput >= 4):  # ensures that at least 2 points are given for a street
            vcg.addStreet(inputList)
        elif (choice == 'c') and (lengthOfInput >= 4):  # ensures that at least 2 points are given for a street
            vcg.changeStreet(inputList)
        elif (choice == 'r') and (lengthOfInput == 2):  # ensures that street name is specified
            vcg.removeStreet(inputList)
        elif (choice == 'g'):
            vcg.displayGraph()
            print "V "
            print len(vcg.vertexCoordinate)
            print "V = {"
            for key in vcg.vertexCoordinate:
                print vcg.vertexCoordinate[key], ":", key
            print "}"
            edgeList = []
            for v in vcg:
                for w in v.getConnections():
                    edgeList.append((v.getId(),w.getId()))
            edgeSet = set(edgeList)
            edgelist = list(edgeSet)
            print "E = {"
            for i in range(len(edgelist)):
                print edgelist[i]
            print "}"
            
        else:
            sys.stderr.write( 'Error:Please choose an option among a,c,r or g with correct number of arguments')
    except EOFError:
        break
        


    
