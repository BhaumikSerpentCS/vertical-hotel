# See LICENSE file for full copyright and licensing details.

from odoo import models


class HotelFrontdesk(models.Model):
    _name = "hotel.test.reserv"

    def _get_action(self, action_xmlid):
        # TDE TODO check to have one view + custom in methods
        action = self.env.ref(action_xmlid).read()[0]
        if self:
            action['display_name'] = self.display_name
        return action

    def get_action_view_frontdesk_cal(self):
        return self._get_action('board_frontdesk.action_view_frontdesk_cal')

    def get_action_hotel_reservation_summary(self):
        return self.\
            _get_action('board_frontdesk.action_hotel_reservation_summary')

    def get_action_hotel_room_board(self):
        return self._get_action('board_frontdesk.action_hotel_room_board')

    def get_action_hotel_restaurant_order(self):
        return self.\
            _get_action('board_frontdesk.action_hotel_restaurant_order')

    def get_action_table_order_board(self):
        return self._get_action('board_frontdesk.action_table_order_board')
