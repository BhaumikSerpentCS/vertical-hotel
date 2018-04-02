# See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class ActivityReport(models.AbstractModel):
    _name = 'report.hotel_housekeeping.housekeeping_report'

    def get_room_activity_detail(self, date_start, date_end, room_no):
        activity_detail = []
        act_val = {}
        house_keep_act_obj = self.env['hotel.housekeeping.activities']

        act_domain = [('clean_start_time', '>=', date_start),
                      ('clean_end_time', '<=', date_end),
                      ('a_list', '=', room_no)]
        activity_line_ids = house_keep_act_obj.search(act_domain)

        for activity in activity_line_ids:
            ss_date = datetime.strptime(activity.clean_start_time,
                                        DEFAULT_SERVER_DATETIME_FORMAT)
            ee_date = datetime.strptime(activity.clean_end_time,
                                        DEFAULT_SERVER_DATETIME_FORMAT)
            diff = ee_date - ss_date

            act_val.update({'current_date': activity.today_date,
                            'activity': (activity.activity_name and
                                         activity.activity_name.name or
                                         ''),
                            'login': (activity.housekeeper and
                                      activity.housekeeper.name or ''),
                            'clean_start_time': activity.clean_start_time,
                            'clean_end_time': activity.clean_end_time,
                            'duration': diff})
            activity_detail.append(act_val)
        return activity_detail

    @api.model
    def get_report_values(self, docids, data):
        self.model = self.env.context.get('active_model')
        if data == None:
            data = {}
        if not docids:
            docids = data['form'].get('docids')
        activity_doc = self.env['hotel.housekeeping.activities'].browse(docids)
        date_start = data['form'].get('date_start', fields.Date.today())
        date_end = data['form'].get('date_end', str(datetime.now() +
                                                    relativedelta(months=+1,
                                                                  day=1, days=-1))[:10])
        room_no = data['form'].get('room_no')[0]
        return {
            'doc_ids': docids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': activity_doc,
            'time': time,
            'activity_detail': self.get_room_activity_detail(date_start,
                                                             date_end, room_no)
        }
