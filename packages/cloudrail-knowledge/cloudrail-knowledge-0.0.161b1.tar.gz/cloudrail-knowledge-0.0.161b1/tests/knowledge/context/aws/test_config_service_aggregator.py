from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestConfigAggregator(AwsContextTest):

    def get_component(self):
        return "configservice/config_aggregator"

    @context(module_path="account_all_regions_disabled")
    def test_account_all_regions_disabled(self, ctx: AwsEnvironmentContext):
        aggregator = next((aggregator for aggregator in ctx.aws_config_aggregators
                           if aggregator.aggregator_name == 'all_regions_disabled_organization'), None)
        self.assertIsNotNone(aggregator)
        self.assertTrue(aggregator.arn)
        self.assertTrue(aggregator.account_aggregation_used)
        self.assertFalse(aggregator.account_aggregation_all_regions_enabled)
        self.assertFalse(aggregator.organization_aggregation_used)

    @context(module_path="account_all_regions_enabled")
    def test_account_all_regions_enabled(self, ctx: AwsEnvironmentContext):
        aggregator = next((aggregator for aggregator in ctx.aws_config_aggregators
                           if aggregator.aggregator_name == 'all_regions_enabled_account'), None)
        self.assertIsNotNone(aggregator)
        self.assertTrue(aggregator.arn)
        self.assertTrue(aggregator.account_aggregation_used)
        self.assertTrue(aggregator.account_aggregation_all_regions_enabled)
        self.assertFalse(aggregator.organization_aggregation_used)

    # Not running drift as unable to create drift data - need additional permissions for the account
    @context(module_path="organization_all_regions_disabled", test_options=TestOptions(run_drift_detection=False))
    def test_organization_all_regions_disabled(self, ctx: AwsEnvironmentContext):
        aggregator = next((aggregator for aggregator in ctx.aws_config_aggregators
                           if aggregator.aggregator_name == 'all_regions_disabled_organization'), None)
        self.assertIsNotNone(aggregator)
        self.assertTrue(aggregator.arn)
        self.assertFalse(aggregator.account_aggregation_used)
        self.assertTrue(aggregator.organization_aggregation_used)
        self.assertFalse(aggregator.organization_aggregation_all_regions_enabled)

    # Not running drift as unable to create drift data - need additional permissions for the account
    @context(module_path="organization_all_regions_enabled", test_options=TestOptions(run_drift_detection=False))
    def test_organization_all_regions_enabled(self, ctx: AwsEnvironmentContext):
        aggregator = next((aggregator for aggregator in ctx.aws_config_aggregators
                           if aggregator.aggregator_name == 'all_regions_enabled_organization'), None)
        self.assertIsNotNone(aggregator)
        self.assertTrue(aggregator.arn)
        self.assertFalse(aggregator.account_aggregation_used)
        self.assertTrue(aggregator.organization_aggregation_used)
        self.assertTrue(aggregator.organization_aggregation_all_regions_enabled)
