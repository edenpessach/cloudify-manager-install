from .. import constants
from ..config import config
from ..logger import get_logger

from .service_names import RABBITMQ, MANAGER, AGENT, CONSTANTS

from . import PRIVATE_IP, ENDPOINT_IP, SECURITY, SOURCES

BROKER_IP = 'broker_ip'

logger = get_logger('Globals')


def _set_external_port_and_protocol():
    if config[MANAGER][SECURITY]['ssl_enabled']:
        logger.info('SSL is enabled, setting rest port to 443 and '
                    'rest protocol to https...')
        external_rest_port = 443
        external_rest_protocol = 'https'
    else:
        logger.info('SSL is disabled, setting rest port '
                    'to 80 and rest protocols to http...')
        external_rest_port = 80
        external_rest_protocol = 'http'

    config[MANAGER]['external_rest_port'] = external_rest_port
    config[MANAGER]['external_rest_protocol'] = external_rest_protocol


def _set_rabbitmq_config():
    config[RABBITMQ][ENDPOINT_IP] = config[AGENT][BROKER_IP]
    config[RABBITMQ]['broker_cert_path'] = constants.CA_CERT_PATH


def _set_ip_config():
    private_ip = config[MANAGER][PRIVATE_IP]
    config[AGENT][BROKER_IP] = private_ip

    config[MANAGER]['file_server_root'] = constants.MANAGER_RESOURCES_HOME
    config[MANAGER]['file_server_url'] = 'https://{0}:{1}/resources'.format(
        private_ip,
        constants.INTERNAL_REST_PORT
    )

    networks = config[AGENT]['networks']
    if not networks or 'default' not in networks:
        networks['default'] = private_ip


def _set_constant_config():
    const_conf = config.setdefault(CONSTANTS, {})

    const_conf['ca_cert_path'] = constants.CA_CERT_PATH
    const_conf['internal_cert_path'] = constants.INTERNAL_CERT_PATH
    const_conf['internal_key_path'] = constants.INTERNAL_KEY_PATH
    const_conf['external_cert_path'] = constants.EXTERNAL_CERT_PATH
    const_conf['external_key_path'] = constants.EXTERNAL_KEY_PATH

    const_conf['internal_rest_port'] = constants.INTERNAL_REST_PORT


def _set_community_edition():
    if 'community' in config[MANAGER][SOURCES]['manager_resources_package']:
        logger.info('Working with `Community` edition')
        config[MANAGER]['premium_edition'] = False
    else:
        logger.info('Working with `Premium` edition')


def set_globals():
    _set_ip_config()
    _set_rabbitmq_config()
    _set_external_port_and_protocol()
    _set_constant_config()
    _set_community_edition()
