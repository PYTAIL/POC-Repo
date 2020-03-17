from poc_repo.api.resources import OcpProjects, OcpTemplates
from pprint import pprint
import pytest
import json
from random import randint


@pytest.fixture(scope='class')
def setup_params(get_kubeconfig):
    params_dict = {}
    params_dict['test_project'] = 'template-project'
    params_dict['project_api_obj'] = OcpProjects(kube_config_file=get_kubeconfig)
    params_dict['template_api_obj'] = OcpTemplates(kube_config_file=get_kubeconfig)
    params_dict['ident'] = randint(0, 10)
    params_dict['app_name'] = 'httpd-example'
    return params_dict


class TestOcpTemplates(object):

    def test_create_a_template_in_a_namespace(self, setup_params):
        """
        1. Create a test project
        2. Load a raw/json template to that project
        3. Copy the template to the test project using the
           create_a_template_in_a_namespace method.
        4. Check that the template has been successfully copied to
           that projects by checking the kind and name of the
           response object.
        """
        project_api_obj = setup_params['project_api_obj']
        project_api_obj.create_a_project(setup_params['test_project'])
        template_api_obj = setup_params['template_api_obj']
        with open('poc_repo/tests/resources/templates/httpd.json') as t:
            body = json.load(t)
        api_response = template_api_obj.create_a_template_in_a_namespace(body, project=setup_params['test_project'])
        pprint(api_response)
        assert api_response.kind == 'Template'
        assert api_response.metadata.name == setup_params['app_name']

    def test_get_a_template_in_a_namespace(self, setup_params):
        """
        1. Verify that we are able to obtain the template that
           we added to our test project using the
           get_a_template_in_a_namespace method.
        2. Verify the success of the previous operation
           by checking the kind and name of response object.
        """
        template_api_obj = setup_params['template_api_obj']
        api_response = template_api_obj.get_a_template_in_a_namespace(setup_params['app_name'],
                                                                      project=setup_params['test_project'])
        pprint(api_response)
        assert api_response['kind'] == 'Template'
        assert api_response['metadata']['name'] == setup_params['app_name']

    def test_get_all_templates_in_a_namespace(self, setup_params):
        """
        1. Verify that we are able to obtain all the templates
           in the test project (in this case, one) using the
           get_all_templates_in_a_namespace method.
        2. Verify the success of the previous operation
           by checking the kind and name of of the item in
           the response object list.
        """
        template_api_obj = setup_params['template_api_obj']
        api_response = template_api_obj.get_all_templates_in_a_namespace(project=setup_params['test_project'])
        pprint(api_response)
        assert api_response.kind == 'TemplateList'
        assert api_response.items[0].metadata.name == setup_params['app_name']

    def test_enumerate_unprocessed_template(self, setup_params):
        """
        1. Fetch the template we created in our test project
        2. Enumerate it using the enumerate_unprocessed_template method.
        3. Verify that the appropriate default value in the parameters
           list has been modified by appending -ident to it.
        """
        template_api_obj = setup_params['template_api_obj']
        template = template_api_obj.get_a_template_in_a_namespace(setup_params['app_name'],
                                                                  project=setup_params['test_project'])
        api_response = template_api_obj.enumerate_unprocessed_template(template, setup_params['ident'])
        pprint(api_response)
        assert api_response['parameters'][0]['value'] == setup_params['app_name']+'-'+str(setup_params['ident'])

    def test_create_a_processed_template(self, setup_params):
        """
        1. Fetch the template we created in our test project
        2. Enumerate it using the enumerate_unprocessed_template method.
        3. Process the enumerated raw template using the
           create_a_processed_template method.
        3. Verify that the resource names have been modified
           by appending -ident to it.
        """
        template_api_obj = setup_params['template_api_obj']
        raw_template = template_api_obj.get_a_template_in_a_namespace(setup_params['app_name'],
                                                                      project=setup_params['test_project'])
        enumrated_template = template_api_obj.enumerate_unprocessed_template(raw_template, setup_params['ident'])
        processed_template = template_api_obj.create_a_processed_template(enumrated_template)
        pprint(processed_template)
        for resource in processed_template['objects']:
            assert resource['metadata']['name'] == setup_params['app_name']+'-'+str(setup_params['ident'])
