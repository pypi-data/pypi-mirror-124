from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_in_transit.ensure_cloudfront_distribution_field_level_encryption_rule import \
    EnsureCloudfrontDistributionFieldLevelEncryptionRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureCloudfrontDistributionFieldLevelEncryptionRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudfrontDistributionFieldLevelEncryptionRule()

    @rule_test('field_level_encryption_enabled', False)
    def test_field_level_encryption_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('protocol_viewer_policy_allow_all', True)
    def test_protocol_viewer_policy_allow_all(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("is not set to use Field Level Encryption to protect data in transit in default_cache_behavior and in"
                        " [\'ordered_cache_behavior #1\', \'ordered_cache_behavior #2\']" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudFront Distribution')
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_cloudfront_distribution.s3_distribution')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudFront Distribution')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_cloudfront_distribution.s3_distribution')
