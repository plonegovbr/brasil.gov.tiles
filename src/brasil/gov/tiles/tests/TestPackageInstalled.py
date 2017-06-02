# -*- coding: utf-8 -*-
import pkg_resources


def package_installed(package):
    try:
        pkg_resources.get_distribution(package)
    except pkg_resources.DistributionNotFound:
        return False
    else:
        return True
