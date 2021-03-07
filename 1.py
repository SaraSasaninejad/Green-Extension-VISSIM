import math
import ast
from math import e
from decimal import *
getcontext().prec = 28


def toList(NestedTuple):
    return list(map(toList, NestedTuple)) if isinstance(NestedTuple, (list, tuple)) else NestedTuple


def Init():
    global FreightVehicles
    global vehsAttributes
    global vehsAttNames
    
    vehsAttributes = []
    vehsAttNames = []
    vehTypesAttributes = Vissim.Net.VehicleTypes.GetMultipleAttributes(['No', 'IsFreight'])
    FreightVehicles = [x[0] for x in vehTypesAttributes if x[1] == True]
    


def GetVissimDataVehicles():
    global vehsAttributes
    global vehsAttNames
    vehsAttributesNames = ['No', 'VehType\No','Lane\Link', 'Speed','DistanceToSigHead']
    vehsAttributes = toList(Vissim.Net.Vehicles.GetMultipleAttributes(vehsAttributesNames))
    vehsAttNames = {}
    cnt = 0
    for att in vehsAttributesNames:
        vehsAttNames.update({att: cnt})
        cnt += 1



def Signal():
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('Seconds',Vissim.Net.Simulation.SimulationSecond)
    Seconds = Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('Seconds')
    GetVissimDataVehicles()


    if Seconds<=1:
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('teg',10.5)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('ContrByCOM',True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('ContrByCOM',True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('GreenTimeDuration',31+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('teg'))
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('GreenTimeDuration',11)        
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('GreenStart',4)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenTimeDuration'))
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenEnd')+4)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue ('GreenTimeDuration'))



    for vehAttributes in vehsAttributes:
        if vehAttributes[vehsAttNames['VehType\No']] in FreightVehicles:
            Lane = vehAttributes[vehsAttNames['Lane\Link']]
            if Lane  == '1' or Lane  == '4':
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('teg',10.5)
                                                                               
                break
            if Lane  != '1' or Lane  != '4':
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('teg',0)
                continue
        if vehAttributes[vehsAttNames['VehType\No']] not in FreightVehicles:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('teg',0)
            continue


    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('GreenTimeDuration',31+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('teg'))
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('GreenTimeDuration',11)        
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenTimeDuration'))
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenEnd')+4)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue ('GreenTimeDuration'))







    if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenStart')-1:
        if Seconds <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenEnd')-1:               
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('SigState','GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('SigState','RED')
        if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenEnd')-1:
            if Seconds < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenEnd')+3:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('SigState','RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('SigState','RED')



    if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue ('GreenStart')-1:
        if Seconds <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue ('GreenEnd')-1:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('SigState','GREEN')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('SigState','RED')      
        if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue ('GreenEnd')-1:
            if Seconds < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue ('GreenEnd')+3:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('SigState','RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('SigState','RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('GreenStart',4+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue ('GreenEnd'))
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenTimeDuration'))
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue ('GreenEnd')+4)
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue ('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue ('GreenStart')+Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue ('GreenTimeDuration'))



