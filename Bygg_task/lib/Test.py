# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import request
from flask import json
from lib.Login import RestLogin
from lib.helpers import Helpers

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
        if(check_access):
            get_all_tasks = api_class.api_search_read(modelName,fields)
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
        update
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

@app.route('/api/v1/multiupdate',methods=['POST'])
def multi_update():
    modelName = "stock.warehouse.logistic.task"
    update_list = list()
    if(request.data):
        data_list = json.loads(request.data)
        request_dict = data_list['params']
        list_arry = request_dict['to_update_id']
        state = request_dict['update_data']

        for dict in (list_arry):
             update_id = dict
             api_class=Helpers(request_dict['url'],request_dict['db'],int(request_dict['uid']),request_dict['password'])
             check_access = api_class.check_access_rights(modelName)
             if(check_access):
                 update = api_class.api_multi_update(modelName,update_id,state)
                 print update
                 if(update):
                     update_list.append(update_id)

        if(update_list):
            response = {'status':'assigned','msg':'Updated Successfully', 'update_ids':update_list}
        else:
            response = {'status':'failed','msg':'Some Tasks are not updated'}

        return jsonify(response)

    @app.route('/api/v1/locationdetails', methods=['POST'])
    def find_location():
        modelName1 = "res.partner"
        fields_toget = ['street2', 'city', 'state_id', 'country_id', ]
        if (request.data):
            data_list = json.loads(request.data)
            request_dict = data_list['params']
            user_id = request_dict['uid']
            partner_id = request_dict['partner_id']
            api_class = Helpers(request_dict['url'], request_dict['db'], int(request_dict['uid']),
                                request_dict['password'])
            check_access = api_class.check_access_rights(modelName1)
            if (check_access):
                assigned_user = api_class.location_details(modelName1, partner_id, fields_toget)
                print assigned_user
                source = 'california'
                string_data = ''
                # string_data=assigned_user['city']+','+assigned_user['state_id'][1]+','+assigned_user['country_id'][1]
                if assigned_user['street2'] != False:
                    string_data = assigned_user['street2'] + ','
                if assigned_user['city'] != False:
                    string_data = string_data + assigned_user['city'] + ','
                if assigned_user['state_id'] != False:
                    string_data = string_data + assigned_user['state_id'][1] + ','
                if assigned_user['country_id'] != False:
                    string_data = string_data + assigned_user['country_id'][1]
                print (string_data)
                data = api_class.get_location_data(source, string_data)
                print data
        return jsonify(data)





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
    app.run(debug=True)
