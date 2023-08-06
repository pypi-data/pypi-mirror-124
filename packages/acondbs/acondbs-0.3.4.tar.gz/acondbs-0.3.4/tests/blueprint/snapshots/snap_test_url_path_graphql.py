# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_graphql 1'] = {
    'data': {
        'webConfig': {
            'headTitle': 'Product DB (test)',
            'toolbarTitle': 'Product DB (test)'
        }
    }
}
