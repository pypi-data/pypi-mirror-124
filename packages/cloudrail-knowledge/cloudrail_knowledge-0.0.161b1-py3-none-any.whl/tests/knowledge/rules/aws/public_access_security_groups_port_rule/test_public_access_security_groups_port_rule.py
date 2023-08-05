from cloudrail.knowledge.rules.base_rule import RuleResponse
import unittest

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_security_groups_port_rule \
    import PublicAccessSecurityGroupsSshPortRule


class TestPublicAccessSecurityGroupsPortRule(AwsBaseRuleTest):

    def get_rule(self):
        return PublicAccessSecurityGroupsSshPortRule()

    @rule_test('all_ports_range', False)
    def test_all_ports_range(self, rule_result: RuleResponse):
        pass

    @rule_test('port_22_allowed_from_internet_to_ec2_explicit')
    def test_port_22_allowed_from_internet_to_ec2_explicit(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("Instance uses security group `aws_security_group.sg`."
                        " `aws_security_group.sg` allows port `22`." in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_instance.test')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'EC2 Instance')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'aws_security_group.sg.name')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')

    @rule_test('port_22_allowed_from_internet_to_ec2_using_tf_complete_vpc_module')
    def test_port_22_allowed_from_internet_to_ec2_using_tf_complete_vpc_module(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("Instance uses security group `aws_security_group.sg`."
                        " `aws_security_group.sg` allows port `22`." in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_instance.test')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'EC2 Instance')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'aws_security_group.sg.name')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')

    @rule_test('port_22_allowed_from_internet_but_instance_on_private_subnet', False)
    def test_port_22_allowed_from_internet_but_instance_on_private_subnet(self, rule_result: RuleResponse):
        pass

    @rule_test('port_22_allowed_from_internet_to_ec2_using_tf_ssh_module', True)
    def test_port_22_allowed_from_internet_to_ec2_using_tf_ssh_module(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("allows port `22`." in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_instance.test')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'EC2 Instance')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')

    @rule_test('port_22_allowed_from_internet_to_ec2_using_tf_instance_module', True)
    def test_port_22_allowed_from_internet_to_ec2_using_tf_instance_module(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("allows port `22`." in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'PublicAccessSecurityGroupsPort test - use case 4')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'EC2 Instance')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')

    @rule_test('port_22_allowed_from_internet_to_load_balancer_explicit', True)
    def test_port_22_allowed_from_internet_to_load_balancer_explicit(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("allows port `22`." in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'aws_lb.test.name')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Load Balancer')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')

    @rule_test('load_balancer_listens_to_different_port', False)
    def test_load_balancer_listens_to_different_port(self, rule_result: RuleResponse):
        pass

    @rule_test('load_balancer_no_listener', False)
    def test_load_balancer_no_listener(self, rule_result: RuleResponse):
        pass

    @rule_test('load_balancer_internal', False)
    def test_load_balancer_internal(self, rule_result: RuleResponse):
        pass

    @unittest.skip("Waiting for Idan's fix, see CR-282")
    @rule_test('port_22_allowed_from_internet_to_ecs_using_modules', True)
    def test_port_22_allowed_from_internet_to_ecs_using_modules(self, rule_result: RuleResponse):
        pass

    @rule_test('atlantis_only', False)
    def test_atlantis_only(self, rule_result: RuleResponse):
        pass

    @rule_test('bastion_server', True)
    def test_bastion_server(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("allows port `22`." in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'test-dev-bastion')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'EC2 Instance')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'test-dev-bastion')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')

    @rule_test('auto-scaling-group-public-ip-exposure', True)
    def test_auto_scaling_group_public_ip_exposure(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("allows port `22`." in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'test-autoscaling-group-pseudo-instance-subnet-public-subnet')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'EC2 Instance')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'aws_security_group.allow-ssh.name')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')

    @rule_test('auto-scaling-group-public-ip-not-exposure', False)
    def test_auto_scaling_group_public_ip_not_exposure(self, rule_result: RuleResponse):
        pass

    @rule_test('port_22_allowed_from_internet_to_ec2_instances_from_launch_config', True, 2)
    def test_port_22_allowed_from_internet_to_ec2_instances_from_launch_config(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        for issue_item in rule_result.issues:
            self.assertTrue("`aws_security_group.default` allows port `22`" in issue_item.evidence)
            self.assertTrue(issue_item.exposed.is_pseudo)
            self.assertEqual(issue_item.violating.get_type(), 'Security group')

    @rule_test('neptune_cluster_public_access_test_exclude', False)
    def test_neptune_cluster_public_access_test_exclude(self, rule_result: RuleResponse):
        pass
