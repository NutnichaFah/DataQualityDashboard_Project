from flask import request, render_template , url_for, request, jsonify , redirect
from sqlalchemy import text

from ..app import app
from .. import db
from ..models.packages_models import package
from ..models.resources_models import resource

import os, datetime as dtt

# @app.route("/pa", methods=['GET'])
# def list_all_package():
#     heading = 'Package Table'
#     packages = package.query.all()
#     return render_template("packages.html", packages=packages, heading=heading)

# Package join Resource
@app.route("/pa/join-re", methods=['GET'])
def pa_join_re():
    pa_join_re = db.session.query(package, resource).join(resource, package.id == resource.package_id)
    pa_join_re_data = pa_join_re.all()

    return render_template("table/pa_join_re.html", pa_join_re_data=pa_join_re_data, heading="Package Join Resource", the_title="Package Table")

######################### Package Page ######################### 
## Pagination ##
# ######### path 'pa' ตั้งค่า default ให้เป็นหน้าที่ 1 ##########
@app.route('/pa/', defaults={'page_num': 1})
@app.route('/pa/<page_num>')
def package_page(page_num):
    # Pagination
    page_num = request.args.get('page_num', 1, type=int)
    per_page = 10
    package_q = (db.session.query(package).filter(package.state == 'active').paginate(page=page_num, per_page=per_page))
    
    return render_template("packages.html", package_q=package_q, the_title="Package Table")


@app.route("/range/",defaults={'page_num': 1}, methods=["POST", "GET"])
@app.route("/range/<int:page_num>", methods=["POST", "GET"])
def range(page_num=None):
    if request.method == 'POST':
        startdate = dtt.datetime.strptime(request.form['startdate'], '%d/%m/%Y')
        enddate = dtt.datetime.strptime(request.form['enddate'], '%d/%m/%Y')

        data = package.query.filter(package.state == 'active')
        ordersrange = data.filter(package.metadata_created >= startdate).filter(package.metadata_created <= enddate)
        pagination = ordersrange.paginate(per_page=5, page=page_num, error_out=False)
        # Render the template and include ordersrange in the context
        return render_template('response.html', ordersrange=ordersrange, pagination=pagination)