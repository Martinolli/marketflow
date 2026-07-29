from __future__ import annotations

import ipaddress
import socket
from typing import Any


_ORIGINAL_CREATE_CONNECTION = socket.create_connection
_ORIGINAL_SOCKET_CONNECT = socket.socket.connect
_ORIGINAL_SOCKET_CONNECT_EX = socket.socket.connect_ex


def _host_is_loopback(host: Any) -> bool:
    if host in {"localhost", "127.0.0.1", "::1"}:
        return True
    try:
        return ipaddress.ip_address(str(host)).is_loopback
    except ValueError:
        return False


def _assert_offline(address: Any) -> None:
    host = address[0] if isinstance(address, tuple) and address else address
    if not _host_is_loopback(host):
        raise RuntimeError(f"default pytest suite blocked external socket connection to {host!r}")


def _guarded_create_connection(address: Any, *args: Any, **kwargs: Any) -> Any:
    _assert_offline(address)
    return _ORIGINAL_CREATE_CONNECTION(address, *args, **kwargs)


def _guarded_socket_connect(self: socket.socket, address: Any) -> Any:
    _assert_offline(address)
    return _ORIGINAL_SOCKET_CONNECT(self, address)


def _guarded_socket_connect_ex(self: socket.socket, address: Any) -> Any:
    _assert_offline(address)
    return _ORIGINAL_SOCKET_CONNECT_EX(self, address)


socket.create_connection = _guarded_create_connection
socket.socket.connect = _guarded_socket_connect
socket.socket.connect_ex = _guarded_socket_connect_ex
