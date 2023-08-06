# Copyright (c) 2021 Red Hat
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import absolute_import

import testtools
from oslo_log import log

import tobiko
from tobiko.openstack import keystone
from tobiko.openstack import octavia
from tobiko.openstack import stacks
from tobiko import tripleo


LOG = log.getLogger(__name__)


@keystone.skip_if_missing_service(name='octavia')
@tripleo.skip_if_missing_overcloud
class OctaviaBasicFaultTest(testtools.TestCase):
    """Octavia fault scenario test.

    Create a load balancer with 2 members that run a server application,
    Create a client that is connected to the load balancer VIP port,
    Generate network traffic from the client to the load balanacer VIP.
    Restart the amphora's compute node to create a failover.
    Reach the members to make sure they are ready to be checked.
    Generate network traffic again to verify Octavia functionality.
    """
    loadbalancer_stack = tobiko.required_setup_fixture(
        stacks.OctaviaLoadbalancerStackFixture)

    listener_stack = tobiko.required_setup_fixture(
        stacks.OctaviaListenerStackFixture)

    pool_stack = tobiko.required_setup_fixture(
        stacks.OctaviaPoolStackFixture)

    member1_stack = tobiko.required_setup_fixture(
        stacks.OctaviaMemberServerStackFixture)

    member2_stack = tobiko.required_setup_fixture(
        stacks.OctaviaOtherMemberServerStackFixture)

    members_count = 2

    def setUp(self):
        # pylint: disable=no-member
        super(OctaviaBasicFaultTest, self).setUp()

        # Skipping the test in case the topology is Active/Standby
        if len(octavia.list_amphorae(
                self.loadbalancer_stack.loadbalancer_id)) > 1:
            tobiko.skip_test('Fault tests to Active/Standby topology were not'
                             ' implemented yet')

        # Wait for Octavia objects to be active
        octavia.wait_for_active_members_and_lb(
                members=[self.member1_stack.member_id,
                         self.member2_stack.member_id],
                pool_id=self.pool_stack.pool_id,
                loadbalancer_id=self.loadbalancer_stack.loadbalancer_id)

        # Send traffic
        octavia.check_members_balanced(
            members_count=self.members_count,
            ip_address=self.loadbalancer_stack.floating_ip_address,
            lb_algorithm=self.pool_stack.lb_algorithm,
            protocol=self.listener_stack.lb_protocol,
            port=self.listener_stack.lb_port)

    def test_reboot_amphora_compute_node(self):
        amphora_compute_hosts = octavia.get_amphoras_compute_nodes(
            self.loadbalancer_stack.loadbalancer_id)

        LOG.debug('Rebooting compute node...')

        # Reboot Amphora's compute node will initiate a failover
        amphora_compute_hosts[0].reboot_overcloud_node()

        LOG.debug('Compute node has been rebooted')

        # Wait for LB to be updated and active
        octavia.wait_for_lb_to_be_updated_and_active(
                self.loadbalancer_stack.loadbalancer_id)

        LOG.debug(f'Load Balancer {self.loadbalancer_stack.loadbalancer_id} is'
                  f' ACTIVE')

        # Wait for Octavia objects' provisioning status to be ACTIVE
        octavia.wait_for_active_and_functional_members_and_lb(
            members=[self.member1_stack,
                     self.member2_stack],
            pool_id=self.pool_stack.pool_id,
            lb_protocol=self.listener_stack.lb_protocol,
            lb_port=self.listener_stack.lb_port,
            loadbalancer_id=self.loadbalancer_stack.loadbalancer_id)

        # Verify Octavia functionality
        octavia.check_members_balanced(
            members_count=self.members_count,
            ip_address=self.loadbalancer_stack.floating_ip_address,
            lb_algorithm=self.pool_stack.lb_algorithm,
            protocol=self.listener_stack.lb_protocol,
            port=self.listener_stack.lb_port)
