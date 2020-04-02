import pytest


def pytest_addoption(parser):
    parser.addoption("--program",
                     type=str,
                     action="store",
                     help="Camino hacia el ejecutable de su shell")
