from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_rds_rule import PublicAccessDbRdsRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestPublicAccessDbRdsRule(AwsBaseRuleTest):

    def get_rule(self):
        return PublicAccessDbRdsRule()

    @rule_test('aurora/defaults-only', False)  # No instances, so no issues
    def test_aurora_defaults_only(self, rule_result: RuleResponse):
        pass

    @rule_test('aurora/vpc-controlled', False)  # No instances, so no issues
    def test_aurora_vpc_controlled(self, rule_result: RuleResponse):
        pass

    # 2 instances with 2 ENI's each resulting in 4 connections but we only take the first issue for each instance. so 2 issues
    @rule_test('aurora/vpc-controlled-public', True, 1)
    def test_aurora_vpc_controlled_public(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("RDS Instance uses subnet(s) `aws_security_group.nondefault`." in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_rds_cluster.test')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'RDS DB cluster')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'aws_security_group.nondefault.name')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')

    @rule_test('individual-instance/defaults-only', False)  # Not publicly accessible + Not in VPC
    def test_individual_defaults_only(self, rule_result: RuleResponse):
        pass

    @rule_test('individual-instance/defaults-with-public-on', False)  # Not in VPC
    def test_individual_defaults_with_public_on(self, rule_result: RuleResponse):
        pass

    @rule_test('individual-instance/vpc-controlled-not-public', False)  # Not public
    def test_individual_vpc_controlled_not_public(self, rule_result: RuleResponse):
        pass

    # 1 instance with 2 ENI resulting in 2 connections but we only take the first issue for each instance so 1 issue
    @rule_test('individual-instance/vpc-controlled-public', True, 1)
    def test_individual_vpc_controlled_public(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("RDS Instance uses the subnets `aws_subnet.nondefault_1, aws_subnet.nondefault_2`."
                        " RDS Instance is reachable" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_db_instance.test')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'RDS Instance')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'aws_security_group.nondefault.name')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')
