from flask import request, render_template, jsonify
from sqlalchemy import func

from ..app import app
from .. import db
from ..models.qualities_models import Data_quality_metrics as dq
from ..models.packages_models import package 
from ..models.resources_models import resource
from ..models.group_models import group
from ..models.member_models import member

# Dataset Page - DataQuality Join Package 
@app.route("/datasets", methods=['GET'])
def list_datasets():

    # Pagination
    page_num = request.args.get('page_num', 1, type=int)
    per_page = 10
    datasets_q = (
        db.session.query(
            package.name,
            package.title,
            dq.timeliness, 
            dq.openness, 
            dq.downloadable, 
            dq.validity, 
            dq.consistency, 
            dq.machine_readable, 
            dq.ref_id,
            )
            .join(package, dq.ref_id==package.id)
            .paginate(page=page_num, per_page=per_page)
        )


    return render_template("datasets/datasets.html", the_title='Datasets Table', datasets_q=datasets_q)

@app.route("/datasets2", methods=['POST'])
def datasets2():

    package_id = request.form.get('packageId')
    package_title = request.form.get('packageTitle')
    
    # Count the number of resources
    resource_count = (
        db.session.query(func.count(resource.id))
            .join(dq, resource.id == dq.ref_id)
            .filter(resource.package_id == package_id)
            .scalar()
    )
    resource_q = (
        db.session.query(
            resource.id,
            resource.name,
            resource.format,
            dq.timeliness,
            dq.openness,
            dq.downloadable,
            dq.validity,
            dq.consistency,
            dq.machine_readable,
        )
        .join(resource,dq.ref_id == resource.id)
        .filter(resource.package_id == package_id)
        .all()
    )
    
    resource_read = render_template('datasets/show_resource.txt', resource_q=resource_q)
    
    res_data = {
        'package_title': package_title,
        'resource_count': resource_count,
        'resource_read' : resource_read
    }

    return jsonify(res_data)
