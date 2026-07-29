from __future__ import annotations

import socket

import pytest


def test_default_pytest_blocks_external_create_connection():
    with pytest.raises(RuntimeError, match="blocked external socket connection"):
        socket.create_connection(("203.0.113.1", 80), timeout=0.01)


def test_default_pytest_blocks_external_socket_connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        with pytest.raises(RuntimeError, match="blocked external socket connection"):
            sock.connect(("203.0.113.1", 80))
    finally:
        sock.close()


def test_default_pytest_blocks_external_socket_connect_ex():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        with pytest.raises(RuntimeError, match="blocked external socket connection"):
            sock.connect_ex(("203.0.113.1", 80))
    finally:
        sock.close()
