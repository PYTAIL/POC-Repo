# PIQE Test Libraries - POC Repo

**This is a work in progress and not recommended for consumption at this point.**

The PIQE test libraries are a collection of Python libraries that enable you to interact with OpenShift instances.


## Requirements

* A target OpenShift environment.
* A Kubeconfig file that provides access to the target environment.
* An Openshift OC client that matches the version of your environment

## Getting started
The following steps will prepare your environment for executing or developing tests.

#### Prepare the environment

Eventually a Python Package will be available, but for now, simply clone this repo.

    git clone https://github.com/piqe-test-libraries/POC-Repo.git

Change directory to POC_Repo and create a virtual environment.

    python3 -m venv scenario

Enter the virtual envirnoment, export the environment variables and performn a pip install.

    source scenario/bin/activate  
    export WORKSPACE=$PWD  
    export KUBECONFIG=/vagrant/auth/ocp43/kubeconfig  
    pip install .

At this point, your environment is prepared. Verify that you can connect to your OpenShift instance.

    $ oc cluster-info
    Kubernetes master is running at https://api.<yourdomain>.com:6443  

#### Try running a test

The API library resides under poc_repo/api/resources, and the corresponding tests reside under poc_repo/tests/resources.

Run the test_ocp_base tests
  
    pytest -sv poc_repo/tests/resources/test_ocp_base.py
    
The following results should be presented.

    ====================================== test session starts ======================================
    platform linux -- Python 3.7.6, pytest-5.4.1, py-1.8.1, pluggy-0.13.1 -- /vagrant/piqe-test-libraries/POC-Repo/scenario/bin/python3
    cachedir: .pytest_cache
    OpenShift version: latest
    rootdir: /vagrant/piqe-test-libraries/POC-Repo
    plugins: dependency-0.5.1, forked-1.1.3, xdist-1.31.0
    collected 1 item                                                                                

    poc_repo/tests/resources/test_ocp_base.py::TestOcpBase::test_init 2020-03-18 16:00:03,318 INFO (get_openshift_cluster_info) openshift tests default configs:
    {'first_master': None}
    2020-03-18 16:00:03,318 INFO (log_start_test_case) Starting test case: test_init
    2020-03-18 16:00:03,883 - [INFO] - piqe_api_logger - test_ocp_base@test_init:25 - The obtained version is: 4.3.0
    PASSED2020-03-18 16:00:03,884 INFO (log_end_test_case) Ending test case: test_init
    
    
    ======================================= 1 passed in 0.96s =======================================
