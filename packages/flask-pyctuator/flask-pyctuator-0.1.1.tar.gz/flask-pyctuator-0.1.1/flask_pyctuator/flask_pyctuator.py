import ssl
from typing import Optional, Callable

from flask import Flask
from pyctuator.auth import Auth
from pyctuator.pyctuator import Pyctuator
from pyctuator.pyctuator import default_logfile_format


class FlaskPyctuator:
    # pylint: disable=too-many-locals,too-many-instance-attributes
    def __init__(
            self,
            app: Optional[Flask],
            app_name: Optional[str] = None,
            app_url: str = "http://localhost:5000",
            pyctuator_endpoint_url: str = "http://localhost:5000/pyctuator",
            registration_url: Optional[str] = "http://localhost:8080/instances",
            registration_auth: Optional[Auth] = None,
            app_description: Optional[str] = None,
            registration_interval_sec: float = 10,
            free_disk_space_down_threshold_bytes: int = 1024 * 1024 * 100,
            logfile_max_size: int = 10000,
            logfile_formatter: str = default_logfile_format,
            auto_deregister: bool = True,
            metadata: Optional[dict] = None,
            additional_app_info: Optional[dict] = None,
            ssl_context: Optional[ssl.SSLContext] = None,
            customizer: Optional[Callable] = None,
    ) -> None:
        """Configure Pyctuator and integrate it with the Flask application adding REST API that is used by Spring Boot
        Admin.

        :param app: optional Flask application, if provided, Pycuator will be initialized and hooked to the app
        :param app_name: the application's name that will be presented in the "Info" section in boot-admin, defaults to
         the flask application-name
        :param app_url: the full URL of the application being monitored which will be displayed in spring-boot-admin, we
         recommend this URL to be accessible by those who manage the application (i.e. don't use "http://localhost..."
         as it is only accessible from within the application's host)
        :param pyctuator_endpoint_url: the public URL from which Pyctuator REST API will be accessible, used for
         registering the application with spring-boot-admin, must be accessible from spring-boot-admin server (i.e.
         don't use http://localhost:8080/... unless spring-boot-admin is running on the same host as the monitored
         application)
        :param registration_url: the spring-boot-admin endpoint to which registration requests must be posted
        :param registration_auth: optional authentication details to use when registering with spring-boot-admin
        :param app_description: a description that will be presented in the "Info" section in boot-admin
        :param registration_interval_sec: how often pyctuator will renew its registration with spring-boot-admin
        :param free_disk_space_down_threshold_bytes: amount of free space in bytes in "./" (the application's current
         working directory) below which the built-in disk-space health-indicator will fail
        :param auto_deregister: if true, pyctuator will automatically deregister from SBA during shutdown, needed for
        example when running in k8s so every time a new pod is created it is assigned a different IP address, resulting
        with SBA showing "offline" instances
        :param metadata: optional metadata key-value pairs that are displayed in SBA main page of an instance
        :param additional_app_info: additional arbitrary information to add to the application's "Info" section
        :param ssl_context: optional SSL context to be used when registering with SBA
        :param customizer: a function that can customize the integration with the web-framework which is therefore web-
         framework specific. For FastAPI, the function receives pyctuator's APIRouter allowing to add "dependencies" and
         anything else that's provided by the router. See fastapi_with_authentication_example_app.py
        """

        self.app_name = app_name
        self.app_url = app_url
        self.pyctuator_endpoint_url = pyctuator_endpoint_url
        self.registration_url = registration_url
        self.registration_auth = registration_auth
        self.app_description = app_description
        self.registration_interval_sec = registration_interval_sec
        self.free_disk_space_down_threshold_bytes = free_disk_space_down_threshold_bytes
        self.logfile_max_size = logfile_max_size
        self.logfile_formatter = logfile_formatter
        self.auto_deregister = auto_deregister
        self.metadata = metadata
        self.additional_app_info = additional_app_info
        self.ssl_context = ssl_context
        self.customizer = customizer

        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app_name = self.app_name if self.app_name else app.name
        Pyctuator(
            app=app,
            app_name=app_name,
            app_url=self.app_url,
            pyctuator_endpoint_url=self.pyctuator_endpoint_url,
            registration_url=self.registration_url,
            registration_auth=self.registration_auth,
            app_description=self.app_description,
            registration_interval_sec=self.registration_interval_sec,
            free_disk_space_down_threshold_bytes=self.free_disk_space_down_threshold_bytes,
            logfile_max_size=self.logfile_max_size,
            logfile_formatter=self.logfile_formatter,
            auto_deregister=self.auto_deregister,
            metadata=self.metadata,
            additional_app_info=self.additional_app_info,
            ssl_context=self.ssl_context,
            customizer=self.customizer,
        )
