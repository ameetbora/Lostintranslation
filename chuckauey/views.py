# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.serializers.json import DjangoJSONEncoder
import json as simplejson
from sodapy import Socrata
import ast, datetime, re
from math import sqrt
from pygeocoder import Geocoder
from time import sleep

#from chuckauey import forms
from chuckauey.models import OnstreetParkingBaySensors

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

day_map = {'Sun':0,'Mon':1,'Tue':2,'Wed':3,'Thu':4,'Fri':5,'Sat':6}
nostop_restriction_list = ['Loading Zone 15M','Loading Zone 30M 722','Loading Zone 30M','S/ (No Stopping)','Clearway (Tow away)','P/ (No Parking)','P/ (No Parking) - No Park','Loading Zone 1HR']
paid_park_list = ['1/2P Meter', '1/2P Ticket A', '1P Meter', '1P Ticket A', '2P Meter', '2P Ticket A', '3P Meter', '3P Ticket A', '4P Meter','4P Ticket A']
regex1 = re.compile(".*(Loading Zone).*")
regex2 = re.compile(".*(No Parking).*")
regex3 = re.compile(".*(No Stopping).*")
regex4 = re.compile(".*(Clearway).*")

def restrictioncheck(restriction_dict, day, time):
    responsedict = dict()
    for key in restriction_dict:
        if key == 'restrict1':
            if not restriction_dict[key]['Desc1'] in nostop_restriction_list:
                x = datetime.datetime.strptime(restriction_dict[key]['Start1'],'%H:%M:%S')
                y = datetime.datetime.strptime(restriction_dict[key]['End1'],'%H:%M:%S')
                t = datetime.datetime.strptime(time,'%H:%M:%S')
                if day_map[day]>=int(restriction_dict[key]['From1']) and day_map[day]<=int(restriction_dict[key]['To1']) and x<=t<y:
                    #responsedict.append(ast.literal_eval({'Response':"Yes", 'ParkingTime':int(restriction_dict[key]['Duration1'])/60,'ParkingType':restriction_dict[key]['Desc1']}))
                    responsedict['Response']='Yes'
                    responsedict['ParkingTime']=int(restriction_dict[key]['Duration1'])/60.00
                    if not restriction_dict[key]['Desc1'] in paid_park_list:
                        responsedict['ParkingType']="Free"
                    else:
                        responsedict['ParkingType']="Paid"
                    break;
            else:
                responsedict['Response']="Can't park here"
                if restriction_dict[key]['Desc1'] in [m.group(0) for l in nostop_restriction_list for m in [regex1.search(l)] if m]:
                    responsedict['ParkingType']="Loading Zone"
                elif restriction_dict[key]['Desc1'] in [m.group(0) for l in nostop_restriction_list for m in [regex2.search(l)] if m]:
                    responsedict['ParkingType']="No Parking"
                elif restriction_dict[key]['Desc1'] in [m.group(0) for l in nostop_restriction_list for m in [regex3.search(l)] if m]:
                    responsedict['ParkingType']="No Stopping"
                elif restriction_dict[key]['Desc1'] in [m.group(0) for l in nostop_restriction_list for m in [regex4.search(l)] if m]:
                    responsedict['ParkingType']="Clearway"
                else:
                    responsedict['ParkingType']=""
                break
        elif key == 'restrict2':
            if not restriction_dict[key]['Desc2'] in nostop_restriction_list:
                x = datetime.datetime.strptime(restriction_dict[key]['Start2'],'%H:%M:%S')
                y = datetime.datetime.strptime(restriction_dict[key]['End2'],'%H:%M:%S')
                t = datetime.datetime.strptime(time,'%H:%M:%S')
                if day_map[day]>=int(restriction_dict[key]['From2']) and day_map[day]<=int(restriction_dict[key]['To2']) and x<=t<y:
                    #responsedict.append(ast.literal_eval({'Response': "Yes", 'ParkingTime': int(restriction_dict[key]['Duration2']) / 60,'ParkingType': restriction_dict[key]['Desc2']}))
                    responsedict['Response']='Yes'
                    responsedict['ParkingTime']=int(restriction_dict[key]['Duration2'])/60.00
                    if not restriction_dict[key]['Desc2'] in paid_park_list:
                        responsedict['ParkingType']="Free"
                    else:
                        responsedict['ParkingType']="Paid"
                    break;
            else:
                responsedict['Response']="Can't park here"
                if restriction_dict[key]['Desc2'] in [m.group(0) for l in nostop_restriction_list for m in [regex1.search(l)] if m]:
                    responsedict['ParkingType']="Loading Zone"
                elif restriction_dict[key]['Desc2'] in [m.group(0) for l in nostop_restriction_list for m in [regex2.search(l)] if m]:
                    responsedict['ParkingType']="No Parking"
                elif restriction_dict[key]['Desc2'] in [m.group(0) for l in nostop_restriction_list for m in [regex3.search(l)] if m]:
                    responsedict['ParkingType']="No Stopping"
                elif restriction_dict[key]['Desc2'] in [m.group(0) for l in nostop_restriction_list for m in [regex4.search(l)] if m]:
                    responsedict['ParkingType']="Clearway"
                else:
                    responsedict['ParkingType']=""
                break
        elif key == 'restrict3':
            if not restriction_dict[key]['Desc3'] in nostop_restriction_list:
                x = datetime.datetime.strptime(restriction_dict[key]['Start3'],'%H:%M:%S')
                y = datetime.datetime.strptime(restriction_dict[key]['End3'],'%H:%M:%S')
                t = datetime.datetime.strptime(time,'%H:%M:%S')
                if day_map[day]>=int(restriction_dict[key]['From3']) and day_map[day]<=int(restriction_dict[key]['To3']) and x<=t<y:
                    #responsedict.append(ast.literal_eval({'Response': "Yes", 'ParkingTime': int(restriction_dict[key]['Duration3']) / 60,'ParkingType': restriction_dict[key]['Desc3']}))
                    responsedict['Response']='Yes'
                    responsedict['ParkingTime']=int(restriction_dict[key]['Duration3'])/60.00
                    if not restriction_dict[key]['Desc3'] in paid_park_list:
                        responsedict['ParkingType']="Free"
                    else:
                        responsedict['ParkingType']="Paid"
                    break;
            else:
                responsedict['Response']="Can't park here"
                if restriction_dict[key]['Desc3'] in [m.group(0) for l in nostop_restriction_list for m in [regex1.search(l)] if m]:
                    responsedict['ParkingType']="Loading Zone"
                elif restriction_dict[key]['Desc3'] in [m.group(0) for l in nostop_restriction_list for m in [regex2.search(l)] if m]:
                    responsedict['ParkingType']="No Parking"
                elif restriction_dict[key]['Desc3'] in [m.group(0) for l in nostop_restriction_list for m in [regex3.search(l)] if m]:
                    responsedict['ParkingType']="No Stopping"
                elif restriction_dict[key]['Desc3'] in [m.group(0) for l in nostop_restriction_list for m in [regex4.search(l)] if m]:
                    responsedict['ParkingType']="Clearway"
                else:
                    responsedict['ParkingType']=""
                break
        elif key == 'restrict4':
            if not restriction_dict[key]['Desc4'] in nostop_restriction_list:
                x = datetime.datetime.strptime(restriction_dict[key]['Start4'],'%H:%M:%S')
                y = datetime.datetime.strptime(restriction_dict[key]['End4'],'%H:%M:%S')
                t = datetime.datetime.strptime(time,'%H:%M:%S')
                if day_map[day]>=int(restriction_dict[key]['From4']) and day_map[day]<=int(restriction_dict[key]['To4']) and x<=t<y:
                    #responsedict.append(ast({'Response': "Yes", 'ParkingTime': int(restriction_dict[key]['Duration4']) / 60,'ParkingType': restriction_dict[key]['Desc4']}))
                    responsedict['Response']='Yes'
                    responsedict['ParkingTime']=int(restriction_dict[key]['Duration4'])/60.00
                    if not restriction_dict[key]['Desc4'] in paid_park_list:
                        responsedict['ParkingType']="Free"
                    else:
                        responsedict['ParkingType']="Paid"
                    break;
            else:
                responsedict['Response']="Can't park here"
                if restriction_dict[key]['Desc4'] in [m.group(0) for l in nostop_restriction_list for m in [regex1.search(l)] if m]:
                    responsedict['ParkingType']="Loading Zone"
                elif restriction_dict[key]['Desc4'] in [m.group(0) for l in nostop_restriction_list for m in [regex2.search(l)] if m]:
                    responsedict['ParkingType']="No Parking"
                elif restriction_dict[key]['Desc4'] in [m.group(0) for l in nostop_restriction_list for m in [regex3.search(l)] if m]:
                    responsedict['ParkingType']="No Stopping"
                elif restriction_dict[key]['Desc4'] in [m.group(0) for l in nostop_restriction_list for m in [regex4.search(l)] if m]:
                    responsedict['ParkingType']="Clearway"
                else:
                    responsedict['ParkingType']=""
                break
        elif key == 'restrict5':
            if not restriction_dict[key]['Desc5'] in nostop_restriction_list:
                x = datetime.datetime.strptime(restriction_dict[key]['Start5'],'%H:%M:%S')
                y = datetime.datetime.strptime(restriction_dict[key]['End5'],'%H:%M:%S')
                t = datetime.datetime.strptime(time,'%H:%M:%S')
                if day_map[day]>=int(restriction_dict[key]['From5']) and day_map[day]<=int(restriction_dict[key]['To5']) and x<=t<y:
                    #responsedict.append(ast.literal_eval({'Response': "Yes", 'ParkingTime': int(restriction_dict[key]['Duration1']) / 60,'ParkingType': restriction_dict[key]['Desc1']}))
                    responsedict['Response']='Yes'
                    responsedict['ParkingTime']=int(restriction_dict[key]['Duration5'])/60.00
                    if not restriction_dict[key]['Desc5'] in paid_park_list:
                        responsedict['ParkingType']="Free"
                    else:
                        responsedict['ParkingType']="Paid"
                    break;
            else:
                responsedict['Response']="Can't park here"
                if restriction_dict[key]['Desc5'] in [m.group(0) for l in nostop_restriction_list for m in [regex1.search(l)] if m]:
                    responsedict['ParkingType']="Loading Zone"
                elif restriction_dict[key]['Desc5'] in [m.group(0) for l in nostop_restriction_list for m in [regex2.search(l)] if m]:
                    responsedict['ParkingType']="No Parking"
                elif restriction_dict[key]['Desc5'] in [m.group(0) for l in nostop_restriction_list for m in [regex3.search(l)] if m]:
                    responsedict['ParkingType']="No Stopping"
                elif restriction_dict[key]['Desc5'] in [m.group(0) for l in nostop_restriction_list for m in [regex4.search(l)] if m]:
                    responsedict['ParkingType']="Clearway"
                else:
                    responsedict['ParkingType']=""
                break
        elif key == 'restrict6':
            if not restriction_dict[key]['Desc5'] in nostop_restriction_list:
                x = datetime.datetime.strptime(restriction_dict[key]['Start6'],'%H:%M:%S')
                y = datetime.datetime.strptime(restriction_dict[key]['End6'],'%H:%M:%S')
                t = datetime.datetime.strptime(time,'%H:%M:%S')
                if day_map[day]>=int(restriction_dict[key]['From6']) and day_map[day]<=int(restriction_dict[key]['To6']) and x<=t<y:
                    #responsedict.append(ast.literal_eval({'Response': "Yes", 'ParkingTime': int(restriction_dict[key]['Duration1']) / 60,'ParkingType': restriction_dict[key]['Desc1']}))
                    responsedict['Response']='Yes'
                    responsedict['ParkingTime']=int(restriction_dict[key]['Duration6'])/60.00
                    if not restriction_dict[key]['Desc6'] in paid_park_list:
                        responsedict['ParkingType']="Free"
                    else:
                        responsedict['ParkingType']="Paid"
                    break;
            else:
                responsedict['Response']="Can't park here"
                if restriction_dict[key]['Desc6'] in [m.group(0) for l in nostop_restriction_list for m in [regex1.search(l)] if m]:
                    responsedict['ParkingType']="Loading Zone"
                elif restriction_dict[key]['Desc6'] in [m.group(0) for l in nostop_restriction_list for m in [regex2.search(l)] if m]:
                    responsedict['ParkingType']="No Parking"
                elif restriction_dict[key]['Desc6'] in [m.group(0) for l in nostop_restriction_list for m in [regex3.search(l)] if m]:
                    responsedict['ParkingType']="No Stopping"
                elif restriction_dict[key]['Desc6'] in [m.group(0) for l in nostop_restriction_list for m in [regex4.search(l)] if m]:
                    responsedict['ParkingType']="Clearway"
                else:
                    responsedict['ParkingType']=""
                break
        else:
            responsedict['Response']='No restriction'
            break;
    return responsedict

def fillrestriction(result):
    restriction_dict = dict()
    for item in result:
        #print (item)
        for key in item:
            if key == 'bayid':
                restriction_dict['bayid'] = item['bayid']
                #del result[0][key]
            if key == 'typedesc1' or key == 'starttime1' or key == 'duration1' or key == 'endtime1' or key == 'fromday1' or key == 'today1':
                restriction_dict['restrict1'] = ast.literal_eval("{\'Desc1\':" +"\'"+item['typedesc1']+"\'"+ ",\'Start1\':" +"\'"+item['starttime1']+"\'"+ ",\'End1\':" +"\'"+item['endtime1']+"\'"+ ",\'From1\':" +"\'"+item['fromday1']+"\'"+ ",\'To1\':" +"\'"+item['today1']+"\'"+ ",\'Duration1\':" +"\'"+item['duration1']+"\'"+ "}")
            elif key == 'typedesc2' or key == 'starttime2' or key == 'duration2' or key == 'endtime2' or key == 'fromday2' or key == 'today2':
                restriction_dict['restrict2'] = ast.literal_eval("{\'Desc2\':" +"\'"+item['typedesc2']+"\'"+ ",\'Start2\':" +"\'"+item['starttime2']+"\'"+ ",\'End2\':" +"\'"+item['endtime2']+"\'"+ ",\'From2\':" +"\'"+item['fromday2']+"\'"+ ",\'To2\':" +"\'"+item['today2']+"\'"+ ",\'Duration2\':" +"\'"+item['duration2']+"\'"+ "}")
            elif key == 'typedesc3' or key == 'starttime3' or key == 'duration3' or key == 'endtime3' or key == 'fromday3' or key == 'today3':
                restriction_dict['restrict3'] = ast.literal_eval("{\'Desc3\':" +"\'"+item['typedesc3']+"\'"+ ",\'Start3\':" +"\'"+item['starttime3']+"\'"+ ",\'End3\':" +"\'"+item['endtime3']+"\'"+ ",\'From3\':" +"\'"+item['fromday3']+"\'"+ ",\'To3\':" +"\'"+item['today3']+"\'"+ ",\'Duration3\':" +"\'"+item['duration3']+"\'"+ "}")
            elif key == 'typedesc4' or key == 'starttime4' or key == 'duration4' or key == 'endtime4' or key == 'fromday4' or key == 'today4':
                restriction_dict['restrict4'] = ast.literal_eval("{\'Desc4\':" +"\'"+item['typedesc4']+"\'"+ ",\'Start4\':" +"\'"+item['starttime4']+"\'"+ ",\'End4\':" +"\'"+item['endtime4']+"\'"+ ",\'From4\':" +"\'"+item['fromday4']+"\'"+ ",\'To4\':" +"\'"+item['today4']+"\'"+ ",\'Duration4\':" +"\'"+item['duration4']+"\'"+ "}")
            elif key == 'typedesc5' or key == 'starttime5' or key == 'duration5' or key == 'endtime5' or key == 'fromday5' or key == 'today5':
                restriction_dict['restrict5'] = ast.literal_eval("{\'Desc5\':" +"\'"+item['typedesc5']+"\'"+ ",\'Start5\':" +"\'"+item['starttime5']+"\'"+ ",\'End5\':" +"\'"+item['endtime5']+"\'"+ ",\'From5\':" +"\'"+item['fromday5']+"\'"+ ",\'To5\':" +"\'"+item['today5']+"\'"+ ",\'Duration5\':" +"\'"+item['duration5']+"\'"+ "}")
            elif key == 'typedesc6' or key == 'starttime6' or key == 'duration6' or key == 'endtime6' or key == 'fromday6' or key == 'today6':
                restriction_dict['restrict6'] = ast.literal_eval("{\'Desc6\':" +"\'"+item['typedesc6']+"\'"+ ",\'Start6\':" +"\'"+item['starttime6']+"\'"+ ",\'End6\':" +"\'"+item['endtime6']+"\'"+ ",\'From6\':" +"\'"+item['fromday6']+"\'"+ ",\'To6\':" +"\'"+item['today6']+"\'"+ ",\'Duration6\':" +"\'"+item['duration6']+"\'"+ "}")
            else:
                pass

    return restriction_dict

class CanPark(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    def get(self, request, format=None,*args, **kwargs):
        print ("#######################################START#######################################")

        lat = request.GET.get('lat')
        # print lat
        lon = request.GET.get('lon')
        # usernames = {"lat": lat, "lon": lon}
        # context_dict = {}
        day1 = request.GET.get('day').encode('utf-8').strip()
        #print (day1)
        day = re.sub(r'\W+','',day1)
        day = day.capitalize()
        #print (day)
        time = request.GET.get('time')
        mlist = list()
        responsedict = dict()
        restriction_dict = dict()
        Latt1=-37.877752
        Lont1=145.043742
        #restriction_key = ['starttime6', 'starttime5', 'starttime4', 'starttime3', 'starttime2', 'starttime1', 'today6', 'duration1', 'duration3', 'duration2', 'effectiveonph2', 'duration4', 'effectiveonph1', 'fromday1', 'today3', 'typedesc1', 'typedesc2', 'typedesc3', 'typedesc4', 'today1', 'bayid', 'endtime4', 'endtime5', 'endtime6', 'endtime1', 'endtime2', 'endtime3', 'disabilityext6', 'disabilityext5', 'disabilityext4', 'disabilityext3', 'disabilityext2', 'disabilityext1', 'effectiveonph4', 'fromday2', 'fromday3', 'today5', 'effectiveonph5', 'fromday6', 'today2', 'fromday4', 'fromday5', 'duration5', 'effectiveonph3', 'description6', 'description4', 'description5', 'description2', 'description3', 'description1', 'effectiveonph6', 'duration6', 'typedesc5', 'today4', 'typedesc6', 'deviceid']
        #[u'starttime6', u'starttime5', u'starttime4', u'starttime3', u'starttime2', u'starttime1', u'today6', u'duration1', u'duration3', u'duration2', u'effectiveonph2', u'duration4', u'effectiveonph1', u'fromday1', u'today3', u'typedesc1', u'typedesc2', u'typedesc3', u'typedesc4', u'today1', u'bayid', u'endtime4', u'endtime5', u'endtime6', u'endtime1', u'endtime2', u'endtime3', u'disabilityext6', u'disabilityext5', u'disabilityext4', u'disabilityext3', u'disabilityext2', u'disabilityext1', u'effectiveonph4', u'fromday2', u'fromday3', u'today5', u'effectiveonph5', u'fromday6', u'today2', u'fromday4', u'fromday5', u'duration5', u'effectiveonph3', u'description6', u'description4', u'description5', u'description2', u'description3', u'description1', u'effectiveonph6', u'duration6', u'typedesc5', u'today4', u'typedesc6', u'deviceid']
        try:
            if lat and lon and day and time:
                if sqrt( (Lont1 - float(lon))**2 + (Latt1 - float(lat))**2) < 0.005:
                    responsedict['Response']="Yes"
                    responsedict['ParkingType']="Paid"
                    responsedict['ParkingTime']=2
                    return Response(responsedict)
                #query = """SELECT 1 as id, Bay_id, (3959*acos(cos(radians(%2f))*cos(radians(Lat))*cos(radians(Lon)-radians(%2f))+sin(radians(%2f))*sin(radians(Lat)))) AS distance FROM chuckauey.onstreet_parking_bay_sensors HAVING distance < 1 ORDER BY distance LIMIT 0, 20""" % (float(lat), float(lon), float(lat),)
                query = 'SELECT 1 as id, Bay_id, Location, SQRT( POW(Lon - (%2f), 2) + POW(Lat - (%2f), 2) ) as distance FROM onstreet_parking_bay_sensors HAVING distance < 0.00004 ORDER BY distance LIMIT 0,20'%(float(lon),float(lat))
                signs = OnstreetParkingBaySensors.objects.raw(query)
                print (lat, lon, day, time)
                for sign in signs:
                    print (sign.bay_id, sign.distance, sign.location)
                    mlist.append({u'Bay_id': sign.bay_id, u'distance': sign.distance, u'Location':sign.location})
                print (mlist[0]['Bay_id'])
                client = Socrata("data.melbourne.vic.gov.au", None)
                result = client.get("rzb8-bz3y", bayid=int(mlist[0]['Bay_id']))
                #result = client.get("rzb8-bz3y", bayid=5516)
                #print (result[0])
                restriction_dict = fillrestriction(result)
                print(restriction_dict)
                responsedict=restrictioncheck(restriction_dict,day,time)

            else:
                responsedict['Response']= 'Input parameters missing'
        except Exception as e:
            print (e)
            responsedict['Response']='No parking information found'
        #data = simplejson.dumps(responsedict,cls=DjangoJSONEncoder,ensure_ascii=True)
        #print type(data)
        print (responsedict)
        print ("##################################END#####################################################")
        return Response(responsedict)


class FindPark(APIView):

    def get(self, request, format=None,*args, **kwargs):
        lat = request.GET.get('lat')
        # print lat
        lon = request.GET.get('lon')
        day1 = request.GET.get('day').encode('utf-8').strip()
        #print (day1)
        day = re.sub(r'\W+','',day1)
        day = day.capitalize()
        #print (day)
        time = request.GET.get('time')
        free = request.GET.get('free')
        responsedict = dict()
        restriction_dict = dict()
        try:
            if lat and lon and day and time and free:
                print ('############-------------Start Nearby Parking--------------------------###################')
                print (lat,lon,day,time,free)
                query = 'SELECT 1 as id, Bay_id, Lat, Lon, St_marker_id, (6367*acos(cos(radians(%2f))*cos(radians(Lat))*cos(radians(Lon)-radians(%2f))+sin(radians(%2f))*sin(radians(Lat)))) AS distance FROM onstreet_parking_bay_sensors HAVING distance > 0.05 ORDER BY distance LIMIT 0,50' %(float(lat),float(lon),float(lat))
                signs = OnstreetParkingBaySensors.objects.raw(query)
                client = Socrata("data.melbourne.vic.gov.au", None)
                #print(signs)
                mlist = list()
                mlist_free = list()
                for sign in signs:
                    temp = dict()
                    #print(sign.bay_id, sign.distance, sign.lat, sign.lon)
                    temp['Bay_ID']=int(sign.bay_id)
                    temp['Distance']=sign.distance
                    temp['Lat']=sign.lat
                    temp['Lon']=sign.lon
                    temp['Marker_ID'] = sign.st_marker_id
                    find_status = client.get("vh2v-4nfs", bay_id=sign.bay_id)
                    #print (find_status)
                    if find_status:
                        if find_status[0]['status'] == "Unoccupied":
                            temp['Status'] = find_status[0]['status']
                        else:
                            continue
                    else:
                        continue
                    result = client.get("rzb8-bz3y", bayid=temp['Bay_ID'])
                    #print (result)
                    if result:
                        restriction_dict = fillrestriction(result)
                        #print(restriction_dict)
                        res=restrictioncheck(restriction_dict,day,time)
                        #print(res)
                    else:
                        continue
                    street = client.get("wuf8-susg",marker_id=str(temp['Marker_ID']))
                    if street:
                        temp['Street'] = str(street[0]['rd_seg_dsc'])
                    else:
                        temp['Street'] = 'Unknown Street'
                    temp.update(res)

                    temp.pop('Bay_ID', None)
                    temp.pop('Marker_ID', None)
                    print(temp)
                    if temp['Response'] == 'Yes' or temp['Response'] == 'No restriction':
                        if 'ParkingType' in temp:
                            if temp['ParkingType'] == 'Free':
                                mlist_free.append(temp)
                                mlist.append(temp)
                            else:
                                mlist.append(temp)
                        else:
                            mlist_free.append(temp)
                            mlist.append(temp)
                        #print (mlist)
                    else:
                        continue

                print(mlist)
                print(mlist_free)
                if free == 'yes':
                    if len(mlist_free)>0 and len(mlist_free) < 5:
                        return Response(mlist_free)
                    elif len(mlist_free) > 5:
                        return Response(mlist_free[0:5])
                    else:
                        responsedict['Response']='No Nearby Free parking available'
                        return Response(responsedict)
                else:
                    if len(mlist) < 5:
                        return Response(mlist)
                    else:
                        return Response(mlist[0:5])

            else:
                responsedict['Response']= 'Input parameters missing'
                return Response(responsedict)
        except Exception as e:
            print(e)
            responsedict['Response']='No Nearby parking available'
            return Response(responsedict)

