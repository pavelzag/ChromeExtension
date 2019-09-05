from configuration import get_config
from json import dumps

from flask import Flask, request, Response
import jenkins as jenkins_python_module

JENKINS_URL = get_config("jenkins_url")
JENKINS_JOB_NAME = get_config("jenkins_job_name")
JENKINS_USER = get_config("jenkins_user")
JENKINS_PASSWORD = get_config("jenkins_password")
SUCCESS_MESSAGE = {
   "status": "OK"
}

FAILURE_MESSAGE = {
   "status": "Failure"
}
app = Flask(__name__)

server = jenkins_python_module.Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_PASSWORD)


def get_language(city_name):
    if city_name == 'New York City' or city_name == 'London':
        return 'English'
    elif city_name == 'Amsterdam':
        return 'Dutch'
    elif city_name == 'Berlin':
        return 'German'
    elif city_name == 'Tel Aviv':
        return 'Hebrew'
    else:
        return 'English'


def get_country(city_name):
    if city_name == 'New York City':
        return 'USA'
    elif city_name == 'London':
        return 'UK'
    elif city_name == 'Amsterdam':
        return 'Netherlands'
    elif city_name == 'Berlin':
        return 'Germany'
    elif city_name == 'Tel Aviv':
        return 'Israel'
    else:
        return 'USA'


@app.route('/trigger_jenkins_job', methods=['POST'])
def trigger_jenkins_job():
    content = request.get_json()
    city_name = content['city_name']
    country_language = get_language(city_name)
    country_name = get_country(city_name)
    result = server.build_job(name=JENKINS_JOB_NAME, parameters={'CITY_NAME': city_name,
                                                                 'COUNTRY_NAME': country_name,
                                                                 'COUNTRY_LANGUAGE': country_language})
    if result:
        return Response(dumps(SUCCESS_MESSAGE), status=200, mimetype='application/json')
    else:
        return Response(dumps(FAILURE_MESSAGE), status=400, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=True, port=8081)