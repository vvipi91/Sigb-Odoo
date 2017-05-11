# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import request
from flask import json
from lib.Login import RestLogin
from lib.helpers import Helpers
import re
from geopy.geocoders import Nominatim
import geocoder


app = Flask(__name__)

@app.route('/api/v1/login',methods=['POST'])
def do_login():

    if(request.data):
        data_list =  json.loads(request.data)
        print data_list
        db = data_list['params']['db']
        url = data_list['params']['url']
        username = data_list['params']['username']
        password = data_list['params']['password']

        login = RestLogin(db,url,username,password)
        user_id = login.authenticate_user()
        print user_id
        if (user_id and user_id != 'None'):
            response = {'status': 'success', 'uid': user_id, 'msg': 'Logged in successfully'}
        else:
            response = {'status': 'error', 'msg': 'Login Failed'}
    print(response)
    return jsonify(response)

# Services for Byggtrd Starts here =====================>
# ==============================>Api Call Created By Vipin<======================================================
# get project list ==>
@app.route('/api/v1/projects',methods=['POST'])
def get_project():
    print "entered into project listing"
    modelName= "project.project"
    fields =['name']
    if request.data:
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        api_class = Helpers(request_dict['url'], request_dict['db'], int(request_dict['uid']), request_dict['password'])
        check_access = api_class.check_access_rights(modelName)

        checksum = [['user_id', '=', int(request_dict['uid'])]]
        if (check_access):
            get_all_tasks = api_class.api_search_read(modelName,checksum, fields)
            if (get_all_tasks):
                response = get_all_tasks
            else:
                response = {'status': 'error', 'msg': 'No Tasks Found'}
    return jsonify(response)

# get project Task list ==>
@app.route('/api/v1/project_tasks',methods=['POST'])
def get_project_task():
    print "entered into project listing"
    modelName= "project.task"
    fields =['name','project_id','user_id','planned_hours','material_ids','description','stage_id']
    if request.data:
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        api_class = Helpers(request_dict['url'], request_dict['db'], int(request_dict['uid']), request_dict['password'])
        check_access = api_class.check_access_rights(modelName)
        if 'project_id' in request_dict:
            checksum = [['project_id', '=', int(request_dict['project_id'])]]
        else:
            checksum = []
        if (check_access):
            get_all_tasks = api_class.api_search_read(modelName,checksum, fields)
            if (get_all_tasks):
                for all in get_all_tasks:
                    test=all['description']
                    plain_text= re.sub(r'<.*?>', '', test)
                    all['description'] = plain_text
                response = get_all_tasks
            else:
                response = {'status': 'error', 'msg': 'No Tasks Found'}
    return jsonify(response)

# # get project Tasks Details (Materials Details)==>

@app.route('/api/v1/task_details',methods=['POST'])
def get_tasks_det():
    #api defaults
    modelName = "project.materials"
    fields_toget = ['product_id','to_use','used']

    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        print "data is %s"%request_dict
        checksum = [['task_id', '=', int(request_dict['task_id'])]]
        api_class = Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
        check_access = api_class.check_access_rights(modelName)
        if(check_access):
            get_task_lines = api_class.api_search_read(modelName,checksum,fields_toget)
            if(get_task_lines):
                response = get_task_lines
            else:
                response = {'status': 'error', 'msg': 'No Materials Found'}


        return jsonify(response)

# SHOW ALL CUSTOMERS FROM ODOO
@app.route('/api/v1/partner_all_details', methods=['POST'])
def partner_det():
    print "Entered into partner Details"
    modelName1 = "res.partner"
    fields_toget = ['street','street2', 'city', 'state_id', 'country_id', 'name','zip']
    if (request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        user_id = request_dict['uid']
        checksum = [['customer','=',True]]
        # partner_id = request_dict['partner_id']
        api_class = Helpers(request_dict['url'], request_dict['db'], int(request_dict['uid']),
                            request_dict['password'])
        check_access = api_class.check_access_rights(modelName1)
        if (check_access):
            assigned_user = api_class.api_search_read(modelName1,checksum,fields_toget)
            print assigned_user
            if assigned_user:
                for loc_det in assigned_user:

                    string_data = ''
                    # string_data=assigned_user['city']+','+assigned_user['state_id'][1]+','+assigned_user['country_id'][1]
                    if loc_det['street'] != False:
                        string_data = loc_det['street'] + ','
                    if loc_det['street2'] != False:
                        string_data = string_data + loc_det['street2'] + ','
                    if loc_det['city'] != False:
                        string_data = string_data + loc_det['city'] + ','
                    if loc_det['state_id'] != False:
                        string_data = string_data + loc_det['state_id'][1] + ','
                    if loc_det['country_id'] != False:
                        string_data = string_data + loc_det['country_id'][1]
                    print (string_data)
                    partner_location = geocoder.google(string_data)
                    print partner_location.latlng
                    partner_loc = partner_location.latlng
                    if partner_loc:
                        loc_det['latitude'] = partner_loc[0]
                        loc_det['longitude'] = partner_loc[1]
                    else:
                        loc_det['latitude'] = False
                        loc_det['longitude'] = False
                response = assigned_user
            else:
                response = {'status': 'error', 'msg': 'No Customers Found'}

    return jsonify(response)

# ==============================>Api Call for Byggtrd Ends Here<==========================================================

@app.route('/api/v1/tasks',methods=['POST'])
def get_tasks():

    #api_defaults
    modelName = "stock.warehouse.logistic.task"
    fields = ['name',
              'purchase_id',
              'partner_id',
              'type',
              'date_planned',
              'create_uid',
              'state',
              'line_ids']


    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        api_class = Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
        check_access = api_class.check_access_rights(modelName)
        checksum = []
        if(check_access):
            get_all_tasks = api_class.api_search_read(modelName,checksum,fields)
            if(get_all_tasks):
                response = get_all_tasks
            else:
                response = {'status': 'error', 'msg': 'No Tasks Found'}
    return jsonify(response)

@app.route('/api/v1/tasklines',methods=['POST'])
def get_tasks_line():
    #api defaults
    modelName = "stock.warehouse.logistic.task.line"
    fields_toget = ['name','qty','state','note',]

    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        print "data is %s"%request_dict
        line_ids = request_dict['line_ids']
        list_lines = (line_ids.split(','))
        new_list = [int(x) for x in list_lines]
        api_class = Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
        check_access = api_class.check_access_rights(modelName)
        if(check_access):
            get_task_lines = api_class.api_read(modelName,new_list,fields_toget)
            if(get_task_lines):
                response = get_task_lines
            else:
                response = {'status': 'error', 'msg': 'No Lines Found'}


        return jsonify(response)

@app.route('/api/v1/postTasks' , methods=['POST'])
def post_tasks1():
    #api_defaults
    modelName = "stock.warehouse.logistic.task"

    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        update_id = request_dict['to_update_id']

    return "Ok"

@app.route('/api/v1/updatetasks' , methods=['POST'])
def post_tasks():
    #api_defaults
    modelName = "stock.warehouse.logistic.task"

    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        update_id = request_dict['to_update_id']
        update_data = request_dict['update_data']
        print update_data
        api_class = Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
        check_access = api_class.check_access_rights(modelName)
        if(check_access):
            updated_id = api_class.api_update(modelName,update_id,update_data)
            if(updated_id):
                response = {'status': 'success', 'msg': 'Updated Successfully'}
            else:
                response = {'status': 'error', 'msg': 'updation failed'}

    return jsonify(response)

@app.route('/api/v1/updatetasklines' , methods=['POST'])
def post_tasks_lines():
    #api_defaults
    modelName = "stock.warehouse.logistic.task.line"

    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        update_id = request_dict['to_update_id']
        update_data = request_dict['update_data']
        api_class = Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
        check_access = api_class.check_access_rights(modelName)
        if(check_access):
            updated_id = api_class.api_update(modelName,update_id,update_data)
            if(updated_id):
                response = {'status': 'success', 'msg': 'Updated Successfully'}
            else:
                response = {'status': 'error', 'msg': 'updation failed'}

    return jsonify(response)

@app.route('/api/v1/updatetaskstate' , methods=['POST'])
def update_task_flow():
    response={}
    modelName = "stock.warehouse.logistic.task"
    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        update_id = request_dict['to_update_id']
        state = request_dict['update_data']
        print update_id
        api_class=Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
        check_access = api_class.check_access_rights(modelName)
        if(check_access):
            if(state=='confirmed'):
                updated_id=api_class.api_workflow(modelName,update_id)
                print("updated id is %s"%updated_id)
                response={'status':'success','msg':'updated Successfully'}
            if(state=='assigned'):
                updated_id=api_class.api_workflow_assign(modelName,update_id)
                print("updated id is %s"%updated_id)
                response={'status':'success','msg':'updated Successfully'}
            if(state=='accepted'):
                updated_id=api_class.api_workflow_accept(modelName,update_id)
                print("updated id is %s"%updated_id)
                response={'status':'success','msg':'updated Successfully'}
            if(state=='done'):
                updated_id=api_class.api_workflow_done(modelName,update_id)
                print("updated id is %s"%updated_id)
                response={'status':'success','msg':'updated Successfully'}
            if(state=='cancel'):
                updated_id=api_class.api_workflow_cancel(modelName,update_id)
                print("updated id is %s"%updated_id)
                response={'status':'success','msg':'updated Successfully'}
            if(state=='rejected'):
                updated_id=api_class.api_workflow_reject(modelName,update_id)
                print("updated id is %s"%updated_id)
                response={'status':'success','msg':'updated Successfully'}
            if(state=='failed'):
                updated_id=api_class.api_workflow_fail(modelName,update_id)
                print("updated id is %s"%updated_id)
                response={'status':'success','msg':'updated Successfully'}
            if(state=='draft'):
                updated_id=api_class.api_workflow_draft(modelName,update_id)
                print("updated id is %s"%updated_id)
                response={'status':'success','msg':'updated Successfully'}
    return jsonify(response)

@app.route('/api/v1/updatetaskcancel' , methods=['POST'])
def update_task_flow_assign():
    modelName = "stock.warehouse.logistic.task"
    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        update_id = request_dict['to_update_id']
        print update_id
        api_class=Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
        check_access = api_class.check_access_rights(modelName)
        if(check_access):
            updated_id=api_class.api_workflow_cancel(modelName,update_id)
            print("updated id is %s"%updated_id)
            response={'status':'success','msg':'updated Successfully'}
    return jsonify(response)
#
@app.route('/api/v1/updatetaskreject' , methods=['POST'])
def update_task_flow_accept():
    modelName = "stock.warehouse.logistic.task"
    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        update_id = request_dict['to_update_id']
        print update_id
        api_class=Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
        check_access = api_class.check_access_rights(modelName)
        if(check_access):
            updated_id=api_class.api_workflow_reject(modelName,update_id)
            print("updated id is %s"%updated_id)
            response={'status':'success','msg':'updated Successfully'}
    return jsonify(response)



@app.route('/api/v1/assigntask',methods=['POST'])
def assign_task():
    modelName = "stock.warehouse.logistic.task"
    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        update_id = request_dict['to_update_id']
        assign_uid=request_dict['uid']
        api_class=Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
        check_access = api_class.check_access_rights(modelName)
        if(check_access):
            assigned_user=api_class.api_check_assigned_user(modelName,update_id)
            print assigned_user
            if assigned_user and assigned_user['assigned_id'] !=False:
                response={'status':'assigned','msg':'already assigned task'}
            else:
                updated_id=api_class.assign_user(modelName,update_id,assign_uid)
                if updated_id:
                    status_update=api_class.api_workflow_assign(modelName,update_id)
                    print status_update
                    response={'status':'assigned','msg':'you are assigned to this task'}

    return jsonify(response)

@app.route('/api/v1/locationdetails',methods=['POST'])
def find_location():
    modelName1 = "res.partner"
    fields_toget = ['street2','city','state_id','country_id',]
    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        user_id = request_dict['uid']
        partner_id=request_dict['partner_id']
        api_class=Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
        check_access = api_class.check_access_rights(modelName1)
        if(check_access):
            assigned_user=api_class.location_details(modelName1,partner_id,fields_toget)
            print assigned_user
            source='La Plata'
            string_data=''
            # string_data=assigned_user['city']+','+assigned_user['state_id'][1]+','+assigned_user['country_id'][1]
            if assigned_user['street2'] != False:
                string_data=assigned_user['street2']+','
            if assigned_user['city'] != False:
                string_data=string_data+assigned_user['city']+','
            if assigned_user['state_id'] != False:
                string_data=string_data+assigned_user['state_id'][1]+','
            if assigned_user['country_id'] != False:
                string_data=string_data+assigned_user['country_id'][1]
            print (string_data)
            data=api_class.get_location_data(source,string_data)
            print data
    return jsonify(data)

@app.route('/api/v1/partner_name_details',methods=['POST'])
def partner_find():
    print "entered into function"
    modelName="res.partner"

    if request.data:
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        user_id = request_dict['uid']

        partner_id = request_dict['partner_id']
        city = request_dict['city']
        api_class = Helpers(request_dict['url'], request_dict['db'], int(request_dict['uid']), request_dict['password'])
        check_access = api_class.check_access_rights(modelName)
        if (check_access):
            assigned_user = api_class.partner_name_details(modelName, partner_id, city)
            response = {'status': 'success', 'msg': 'updated Successfully'}
            print assigned_user


    return jsonify(response)



# SHOW ALL PRODUCT FROM ODOO WHICH IS AVAILABLE IN POS
@app.route('/api/v1/product_all_pos',methods=['POST'])
def product_details():
    print "entered"





# @app.route('/api/v1/updatetaskfail' , methods=['POST'])
# def update_task_flow_accept():
#     modelName = "stock.warehouse.logistic.task"
#     if(request.data):
#         data_list = json.loads(request.data)
#         request_dict = data_list['params']
#         update_id = request_dict['to_update_id']
#         print update_id
#         api_class=Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
#         check_access = api_class.check_access_rights(modelName)
#         if(check_access):
#             updated_id=api_class.api_workflow_fail(modelName,update_id)
#             print("updated id is %s"%updated_id)
#             response={'status':'success','msg':'updated Successfully'}
#     return jsonify(response)




if __name__ == '__main__':
    app.run(host='172.16.100.45' , port=9002, debug=True)