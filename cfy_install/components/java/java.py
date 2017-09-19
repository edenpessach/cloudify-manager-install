from os.path import join, isfile

from ..service_names import JAVA

from ... import constants
from ...logger import get_logger
from ...config import config

from ...utils.common import move, mkdir, sudo
from ...utils.install import yum_install, yum_remove
from ...utils.files import remove_files, copy_notice, remove_notice

logger = get_logger(JAVA)
HOME_DIR = join('/opt', JAVA)
LOG_DIR = join(constants.BASE_LOG_DIR, JAVA)


def _install():
    java_source_url = config[JAVA]['sources']['java_source_url']
    yum_install(java_source_url)


def _move_java_log():
    mkdir(LOG_DIR)

    # Java install log is dropped in /var/log.
    # Move it to live with the rest of the cloudify logs
    java_install_log = '/var/log/java_install.log'
    if isfile(java_install_log):
        move(java_install_log, LOG_DIR)


def _validate_java_installed():
    java_result = sudo(['java', '-version'], ignore_failures=True)
    if java_result.returncode != 0:
        raise StandardError('Java runtime error: java was not installed')


def _configure():
    copy_notice(JAVA)
    _move_java_log()
    _validate_java_installed()


def install():
    logger.notice('Installing Java...')
    _install()
    _configure()
    logger.notice('Java successfully installed')


def configure():
    logger.info('Configuring Java...')
    _configure()
    logger.info('Java successfully configured')


def remove():
    logger.notice('Removing Java...')
    remove_notice(JAVA)
    remove_files([LOG_DIR])
    yum_remove(JAVA)
    logger.notice('Java successfully removed')