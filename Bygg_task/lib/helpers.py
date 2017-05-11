# -*- coding: utf-8 -*-
import xmlrpclib
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from geopy.distance import great_circle
from math import sqrt
import math


import simplejson,urllib



class Helpers(object):

    url = None
    db = None
    uid = None
    password = None
    common = None

    def __init__(self,url,db,uid,password):
        self.url = url
        self.db = db
        self.uid = uid
        self.password = password
        self.common = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(self.url))


    def check_access_rights(self,model_name):

        return self.common.execute_kw(self.db, self.uid, self.password,
                                     model_name, 'check_access_rights',
                                     ['read'], {'raise_exception': False})


    def api_search_read(self,model_name,list_values,field_names):

        return self.common.execute_kw(self.db, self.uid, self.password,
                              model_name, 'search_read',
                              [list_values],
                              {'fields':field_names})

    def api_read(self,model_name,list_values,field_names):

        return self.common.execute_kw(self.db, self.uid, self.password,
                              model_name, 'read',
                              [list_values],
                              {'fields':field_names})

    def api_update(self,model_name,id,updated_dict):

        return self.common.execute_kw(self.db, self.uid, self.password, model_name, 'write', [[id],
                                                                             updated_dict])

    def api_workflow(self,model_name,id):
        print model_name
        print id

        return self.common.exec_workflow(self.db,self.uid,self.password,model_name,'action_confirm',int(id))

    def api_workflow_assign(self,model_name,id):
        print model_name
        print id
        return self.common.exec_workflow(self.db,self.uid,self.password,model_name,'action_assign',int(id))

    def api_workflow_accept(self,model_name,id):
        print model_name
        print id

        return self.common.exec_workflow(self.db,self.uid,self.password,model_name,'action_accept',int(id))

    def api_workflow_done(self,model_name,id):
        print model_name
        print id

        return self.common.exec_workflow(self.db,self.uid,self.password,model_name,'action_done',int(id))

    def api_workflow_cancel(self,model_name,id):
        print model_name
        print id

        return self.common.exec_workflow(self.db,self.uid,self.password,model_name,'action_cancel',int(id))

    def api_workflow_reject(self,model_name,id):
        print model_name
        print id

        return self.common.exec_workflow(self.db,self.uid,self.password,model_name,'action_reject',int(id))

    def api_workflow_fail(self,model_name,id):
        print model_name
        print id

        return self.common.exec_workflow(self.db,self.uid,self.password,model_name,'action_fail',int(id))

    def api_workflow_draft(self,model_name,id):
        print model_name
        print id

        return self.common.exec_workflow(self.db,self.uid,self.password,model_name,'action_draft',int(id))

    def api_check_assigned_user(self,model_name,id):
        return self.common.execute_kw(self.db, self.uid, self.password,model_name, 'read',[id],{'fields':['assigned_id']})

    def assign_user(self,model_name,id,assign_id):
        return self.common.execute_kw(self.db, self.uid, self.password, model_name, 'write', [[id],{'assigned_id':assign_id}])

    def location_details(self,model_name,partner_id,fields_to_get):
        data=self.common.execute_kw(self.db, self.uid, self.password,model_name, 'read',[partner_id],{'fields':fields_to_get})
        print("data is %s"%data)
        return data

    def get_location_data(self,source,destination):
        dest=destination
        geolocator = Nominatim()
        source_location=geolocator.geocode(source)
        destination_location=geolocator.geocode(dest)
        url1="https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=%s,%s&destinations=%s,%s&mode=driving&key=AIzaSyCclj60d0LRbAy9u0GWVRYdCt7LouYZlvE"%(source_location.latitude,source_location.longitude,destination_location.latitude,destination_location.longitude)
        result= simplejson.load(urllib.urlopen(url1))
        driving_time = result['rows'][0]['elements'][0]['duration']['text']
        distance=result['rows'][0]['elements'][0]['distance']['text']
        datalist=[]
        datalist.append(driving_time)
        datalist.append(distance)
        return datalist

    def partner_name_details(self,model_name,partner_id,fields_to_get):
        data = self.common.execute_kw(self.db, self.uid, self.password, model_name, 'write', [[partner_id], {'city':fields_to_get}])
        print("data is %s" % data)
        return data
    def partner_all(self,model_name):
        return self.common.execute_kw(self.db, self.uid, self.password,model_name, 'search_read',[[ ['customer', '=', True]]],
    {'fields': ['name', 'country_id', 'comment'], 'limit': 5})










