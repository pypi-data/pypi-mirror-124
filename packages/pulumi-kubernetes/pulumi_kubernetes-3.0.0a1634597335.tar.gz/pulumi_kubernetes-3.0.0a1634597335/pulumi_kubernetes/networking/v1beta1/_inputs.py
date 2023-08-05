# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ... import core as _core
from ... import meta as _meta

__all__ = [
    'HTTPIngressPathArgs',
    'HTTPIngressRuleValueArgs',
    'IngressBackendArgs',
    'IngressClassSpecArgs',
    'IngressClassArgs',
    'IngressRuleArgs',
    'IngressSpecArgs',
    'IngressStatusArgs',
    'IngressTLSArgs',
    'IngressArgs',
]

@pulumi.input_type
class HTTPIngressPathArgs:
    def __init__(__self__, *,
                 backend: pulumi.Input['IngressBackendArgs'],
                 path: Optional[pulumi.Input[str]] = None,
                 path_type: Optional[pulumi.Input[str]] = None):
        """
        HTTPIngressPath associates a path regex with a backend. Incoming urls matching the path are forwarded to the backend.
        :param pulumi.Input['IngressBackendArgs'] backend: Backend defines the referenced service endpoint to which the traffic will be forwarded to.
        :param pulumi.Input[str] path: Path is an extended POSIX regex as defined by IEEE Std 1003.1, (i.e this follows the egrep/unix syntax, not the perl syntax) matched against the path of an incoming request. Currently it can contain characters disallowed from the conventional "path" part of a URL as defined by RFC 3986. Paths must begin with a '/'. If unspecified, the path defaults to a catch all sending traffic to the backend.
        :param pulumi.Input[str] path_type: PathType determines the interpretation of the Path matching. PathType can be one of the following values: * Exact: Matches the URL path exactly. * Prefix: Matches based on a URL path prefix split by '/'. Matching is
                 done on a path element by element basis. A path element refers is the
                 list of labels in the path split by the '/' separator. A request is a
                 match for path p if every p is an element-wise prefix of p of the
                 request path. Note that if the last element of the path is a substring
                 of the last element in request path, it is not a match (e.g. /foo/bar
                 matches /foo/bar/baz, but does not match /foo/barbaz).
               * ImplementationSpecific: Interpretation of the Path matching is up to
                 the IngressClass. Implementations can treat this as a separate PathType
                 or treat it identically to Prefix or Exact path types.
               Implementations are required to support all path types. Defaults to ImplementationSpecific.
        """
        pulumi.set(__self__, "backend", backend)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if path_type is not None:
            pulumi.set(__self__, "path_type", path_type)

    @property
    @pulumi.getter
    def backend(self) -> pulumi.Input['IngressBackendArgs']:
        """
        Backend defines the referenced service endpoint to which the traffic will be forwarded to.
        """
        return pulumi.get(self, "backend")

    @backend.setter
    def backend(self, value: pulumi.Input['IngressBackendArgs']):
        pulumi.set(self, "backend", value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        """
        Path is an extended POSIX regex as defined by IEEE Std 1003.1, (i.e this follows the egrep/unix syntax, not the perl syntax) matched against the path of an incoming request. Currently it can contain characters disallowed from the conventional "path" part of a URL as defined by RFC 3986. Paths must begin with a '/'. If unspecified, the path defaults to a catch all sending traffic to the backend.
        """
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)

    @property
    @pulumi.getter(name="pathType")
    def path_type(self) -> Optional[pulumi.Input[str]]:
        """
        PathType determines the interpretation of the Path matching. PathType can be one of the following values: * Exact: Matches the URL path exactly. * Prefix: Matches based on a URL path prefix split by '/'. Matching is
          done on a path element by element basis. A path element refers is the
          list of labels in the path split by the '/' separator. A request is a
          match for path p if every p is an element-wise prefix of p of the
          request path. Note that if the last element of the path is a substring
          of the last element in request path, it is not a match (e.g. /foo/bar
          matches /foo/bar/baz, but does not match /foo/barbaz).
        * ImplementationSpecific: Interpretation of the Path matching is up to
          the IngressClass. Implementations can treat this as a separate PathType
          or treat it identically to Prefix or Exact path types.
        Implementations are required to support all path types. Defaults to ImplementationSpecific.
        """
        return pulumi.get(self, "path_type")

    @path_type.setter
    def path_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path_type", value)


@pulumi.input_type
class HTTPIngressRuleValueArgs:
    def __init__(__self__, *,
                 paths: pulumi.Input[Sequence[pulumi.Input['HTTPIngressPathArgs']]]):
        """
        HTTPIngressRuleValue is a list of http selectors pointing to backends. In the example: http://<host>/<path>?<searchpart> -> backend where where parts of the url correspond to RFC 3986, this resource will be used to match against everything after the last '/' and before the first '?' or '#'.
        :param pulumi.Input[Sequence[pulumi.Input['HTTPIngressPathArgs']]] paths: A collection of paths that map requests to backends.
        """
        pulumi.set(__self__, "paths", paths)

    @property
    @pulumi.getter
    def paths(self) -> pulumi.Input[Sequence[pulumi.Input['HTTPIngressPathArgs']]]:
        """
        A collection of paths that map requests to backends.
        """
        return pulumi.get(self, "paths")

    @paths.setter
    def paths(self, value: pulumi.Input[Sequence[pulumi.Input['HTTPIngressPathArgs']]]):
        pulumi.set(self, "paths", value)


@pulumi.input_type
class IngressBackendArgs:
    def __init__(__self__, *,
                 service_name: pulumi.Input[str],
                 service_port: pulumi.Input[Union[int, str]],
                 resource: Optional[pulumi.Input['_core.v1.TypedLocalObjectReferenceArgs']] = None):
        """
        IngressBackend describes all endpoints for a given service and port.
        :param pulumi.Input[str] service_name: Specifies the name of the referenced service.
        :param pulumi.Input[Union[int, str]] service_port: Specifies the port of the referenced service.
        :param pulumi.Input['_core.v1.TypedLocalObjectReferenceArgs'] resource: Resource is an ObjectRef to another Kubernetes resource in the namespace of the Ingress object. If resource is specified, serviceName and servicePort must not be specified.
        """
        pulumi.set(__self__, "service_name", service_name)
        pulumi.set(__self__, "service_port", service_port)
        if resource is not None:
            pulumi.set(__self__, "resource", resource)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the referenced service.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter(name="servicePort")
    def service_port(self) -> pulumi.Input[Union[int, str]]:
        """
        Specifies the port of the referenced service.
        """
        return pulumi.get(self, "service_port")

    @service_port.setter
    def service_port(self, value: pulumi.Input[Union[int, str]]):
        pulumi.set(self, "service_port", value)

    @property
    @pulumi.getter
    def resource(self) -> Optional[pulumi.Input['_core.v1.TypedLocalObjectReferenceArgs']]:
        """
        Resource is an ObjectRef to another Kubernetes resource in the namespace of the Ingress object. If resource is specified, serviceName and servicePort must not be specified.
        """
        return pulumi.get(self, "resource")

    @resource.setter
    def resource(self, value: Optional[pulumi.Input['_core.v1.TypedLocalObjectReferenceArgs']]):
        pulumi.set(self, "resource", value)


@pulumi.input_type
class IngressClassSpecArgs:
    def __init__(__self__, *,
                 controller: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input['_core.v1.TypedLocalObjectReferenceArgs']] = None):
        """
        IngressClassSpec provides information about the class of an Ingress.
        :param pulumi.Input[str] controller: Controller refers to the name of the controller that should handle this class. This allows for different "flavors" that are controlled by the same controller. For example, you may have different Parameters for the same implementing controller. This should be specified as a domain-prefixed path no more than 250 characters in length, e.g. "acme.io/ingress-controller". This field is immutable.
        :param pulumi.Input['_core.v1.TypedLocalObjectReferenceArgs'] parameters: Parameters is a link to a custom resource containing additional configuration for the controller. This is optional if the controller does not require extra parameters.
        """
        if controller is not None:
            pulumi.set(__self__, "controller", controller)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)

    @property
    @pulumi.getter
    def controller(self) -> Optional[pulumi.Input[str]]:
        """
        Controller refers to the name of the controller that should handle this class. This allows for different "flavors" that are controlled by the same controller. For example, you may have different Parameters for the same implementing controller. This should be specified as a domain-prefixed path no more than 250 characters in length, e.g. "acme.io/ingress-controller". This field is immutable.
        """
        return pulumi.get(self, "controller")

    @controller.setter
    def controller(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "controller", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input['_core.v1.TypedLocalObjectReferenceArgs']]:
        """
        Parameters is a link to a custom resource containing additional configuration for the controller. This is optional if the controller does not require extra parameters.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input['_core.v1.TypedLocalObjectReferenceArgs']]):
        pulumi.set(self, "parameters", value)


@pulumi.input_type
class IngressClassArgs:
    def __init__(__self__, *,
                 api_version: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']] = None,
                 spec: Optional[pulumi.Input['IngressClassSpecArgs']] = None):
        """
        IngressClass represents the class of the Ingress, referenced by the Ingress Spec. The `ingressclass.kubernetes.io/is-default-class` annotation can be used to indicate that an IngressClass should be considered default. When a single IngressClass resource has this annotation set to true, new Ingress resources without a class specified will be assigned this default class.
        :param pulumi.Input[str] api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param pulumi.Input[str] kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        :param pulumi.Input['_meta.v1.ObjectMetaArgs'] metadata: Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        :param pulumi.Input['IngressClassSpecArgs'] spec: Spec is the desired state of the IngressClass. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        """
        if api_version is not None:
            pulumi.set(__self__, "api_version", 'networking.k8s.io/v1beta1')
        if kind is not None:
            pulumi.set(__self__, "kind", 'IngressClass')
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if spec is not None:
            pulumi.set(__self__, "spec", spec)

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> Optional[pulumi.Input[str]]:
        """
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        """
        return pulumi.get(self, "api_version")

    @api_version.setter
    def api_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_version", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']]:
        """
        Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        """
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']]):
        pulumi.set(self, "metadata", value)

    @property
    @pulumi.getter
    def spec(self) -> Optional[pulumi.Input['IngressClassSpecArgs']]:
        """
        Spec is the desired state of the IngressClass. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        """
        return pulumi.get(self, "spec")

    @spec.setter
    def spec(self, value: Optional[pulumi.Input['IngressClassSpecArgs']]):
        pulumi.set(self, "spec", value)


@pulumi.input_type
class IngressRuleArgs:
    def __init__(__self__, *,
                 host: Optional[pulumi.Input[str]] = None,
                 http: Optional[pulumi.Input['HTTPIngressRuleValueArgs']] = None):
        """
        IngressRule represents the rules mapping the paths under a specified host to the related backend services. Incoming requests are first evaluated for a host match, then routed to the backend associated with the matching IngressRuleValue.
        :param pulumi.Input[str] host: Host is the fully qualified domain name of a network host, as defined by RFC 3986. Note the following deviations from the "host" part of the URI as defined in the RFC: 1. IPs are not allowed. Currently an IngressRuleValue can only apply to the
               	  IP in the Spec of the parent Ingress.
               2. The `:` delimiter is not respected because ports are not allowed.
               	  Currently the port of an Ingress is implicitly :80 for http and
               	  :443 for https.
               Both these may change in the future. Incoming requests are matched against the host before the IngressRuleValue. If the host is unspecified, the Ingress routes all traffic based on the specified IngressRuleValue.
        """
        if host is not None:
            pulumi.set(__self__, "host", host)
        if http is not None:
            pulumi.set(__self__, "http", http)

    @property
    @pulumi.getter
    def host(self) -> Optional[pulumi.Input[str]]:
        """
        Host is the fully qualified domain name of a network host, as defined by RFC 3986. Note the following deviations from the "host" part of the URI as defined in the RFC: 1. IPs are not allowed. Currently an IngressRuleValue can only apply to the
        	  IP in the Spec of the parent Ingress.
        2. The `:` delimiter is not respected because ports are not allowed.
        	  Currently the port of an Ingress is implicitly :80 for http and
        	  :443 for https.
        Both these may change in the future. Incoming requests are matched against the host before the IngressRuleValue. If the host is unspecified, the Ingress routes all traffic based on the specified IngressRuleValue.
        """
        return pulumi.get(self, "host")

    @host.setter
    def host(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host", value)

    @property
    @pulumi.getter
    def http(self) -> Optional[pulumi.Input['HTTPIngressRuleValueArgs']]:
        return pulumi.get(self, "http")

    @http.setter
    def http(self, value: Optional[pulumi.Input['HTTPIngressRuleValueArgs']]):
        pulumi.set(self, "http", value)


@pulumi.input_type
class IngressSpecArgs:
    def __init__(__self__, *,
                 backend: Optional[pulumi.Input['IngressBackendArgs']] = None,
                 ingress_class_name: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Sequence[pulumi.Input['IngressRuleArgs']]]] = None,
                 tls: Optional[pulumi.Input[Sequence[pulumi.Input['IngressTLSArgs']]]] = None):
        """
        IngressSpec describes the Ingress the user wishes to exist.
        :param pulumi.Input['IngressBackendArgs'] backend: A default backend capable of servicing requests that don't match any rule. At least one of 'backend' or 'rules' must be specified. This field is optional to allow the loadbalancer controller or defaulting logic to specify a global default.
        :param pulumi.Input[str] ingress_class_name: IngressClassName is the name of the IngressClass cluster resource. The associated IngressClass defines which controller will implement the resource. This replaces the deprecated `kubernetes.io/ingress.class` annotation. For backwards compatibility, when that annotation is set, it must be given precedence over this field. The controller may emit a warning if the field and annotation have different values. Implementations of this API should ignore Ingresses without a class specified. An IngressClass resource may be marked as default, which can be used to set a default value for this field. For more information, refer to the IngressClass documentation.
        :param pulumi.Input[Sequence[pulumi.Input['IngressRuleArgs']]] rules: A list of host rules used to configure the Ingress. If unspecified, or no rule matches, all traffic is sent to the default backend.
        :param pulumi.Input[Sequence[pulumi.Input['IngressTLSArgs']]] tls: TLS configuration. Currently the Ingress only supports a single TLS port, 443. If multiple members of this list specify different hosts, they will be multiplexed on the same port according to the hostname specified through the SNI TLS extension, if the ingress controller fulfilling the ingress supports SNI.
        """
        if backend is not None:
            pulumi.set(__self__, "backend", backend)
        if ingress_class_name is not None:
            pulumi.set(__self__, "ingress_class_name", ingress_class_name)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)
        if tls is not None:
            pulumi.set(__self__, "tls", tls)

    @property
    @pulumi.getter
    def backend(self) -> Optional[pulumi.Input['IngressBackendArgs']]:
        """
        A default backend capable of servicing requests that don't match any rule. At least one of 'backend' or 'rules' must be specified. This field is optional to allow the loadbalancer controller or defaulting logic to specify a global default.
        """
        return pulumi.get(self, "backend")

    @backend.setter
    def backend(self, value: Optional[pulumi.Input['IngressBackendArgs']]):
        pulumi.set(self, "backend", value)

    @property
    @pulumi.getter(name="ingressClassName")
    def ingress_class_name(self) -> Optional[pulumi.Input[str]]:
        """
        IngressClassName is the name of the IngressClass cluster resource. The associated IngressClass defines which controller will implement the resource. This replaces the deprecated `kubernetes.io/ingress.class` annotation. For backwards compatibility, when that annotation is set, it must be given precedence over this field. The controller may emit a warning if the field and annotation have different values. Implementations of this API should ignore Ingresses without a class specified. An IngressClass resource may be marked as default, which can be used to set a default value for this field. For more information, refer to the IngressClass documentation.
        """
        return pulumi.get(self, "ingress_class_name")

    @ingress_class_name.setter
    def ingress_class_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ingress_class_name", value)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IngressRuleArgs']]]]:
        """
        A list of host rules used to configure the Ingress. If unspecified, or no rule matches, all traffic is sent to the default backend.
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IngressRuleArgs']]]]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter
    def tls(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IngressTLSArgs']]]]:
        """
        TLS configuration. Currently the Ingress only supports a single TLS port, 443. If multiple members of this list specify different hosts, they will be multiplexed on the same port according to the hostname specified through the SNI TLS extension, if the ingress controller fulfilling the ingress supports SNI.
        """
        return pulumi.get(self, "tls")

    @tls.setter
    def tls(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IngressTLSArgs']]]]):
        pulumi.set(self, "tls", value)


@pulumi.input_type
class IngressStatusArgs:
    def __init__(__self__, *,
                 load_balancer: Optional[pulumi.Input['_core.v1.LoadBalancerStatusArgs']] = None):
        """
        IngressStatus describe the current state of the Ingress.
        :param pulumi.Input['_core.v1.LoadBalancerStatusArgs'] load_balancer: LoadBalancer contains the current status of the load-balancer.
        """
        if load_balancer is not None:
            pulumi.set(__self__, "load_balancer", load_balancer)

    @property
    @pulumi.getter(name="loadBalancer")
    def load_balancer(self) -> Optional[pulumi.Input['_core.v1.LoadBalancerStatusArgs']]:
        """
        LoadBalancer contains the current status of the load-balancer.
        """
        return pulumi.get(self, "load_balancer")

    @load_balancer.setter
    def load_balancer(self, value: Optional[pulumi.Input['_core.v1.LoadBalancerStatusArgs']]):
        pulumi.set(self, "load_balancer", value)


@pulumi.input_type
class IngressTLSArgs:
    def __init__(__self__, *,
                 hosts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 secret_name: Optional[pulumi.Input[str]] = None):
        """
        IngressTLS describes the transport layer security associated with an Ingress.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] hosts: Hosts are a list of hosts included in the TLS certificate. The values in this list must match the name/s used in the tlsSecret. Defaults to the wildcard host setting for the loadbalancer controller fulfilling this Ingress, if left unspecified.
        :param pulumi.Input[str] secret_name: SecretName is the name of the secret used to terminate SSL traffic on 443. Field is left optional to allow SSL routing based on SNI hostname alone. If the SNI host in a listener conflicts with the "Host" header field used by an IngressRule, the SNI host is used for termination and value of the Host header is used for routing.
        """
        if hosts is not None:
            pulumi.set(__self__, "hosts", hosts)
        if secret_name is not None:
            pulumi.set(__self__, "secret_name", secret_name)

    @property
    @pulumi.getter
    def hosts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Hosts are a list of hosts included in the TLS certificate. The values in this list must match the name/s used in the tlsSecret. Defaults to the wildcard host setting for the loadbalancer controller fulfilling this Ingress, if left unspecified.
        """
        return pulumi.get(self, "hosts")

    @hosts.setter
    def hosts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "hosts", value)

    @property
    @pulumi.getter(name="secretName")
    def secret_name(self) -> Optional[pulumi.Input[str]]:
        """
        SecretName is the name of the secret used to terminate SSL traffic on 443. Field is left optional to allow SSL routing based on SNI hostname alone. If the SNI host in a listener conflicts with the "Host" header field used by an IngressRule, the SNI host is used for termination and value of the Host header is used for routing.
        """
        return pulumi.get(self, "secret_name")

    @secret_name.setter
    def secret_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_name", value)


@pulumi.input_type
class IngressArgs:
    def __init__(__self__, *,
                 api_version: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']] = None,
                 spec: Optional[pulumi.Input['IngressSpecArgs']] = None,
                 status: Optional[pulumi.Input['IngressStatusArgs']] = None):
        """
        Ingress is a collection of rules that allow inbound connections to reach the endpoints defined by a backend. An Ingress can be configured to give services externally-reachable urls, load balance traffic, terminate SSL, offer name based virtual hosting etc.

        This resource waits until its status is ready before registering success
        for create/update, and populating output properties from the current state of the resource.
        The following conditions are used to determine whether the resource creation has
        succeeded or failed:

        1.  Ingress object exists.
        2.  Endpoint objects exist with matching names for each Ingress path (except when Service
            type is ExternalName).
        3.  Ingress entry exists for '.status.loadBalancer.ingress'.

        If the Ingress has not reached a Ready state after 10 minutes, it will
        time out and mark the resource update as Failed. You can override the default timeout value
        by setting the 'customTimeouts' option on the resource.
        :param pulumi.Input[str] api_version: APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        :param pulumi.Input[str] kind: Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        :param pulumi.Input['_meta.v1.ObjectMetaArgs'] metadata: Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        :param pulumi.Input['IngressSpecArgs'] spec: Spec is the desired state of the Ingress. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        :param pulumi.Input['IngressStatusArgs'] status: Status is the current state of the Ingress. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        """
        if api_version is not None:
            pulumi.set(__self__, "api_version", 'networking.k8s.io/v1beta1')
        if kind is not None:
            pulumi.set(__self__, "kind", 'Ingress')
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if spec is not None:
            pulumi.set(__self__, "spec", spec)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> Optional[pulumi.Input[str]]:
        """
        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
        """
        return pulumi.get(self, "api_version")

    @api_version.setter
    def api_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_version", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']]:
        """
        Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        """
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input['_meta.v1.ObjectMetaArgs']]):
        pulumi.set(self, "metadata", value)

    @property
    @pulumi.getter
    def spec(self) -> Optional[pulumi.Input['IngressSpecArgs']]:
        """
        Spec is the desired state of the Ingress. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        """
        return pulumi.get(self, "spec")

    @spec.setter
    def spec(self, value: Optional[pulumi.Input['IngressSpecArgs']]):
        pulumi.set(self, "spec", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input['IngressStatusArgs']]:
        """
        Status is the current state of the Ingress. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input['IngressStatusArgs']]):
        pulumi.set(self, "status", value)


