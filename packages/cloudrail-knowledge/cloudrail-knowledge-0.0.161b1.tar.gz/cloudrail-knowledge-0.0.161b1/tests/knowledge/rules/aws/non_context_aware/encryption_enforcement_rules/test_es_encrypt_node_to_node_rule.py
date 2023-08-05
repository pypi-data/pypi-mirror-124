import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.es_encrypt_node_to_node_rule import EsEncryptNodeToNodeRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEsEncryptNodeToNodeRule(unittest.TestCase):
    def setUp(self):
        self.rule = EsEncryptNodeToNodeRule()

    def test_not_car_elasticsearch_domains_encrypted_note_to_node_fail(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        terraform_state = create_empty_entity(IacState)
        es_domain.iac_state = terraform_state
        es_domain.iac_state.is_new = True
        es_domain.encrypt_node_to_node_state = False
        es_domain.es_domain_version = '6.0'
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_elasticsearch_domains_encrypted_note_to_node__not_new__pass(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        terraform_state = create_empty_entity(IacState)
        es_domain.iac_state = terraform_state
        es_domain.iac_state.is_new = False
        es_domain.encrypt_node_to_node_state = False
        es_domain.es_domain_version = '6.0'
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_elasticsearch_domains_encrypted_note_to_node_pass(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        terraform_state = create_empty_entity(IacState)
        es_domain.iac_state = terraform_state
        es_domain.iac_state.is_new = True
        es_domain.encrypt_node_to_node_state = True
        es_domain.es_domain_version = '6.0'
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_elasticsearch_domains_encrypted_note_to_node__unsupported_ver__pass(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        terraform_state = create_empty_entity(IacState)
        es_domain.iac_state = terraform_state
        es_domain.iac_state.is_new = True
        es_domain.es_domain_version = '2.3'
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
