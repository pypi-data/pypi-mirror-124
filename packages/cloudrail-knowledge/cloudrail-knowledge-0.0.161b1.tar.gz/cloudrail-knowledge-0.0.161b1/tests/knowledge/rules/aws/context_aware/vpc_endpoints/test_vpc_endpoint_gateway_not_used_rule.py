
# import unittest
#
# from .cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
# from cloudrail.knowledge.rules.base_rule import RuleResultType
# from cloudrail.dev_tools.rule_test_utils import create_empty_entity
#
#
# class TestDynamoDbVpcEndpointGatewayNotUsedRule(unittest.TestCase):
#     def setUp(self):
#         self.rule = DynamoDbVpcEndpointGatewayNotUsedRule()
#
#     def test_vpc_endpoint_dynamodb_exposure_fail(self):
#         # Arrange
#         context = AwsEnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.FAILED, result.status)
#         self.assertEqual(1, len(result.issues))
#
#     def test_vpc_endpoint_dynamodb_exposure_pass(self):
#         # Arrange
#         context = AwsEnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.SUCCESS, result.status)
#         self.assertEqual(0, len(result.issues))
