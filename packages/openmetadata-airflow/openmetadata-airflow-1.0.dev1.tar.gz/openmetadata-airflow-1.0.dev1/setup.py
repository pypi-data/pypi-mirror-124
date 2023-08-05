from setuptools import find_namespace_packages, setup

setup(
    name="openmetadata-airflow",
    version="1.0.dev1",
    description="Python Distribution Utilities",
   packages=['airflow_provider_openmetadata'],
    entry_points={
        "apache_airflow_provider": [
            "provider_info = airflow_provider_openmetadata:get_provider_config"
        ],
    },
)
