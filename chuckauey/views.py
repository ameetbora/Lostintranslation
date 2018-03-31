# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.serializers.json import DjangoJSONEncoder
import json as simplejson
from sodapy import Socrata
import ast, datetime

from chuckauey import forms
from chuckauey.models import OnstreetParkingBaySensors

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    def get(self, request, format=None,*args, **kwargs):
        """
        Return a list of all users.
        """
        day_map = {'Sun':0,'Mon':1,'Tue':2,'Wed':3,'Thu':4,'Fri':5,'Sat':6}
        lat = request.GET.get('lat')
        # print lat
        lon = request.GET.get('lon')
        # usernames = {"lat": lat, "lon": lon}
        # context_dict = {}
        day = request.GET.get('day')
        time = request.GET.get('time')
        mlist = list()
        responsedict = dict()
        restriction_dict = dict()
        restriction_key = ['starttime6', 'starttime5', 'starttime4', 'starttime3', 'starttime2', 'starttime1', 'today6', 'duration1', 'duration3', 'duration2', 'effectiveonph2', 'duration4', 'effectiveonph1', 'fromday1', 'today3', 'typedesc1', 'typedesc2', 'typedesc3', 'typedesc4', 'today1', 'bayid', 'endtime4', 'endtime5', 'endtime6', 'endtime1', 'endtime2', 'endtime3', 'disabilityext6', 'disabilityext5', 'disabilityext4', 'disabilityext3', 'disabilityext2', 'disabilityext1', 'effectiveonph4', 'fromday2', 'fromday3', 'today5', 'effectiveonph5', 'fromday6', 'today2', 'fromday4', 'fromday5', 'duration5', 'effectiveonph3', 'description6', 'description4', 'description5', 'description2', 'description3', 'description1', 'effectiveonph6', 'duration6', 'typedesc5', 'today4', 'typedesc6', 'deviceid']
        #[u'starttime6', u'starttime5', u'starttime4', u'starttime3', u'starttime2', u'starttime1', u'today6', u'duration1', u'duration3', u'duration2', u'effectiveonph2', u'duration4', u'effectiveonph1', u'fromday1', u'today3', u'typedesc1', u'typedesc2', u'typedesc3', u'typedesc4', u'today1', u'bayid', u'endtime4', u'endtime5', u'endtime6', u'endtime1', u'endtime2', u'endtime3', u'disabilityext6', u'disabilityext5', u'disabilityext4', u'disabilityext3', u'disabilityext2', u'disabilityext1', u'effectiveonph4', u'fromday2', u'fromday3', u'today5', u'effectiveonph5', u'fromday6', u'today2', u'fromday4', u'fromday5', u'duration5', u'effectiveonph3', u'description6', u'description4', u'description5', u'description2', u'description3', u'description1', u'effectiveonph6', u'duration6', u'typedesc5', u'today4', u'typedesc6', u'deviceid']
        try:
            if lat and lon and day and time:
                #query = """SELECT 1 as id, Bay_id, (3959*acos(cos(radians(%2f))*cos(radians(Lat))*cos(radians(Lon)-radians(%2f))+sin(radians(%2f))*sin(radians(Lat)))) AS distance FROM chuckauey.onstreet_parking_bay_sensors HAVING distance < 1 ORDER BY distance LIMIT 0, 20""" % (float(lat), float(lon), float(lat),)
                query = 'SELECT 1 as id, Bay_id, Location, SQRT( POW(Lon - (%2f), 2) + POW(Lat - (%2f), 2) ) as distance FROM chuckauey.onstreet_parking_bay_sensors HAVING distance < 0.00004 ORDER BY distance LIMIT 0,20'%(float(lon),float(lat))
                signs = OnstreetParkingBaySensors.objects.raw(query)
                for sign in signs:
                    #print sign.bay_id, sign.distance, sign.location
                    mlist.append({u'Bay_id': sign.bay_id, u'distance': sign.distance, u'Location':sign.location})
                #print mlist[0]['Bay_id']
                client = Socrata("data.melbourne.vic.gov.au", None)
                result = client.get("rzb8-bz3y", bayid=int(mlist[0]['Bay_id']))
                #print result[0]
                for key in result[0]:
                    if key == 'bayid':
                        restriction_dict['bayid'] = result[0]['bayid']
                    #del result[0][key]
                    elif key == 'typedesc1' or key == 'starttime1' or key == 'duration1' or key == 'endtime1' or key == 'fromday1' or key == 'today1':
                        restriction_dict['restrict1'] = ast.literal_eval("{\'Desc1\':" +"\'"+result[0]['typedesc1']+"\'"+ ",\'Start1\':" +"\'"+result[0]['starttime1']+"\'"+ ",\'End1\':" +"\'"+result[0]['endtime1']+"\'"+ ",\'From1\':" +"\'"+result[0]['fromday1']+"\'"+ ",\'To1\':" +"\'"+result[0]['today1']+"\'"+ ",\'Duration1\':" +"\'"+result[0]['duration1']+"\'"+ "}")
                    elif key == 'typedesc2' or key == 'starttime2' or key == 'duration2' or key == 'endtime2' or key == 'fromday2' or key == 'today2':
                        restriction_dict['restrict2'] = ast.literal_eval("{\'Desc2\':" +"\'"+result[0]['typedesc2']+"\'"+ ",\'Start2\':" +"\'"+result[0]['starttime2']+"\'"+ ",\'End2\':" +"\'"+result[0]['endtime2']+"\'"+ ",\'From2\':" +"\'"+result[0]['fromday2']+"\'"+ ",\'To2\':" +"\'"+result[0]['today2']+"\'"+ ",\'Duration2\':" +"\'"+result[0]['duration2']+"\'"+ "}")
                    elif key == 'typedesc3' or key == 'starttime3' or key == 'duration3' or key == 'endtime3' or key == 'fromday3' or key == 'today3':
                        restriction_dict['restrict3'] = ast.literal_eval("{\'Desc3\':" +"\'"+result[0]['typedesc3']+"\'"+ ",\'Start3\':" +"\'"+result[0]['starttime3']+"\'"+ ",\'End3\':" +"\'"+result[0]['endtime3']+"\'"+ ",\'From3\':" +"\'"+result[0]['fromday3']+"\'"+ ",\'To3\':" +"\'"+result[0]['today3']+"\'"+ ",\'Duration3\':" +"\'"+result[0]['duration3']+"\'"+ "}")
                    elif key == 'typedesc4' or key == 'starttime4' or key == 'duration4' or key == 'endtime4' or key == 'fromday4' or key == 'today4':
                        restriction_dict['restrict4'] = ast.literal_eval("{\'Desc4\':" +"\'"+result[0]['typedesc4']+"\'"+ ",\'Start4\':" +"\'"+result[0]['starttime4']+"\'"+ ",\'End4\':" +"\'"+result[0]['endtime4']+"\'"+ ",\'From4\':" +"\'"+result[0]['fromday4']+"\'"+ ",\'To4\':" +"\'"+result[0]['today4']+"\'"+ ",\'Duration4\':" +"\'"+result[0]['duration4']+"\'"+ "}")
                    elif key == 'typedesc5' or key == 'starttime5' or key == 'duration5' or key == 'endtime5' or key == 'fromday5' or key == 'today5':
                        restriction_dict['restrict5'] = ast.literal_eval("{\'Desc5\':" +"\'"+result[0]['typedesc5']+"\'"+ ",\'Start5\':" +"\'"+result[0]['starttime5']+"\'"+ ",\'End5\':" +"\'"+result[0]['endtime5']+"\'"+ ",\'From5\':" +"\'"+result[0]['fromday5']+"\'"+ ",\'To5\':" +"\'"+result[0]['today5']+"\'"+ ",\'Duration5\':" +"\'"+result[0]['duration5']+"\'"+ "}")
                    elif key == 'typedesc6' or key == 'starttime6' or key == 'duration6' or key == 'endtime6' or key == 'fromday6' or key == 'today6':
                        restriction_dict['restrict6'] = ast.literal_eval("{\'Desc6\':" +"\'"+result[0]['typedesc6']+"\'"+ ",\'Start6\':" +"\'"+result[0]['starttime6']+"\'"+ ",\'End6\':" +"\'"+result[0]['endtime6']+"\'"+ ",\'From6\':" +"\'"+result[0]['fromday6']+"\'"+ ",\'To6\':" +"\'"+result[0]['today6']+"\'"+ ",\'Duration6\':" +"\'"+result[0]['duration6']+"\'"+ "}")
                    else:
                        pass

                for key in restriction_dict:
                    if key == 'restrict1':
                        x = datetime.datetime.strptime(restriction_dict[key]['Start1'],'%H:%M:%S')
                        y = datetime.datetime.strptime(restriction_dict[key]['End1'],'%H:%M:%S')
                        t = datetime.datetime.strptime(time,'%H:%M:%S')
                        if day_map[day]>=int(restriction_dict[key]['From1']) and day_map[day]<=int(restriction_dict[key]['To1']) and x<=t<=y:
                            #responsedict.append(ast.literal_eval({'Response':"Yes", 'ParkingTime':int(restriction_dict[key]['Duration1'])/60,'ParkingType':restriction_dict[key]['Desc1']}))
                            responsedict['Response']='Yes'
                            responsedict['ParkingTime']=int(restriction_dict[key]['Duration1'])/60
                            responsedict['ParkingType']=restriction_dict[key]['Desc1']
                            break;
                    elif key == 'restrict2':
                        x = datetime.datetime.strptime(restriction_dict[key]['Start2'],'%H:%M:%S')
                        y = datetime.datetime.strptime(restriction_dict[key]['End2'],'%H:%M:%S')
                        t = datetime.datetime.strptime(time,'%H:%M:%S')
                        if day_map[day]>=int(restriction_dict[key]['From2']) and day_map[day]<=int(restriction_dict[key]['To2']) and x<=t<=y:
                            #responsedict.append(ast.literal_eval({'Response': "Yes", 'ParkingTime': int(restriction_dict[key]['Duration2']) / 60,'ParkingType': restriction_dict[key]['Desc2']}))
                            responsedict['Response']='Yes'
                            responsedict['ParkingTime']=int(restriction_dict[key]['Duration2'])/60
                            responsedict['ParkingType']=restriction_dict[key]['Desc2']
                            break;
                    elif key == 'restrict3':
                        x = datetime.datetime.strptime(restriction_dict[key]['Start3'],'%H:%M:%S')
                        y = datetime.datetime.strptime(restriction_dict[key]['End3'],'%H:%M:%S')
                        t = datetime.datetime.strptime(time,'%H:%M:%S')
                        if day_map[day]>=int(restriction_dict[key]['From3']) and day_map[day]<=int(restriction_dict[key]['To3']) and x<=t<=y:
                            #responsedict.append(ast.literal_eval({'Response': "Yes", 'ParkingTime': int(restriction_dict[key]['Duration3']) / 60,'ParkingType': restriction_dict[key]['Desc3']}))
                            responsedict['Response']='Yes'
                            responsedict['ParkingTime']=int(restriction_dict[key]['Duration3'])/60
                            responsedict['ParkingType']=restriction_dict[key]['Desc3']
                            break;
                    elif key == 'restrict4':
                        x = datetime.datetime.strptime(restriction_dict[key]['Start4'],'%H:%M:%S')
                        y = datetime.datetime.strptime(restriction_dict[key]['End4'],'%H:%M:%S')
                        t = datetime.datetime.strptime(time,'%H:%M:%S')
                        if day_map[day]>=int(restriction_dict[key]['From4']) and day_map[day]<=int(restriction_dict[key]['To4']) and x<=t<=y:
                            #responsedict.append(ast({'Response': "Yes", 'ParkingTime': int(restriction_dict[key]['Duration4']) / 60,'ParkingType': restriction_dict[key]['Desc4']}))
                            responsedict['Response']='Yes'
                            responsedict['ParkingTime']=int(restriction_dict[key]['Duration4'])/60
                            responsedict['ParkingType']=restriction_dict[key]['Desc4']
                            break;
                    elif key == 'restrict5':
                        x = datetime.datetime.strptime(restriction_dict[key]['Start5'],'%H:%M:%S')
                        y = datetime.datetime.strptime(restriction_dict[key]['End5'],'%H:%M:%S')
                        t = datetime.datetime.strptime(time,'%H:%M:%S')
                        if day_map[day]>=int(restriction_dict[key]['From5']) and day_map[day]<=int(restriction_dict[key]['To5']) and x<=t<=y:
                            #responsedict.append(ast.literal_eval({'Response': "Yes", 'ParkingTime': int(restriction_dict[key]['Duration1']) / 60,'ParkingType': restriction_dict[key]['Desc1']}))
                            responsedict['Response']='Yes'
                            responsedict['ParkingTime']=int(restriction_dict[key]['Duration5'])/60
                            responsedict['ParkingType']=restriction_dict[key]['Desc5']
                            break;
                    elif key == 'restrict6':
                        x = datetime.datetime.strptime(restriction_dict[key]['Start6'],'%H:%M:%S')
                        y = datetime.datetime.strptime(restriction_dict[key]['End6'],'%H:%M:%S')
                        t = datetime.datetime.strptime(time,'%H:%M:%S')
                        if day_map[day]>=int(restriction_dict[key]['From6']) and day_map[day]<=int(restriction_dict[key]['To6']) and x<=t<=y:
                            #responsedict.append(ast.literal_eval({'Response': "Yes", 'ParkingTime': int(restriction_dict[key]['Duration1']) / 60,'ParkingType': restriction_dict[key]['Desc1']}))
                            responsedict['Response']='Yes'
                            responsedict['ParkingTime']=int(restriction_dict[key]['Duration6'])/60
                            responsedict['ParkingType']=restriction_dict[key]['Desc6']
                            break;
                    else:
                        responsedict['Response']='No restriction'
                        break;
                else:
                    responsedict['Response']= 'Input parameters missing'
        except Exception as e:
            print e
            responsedict['Response']='No parking information found'
        #data = simplejson.dumps(responsedict,cls=DjangoJSONEncoder,ensure_ascii=True)
        #print type(data)
        return Response(responsedict)
