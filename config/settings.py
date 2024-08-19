#!/usr/bin/python3 
#coding=utf-8

import logging;
import os

from tools.utils import load_config

BASC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = BASC_DIR + '/config/config.yml'


def get_config():
	config = load_config(config_path)
	config['BASC_DIR'] = BASC_DIR
	# if __name__ == '__main__':
	# 	logging.info(config)
	return config

