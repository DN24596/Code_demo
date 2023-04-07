import requests

def get_logs():
    """
    Get the logs for the given time period and service_ID.
    """
    url = "http://your-splunk-instance:8080/services/search/jobs/export"
    headers = {"Authorization": "Splunk <your-splunk-token>"}
    data = {
        "search": 'index="GUI" AND service_ID="33.FOO.010261..FOO" earliest="2/23/2023:00:00:00" latest=@d',
        "output_mode": "json",
        "field_list": "_time,Attempt,service_ID,service_Type,services,CPE_Resource_ID,Details,Device,GUI_Instance,GUI_Feature,host,index,Log_ID,Log_Message,User,Manager,Market,Operation,Operation_ID,Resource_ID,Response_Time,SCOD_Error_Code,Step,Step_Error,TID,_raw,timeout",
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()

def filter_logs(logs):
    """
    Filter the logs to get the time out messages.
    """
    timeout_logs = []
    for log in logs:
        if "timeout" in log and log["timeout"] == "Device Activation Timed Out After 10 Minutes":
            timeout_logs.append(log)
    return timeout_logs

def write_to_database(logs):
    """
    Write the service_ID and timeout message to a database.
    """
    # your database write code here

def main():
    logs = get_logs()
    timeout_logs = filter_logs(logs)
    write_to_database(timeout_logs)

if __name__ == "__main__":
    main()
