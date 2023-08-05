from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import OperatingSystemType

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestAzureVirtualMachine(AzureContextTest):

    def get_component(self):
        return "virtual_machine"

    @context(module_path="no_os_vm")
    def test_no_os_vm(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2460-vm'))
        self.assertIsNotNone(vm)
        self.assertEqual(vm.os_type, OperatingSystemType.WINDOWS)
        self.assertEqual(len(vm.network_interfaces), 1)

    @context(module_path="linux_vm")
    def test_linux_vm(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2460-vm'))
        self.assertIsNotNone(vm)
        self.assertEqual(vm.os_type, OperatingSystemType.LINUX)
        self.assertEqual(len(vm.network_interfaces), 1)
        self.assertEqual(vm.disk_settings.data_disks, [])
        self.assertTrue(vm.disk_settings.os_disk.is_managed_disk)
        if vm.is_managed_by_iac:
            self.assertFalse(vm.disk_settings.os_disk.name)
        else:
            self.assertEqual(vm.disk_settings.os_disk.name, 'cr2460-vm_OsDisk_1_d04be4d0ac104399a71348d74c1da7fb')

    @context(module_path="windows_vm")
    def test_windows_vm(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2460-vm'))
        self.assertIsNotNone(vm)
        self.assertEqual(vm.os_type, OperatingSystemType.WINDOWS)
        self.assertEqual(len(vm.network_interfaces), 1)

    @context(module_path="no_os_managed_disk")
    def test_no_os_managed_disk(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2340-vm'))
        self.assertIsNotNone(vm)
        self.assertEqual(vm.os_type, OperatingSystemType.LINUX)
        self.assertIsNotNone(vm.disk_settings)
        self.assertTrue(vm.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(vm.disk_settings.os_disk.name, 'myosdisk1')
        self.assertFalse(vm.disk_settings.data_disks)

    @context(module_path="no_os_vm_unmanaged_disk")
    def test_no_os_vm_unmanaged_disk(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2340-vm'))
        self.assertIsNotNone(vm)
        self.assertEqual(vm.os_type, OperatingSystemType.LINUX)
        self.assertIsNotNone(vm.disk_settings)
        self.assertFalse(vm.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(vm.disk_settings.os_disk.name, 'myosdisk1')
        self.assertEqual(vm.disk_settings.data_disks, [])

    @context(module_path="no_os_vm_with_data_disks")
    def test_no_os_vm_with_data_disks(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2460-vm'))
        self.assertIsNotNone(vm)
        self.assertIsNotNone(vm.disk_settings)
        self.assertTrue(vm.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(vm.disk_settings.os_disk.name, 'myosdisk1')
        self.assertEqual(len(vm.disk_settings.data_disks), 2)
        self.assertTrue(all(data_disk.name in ('testdatadisk', 'testdatadisk2') for data_disk in vm.disk_settings.data_disks))
        self.assertTrue(all(data_disk.is_managed_disk for data_disk in vm.disk_settings.data_disks))

    @context(module_path="no_os_both_disks_unmanaged")
    def test_no_os_both_disks_unmanaged(self, ctx: AzureEnvironmentContext):
        vm = next((vm for vm in ctx.virtual_machines if vm.name == 'cr2460-vm'))
        self.assertIsNotNone(vm)
        self.assertIsNotNone(vm.disk_settings)
        self.assertFalse(vm.disk_settings.os_disk.is_managed_disk)
        self.assertEqual(len(vm.disk_settings.data_disks), 1)
        self.assertTrue(all(not data_disk.is_managed_disk for data_disk in vm.disk_settings.data_disks))
