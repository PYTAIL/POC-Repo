from css_openshift.lib.ocpmgmt.ocp_base import OcpBase
from kubernetes.client.rest import ApiException
import logging
from poc_repo import __loggername__

logger = logging.getLogger(__loggername__)


class Network(OcpBase):
    """
        Network Class extends OcpBase and encapsulates all methods
        related to OCP network definition.
        :param kube_config_file: A kubernetes config file. It overrides
                                 the hostname/username/password params
                                 if specified.
        :return: None
        """

    def __init__(self, kube_config_file):
        super(Network, self).__init__(kube_config_file=kube_config_file)
        self.ocp_nad = NetworkAttachmentDefinition(kube_config_file=kube_config_file)
        self.api_version = 'operator.openshift.io/v1'
        self.kind = 'Network'
        self.ocp_network = self.dyn_client.resources.get(api_version=self.api_version, kind=self.kind)

    def get_network_operator_config(self, name="cluster"):
        try:
            api_response = self.ocp_network.get(name)
        except ApiException as e:
            logger.error("Exception while getting network operator config: %s\n", e)
        return api_response

    def modify_network_operator_config(self, network_definition, name="cluster"):
        """
        Modify network operator config with new network definition
        :param network_definition: Network Definition
        :param name: Name of network operator
        :return: Modified network operator config
        :raise: Raise ApiException if fail to edit/modify operator config
        """
        modified_network_operator_config = None
        network_operator_config = self.get_network_operator_config(name)
        is_network_definition_exist = self.check_if_network_attachment_definition_exist(network_definition)
        if is_network_definition_exist:
            raise Exception("Network definition {} already exist in network operator config"
                            .format(network_definition["name"]))
        if network_operator_config:
            if network_operator_config.spec["additionalNetworks"]:
                network_operator_config.spec.additionalNetworks.append(network_definition)
            else:
                network_operator_config.spec.update({"additionalNetworks": [network_definition]})
            logger.debug("Network Operator Config in Memory : %s", network_operator_config)
            try:
                modified_network_operator_config = self.ocp_network.apply(body=network_operator_config)
            except ApiException as e:
                logger.exception("Exception when editing network operator config: %s\n" % e)
        return modified_network_operator_config

    def delete_additional_network_definitions(self, name, namespace="default"):
        """
        Edit network operator config and delete network attachment definitions
        :param name: Name of the network attachment definitions
        :param namespace: Namespace where network attachment definitions reside
        :return api_response: Delete api response
        """
        network_operator_config = self.get_network_operator_config()
        if network_operator_config:
            logger.debug("Available Additional Networks : %s\n", network_operator_config.spec.additionalNetworks)
            for additional_network_config in network_operator_config.spec.additionalNetworks:
                logger.debug("Network Def Name : ", additional_network_config["name"])
                if additional_network_config["name"] == name:
                    logger.debug("Removing network attachment definition from network operator config : %s\n",
                                 additional_network_config)
                    network_operator_config.spec.additionalNetworks.remove(additional_network_config)
            try:
                self.ocp_network.apply(body=network_operator_config)
            except ApiException as e:
                logger.exception("Exception when editing network operator config: %s\n" % e)
            return self.ocp_nad.delete_network_attachment_definition(name, namespace)
        else:
            logger.error("There are no network attachment definitions exist.")

    def check_if_network_attachment_definition_exist(self, network_definition):
        """
        This utility method checks if network attachment definition already exist or applied to network config
        :param network_definition:
        :return: returns boolean value
        """
        results = self.ocp_nad.get_all_network_attachment_definition()
        if results.items:
            list_of_network_def = (item["metadata"]["name"] for item in results.items)
            if network_definition["name"] in list_of_network_def:
                return True
            else:
                return False

    """
    TODO : If we modify the cluster network operator, Restore it's config after test run
    Hint : Cache the network config before modifying
    """
    def restore_cluster_network_operator_config(self):
        pass


class NetworkAttachmentDefinition(OcpBase):
    """
        NetworkAttachmentDefinition Class extends OcpBase and encapsulates all methods
        related to modify openshift network definition.
        :param kube_config_file: A kubernetes config file. It overrides
                                 the hostname/username/password params
                                 if specified.
        :return: None
        """

    def __init__(self, kube_config_file=None):
        super(NetworkAttachmentDefinition, self).__init__(kube_config_file=kube_config_file)
        self.api_version = 'v1'
        self.kind = 'NetworkAttachmentDefinition'
        self.ocp_nad = self.dyn_client.resources.get(api_version=self.api_version, kind=self.kind)

    def create_network_attachment_definition(self, definition):
        """
        Create Network Attachment Definitions in specific namespace
        :param definition: Definition for additional network interface in dict form
        :return: api_response
        """
        api_response = None
        try:
            api_response = self.ocp_nad.create(body=definition)
        except ApiException as e:
            logger.exception("Exception while creating network attachment definitions : %s\n" % e)
        return api_response

    def get_network_attachment_definition(self, name, namespace="default"):
        """
        Get specific network attachment definitions from specific namespace or cluster operator
        :param self:
        :param name: name of the definition
        :param namespace: namespace of network definition
        :return: api_response:
        """
        api_response = None
        try:
            api_response = self.ocp_nad.get(name, namespace)
        except ApiException as e:
            logger.exception("Exception while getting network attachment definitions for %s : %s\n" % name, e)
        return api_response

    def get_all_network_attachment_definition(self):
        """
        Get all network attachment definitions for cluster operator
        :return: api_response : List of all network attachment definitions
        """
        api_response = None
        try:
            api_response = self.ocp_nad.get()
        except ApiException as e:
            logger.exception("Exception while getting network attachment definitions: %s\n" % e)
        return api_response

    def delete_network_attachment_definition(self, name, namespace="default"):
        """
         Delete network attachment definitions from network operator
        :param self:
        :param name: Name of the Network Attachment Definition
        :param namespace: Namespace where network attachment definitions resides
        :return: api_response: Delete api response
        """
        api_response = None
        try:
            api_response = self.ocp_nad.delete(name, namespace)
        except ApiException as e:
            logger.exception("Exception while deleting network attachment definitions: %s\n" % e)
        return api_response
