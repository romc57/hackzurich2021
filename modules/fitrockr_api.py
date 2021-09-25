import requests
from datetime import datetime
import os


def time_to_sec(hour, minute, sec):
    '''
    Convert time to seconds for comparison
    '''
    return int(hour)*3600 + int(minute)*60 + int(sec)


def execute_fitrockr_api_call(end_point):
    '''
    Execute a general api call to fitrockr with a given endpoint
    :param end_point: end point contains the query parameters and the api method
    :return: response on successful call, False on failure
    '''
    url = 'https://api.fitrockr.com/{}'.format(end_point)
    headers = {'X-Tenant': 'hackzurich', 'Content-Type': 'application/json',
               'X-API-Key': os.environ['FITROCKR_API_KEY']}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return False
    return response.json()


def get_user_stress_records(user_id, start_date, end_date):
    '''
    Get the user statistics for the dates given
    :param user_id: id in the fitrockr
    :param start_date: start date
    :param end_date: end date
    :return: response: list of records
    '''
    end_point = 'v1/users/{}/stress?startDate={}&endDate={}'.format(user_id, start_date, end_date)
    response = execute_fitrockr_api_call(end_point)
    return response


def get_user_info(query):
    '''
    Get the user profile info by query of name, email
    :param query: query
    :return: response if got a user, False if there was no user match
    '''
    end_point = 'v1/users?query={}&page=0&size=10'.format(query)
    response = execute_fitrockr_api_call(end_point)
    if not response or len(response) == 0:
        return False
    return response


def get_user_stress_level(user_id, time_in_sec, date=str(datetime.now()).split(' ')[0]):
    '''
    Get the stress level of a user in a certain time
    :param user_id: system id of the user
    :param time_in_sec: time to messure stress level - in seconds
    :param date: date
    :return: int- stress level, on failure None
    '''
    user_stats = get_user_stress_records(user_id, date, date)
    if not user_stats:
        return None
    for record in user_stats:
        start_time = record['startTime']['time']
        start_time = time_to_sec(start_time['hour'], start_time['minute'], start_time['second'])
        if start_time <= time_in_sec < start_time + 180:
            return record['stressLevelValue']
    return None
