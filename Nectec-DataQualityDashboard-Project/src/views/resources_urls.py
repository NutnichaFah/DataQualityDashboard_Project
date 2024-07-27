from flask import request, render_template, jsonify

from ..app import app
from .. import db
from ..models.resources_models import resource

# Resource page
@app.route("/re", methods=['GET'])
def list_resource():
    page_num = request.args.get('page_num', 1, type=int)
    per_page = 10
    # resources = resource.query.all()
    resource_query = (
        db.session.query(resource)
        .paginate(page=page_num, per_page=per_page)
    )
    return render_template("resources.html", resources=resource_query)
































# # Resource page
# @app.route("/testres", methods=['GET'])
# def test_resource():
#     connection = db.Session.connection()
#     data = connection.execute('''SELECT * FROM resource''')
#     return jsonify(data)

# # Resource page
# @app.route("/testres", methods=['GET'])
# def test_resource():
#     resources = resource.query.all()
#     response = []
#     for re in resources: response.append(re.toDict())
#     return jsonify(response)