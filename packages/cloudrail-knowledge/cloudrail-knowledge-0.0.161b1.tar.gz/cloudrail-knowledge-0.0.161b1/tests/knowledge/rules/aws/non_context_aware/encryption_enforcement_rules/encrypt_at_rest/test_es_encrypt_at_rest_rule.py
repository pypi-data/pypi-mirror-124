import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.es_encrypt_at_rest_rule import EsEncryptAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEsEncryptAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EsEncryptAtRestRule()

    def test_non_car_es_domain_encrypt_at_rest_creating_fail(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        terraform_state = create_empty_entity(IacState)
        es_domain.iac_state = terraform_state
        es_domain.iac_state.is_new = True
        es_domain.encrypt_at_rest_state = False
        es_domain.es_domain_cluster_instance_type = 'i3.large.elasticsearch'
        es_domain.es_domain_version = '5.1'
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_es_domain_encrypt_at_rest_creating_pass(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        terraform_state = create_empty_entity(IacState)
        es_domain.iac_state = terraform_state
        es_domain.iac_state.is_new = True
        es_domain.encrypt_at_rest_state = True
        es_domain.es_domain_cluster_instance_type = 'i3.large.elasticsearch'
        es_domain.es_domain_version = '5.1'
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_es_domain_encrypt_at_rest_creating__not_new__pass(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        terraform_state = create_empty_entity(IacState)
        es_domain.iac_state = terraform_state
        es_domain.iac_state.is_new = False
        es_domain.encrypt_at_rest_state = False
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_es_domain_encrypt_at_rest_creating__not_supported_ver__pass(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        terraform_state = create_empty_entity(IacState)
        es_domain.iac_state = terraform_state
        es_domain.iac_state.is_new = True
        es_domain.encrypt_at_rest_state = True
        es_domain.es_domain_cluster_instance_type = 'i3.large.elasticsearch'
        es_domain.es_domain_version = '4.5'
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_es_domain_encrypt_at_rest_creating__not_supported_inst_type__pass(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        terraform_state = create_empty_entity(IacState)
        es_domain.iac_state = terraform_state
        es_domain.iac_state.is_new = True
        es_domain.encrypt_at_rest_state = True
        es_domain.es_domain_cluster_instance_type = 'r3.4xlarge.elasticsearch'
        es_domain.es_domain_version = '5.1'
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
