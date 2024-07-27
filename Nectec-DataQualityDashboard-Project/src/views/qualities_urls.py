from flask import request, render_template, jsonify, json, session
from sqlalchemy import func

from ..app import app
from .. import db
from ..models.qualities_models import Data_quality_metrics
from ..models.packages_models import package
from ..models.resources_models import resource

# ######################### Qualities page #########################
@app.route("/qa", methods=['GET'])
def list_all_qualities():
    # qualities = Data_quality_metrics.query.all()
    page_num = request.args.get('page_num', 1, type=int)
    per_page = 10
    # resources = resource.query.all()
    qualities = (
        db.session.query(Data_quality_metrics)
        .paginate(page=page_num, per_page=per_page)
    )
    return render_template("qualities.html", qualities=qualities, the_title="Data Quality Metrics")

# Data Quality Metric join with Resource page
@app.route("/qa/join-re", methods=['GET'])
def join_resource():
    # join
    join_re = db.session.query(Data_quality_metrics, resource).join(resource, Data_quality_metrics.ref_id == resource.id)
    joined_re_data = join_re.all()

    return render_template("qa_join_re.html", the_title="Quality join Resource", joined_re_data=joined_re_data)

# Data Quality Metric join with Package page
@app.route("/qa/join-pa", methods=['GET'])
def join_package():

    join_pa = db.session.query(Data_quality_metrics, package).join(package, Data_quality_metrics.ref_id == package.id)
    join_pa_data = join_pa.all()

    return render_template("qa_join_pa.html", the_title="Quality Join Package", join_pa_data=join_pa_data)