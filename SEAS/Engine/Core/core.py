from SEAS.Engine.Scene.scene import *

from SEAS.Engine.Core.event import *
from SEAS.Engine.Core.screen import *
from SEAS.Engine.Core.filePreset import *
from SEAS.Engine.Core.input import *
from SEAS.Engine.Core.font import *


from typing import Any


class GameCore:
    def __init__(self) -> None:
        self.scenes = {}
        self.targetedScene = None

        self.materials = {}
        self.coreModules = {'Event': Event(), 'Input': Input(),'Screen': Screen(), 'Font': Font()}
        self.hitboxGroup = {}

        self.inputStateDefault = 'Up'

        self.printed1 = 0
        self.printed2 = 0

        self.deltaTime = 0
        self.time1 = 0
        self.time2 = 0

        self.loggingLevel = 'Comment'


    def startCoreModules(self) -> None:
        for mod in self.coreModules:
            self.coreModules[mod].start()

    def startCoreObjects(self) -> None: #The scenes work. Only will run when we hit run() or when a new scene is created
        try:
            self.targetedScene.startObjects()
        except AttributeError as err:
            print("DISCLAMER: This could be because you have not created a scene yet. Pls proceed and check that thats intact!")
            print("\n\n\n\n")
            raise err

    def updateCore(self) -> None:
        self.time1 = time.time()

        # bef
        for module in self.coreModules:
            self.coreModules[module].updateBefore()

        try:
            self.targetedScene.updateScene()
        except AttributeError as err:
            print("DISCLAMER: This could be because you have not created a scene yet. Pls proceed and check that thats intact!")
            print("\n####################\n####################\n####################\n####################\n")
            raise err
        
        pygame.display.update()

        self.time2 = time.time()
        self.deltaTime = self.time2 - self.time1

    def getCoreModule(self, coreModName:str=''):
        if coreModName == '':
            print('SEAS CORE::getCoreModule(): ERROR: U need to specify a coreModName')
        
        try:
            return self.coreModules[coreModName]
        except:
            # Doesnt need to check any loggingLevel
            print('SEAS CORE::getCoreModule(): ERROR: Not a valid coreModuleName')


    def createFilePreset(self, fileName:str) -> None: # This is only experimental
        with open('SEAS/Engine/Core/filePreset.py', 'r') as f:
            filePreset = f.read()
            # Returns the index that 'n' is on
            indexN = filePreset.find('name')
            
            filePreset2 = filePreset[:indexN] + fileName + filePreset[indexN+4:]

        with open(fileName + '.py', 'w+') as f:
            f.write(filePreset2)

    def addScene(self, name:str, frameLimit:int=60, isTargeted:bool=True, overflowObj:str='') -> Any:
        self.scenes[name] = Scene(frameLimit, self.getCoreModule('Screen').wn)

        if isTargeted:
            self.targetedScene = self.scenes[name]

        return self.scenes[name]


    def targetScene(self, sceneName:str) -> None:
        if self.scenes[sceneName] != self.targetScene:
            sceneBef = self.targetedScene
            self.targetedScene = self.scenes[sceneName]
            self.startCoreModules()
            self.targetedScene.currentObj = sceneBef.currentObj

    def getScene(self) -> Any:
        return self.targetedScene

    def getRawScene(self, sceneName:str) -> Any:
        return self.scenes[sceneName]

    def getAllScene(self) -> Any:
        return self.scenes

    def transferObject(self, objectName:str, sceneName:str, resetObject:bool=False) -> None:
        if not (objectName in self.scenes[sceneName].objects):
            self.scenes[sceneName].objects[objectName] = self.targetedScene.objects[objectName]
            
            if resetObject:
                self.scenes[sceneName].objects[objectName].start()
                # TODO: Move object to start positions

    def transferRawObject(self, objectName:str, fromScene:str, toScene:str, resetObject:bool=False) -> None:
        self.scenes[toScene].objects[objectName] = self.scenes[fromScene].objects[objectName]

        if resetObject:
            self.scenes[toScene].objects[objectName].start()
            # TODO: Move object to start positions
    
    def transferAllObject(self, sceneName:str):
        print("transferAllObject() function not implemented yet coming soon sry")

    def transferRawAllObject(self, fromScene:str, toScene:str):
        print("transferRawAllObject() function not implemented yet coming soon sry")


    def createMaterial(self, materialName:str, materialColor:str) -> None: # Color will be hexadecimal
        self.materials[materialName] = materialColor

    def addMaterial(self, materialName:str, objectName:str) -> None:
        material = self.materials[materialName]
        object = self.getScene().objects[objectName]

        object.material = material

    def getMaterial(self) -> str: # This is the material that the current obj has
        return self.getScene().currentObj.material

    def getRawMaterial(self, materialName):
        return self.materials[materialName]

    def getObjectMaterial(self, objectName):
        return self.targetScene.objects[object].material

    def input(self, key:str) -> bool:
        indexAttr = getattr(pygame, 'K_' + key)
        if self.coreModules['Input'].keys[indexAttr]:
            return True
        return False

    def event(self, eventType:str, eventEquals:str) -> bool:
        for event in self.coreModules['Event'].events: # Loop thru events list
            attr = getattr(event, eventType)
            equals = getattr(pygame, eventEquals)

            if attr == equals:
                return True

        return False

    def createHitboxGroup(self, groupName, state=False):
        self.hitboxGroup[groupName] = [[], state]

    def addRawNameHitboxGroup(self, groupName:str, objects:list=[]): # Call this only in a component
        for obj in objects:
            # oAdd.append(self.getScene().objects[obj])
            self.hitboxGroup[groupName][0].append(self.getScene().objects[obj])

        # self.hitboxGroup[groupName][0] = oAdd

    def addRawInitHitboxGroup(self, groupName:str, objects:list=[]): # Call this only in a component
        for obj in objects:
            self.hitboxGroup[groupName][0].append(obj)

    def toggleHitboxGroup(self, groupName:str):
        if self.hitboxGroup[groupName][1] == False:
            self.hitboxGroup[groupName][1] = True
        else:
            self.hitboxGroup[groupName][1] = False

    def getHitboxGroupState(self, groupName:str):
        try:
            return self.hitboxGroup[groupName][1]
        except:
            return False

    def getObjectNameHitboxGroup(self, objectName:str):
        for g in self.hitboxGroup:
            if objectName in self.hitboxGroup[g][0]:
                return g

    def getObjectInitHitboxGroup(self, objectInit:str):
        for g in self.hitboxGroup:
            if objectInit in self.hitboxGroup[g][0]:
                return g

    def sameNameHitboxGroup(self, objectNames:list) -> bool:
        # We need to match one with the other 
        objGroup = []
        for obj in objectNames:
            objH = []
            for h in self.hitboxGroup:
                if self.getScene().objects[obj] in self.hitboxGroup[h][0]:
                    objH.append(h)
            objGroup.append(objH)
        
        for obj1 in objGroup:
            for obj2 in objGroup:
                for i in obj1:
                    for j in obj2:
                        if obj1 != obj2:
                            if i == j:
                                return True
    def sameInitHitboxGroup(self, objectInits:list) -> bool:
        # We need to match one with the other 
        objGroup = []
        for obj in objectInits:
            objH = []
            for h in self.hitboxGroup:
                if obj in self.hitboxGroup[h][0]:
                    objH.append(h)
            objGroup.append(objH)
        
        for obj1 in objGroup:
            for obj2 in objGroup:
                for i in obj1:
                    for j in obj2:
                        if obj1 != obj2:
                            if i == j:
                                return True

    def same(self, iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == x for x in iterator)

    
SEAS = GameCore()
