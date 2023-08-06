
# ascend_deploy

To regenerate package run -
````shell
$ python setup.py sdist bdist_wheel
````
To install package
````shell
$ pip install git+https://<username>:<token>@github.com/X-is-Y/odysseus.git

````
To download Ascend components
````shell
$ ascend_download -c poal-pilot -s Development -f Deployment_Test

where 

-c = client to download from
-s = data_service_id
-f = path to download to (in your laptop)

````
To deploy Ascend components
````shell
$ ascend_deploy -e Deployment_Test -c poal-pilot -s Prod -f Deployment_Test -p kitchensink

where 

-e = path of resource folder in laptop
-c = client destination
-s = data_service_id (target)
-f = dataflow_id
-p = previous_data_service_id (source)

````
