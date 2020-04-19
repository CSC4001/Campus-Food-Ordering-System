from flask import flash, redirect, url_for, render_template, abort, Blueprint
from flask_login import  login_required, current_user
from CFO_System.models import *
from CFO_System.forms import *

admin_bp = Blueprint("admin", __name__)

@admin_bp.before_request
@login_required
def login_protect():
    pass

# TODO: add all administrator functions
'''
index route "/" : display the index of administrator panel
'''
@admin_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('admin/index.html')

'''
user management route "/user_management" : view user info
'''
@admin_bp.route('/user_management', methods=['GET', 'POST'])
def user_management():
    messages = User.query.order_by(User.user_name.desc()).all()
    return render_template('admin/user_management.html', messages=messages)

'''
shop management route "/shop_management" : view shop info
'''
@admin_bp.route('/shop_management', methods=['GET', 'POST'])
def shop_management():
    messages = Shop.query.order_by(Shop.shop_name.desc()).all()
    return render_template('admin/shop_management.html', messages=messages)

'''
open shop application route "/open_shop_application" : 
view & manage applications from users who want to create a new shop
'''
@admin_bp.route('/open_shop_application', methods=['GET', 'POST'])
def open_shop_application():
    messages = Application.query.filter_by(application_status="pending", application_type="open").all()
    return render_template('admin/open_shop_application.html', messages=messages)

'''
cancelling shop application route "/cancel_shop_application" : 
view & manage applications from users who want to shutdown their shops permanently
'''
@admin_bp.route('/cancel_shop_application', methods=['GET', 'POST'])
def cancel_shop_application():
    messages = Application.query.filter_by(application_status="pending", application_type="cancel").all()
    return render_template('admin/cancel_shop_application.html', messages=messages)

'''
unblock shop application route "/unblock_shop_application" : 
view & manage applications from users who want to unblock their shop
'''
@admin_bp.route('/unblock_shop_application', methods=['GET', 'POST'])
def unblock_shop_application():
    messages = Application.query.filter_by(application_status="pending", application_type="unblock").all()
    return render_template('admin/unblock_shop_application.html', messages=messages)

'''
detail page of application. Can approve or reject an application here
'''
@admin_bp.route('/application_detail_<int:application_id>', methods=['GET', 'POST'])
def application_detail(application_id):
    message = Application.query.filter_by(application_id=application_id).first()
    approve_form = ApproveButtonForm()
    reject_form = RejectButtonForm()
    if approve_form.submit_approve.data and  approve_form.validate():
        if message.application_type=='open':
            user = User.query.filter_by(user_id=message.user_id).first()
            new_shop = Shop(
            shop_name = message.shop_name,
            shop_info = message.shop_info,
            shop_delivery_fee = 0,
            shop_rate_total = 0,
            shop_rate_number = 0,
            shop_balance = 0,
            shop_contact = 0,
            shop_location = message.shop_location,
            shop_location_detail = message.shop_location_detail,
            shop_license_number = message.shop_license_number,
            shop_status = 'open'
            # add avatar at the last step
            #shop_avatar = img
            )
            db.session.add(new_shop)
            new_shop.user=user
            message.application_status="approved"
            db.session.commit()
            flash("You approved this application!")
            return redirect(url_for('admin.open_shop_application'))
        if message.application_type=='cancel':
            shop = Shop.query.filter_by(shop_id=message.shop_id).first()
            shop.shop_status="cancelled"
            message.application_status="approved"
            db.session.commit()
            flash("You approved this application!")
            return redirect(url_for('admin.cancel_shop_application'))
        if message.application_type=='unblock':
            shop = Shop.query.filter_by(shop_id=message.shop_id).first()
            shop.shop_status='open'
            message.application_status='approved'
            db.session.commit()
            flash("You approved this application!")
            return redirect(url_for('admin.unblock_shop_application'))
    if reject_form.submit_reject.data and reject_form.validate():
        message.application_status="denied"
        db.session.commit()
        flash("You rejected this application!")
        return redirect(url_for('admin.open_shop_application'))
    return render_template('admin/application_detail.html',message=message, approve_form=approve_form, reject_form=reject_form)

'''
detail page of a shop. Can block a shop here.
'''
@admin_bp.route('/shop_detail_<int:shop_id>', methods=['GET', 'POST'])
def shop_detail(shop_id):
    message = Shop.query.filter_by(shop_id=shop_id).first()
    block_form = BlockButtonForm()
    if block_form.validate_on_submit():
        if message.shop_status != "cancelled" and message.shop_status != "blocked":
            message.shop_status = "blocked"
            flash("Successfully block the shop!")
            db.session.commit()
        else:
            flash("Cannot do this operation. This shop is already blocked or shutdown.")
        return redirect(url_for('admin.shop_detail',shop_id=shop_id))
    return render_template('admin/shop_detail.html',message=message, block_form=block_form)
