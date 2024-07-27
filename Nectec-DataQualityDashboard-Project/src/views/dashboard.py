from flask import request, render_template, session,jsonify
from sqlalchemy import func, and_, not_, case

from ..app import app
from .. import db
from ..models.qualities_models import Data_quality_metrics as dq
from ..models.packages_models import package
from ..models.resources_models import resource
from ..models.group_models import group
from ..models.member_models import member


@app.route("/dashboard", methods=['GET'])
def dashboard():
# ## Form Select ##
    parent_query = (
            db.session.query(
                group.id,
                group.name,
                group.title.label('parent_title')
            )
            .join(member, member.table_id == group.id)
            .filter(member.capacity == 'public' , member.state == 'active', group.type == 'organization')
            .distinct()
            .all()
        )

# ## Score Card ##
    # Number Count-Score card
    # org_count = (
    #     db.session.query(func.count(group.id).label('org_count'))
    #     .filter(group.state == 'active', group.type == 'organization', group.id == org_id).scalar()
    # )
    org_count = (
        db.session.query(func.count(group.id).label('org_count')).filter(group.state == 'active', group.type == 'organization').scalar()
    )

    org_child_count = (
        db.session.query(
            func.count(member.group_id).label('org_child_count')
        ).filter(member.state == 'active', member.table_name == 'group').scalar()
    )

    package_count = (
        db.session.query(
            func.count(package.id).label('package_count')
        )
            .filter(package.state == 'active')
            .scalar()
    )

    resource_count = (
        db.session.query(
            func.count(resource.id).label('resource_count')
        )    
            .filter(resource.state == 'active')
            .scalar()
        
    )

    scorecard_count = {
        'org_count': org_count,
        'org_child_count': org_child_count,
        'package_count': package_count,
        'resource_count': resource_count
    }

# ## Chart ##
# 1-Openness Data
    openness_label = case(
        (dq.openness == 1, '1 star'),
        (dq.openness == 2, '2 star'),
        (dq.openness == 3, '3 star'),
        (dq.openness == 4, '4 star'),
        (dq.openness == 5, '5 star'),
        else_='other'
    )

    openness_q = (
        db.session.query(
            openness_label.label('openness_label'),
            func.count().label('openness_count')
        )
        .join(package, dq.ref_id == package.id)
        .group_by(openness_label)
        .order_by(openness_label)
        .all()
    )

    openness_group = [{
        'label': row.openness_label,
        'count' : row.openness_count
    } for row in openness_q]

# 2-Downloadable Data
    downloadable_label = case(
        (dq.downloadable == 0, 'ไม่สามารถดาวน์โหลดได้'),
        (dq.downloadable == 1, 'สามารถดาวน์โหลดได้'),
    )
    
    downloadable_q = (
        db.session.query(
            downloadable_label.label('downloadable_label'),
            func.count().label('downloadable_count')
        )
        .group_by(downloadable_label)
        .all()
    )

    downloadable_group = [{
        'label': row.downloadable_label,
        'count': row.downloadable_count,
    } for row in downloadable_q]

# 3-Access API Data
    api_label = case(
        (dq.access_api == 0, 'เข้า datastore ไม่ได้ (ตารางไม่สมบูรณ์)'),
        (dq.access_api == 1, 'Machine Readable & API'),
        (dq.access_api == 2, 'Non-Machine Readable เช่น pdf, zip'),
    )

    api_q = (
        db.session.query(
            api_label.label('api_label'),
            func.count().label('api_count')
        )
        .group_by(api_label)
        .all()
    )

    api_group = [{
        'label': row.api_label,
        'count': row.api_count,
    } for row in api_q]

# 4-Machine Readable Data
    # Pagination
    page_num = request.args.get('page_num', 1, type=int)
    per_page = 25
    machine_readable_table = (
        db.session.query(
            dq.machine_readable, 
            dq.consistency, 
            dq.validity, 
            package.name,
            package.title,
            )
            .join(package, dq.ref_id == package.id)
            .paginate(page=page_num, per_page=per_page)
        )
    
# 5-Timeliness Data
    time_label = case(
        (and_(dq.timeliness >= 0, dq.timeliness != 999), 'อัพเดตไม่เกินเวลา'),
        (and_(dq.timeliness > -30, dq.timeliness < 0), 'อัพเดตล่าช้าไม่เกิน 1 เดือน'),
        (dq.timeliness < -30, 'อัพเดตล่าช้า 3 เดือนขึ้นไป'),
        else_='none'
    )

    time_q = (
        db.session.query(
            time_label.label('time_label'),
            func.count().label('time_count')
        )
        .filter(time_label != 'none')
        .group_by(time_label)
        # .order_by(time_label)
        .all() 
        )

    time_group = [{
        'label': row.time_label,
        'count': row.time_count,
    } for row in time_q]

    return render_template("dashboard/dashboard.html",
                           the_title='Data Quality Dashboard',
                           parent_query=parent_query,
                           scorecard_count=scorecard_count,
                           openness_group=openness_group,
                           downloadable_group=downloadable_group,
                           api_group=api_group,
                           time_group=time_group,
                           machine_readable_table=machine_readable_table
                           )

@app.route("/dashboard2", methods=['POST'])
def dashboard2():
    # Get Id ของกระทรวง
    org_id = request.form.get('selectedParent_id')

    # ## Form Select ##
    if org_id != "":
        subq_org_id = db.session.query(
                member.group_id
            ).filter(member.state == 'active', member.table_name == 'group', member.table_id == org_id).all()
    else:
        subq_org_id = (
            db.session.query(
                group.id.label('group_id'),
                group.name,
                group.title.label('parent_title')
            )
            .join(member, member.table_id == group.id.label('group_id'))
            .filter(member.capacity == 'public' , member.state == 'active', group.type == 'organization')
            .distinct()
            .all()
        )

    groupid_list = [row.group_id for row in subq_org_id]

    orgchild_q = db.session.query(
        group.id,
        group.name,
        group.title
    ).filter(group.state == 'active', group.type == 'organization', group.id.in_(groupid_list)).all() 
    
    # selected Form-Child ข้อมูลหน่วยงานย่อย
    orgchild_data = [{'org_id' : row.id,
             'org_name': row.name,
             'org_title': row.title
             } for row in orgchild_q]
    
      
    # ## Score Card ##
    # Number Count-Score card
    # org_count
    if org_id != '':
        org_child_count = (
            db.session.query(
                func.count(member.group_id).label('org_child_count')
            ).filter(member.state == 'active', member.table_name == 'group', member.table_id == org_id).scalar()
        )
    else:
        org_child_count = (
            db.session.query(func.count(group.id).label('org_count')).filter(group.state == 'active', group.type == 'organization').scalar()
        )
# package_count
    subq_package_count = db.session.query(member.group_id).filter(member.state == 'active', member.table_name == 'group', member.table_id == org_id)
    subq_package_count_list = [row.group_id for row in subq_package_count]
    package_count = db.session.query(func.count(package.id).label('package_count')).filter(package.state == 'active')
    if org_id != '':
        package_count = package_count.filter(package.owner_org.in_(groupid_list)).scalar()
    else:
        package_count = package_count.scalar()

# resorece count
    subq_resource_count = db.session.query(package.id)
    if org_id != '':
        subq_resource_count = subq_resource_count.filter(package.owner_org.in_(groupid_list))
    else:
        subq_resource_count = subq_resource_count \
            .join(resource, resource.package_id == package.id) \
            .filter(resource.state == 'active')
    subq_resource_count_list = [row.id for row in subq_resource_count]
    resource_count = (db.session.query(func.count(resource.id).label('resource_count'))    
            .filter(resource.state == 'active', resource.package_id.in_(subq_resource_count_list)).scalar())
    
# ## Chart ##
# 1-Openness Data
    openness_label = case(
        (dq.openness == 1, '1 star'),
        (dq.openness == 2, '2 star'),
        (dq.openness == 3, '3 star'),
        (dq.openness == 4, '4 star'),
        (dq.openness == 5, '5 star'),
        else_='other'
    )

    openness_q = (
        db.session.query(
            openness_label.label('openness_label'),
            func.count().label('openness_count')
        )
        .join(package, dq.ref_id == package.id)
    )
    if org_id != '':
        openness_q = openness_q.filter(package.owner_org.in_(groupid_list))

    openness_q = openness_q.group_by(openness_label).order_by(openness_label).all()

    openness_group = [{
        'label': row.openness_label,
        'count' : row.openness_count
    } for row in openness_q]

# 2-Downloadable Data
    downloadable_label = case(
        (dq.downloadable == 0, 'ไม่สามารถดาวน์โหลดได้'),
        (dq.downloadable == 1, 'สามารถดาวน์โหลดได้'),
    )
    
    downloadable_q = (
        db.session.query(
            downloadable_label.label('downloadable_label'),
            func.count().label('downloadable_count')
        )
        .join(package, dq.ref_id == package.id)
    )
    if org_id != '':
        downloadable_q = downloadable_q.filter(package.owner_org.in_(groupid_list))

    downloadable_q = downloadable_q.group_by(downloadable_label).all()

    downloadable_group = [{
        'label': row.downloadable_label,
        'count': row.downloadable_count,
    } for row in downloadable_q]

# 3-Access API Data
    api_label = case(
        (dq.access_api == 0, 'เข้า datastore ไม่ได้ (ตารางไม่สมบูรณ์)'),
        (dq.access_api == 1, 'Machine Readable & API'),
        (dq.access_api == 2, 'Non-Machine Readable เช่น pdf, zip'),
    )

    api_q = (
        db.session.query(
            api_label.label('api_label'),
            func.count().label('api_count')
        )
        .join(package, dq.ref_id == package.id)
    )
    if org_id != '':
        api_q = api_q.filter(package.owner_org.in_(groupid_list))

    api_q = api_q.group_by(api_label).all()

    api_group = [{
        'label': row.api_label,
        'count': row.api_count,
    } for row in api_q]

# 4-Machine Readable Data
    # Pagination
    page_num = request.args.get('page_num', 1, type=int)
    per_page = 25
    machine_readable_table = (
        db.session.query(
            dq.machine_readable, 
            dq.consistency, 
            dq.validity, 
            package.name,
            package.title,
            )
            .join(package, dq.ref_id == package.id)
        ) 
    if org_id != '':
        machine_readable_table = machine_readable_table.filter(package.owner_org.in_(groupid_list))
    machine_readable_table = machine_readable_table.paginate(page=page_num, per_page=per_page)
    machine_read = render_template('dashboard/tbl_res.txt', machine_readable_table=machine_readable_table)
    

# 5-Timeliness Data
    time_label = case(
        (and_(dq.timeliness >= 0, dq.timeliness != 999), 'อัพเดตไม่เกินเวลา'),
        (and_(dq.timeliness > -30, dq.timeliness < 0), 'อัพเดตล่าช้าไม่เกิน 1 เดือน'),
        (dq.timeliness < -30, 'อัพเดตล่าช้า 3 เดือนขึ้นไป'),
        else_='none'
    )

    time_q = (
        db.session.query(
            time_label.label('time_label'),
            func.count().label('time_count')
        )
        .join(package, dq.ref_id == package.id)
        .filter(time_label != 'none')
        )
    if org_id != '':
        time_q = time_q.filter(package.owner_org.in_(groupid_list))
    time_q = time_q.group_by(time_label).all()

    time_group = [{
        'label': row.time_label,
        'count': row.time_count,
    } for row in time_q]


# Response 
    res_data = {
        'org_child_count' : org_child_count,
        'package_count': package_count,
        'resource_count': resource_count,
        'org_info': orgchild_data,
        'openness_group': openness_group,
        'downloadable_group' : downloadable_group,
        'api_group' : api_group,
        'machine_readable_table': machine_read,
        'time_group' : time_group,

    }
    
    return jsonify(res_data)

@app.route("/dashboard3", methods=['POST'])
def dashboard3():
    # Get Id ของหน่วยงานย่อย
    sub_org_id = request.form.get('sub_org_id')

    # packages of sub_org
    org_child_count = (
        db.session.query(
            func.count(member.group_id).label('org_child_count')
        ).filter(member.state == 'active', member.table_name == 'group', member.table_id == sub_org_id).scalar()
    )
    query_package_lists = db.session.query(package.id).filter(package.owner_org == sub_org_id).all()
    package_lists = [row.id for row in query_package_lists]

# ## Score Card ##
    # package_count
    package_count = (db.session.query(func.count(package.id).label('package_count'))
                        .filter(package.owner_org == sub_org_id).scalar())
    # resorece count
    resource_count = (db.session.query(func.count(resource.id).label('resource_count'))    
                .filter(resource.state == 'active', resource.package_id.in_(package_lists)).scalar())
    

# ## Chart ##
# 1-Openness Data
    openness_label = case(
    (dq.openness == 1, '1 star'),
    (dq.openness == 2, '2 star'),
    (dq.openness == 3, '3 star'),
    (dq.openness == 4, '4 star'),
    (dq.openness == 5, '5 star'),
    else_='other'
)
# การ query chart หลังจากที่ได้ค่า org_id
    openness_q_s = (
        db.session.query(
            openness_label.label('openness_label'),
            func.count().label('openness_count')
        )
        .join(package, dq.ref_id == package.id)
        .filter(package.owner_org == sub_org_id)
        .group_by(openness_label)
        .order_by(openness_label)
        .all()
    )
    openness_group_s = [{
        'label': row.openness_label,
        'count' : row.openness_count
    } for row in openness_q_s]

# 2-Downloadable Data
    downloadable_label = case(
        (dq.downloadable == 0, 'ไม่สามารถดาวน์โหลดได้'),
        (dq.downloadable == 1, 'สามารถดาวน์โหลดได้'),
    )
    
    downloadable_q_s = (
        db.session.query(
            downloadable_label.label('downloadable_label'),
            func.count().label('downloadable_count')
        )
        .join(package, dq.ref_id == package.id)
        .filter(package.owner_org == sub_org_id)
        .group_by(downloadable_label)
        .all()
    )

    downloadable_group_s = [{
        'label': row.downloadable_label,
        'count': row.downloadable_count,
    } for row in downloadable_q_s]

# 3-Access API Data
    api_label = case(
        (dq.access_api == 0, 'เข้า datastore ไม่ได้ (ตารางไม่สมบูรณ์)'),
        (dq.access_api == 1, 'Machine Readable & API'),
        (dq.access_api == 2, 'Non-Machine Readable เช่น pdf, zip'),
    )

    api_q_s = (
        db.session.query(
            api_label.label('api_label'),
            func.count().label('api_count')
        )
        .join(package, dq.ref_id == package.id)
        .filter(package.owner_org == sub_org_id)
        .group_by(api_label)
        .all()
    )

    api_group_s = [{
        'label': row.api_label,
        'count': row.api_count,
    } for row in api_q_s]

# 4-Machine Readable Data
    # Pagination
    page_num = request.args.get('page_num', 1, type=int)
    per_page = 25
    machine_readable_table_s = (
        db.session.query(
            dq.machine_readable, 
            dq.consistency, 
            dq.validity, 
            package.name,
            package.title,
            )
            .join(package, dq.ref_id == package.id)
            .filter(package.owner_org == sub_org_id)
            .paginate(page=page_num, per_page=per_page)
        )
    machine_read = render_template('dashboard/tbl_res.txt', machine_readable_table=machine_readable_table_s)

# 5-Timeliness Data
    time_label = case(
        (and_(dq.timeliness >= 0, dq.timeliness != 999), 'อัพเดตไม่เกินเวลา'),
        (and_(dq.timeliness > -30, dq.timeliness < 0), 'อัพเดตล่าช้าไม่เกิน 1 เดือน'),
        (dq.timeliness < -30, 'อัพเดตล่าช้า 3 เดือนขึ้นไป'),
        else_='none'
    )

    time_q_s = (
        db.session.query(
            time_label.label('time_label'),
            func.count().label('time_count')
        )
        .join(package, dq.ref_id == package.id)
        .filter(time_label != 'none', package.owner_org == sub_org_id)
        .group_by(time_label)
        .all() 
        )

    time_group_s = [{
        'label': row.time_label,
        'count': row.time_count,
    } for row in time_q_s]
    
    res_data = {
        'org_count': org_child_count + 1,
        'package_count': package_count,
        'resource_count': resource_count,
        'openness_group': openness_group_s,
        'downloadable_group': downloadable_group_s,
        'api_group': api_group_s,
        'machine_readable_table': machine_read,
        'time_group': time_group_s,
    }

    return jsonify(res_data)
































