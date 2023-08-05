from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_athena_workgroups_results_encrypted_rule import \
    EnsureAthenaWorkGroupsResultsEncryptedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test



class TestEnsureAthenaWorkgroupsResultsEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureAthenaWorkGroupsResultsEncryptedRule()

    @rule_test('encrypted_work_groups', False)
    def test_encrypted_work_groups(self, rule_result: RuleResponse):
        pass

    @rule_test('non_encrypted_workgroups', True, 2)
    def test_non_encrypted_workgroups(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        item_1 = next((item for item in rule_result.issues if item.exposed.get_name() == 'cloudrail-wg-encrypted-sse-s3'), None)
        item_2 = next((item for item in rule_result.issues if item.exposed.get_name() == 'cloudrail-wg-encrypted-sse-s3-2'), None)
        self.assertIsNotNone(item_1)
        self.assertIsNotNone(item_2)
        self.assertTrue(all('is not set to encrypt at rest the query results' in item.evidence for item in rule_result.issues))

    @rule_test('encrypted_workgroups_not_enforced', True)
    def test_encrypted_workgroups_not_enforced(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("but the workgroup configurations are not set to enforce" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'cloudrail-wg-encrypted-sse-s3')
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Athena Workgroup')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'cloudrail-wg-encrypted-sse-s3')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Athena Workgroup')
