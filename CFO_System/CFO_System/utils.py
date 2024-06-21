# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

# from CFO_System.settings import Operations
# from CFO_System.extensions import db
# from CFO_System.models import User

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, flash
from flask_login import current_user
from CFO_System.models import Shop




def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='shop.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def is_my_shop(shop_id):
    shop = Shop.query.filter_by(shop_id=shop_id).first_or_404()
    if shop not in current_user.shops:
        flash("This is not your shop!",'warning')
        return False
    return True
