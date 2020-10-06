import requests
import os
import sys
import base64
import json
import time
import threading
import subprocess
import random
import math
import re
import signal
import string

class ExoSolution(object):

    def __init__(self):
        try:
            self.EMAIL = "testing@exosite.com"
            self.PASSWORD = "1234eszxcv++"
            self.SOLUTION_HOST = "apps.exosite-staging.io"
            self.HOST = "https://{}/api:1".format(
                "bizapi-staging.hosted.exosite.io")
        except:
            print('import BuiltIn failed')

        self.SESSION = requests.Session()
        self.TOKEN = None

    def __request(self, method, append='', **kwargs):
        resp = self.SESSION.request(method, self.HOST + append, **kwargs)
        if resp.text == "":
            return resp.status_code
        else:
            try:
                return resp.json()
            except ValueError as e:
                return resp.text

    def __headers(self, token=None):
        if self.TOKEN is None:
            if token is None:
                self.TOKEN = self.get_user_token()
            else:
                self.TOKEN = token
        self.SESSION.headers.update({
            "content-type": "application/json",
            'accept': 'application/json',
            'authorization': 'token %s' % self.TOKEN
        })

    def __businessId(self, businessId):
        if businessId is None:
            businessId = self.BuiltIn.run_keyword(
                'ExoYeti.get_business_id', self.TOKEN)
        return businessId

    def get_user_token(self, email=None, password=None):
        if email is None:
            email = self.EMAIL
        if password is None:
            password = self.PASSWORD

        data = {"email": "%s" % email, "password": "%s" % password}
        resp = self.__request('post', "/token/", json=data)
        return resp['token']

    def create_eventhandler_via_api(self, solutionId, service, event, script="", token=None):
        self.__headers(token)
        data = {"solution_id": solutionId, "service": service,
                "event": event, "script": script}
        resp = self.__request(
            'post', "/solution/%s/eventhandler" % solutionId, json=data)
        time.sleep(1)
        if "errors" in resp:
            raise AssertionError(resp["errors"])
        return resp

    # Comment For Create Module Via API
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def create_module_via_api(self, solutionId, moduleName, script="", token=None):
        self.__headers(token)
        data = {"name": "%s" % moduleName, "solution_id": "%s" %
                solutionId, "script": "%s" % script}
        resp = self.__request('post', "/solution/%s/library" %
                              solutionId, json=data)
        if 'id' not in resp:
            raise AssertionError(
                "Module '%s' did not be created --> %s" % (moduleName, resp))
        return resp['id']

    # Comment For Create Role Via API
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def create_role_via_api(self, solutionId, roleId, parameter=None, token=None):
        self.__headers(token)
        data = {"role_id": roleId}
        if parameter is not None:
            data.update({"parameter": parameter})
        resp = self.__request('post', "/solution/%s/role" %
                              solutionId, json=data)
        if resp is 400:
            raise AssertionError(
                "Role '%s' did not be created --> %s" % (roleId, resp))
        return resp

    # Comment For Create User Via API
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def create_user_via_api(self, solutionId, userName, userEmail, userPassword, token=None):
        self.__headers(token)
        data = {"name": userName, "email": userEmail, "password": userPassword}
        resp = self.__request('post', "/solution/%s/user" %
                              solutionId, json=data)
        return resp

    # Comment For Create User And Activate Via API
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def create_activation_user_via_api(self, solutionId, userName, userEmail, userPassword, token=None):
        self.__headers(token)
        verifycode = self.create_user_via_api(
            solutionId, userName, userEmail, userPassword, token)
        resp = self.__request(
            'get', '/solution/%s/user/verify?code=%s' % (solutionId, verifycode))
        if resp != 'OK':
            raise AssertionError(
                "User '%s' did not be activated --> %s" % (userName, resp))
        return resp

    def delete_eventhandler_via_api(self, solutionId, service, event, token=None):
        self.__headers(token)
        eventhandlerId = self.get_eventhandler_id_via_api(
            solutionId, service, event, token)
        resp = self.__request(
            'delete', "/solution/%s/eventhandler/%s" % (solutionId, eventhandlerId))
        return resp

    # Comment For Delete Module Via API
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def delete_module_via_api(self, solutionId, moduleName, token=None):
        self.__headers(token)
        moduleId = self.get_module_id(solutionId, moduleName)
        resp = self.__request(
            'delete', "/solution/%s/library/%s" % (solutionId, moduleId))
        if resp != 204:
            raise AssertionError(
                "Endpoint '%s' did not be deleted --> %s" % (solutionName, resp))
        return resp

    # Comment For Delete Role Via API
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def delete_role_via_api(self, solutionId, roleId, token=None):
        self.__headers(token)
        resp = self.__request(
            'delete', "/solution/%s/role/%s" % (solutionId, roleId))
        if resp != 204:
            raise AssertionError(
                "Role '%s' did not be deleted --> %s " % (roleId, resp))
        return resp

    # Comment For Delete Roles By List Via API
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def delete_roles_by_list_via_api(self, solutionId, token=None):
        roles = self.get_role_lists(solutionId, token)
        if not roles:
            return
        roleIds = map(lambda x: x['role_id'], roles)
        for roleId in roleIds:
            self.delete_role_via_api(solutionId, roleId)
        return

    def delete_service_scriptkey_via_api(self, solutionId, alias, token=None):
        """ Delete service scriptkey """
        self.__headers(token)
        resp = self.__request(
            'delete', "/solution/%s/serviceconfig/%s" % (solutionId, alias))
        if resp != 204:
            raise AssertionError(
                "Service '%s' did not be deleted --> %s " % (solutionId, resp))
        return resp

    # Comment For Delete Solution Via API
    #    If the user is different with setting.py
    #    Please input Business ID and Authorization Token
    def delete_solution_via_api(self, solutionName, token=None, businessId=None):
        self.__headers(token)
        businessId = self.__businessId(businessId)
        solutionSid = self.get_solution_sid(solutionName, token, businessId)
        resp = self.__request(
            'delete', "/business/%s/solution/%s" % (businessId, solutionSid))
        if resp != 204:
            raise AssertionError(
                "Solution '%s' did not be deleted --> %s" % (solutionName, resp))
        return resp

    # Comment For Delete User Via API
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def delete_user_via_api(self, solutionId, userId, token=None):
        self.__headers(token)
        resp = self.__request(
            'delete', "/solution/%s/user/%s" % (solutionId, userId))
        if resp != 204:
            raise AssertionError(
                "User '%s' did not be deleted --> %s " % (userId, resp))
        return resp

    # Comment For Delete Users By List Via API
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def delete_users_by_list_via_api(self, solutionId, token=None):
        users = self.get_user_lists(solutionId, token)
        if not users:
            return
        userIds = map(lambda x: x['id'], users)
        for userId in userIds:
            self.delete_user_via_api(solutionId, userId)
        return

    def get_user_list_via_api(self, solutionId, token=None):
        """ get user list from specific solution.

            Args:
                solutionId (str): Solution id.
                token (str): Authorization token.

            Returns:
                list: The user list.
        """
        self.__headers(token)
        return self.__request('get', "/solution/%s/user/" % (solutionId))

    def update_user_via_api(self, solutionId, userId, userName, userPassword, originalPassword, token=None):
        """ Update specific user with given data.

            Args:
                solutionId (str): Solution id.
                userId (int): User id.
                userName (str): What user name you want to update.
                userPassword (str): What password you want to update.
                originalPassword (str): The password of user.
                token (str): Authorization token.

            Returns:
                bool: The response of update user.
        """
        self.__headers(token)
        payload = {"name": userName, "password": userPassword,
                   "original_password": originalPassword}
        path = "/solution/%s/user/%s" % (solutionId, userId)

        return self.__request('put', path, json=payload)

    def subscribe_product_service(self, solutionId, productId, serviceKey, token=None):
        """ Comment For Update Service Product
            If the user is different with setting.py
            Please input Authorization Token
        """
        self.__headers(token)
        data = {
            "solution_id": solutionId,
            "service": productId,
            "script_key": serviceKey
        }
        resp = self.__request(
            'post', "/solution/%s/serviceconfig/" % (solutionId), json=data)
        if 'statusCode' in resp:
            raise AssertionError("Update failed --> %s" % resp)
        return resp

    def update_eventhandler_via_api(self, solutionId, service, event, script="", token=None):
        self.__headers(token)
        eventhandlerId = self.get_eventhandler_id_via_api(
            solutionId, service, event, token)
        data = {"script": script}
        resp = self.__request('put', "/solution/%s/eventhandler/%s" %
                              (solutionId, eventhandlerId), json=data)
        if resp != 204:
            raise AssertionError("Update failed --> %s" % resp)
        time.sleep(1)
        return resp

    # Comment For Update Module
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def update_module(self, solutionId, moduleId, script, name=None, token=None):
        self.__headers(token)
        if name is None:
            name = self.get_module_name(solutionId, moduleId)
        data = {"name": "%s" % name, "script": "%s" % script}
        resp = self.__request('put', "/solution/%s/library/%s" %
                              (solutionId, moduleId), json=data)
        if resp != 204:
            raise AssertionError("Update failed --> %s" % resp)
        return resp

    # Comment For Update Service Product
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def update_service_product(self, solutionId, script, event="datapoint", service="device", token=None):
        self.__headers(token)
        data = {"script": "%s" % script, "event": "%s" %
                event, "service": "%s" % service}
        resp = self.__request(
            'put', "/solution/%s/eventhandler/%s_device_datapoint" % (solutionId, solutionId), json=data)
        if resp != 204:
            raise AssertionError("Update failed --> %s" % resp)
        return resp

    # Comment For Update Service Timer
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def update_service_timer(self, solutionId, script, event="timer", service="timer", token=None):
        self.__headers(token)
        data = {"script": "%s" % script, "event": "%s" %
                event, "service": "%s" % service}
        resp = self.__request(
            'put', "/solution/%s/eventhandler/%s_timer_timer" % (solutionId, solutionId), json=data)
        if resp != 204:
            raise AssertionError("Update failed --> %s" % resp)
        return resp

    # Comment For Update Solution Product Service
    #    If the user is different with setting.py
    #    Please input Business ID and Authorization Token
    def update_solution_products(self, solutionId, productIds, token=None, businessId=None):
        if isinstance(productIds, list) is not True:
            raise AssertionError(
                "ProductIds is not a array, it should be an array.")
        self.__headers(token)
        businessId = self.__businessId(businessId)
        service = self.get_solution_service(solutionId, token)
        item = filter(lambda i: i["service"] == "device", service["items"])
        if not item:
            raise AssertionError(
                "Service is None, please check solution id is correctly.")
        service = self.__request(
            'get', "/solution/%s/serviceconfig/%s" % (solutionId, item[0]["id"]))
        service["triggers"] = {"pid": productIds, "vendor": productIds}
        service["parameters"]["pid"] = productIds
        resp = self.__request('put', "/solution/%s/serviceconfig/%s" %
                              (solutionId, service["id"]), json=service)
        if resp != 204:
            raise AssertionError("Update failed --> %s" % resp)
        time.sleep(1.5)
        return resp

    def get_eventhandler_via_api(self, solutionId, token=None):
        self.__headers(token)
        resp = self.__request('get', "/solution/%s/eventhandler" % solutionId)
        try:
            return resp["items"]
        except:
            raise AssertionError(resp)

    def get_eventhandler_detail_via_api(self, solutionId, service, event, token=None):
        self.__headers(token)
        eventHandlerId = self.get_eventhandler_id_via_api(
            solutionId, service, event, token)
        resp = self.__request(
            'get', "/solution/%s/eventhandler/%s" % (solutionId, eventHandlerId))
        try:
            return resp
        except:
            raise AssertionError(resp)

    def get_eventhandler_id_via_api(self, solutionId, service, event, token=None):
        self.__headers(token)
        resp = self.get_eventhandler_via_api(solutionId, token)
        eventHandlerId = filter(
            lambda i: i["service"] == service and i["event"] == event, resp)
        return eventHandlerId[0]['id']

    # Comment For Get Module id
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def get_module_id(self, solutionId, name, token=None):
        items, _ = self.get_module_list(solutionId, token)
        moduleId = filter(lambda i: i['name'] == '%s' % name, items)
        if not moduleId:
            raise AssertionError("Module name :'%s' was not existing" % (name))
        return moduleId[0]['id']

    # Comment For Get Module name
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def get_module_name(self, solutionId, moduleId, token=None):
        items, _ = self.get_module_list(solutionId, token)
        moduleName = filter(lambda i: i['id'] == '%s' % moduleId, items)
        if not moduleName:
            raise AssertionError(
                "Module ID :'%s' was not existing" % (moduleId))
        return moduleName[0]['name']

    # Comment For Get Module list
    #    If the user is different with setting.py
    #    Please input Authorization Token
    def get_module_list(self, solutionId, token=None):
        self.__headers(token)
        resp = self.__request('get', "/solution/%s/library" % solutionId)
        return resp['items'], resp['total']

    def get_serviceconfig_via_api(self, solutionId, token=None):
        self.__headers(token)
        resp = self.__request('get', "/solution/%s/serviceconfig" % solutionId)
        try:
            return resp["items"]
        except:
            raise AssertionError(resp)

    def update_serviceconfig_via_api(self, solutionId, serviceconfigID, data, token=None):
        """Comment For Update Serviceconfig Via API
            If the user is different with setting.py
            Please input Authorization Token
        """
        self.__headers(token)
        resp = self.__request(
            'put', "/solution/{}/serviceconfig/{}".format(solutionId, serviceconfigID), data=data)
        try:
            return resp
        except:
            raise AssertionError(resp)

    def get_solution_service_via_api(self, solutionId, serviceconfigID, token=None):
        """Comment For Get Solution Service Via API
            If the user is different with setting.py
            Please input Authorization Token
        """
        self.__headers(token)
        resp = self.__request(
            'get', "/solution/{}/serviceconfig/{}".format(solutionId, serviceconfigID))
        try:
            return resp
        except:
            raise AssertionError(resp)

    # Comment For Update Solution Twilio Service
    #    If the user is different with setting.py
    #    Please input Business ID and Authorization Token
    def update_solution_twilio(self, solutionId, AuthToken=None, AccountSid=None, token=None):
        self.__headers(token)
        service = self.get_solution_service(solutionId, token)
        item = filter(lambda i: i["service"] == "twilio", service["items"])
        if not item:
            raise AssertionError(
                "Service is None, please check solution id is correctly.")
        service = self.__request(
            'get', "/solution/%s/serviceconfig/%s" % (solutionId, item[0]["id"]))

        if AuthToken is not None and AccountSid is not None:
            service["parameters"] = {"AuthToken": "%s" %
                                     AuthToken, "AccountSid": "%s" % AccountSid}
        else:
            service["parameters"] = {}

        resp = self.__request('put', "/solution/%s/serviceconfig/%s" %
                              (solutionId, service["id"]), json=service)
        time.sleep(1)
        return resp

    # Comment For Get Role List
    #    If the user is different with setting.py
    #    Please input and Authorization Token
    def get_role_lists(self, solutionId, token=None):
        self.__headers(token)
        roles = self.__request('get', "/solution/%s/role" % solutionId)
        if not roles:
            return False
        return roles

    # Comment For Get Solution Info
    #    If the user is different with setting.py
    #    Please input Business ID and Authorization Token
    def get_solution_info_via_api(self, solutionName, token=None, businessId=None):
        resp = self.get_solutions_list(token, businessId)
        solutionDomain = '{0}.{1}'.format(solutionName, self.SOLUTION_HOST)
        for solution in resp:
            if solution['domain'] == solutionDomain or solution.get('name') == solutionName:
                return solution
        raise AssertionError("Solution '%s' was not existing" % solutionName)

    # Comment For Get Solution Sid
    #    If the user is different with setting.py
    #    Please input Business ID and Authorization Token
    def get_solution_sid(self, solutionName, token=None, businessId=None):
        solution = self.get_solution_info_via_api(
            solutionName, token, businessId)
        return solution['sid']

    def get_solution_logs(self, solutionId, token=None):
        self.__headers(token)
        resp = self.__request('get', "/solution/{0}/logs".format(solutionId))
        try:
            return resp
        except:
            raise AssertionError("Get solution logs fail -> %s", resp)

    # Comment For Get Solution API ID
    #    If the user is different with setting.py
    #    Please input Business ID and Authorization Token
    def get_solution_id_via_api(self, solutionName, token=None, businessId=None):
        solution = self.get_solution_info_via_api(
            solutionName, token, businessId)
        return solution['apiId']

    # Comment For Get Solution Info From Yeti Database
    #    If the user is different with setting.py
    #    Please input Business ID and Authorization Token
    def get_solution_info_by_id(self, solutionId, token=None, businessId=None):
        self.__headers(token)
        businessId = self.__businessId(businessId)
        resp = self.__request('get', "/business/%s/solution/%s" %
                              (businessId, solutionId))
        return resp

    # Comment For Get Solutions List
    #    If the user is different with setting.py
    #    Please input Business ID and Authorization Token
    def get_solutions_list(self, token=None, businessId=None):
        self.__headers(token)
        businessId = self.__businessId(businessId)
        return self.__request('get', "/business/%s/solution/" % businessId)

    # Comment For Get Solution Service Config
    #    If the user is different with setting.py
    #    Please input Business ID and Authorization Token
    def get_solution_service(self, solutionId, token=None):
        self.__headers(token)
        return self.__request('get', "/solution/%s/serviceconfig" % solutionId)

    # Comment For Get User ID
    #    If the user is different with setting.py
    #    Please input and Authorization Token
    def get_user_id(self, solutionId, email, token=None):
        resp = self.get_user_lists(solutionId, token)
        user = filter(lambda i: i['email'] == email, resp)
        if not user:
            raise AssertionError("User '%s' was not existing" % email)
        return user[0]['id']

    # Comment For Get User List
    #    If the user is different with setting.py
    #    Please input and Authorization Token
    def get_user_lists(self, solutionId, token=None):
        self.__headers(token)
        resp = self.__request('get', "/solution/%s/user" % solutionId)
        return resp

    def verify_solution_tsdb_status(self, solutionId, token=None):
        """Verify Create Solutions status, tsdb status should be ready.
        If will drop error when the status is not ready, and remind user solution not be created yet.
        - It will return message from pegasus host.
        """
        self.__headers(token)
        resp = self.__request(
            'get', "/solution/%s/serviceconfig/%s_tsdb" % (solutionId, solutionId))
        if 'ready' not in resp['status']:
            raise AssertionError(
                "Solution '%s' tsdb did not be created successfully" % solutionId)
        return resp['status']
