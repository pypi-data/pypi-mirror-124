# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_kubernetes.autoscaling.v1 as __v1
    v1 = __v1
    import pulumi_kubernetes.autoscaling.v2beta1 as __v2beta1
    v2beta1 = __v2beta1
    import pulumi_kubernetes.autoscaling.v2beta2 as __v2beta2
    v2beta2 = __v2beta2
else:
    v1 = _utilities.lazy_import('pulumi_kubernetes.autoscaling.v1')
    v2beta1 = _utilities.lazy_import('pulumi_kubernetes.autoscaling.v2beta1')
    v2beta2 = _utilities.lazy_import('pulumi_kubernetes.autoscaling.v2beta2')

