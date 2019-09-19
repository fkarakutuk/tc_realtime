import requests
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

from flask import Flask
from flask import render_template

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = '/Users/furkan/Desktop/furkan/PycharmProjects/tcell_gads/tc_client_secret.json'


def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report_comtr_today(analytics):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': '164198106',

                    'dateRanges': [{'startDate': 'today', 'endDate': 'today'}],

                    'metrics': [{'expression': 'ga:sessions'},
                                {'expression': 'ga:pageviews'},
                                {'expression': 'ga:newUsers'},
                                {'expression': 'ga:bounceRate'}],
                }]
        }
    ).execute()


def get_report_comtr_yesterday(analytics):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': '164198106',

                    'dateRanges': [{'startDate': 'yesterday', 'endDate': 'yesterday'}],

                    'metrics': [{'expression': 'ga:sessions'},
                                {'expression': 'ga:pageviews'},
                                {'expression': 'ga:newUsers'},
                                {'expression': 'ga:bounceRate'}],
                }]
        }
    ).execute()


def get_report_turksporu_today(analytics):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': '188894697',

                    'dateRanges': [{'startDate': 'today', 'endDate': 'today'}],

                    'metrics': [{'expression': 'ga:sessions'},
                                {'expression': 'ga:pageviews'},
                                {'expression': 'ga:newUsers'},
                                {'expression': 'ga:bounceRate'}],
                }]
        }
    ).execute()


def get_report_turksporu_yesterday(analytics):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': '188894697',

                    'dateRanges': [{'startDate': 'yesterday', 'endDate': 'yesterday'}],

                    'metrics': [{'expression': 'ga:sessions'},
                                {'expression': 'ga:pageviews'},
                                {'expression': 'ga:newUsers'},
                                {'expression': 'ga:bounceRate'}],
                }]
        }
    ).execute()


def get_report_lifecell(analytics):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': '160680344',

                    'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],

                    'metrics': [{'expression': 'ga:sessions'},
                                {'expression': 'ga:pageviews'},
                                {'expression': 'ga:newUsers'},
                                {'expression': 'ga:bounceRate'}],
                }]
        }
    ).execute()


@app.route('/')
def hello_world():
    keyfile_dict = '/Users/furkan/Desktop/furkan/PycharmProjects/tcell_gads/tc_client_secret.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile_dict, scopes=[
        'https://www.googleapis.com/auth/analytics.readonly'])

    session = requests.Session()
    session.headers = {'Authorization': 'Bearer ' + credentials.get_access_token().access_token}

    url_kwargs_comtr = {
        'view_id': 164198106,
        'get_args': 'metrics=rt:activeUsers&dimensions=rt:deviceCategory'
    }

    url_kwargs_turksporu = {
        'view_id': 188894697,
        'get_args': 'metrics=rt:activeUsers&dimensions=rt:deviceCategory'
    }

    url_kwargs_lifecell = {
        'view_id': '160680344',
        'get_args': 'metrics=rt:activeUsers&dimensions=rt:deviceCategory'
    }
    response_comtr = session.get(
        'https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(**url_kwargs_comtr))

    response_turksporu = session.get(
        'https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(
            **url_kwargs_turksporu))

    response_lifecell = session.get(
        'https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(
            **url_kwargs_lifecell))

    response_comtr.raise_for_status()
    response_turksporu.raise_for_status()
    #  response_lifecell.raise_for_status()

    result_comtr = response_comtr.json()
    result_turksporu = response_turksporu.json()
    #  result_lifecell = response_lifecell.json()

    analytics = initialize_analyticsreporting()
    response_ctr_t = get_report_comtr_today(analytics)
    response_ctr_y = get_report_comtr_yesterday(analytics)
    response_tspr_t = get_report_turksporu_today(analytics)
    response_tspr_y = get_report_turksporu_yesterday(analytics)

    # response_lfcll = get_report_lifecell(analytics)

    metrics_ctr_t = [response_ctr_t['reports'][0]['data']['rows'][0]['metrics'][0]['values'][0],
                     response_ctr_t['reports'][0]['data']['rows'][0]['metrics'][0]['values'][1],
                     response_ctr_t['reports'][0]['data']['rows'][0]['metrics'][0]['values'][2],
                     response_ctr_t['reports'][0]['data']['rows'][0]['metrics'][0]['values'][3]]

    metrics_ctr_y = [response_ctr_y['reports'][0]['data']['rows'][0]['metrics'][0]['values'][0],
                     response_ctr_y['reports'][0]['data']['rows'][0]['metrics'][0]['values'][1],
                     response_ctr_y['reports'][0]['data']['rows'][0]['metrics'][0]['values'][2],
                     response_ctr_y['reports'][0]['data']['rows'][0]['metrics'][0]['values'][3]]

    metrics_tspr_t = [response_tspr_t['reports'][0]['data']['rows'][0]['metrics'][0]['values'][0],
                      response_tspr_t['reports'][0]['data']['rows'][0]['metrics'][0]['values'][1],
                      response_tspr_t['reports'][0]['data']['rows'][0]['metrics'][0]['values'][2],
                      response_tspr_t['reports'][0]['data']['rows'][0]['metrics'][0]['values'][3]]

    metrics_tspr_y = [response_tspr_y['reports'][0]['data']['rows'][0]['metrics'][0]['values'][0],
                      response_tspr_y['reports'][0]['data']['rows'][0]['metrics'][0]['values'][1],
                      response_tspr_y['reports'][0]['data']['rows'][0]['metrics'][0]['values'][2],
                      response_tspr_y['reports'][0]['data']['rows'][0]['metrics'][0]['values'][3]]

    """ metrics_lcll = [response_lfcll['reports'][0]['data']['rows'][0]['metrics'][0]['values'][0],
                    response_lfcll['reports'][0]['data']['rows'][0]['metrics'][0]['values'][1],
                    response_lfcll['reports'][0]['data']['rows'][0]['metrics'][0]['values'][2],
                    response_lfcll['reports'][0]['data']['rows'][0]['metrics'][0]['values'][3],
                    response_lfcll['reports'][0]['data']['rows'][0]['metrics'][0]['values'][4]] """

    if 'rows' in result_turksporu:
        return render_template("index.html", datacomtr=result_comtr['totalsForAllResults']['rt:activeUsers'],
                               data2comtr=result_comtr['rows'],
                               dataturksporu=result_turksporu['totalsForAllResults']['rt:activeUsers'],
                               data2turksporu=result_turksporu['rows'], metrics_t=metrics_ctr_t,
                               metrics_tsr_t=metrics_tspr_t, metrics_y=metrics_ctr_y, metrics_tsr_y=metrics_tspr_y)
    else:
        return render_template("index.html", datacomtr=result_comtr['totalsForAllResults']['rt:activeUsers'],
                               data2comtr=result_comtr['rows'],
                               dataturksporu=result_turksporu['totalsForAllResults']['rt:activeUsers'],
                               metrics_t=metrics_ctr_t, metrics_tsr_t=metrics_tspr_t, metrics_y=metrics_ctr_y,
                               metrics_tsr_y=metrics_tspr_y)


if __name__ == '__main__':
    app.run()
