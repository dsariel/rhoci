# Copyright 2017 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from flask import render_template
from flask import Blueprint
from flask import jsonify
from flask import request
import logging
import re

from rhoci.jenkins.jjb import generate_job_definition
from rhoci.models import Job


logger = logging.getLogger(__name__)

add_job = Blueprint('add_job', __name__)


@add_job.route('/')
def index():
    """Add job page."""
    return render_template('add_job.html')


@add_job.route('/add_job/generate_jjb/', methods=['GET', 'POST'])
def generate_jjb():
    output = generate_job_definition(request.form['dfg'],
                                     request.form['component'],
                                     request.form['tester'])

    return jsonify(output=output)


@add_job.route('/add_job/job_exists/', methods=['GET', 'POST'])
def job_exists():
    jobs_match = []
    pattern = re.compile('.*(%s).*(%s).*(%s).*' % (request.form['dfg'],
                                                   request.form['component'],
                                                   request.form['tester']))

    jobs = Job.query.all()
    for job in jobs:
        if pattern.match(job.name):
            jobs_match.append(job.name)

    return jsonify(output='\n'.join(jobs_match))
