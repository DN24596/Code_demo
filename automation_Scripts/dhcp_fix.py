# import requests
import re
import logging
from flask_restplus import Namespace, Resource, abort
from compliance_app.dll.ipc import ipc_get, ipc_post
from compliance_app.common.auth import database_api_key  # TODO: Remove database api key from source
from flask import request
import requests
import compliance_app

api = Namespace('v1/ipcontrol', description='updates the Mac Address for RPHY')

logger = logging.getLogger(__name__)


@api.route("")
@api.response(200, 'OK')
@api.response(400, 'Bad Request')
@api.response(404, 'Not Found')
@api.response(500, 'Application Error')
class MacAdd(Resource):
    @api.doc(params={'CID': 'CID',
                     'mac_address': 'MAC Address'})
    def get(self):
        """Takes in CID and returns MAC Address"""

        if 'CID' not in request.args:
            abort(400, 'Missing CID')
        cid = request.args['CID'].strip()

        if 'mac_address' not in request.args:
            abort(400, 'Missing mac_address')
        mac = request.args['mac_address'].strip()
        if not re.match("^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$", mac):
            abort(400, 'Invalid MAC Address')

        database_base_url = compliance_app.app.config['database_url']
        url = f'{database_base_url}/server/app_int/foo_orchestrator_model/views/' \
            f'foo_orchestrator_model_1?cid={cid}&api_key={database_api_key}'  # TODO: Remove database api key from source
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"}
        r = requests.get(url, verify=False, headers=headers)
        response = r.json()

        if r.status_code / 100 != 2:
            abort(500, F"Unable to retrieve data from database")
        response = response['elements'][0]
        if response.length == 0:
            abort(500, F"No results found for CID {cid}")
        try:
            device_uid = response["data"][0]["path_name"].split(".")[-1]
        except (KeyError, IndexError):
            abort(500, F"UID does not exist for CID")
        # TODO: Fix Trailing forward slash in ipc_base_url
        path = f'inc-rest/api/v1/Gets/getDhcpClientClassByName' \
            f'?name=RPD-{device_uid}'
        ipc_response = ipc_get(path)
        # Append MAC Address to DHCP Client Class
        payload = {
            "wsDhcpClientClass":{
                "clientClassType": ipc_response["clientClassType"],
                "dhcpOptionSet": ipc_response["dhcpOptionSet"],
                "dhcpPolicySet": ipc_response["dhcpPolicySet"],
                "ipv6": ipc_response["ipv6"],
                "name": device_uid,
                "id": ipc_response["id"],
                "items": ipc_response["items"]
            }
        }
        payload['wsDhcpClientClass']['items'].append(
            {
                "condition": "exact",
                "value": mac
            })
        path = f'inc-rest/api/v1/Imports/importDHCPClientClass' \
            f'?name={device_uid}'  # TODO: Same as Get
        DHCP_MAC = ipc_post(path, payload=payload)
        return DHCP_MAC
