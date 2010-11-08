# Beaker
#
# Copyright (C) 2010 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys
import email
import unittest
from turbogears.database import session
from bkr.server.test import data_setup, mail_capture
import bkr.server.mail

class MailTest(unittest.TestCase):

    def setUp(self):
        self.mail_capture = mail_capture.MailCaptureThread()
        self.mail_capture.start()

    def tearDown(self):
        self.mail_capture.stop()

    def test_broken_system_notification(self):
        owner = data_setup.create_user(email_address=u'ackbar@calamari.gov')
        system = data_setup.create_system(fqdn=u'home-one', owner=owner)
        data_setup.configure_system_power(system, power_type=u'drac',
                address=u'pdu2.home-one', power_id=u'42')
        session.flush()

        bkr.server.mail.broken_system_notify(system, reason="It's a tarp!")
        self.assertEqual(len(self.mail_capture.captured_mails), 1)
        sender, rcpts, raw_msg = self.mail_capture.captured_mails[0]
        self.assertEqual(rcpts, ['ackbar@calamari.gov'])
        msg = email.message_from_string(raw_msg)
        self.assertEqual(msg['To'], 'ackbar@calamari.gov')
        self.assertEqual(msg['Subject'],
                'System home-one automatically marked broken')
        self.assertEqual(msg['X-Beaker-Notification'], 'system-broken')
        self.assertEqual(msg['X-Beaker-System'], 'home-one')
        self.assertEqual(msg.get_payload(),
                'Beaker has automatically marked system \n'
                'home-one <http://localhost:9090/view/home-one> \n'
                'as broken, due to:\n\n'
                'It\'s a tarp!\n\n'
                'Please investigate this error and take appropriate action.\n\n'
                'Power type: drac\n'
                'Power address: pdu2.home-one\n'
                'Power id: 42')
