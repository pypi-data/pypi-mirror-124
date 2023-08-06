# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2020-2021 Micron Technology, Inc. All rights reserved.

import errno
import os
cimport cython
cimport limits
from enum import Enum, IntFlag, unique
from types import TracebackType
from typing import List, Optional, Tuple, Dict, Iterator, Type, Union, Iterable, SupportsBytes
from libc.stdlib cimport malloc, free


# Throughout these bindings, you will see C pointers be set to NULL after their
# destruction. Please continue to follow this pattern as the HSE C code does
# not do this. We use NULL checks to protect against double free
# issues within the Python bindings.

# bytes(<bytes object>) returns the original bytes object. It is not a copy.


def to_bytes(obj: Optional[Union[str, bytes, SupportsBytes]]) -> bytes:
    if obj is None:
        return None

    if isinstance(obj, str):
        return obj.encode()

    return bytes(obj)


cdef char **to_paramv(tuple params) except NULL:
    cdef char **paramv = <char **>malloc(len(params) * sizeof(char *))
    if not paramv:
        raise MemoryError()
    else:
        for i, param in enumerate(params):
            assert isinstance(param, str)
            paramv[i] = <char *>PyUnicode_AsUTF8(param)
            if not paramv[i]:
                return NULL

    return paramv


def init(config: Optional[Union[str, os.PathLike[str]]] = None, *params: str) -> None:
    """
    Initialize the HSE subsystem.

    This function initializes a range of different internal HSE structures. It
    must be called before any other HSE functions are used.

    This function is not thread safe and is idempotent.

    Args:
        config: Path to a global configuration file.
        params: Parameters in key=value format.

    Raises:
        HseException: Underlying C function returned a non-zero value.
    """
    config_bytes = os.fspath(config).encode() if config else None
    cdef const char *config_addr = <char *>config_bytes if config_bytes else NULL
    cdef char **paramv = to_paramv(params) if len(params) > 0 else NULL

    cdef hse_err_t err = hse_init(config_addr, len(params), <const char * const*>paramv)

    if paramv:
        free(paramv)
    if err != 0:
        raise HseException(err)


def fini() -> None:
    """
    Shutdown the HSE subsystem.

    This function cleanly finalizes a range of different internal HSE structures.
    It should be called prior to application exit.

    After invoking this function, calling any other HSE functions will
    result in undefined behavior unless HSE is re-initialized.

    This function is not thread safe.
    """
    hse_fini()


class HseException(Exception):
    """
    Raised when HSE encounters an error. Wrapper around ``hse_err_t``.

    Attributes:
        returncode: Errno value returned by HSE.
    """
    def __init__(self, hse_err_t returncode):
        self.returncode = hse_err_to_errno(returncode)
        IF HSE_PYTHON_DEBUG != 0:
            cdef char buf[256]
            hse_strerror(returncode, buf, sizeof(buf))
            self.message = buf.decode()
        ELSE:
            self.message = os.strerror(self.returncode)

    def __str__(self):
        return self.message


@unique
class KvdbSyncFlag(IntFlag):
    """
    Attributes:
        ASYNC: Return immediately after initiating operation
    """
    ASYNC = HSE_KVDB_SYNC_ASYNC

IF HSE_PYTHON_EXPERIMENTAL == 1:
    @unique
    class KvdbCompactFlag(IntFlag):
        CANCEL = HSE_KVDB_COMPACT_CANCEL
        SAMP_LWM = HSE_KVDB_COMPACT_SAMP_LWM


cdef class Kvdb:
    def __cinit__(self, kvdb_home: Union[str, os.PathLike[str]], *params: str):
        self._c_hse_kvdb = NULL

        kvdb_home_bytes = os.fspath(kvdb_home).encode() if kvdb_home else None
        cdef const char *kvdb_home_addr = <char *>kvdb_home_bytes if kvdb_home_bytes else NULL
        cdef char **paramv = to_paramv(params) if len(params) > 0 else NULL

        err = hse_kvdb_open(kvdb_home_addr, len(params), <const char * const*>paramv, &self._c_hse_kvdb)
        if paramv:
            free(paramv)
        if err != 0:
            raise HseException(err)

    def close(self) -> None:
        """
        Close a KVDB.

        After invoking this function, calling any other KVDB functions will
        result in undefined behavior unless the KVDB is re-opened.

        This function is not thread safe.

        Args:
            kvdb: KVDB handle from ``Kvdb.open()``.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        if not self._c_hse_kvdb:
            return

        cdef hse_err_t err = hse_kvdb_close(self._c_hse_kvdb)
        if err != 0:
            raise HseException(err)
        self._c_hse_kvdb = NULL

    @staticmethod
    def create(kvdb_home: Union[str, os.PathLike[str]], *params: str) -> None:
        """
        Create a KVDB.

        This function is not thread safe.

        Args:
            kvdb_home: KVDB home directory.
            params: List of parameters in key=value format.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        kvdb_home_bytes = os.fspath(kvdb_home).encode() if kvdb_home else None
        cdef const char *kvdb_home_addr = <char *>kvdb_home_bytes if kvdb_home_bytes else NULL
        cdef char **paramv = to_paramv(params) if len(params) > 0 else NULL

        cdef hse_err_t err = hse_kvdb_create(kvdb_home_addr, len(params), <const char * const*>paramv)
        if paramv:
            free(paramv)
        if err != 0:
            raise HseException(err)

    @staticmethod
    def drop(kvdb_home: Union[str, os.PathLike[str]]) -> None:
        """
        Drop a KVDB.

        It is an error to call this function on a KVDB that is open.

        This function is not thread safe.

        Args:
            kvdb_home: KVDB home directory

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        kvdb_home_bytes = os.fspath(kvdb_home).encode() if kvdb_home else None
        cdef const char *kvdb_home_addr = <char *>kvdb_home_bytes if kvdb_home_bytes else NULL

        cdef hse_err_t err = hse_kvdb_drop(kvdb_home_addr)
        if err != 0:
            raise HseException(err)

    @staticmethod
    def open(kvdb_home: Union[str, os.PathLike[str]], *params: str) -> Kvdb:
        """
        Open a KVDB.

        This function is not thread safe.

        Args:
            kvdb_home: KVDB home directory.
            params: List of parameters in key=value format.

        Returns:
            Kvdb: A KVDB handle.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        return Kvdb(kvdb_home, *params)

    @property
    def kvs_names(self) -> List[str]:
        """
        """
        cdef size_t namec = 0
        cdef char **namev = NULL
        cdef hse_err_t err = hse_kvdb_kvs_names_get(self._c_hse_kvdb, &namec, &namev)
        if err != 0:
            raise HseException(err)

        result = []
        for i in range(namec):
            result.append(namev[i].decode())

        hse_kvdb_kvs_names_free(self._c_hse_kvdb, namev)

        return result

    def kvs_create(self, str name, *params: str) -> None:
        """
        Create a new KVS within the referenced KVDB.

        This function is not thread safe.

        Args:

        name: KVS name.
        params: List of parameters in key=value format.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        name_bytes = name.encode() if name else None
        cdef const char *name_addr = <char *>name_bytes if name_bytes else NULL
        cdef char **paramv = to_paramv(params) if len(params) > 0 else NULL

        cdef hse_err_t err = hse_kvdb_kvs_create(
            self._c_hse_kvdb, name_addr, len(params),
            <const char * const*>paramv)
        if paramv:
            free(paramv)
        if err != 0:
            raise HseException(err)

    def kvs_drop(self, str kvs_name) -> None:
        """
        Drop a KVS from the referenced KVDB.

        It is an error to call this function on a KVS that is open.

        This function is not thread safe.

        Args:
            name: KVS name.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef hse_err_t err = hse_kvdb_kvs_drop(self._c_hse_kvdb, kvs_name.encode())
        if err != 0:
            raise HseException(err)

    def kvs_open(self, str kvs_name, *params: str) -> Kvs:
        """
        Open a KVS in a KVDB.

        This function is not thread safe.

        Args:
            name: KVS name.
            params: List of parameters in key=value format.

        Returns:
            Kvs: A KVS handle.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        return Kvs(self, kvs_name, *params)

    def sync(self, flags: Optional[KvdbSyncFlag] = None) -> None:
        """
        Sync data in all of the referenced KVDB's KVSs to stable media.

        Args:
            flags: Flags for operation specialization.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef unsigned int cflags = int(flags) if flags else 0
        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvdb_sync(self._c_hse_kvdb, cflags)
        if err != 0:
            raise HseException(err)

    IF HSE_PYTHON_EXPERIMENTAL == 1:
        def compact(self, flags: Optional[KvdbCompactFlag] = None) -> None:
            """
            Request a data compaction operation.

            In managing the data within an HSE KVDB, there are maintenance activities
            that occur as background processing. The application may be aware that it is
            advantageous to do enough maintenance now for the database to be as compact
            as it ever would be in normal operation.

            See the property ``Kvdb.compact_status``.

            This function is thread safe.

            Args:
                flags: Compaction flags.

            Raises:
                HseException: Underlying C function returned a non-zero value.
            """
            cdef unsigned int cflags = int(flags) if flags else 0

            cdef hse_err_t err = 0
            with nogil:
                err = hse_kvdb_compact(self._c_hse_kvdb, cflags)
            if err != 0:
                raise HseException(err)

        @property
        def compact_status(self) -> KvdbCompactStatus:
            """
            Get status of an ongoing compaction activity.

            The caller can examine the fields of the ``KvdbCompactStatus`` class to
            determine the current state of maintenance compaction.

            This property is thread safe.

            Returns:
                KvdbCompactStatus: Status of compaction request.

            Raises:
                HseException: Underlying C function returned a non-zero value.
            """
            status: KvdbCompactStatus = KvdbCompactStatus()
            cdef hse_err_t err = 0
            with nogil:
                err = hse_kvdb_compact_status_get(self._c_hse_kvdb, &status._c_hse_kvdb_compact_status)
            if err != 0:
                raise HseException(err)
            return status

    IF HSE_PYTHON_EXPERIMENTAL == 1:
        @property
        def storage_info(self) -> KvdbStorageInfo:
            """
            Get KVDB storage stats.

            Obtain the space usage statistics for a specified kvdb.

            This function is thread safe.

            Returns:
                KvdbStorageInfo: KVDB storage config and stats.

            Raises:
                HseException: Underlying C function returned a non-zero value.
            """
            info: KvdbStorageInfo = KvdbStorageInfo()
            cdef hse_err_t err = 0
            with nogil:
                err = hse_kvdb_storage_info_get(self._c_hse_kvdb, &info._c_hse_kvdb_storage_info)
            if err != 0:
                raise HseException(err)
            return info

    @staticmethod
    def storage_add(kvdb_home: Union[str, os.PathLike[str]], *params: str) -> None:
        """
        Add a new media class storage to an existing offline KVDB.

        This function is not thread safe.

        Args:
            kvdb_home: KVDB home directory.
            params: List of parameters in key=value format.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        kvdb_home_bytes = os.fspath(kvdb_home).encode() if kvdb_home else None
        cdef const char *kvdb_home_addr = <char *>kvdb_home_bytes if kvdb_home_bytes else NULL
        cdef size_t paramc = len(params)
        cdef char **paramv = to_paramv(params) if paramc > 0 else NULL
        cdef hse_err_t err = 0

        with nogil:
            err = hse_kvdb_storage_add(kvdb_home_addr, paramc, <const char * const*>paramv)

        if paramv:
            free(paramv)
        if err != 0:
            raise HseException(err)

    def transaction(self) -> KvdbTransaction:
        """
        Allocate transaction object.

        This object can and should be re-used many times to avoid the overhead of
        allocation.

        This function is thread safe.

        Returns:
            KvdbTransaction: A transaction handle.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        txn = KvdbTransaction(self)

        return txn


@unique
class KvsPutFlag(IntFlag):
    """
    Attributes:
        PRIO: Operation will not be throttled
        VCOMP_OFF: Value will not be compressed
    """
    PRIO = HSE_KVS_PUT_PRIO
    VCOMP_OFF = HSE_KVS_PUT_VCOMP_OFF


@unique
class CursorCreateFlag(IntFlag):
    """
    Attributes:
        REV: iterate in reverse lexicographical order
    """
    REV = HSE_CURSOR_CREATE_REV


IF HSE_PYTHON_EXPERIMENTAL == 1:
    @unique
    class KvsPfxProbeCnt(Enum):
        """
        Number of keys found from a prefix probe operation.

        Attributes:
            ZERO: Zero keys found with prefix.
            ONE: One key found with prefix.
            MUL: Multiple keys found with prefix.
        """
        ZERO = HSE_KVS_PFX_FOUND_ZERO
        ONE = HSE_KVS_PFX_FOUND_ONE
        MUL = HSE_KVS_PFX_FOUND_MUL


cdef class Kvs:
    def __cinit__(self, Kvdb kvdb, str name, *params: str):
        self._c_hse_kvs = NULL

        name_bytes = name.encode() if name else None
        cdef const char *name_addr = <char *>name_bytes if name_bytes else NULL
        cdef char **paramv = to_paramv(params) if len(params) > 0 else NULL

        cdef hse_err_t err = hse_kvdb_kvs_open(kvdb._c_hse_kvdb, name_addr, len(params),
            <const char * const*>paramv, &self._c_hse_kvs)
        if paramv:
            free(paramv)
        if err != 0:
            raise HseException(err)

    def close(self) -> None:
        """
        Close an open KVS.

        After invoking this function, calling any other KVS functions will
        result in undefined behavior unless the KVS is re-opened.

        This function is not thread safe.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        if not self._c_hse_kvs:
            return

        cdef hse_err_t err = hse_kvdb_kvs_close(self._c_hse_kvs)
        if err != 0:
            raise HseException(err)
        self._c_hse_kvs = NULL

    def put(
            self,
            key: Union[str, bytes, SupportsBytes],
            value: Optional[Union[str, bytes, SupportsBytes]],
            KvdbTransaction txn=None,
            flags: Optional[KvsPutFlag]=None,
        ) -> None:
        """
        Put a key-value pair into KVS.

        If the key already exists in the KVS then the value is effectively
        overwritten. See ``KvdbTransaction`` for information on how puts within
        transactions are handled.

        The HSE KVDB attempts to maintain reasonable QoS and for high-throughput
        clients this results in very short sleep's being inserted into the put path.
        For some kinds of data (e.g., control metadata) the client may wish to not
        experience that delay. For relatively low data rate uses, the caller can set
        the ``KvsPutFlags.PRIO`` flag for an ``Kvs.put()``. Care should be taken when
        doing so to ensure that the system does not become overrun. As a rough
        approximation, doing 1M priority puts per second marked as PRIO is likely an
        issue. On the other hand, doing 1K small puts per second marked as PRIO is
        almost certainly fine.

        If compression is enabled for the given kvs, then ``Kvs.put()`` will attempt
        to compress the value unless the ``KvsPutFlags.VCOMP_OFF`` flag is given.
        Otherwise, the ``KvsPutFlags.VCOMP_OFF`` flag is ignored.

        This function is thread safe.

        Args:
            key: Key to put into KVS.
            value: Value associated with ``key``.
            txn: Transaction context.
            flags: Flags for operation specialization.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef unsigned int cflags = int(flags) if flags else 0
        cdef hse_kvdb_txn *txn_addr = NULL
        cdef const void *key_addr = NULL
        cdef size_t key_len = 0
        cdef const void *value_addr = NULL
        cdef size_t value_len = 0

        cdef const unsigned char [:]key_view = to_bytes(key)
        cdef const unsigned char [:]value_view = to_bytes(value)

        if txn:
            txn_addr = txn._c_hse_kvdb_txn
        if key_view is not None:
            key_addr = &key_view[0]
            key_len = key_view.shape[0]
        if value_view is not None:
            value_addr = &value_view[0]
            value_len = value_view.shape[0]

        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvs_put(self._c_hse_kvs, cflags, txn_addr, key_addr, key_len, value_addr, value_len)
        if err != 0:
            raise HseException(err)

    def get(
            self,
            key: Union[str, bytes, SupportsBytes],
            KvdbTransaction txn=None,
            unsigned char [:]buf=bytearray(limits.HSE_KVS_VALUE_LEN_MAX),
        ) -> Tuple[Optional[bytes], int]:
        """
        Retrieve the value for a given key from the KVS.

        If the key exists in the KVS, then the returned key is not None.
        If the caller's value buffer is large enough then the data will be returned.
        Regardless, the actual length of the value is returned. See
        ``KvdbTransaction`` for information on how gets within transactions are handled.

        This function is thread safe.

        Args:
            key: Key to get from the KVS.
            txn: Transaction context.
            buf: Buffer into which the value associated with ``key`` will be copied.

        Returns:
            tuple: Value and length of the value.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef unsigned int cflags = 0
        cdef hse_kvdb_txn *txn_addr = NULL
        cdef const void *key_addr = NULL
        cdef size_t key_len = 0
        cdef void *buf_addr = NULL
        cdef size_t buf_len = 0

        cdef const unsigned char [:]key_view = to_bytes(key)

        if txn:
            txn_addr = txn._c_hse_kvdb_txn
        if key_view is not None:
            key_addr = &key_view[0]
            key_len = key_view.shape[0]
        if buf is not None:
            buf_addr = &buf[0]
            buf_len = buf.shape[0]

        cdef cbool found = False
        cdef size_t value_len = 0
        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvs_get(self._c_hse_kvs, cflags, txn_addr, key_addr,
                key_len, &found, buf_addr, buf_len, &value_len)
        if err != 0:
            raise HseException(err)
        if not found:
            return None, 0

        if buf is None:
            return None, value_len

        if value_len < len(buf):
            return bytes(buf)[:value_len], value_len

        return bytes(buf), value_len

    def delete(self, key: Union[str, bytes, SupportsBytes], KvdbTransaction txn=None) -> None:
        """
        Delete the key and its associated value from the KVS.

        It is not an error if the key does not exist within the KVS. See
        ``KvdbTransaction`` for information on how deletes within transactions are
        handled.

        Args:
            key: Key to be deleted from the KVS.
            txn: Transaction context.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef unsigned int cflags = 0
        cdef hse_kvdb_txn *txn_addr = NULL
        cdef const void *key_addr = NULL
        cdef size_t key_len = 0

        cdef const unsigned char [:]key_view = to_bytes(key)

        if txn:
            txn_addr = txn._c_hse_kvdb_txn
        if key_view is not None:
            key_addr = &key_view[0]
            key_len = key_view.shape[0]

        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvs_delete(self._c_hse_kvs, cflags, txn_addr, key_addr, key_len)
        if err != 0:
            raise HseException(err)

    def prefix_delete(self, pfx: Union[str, bytes], txn: KvdbTransaction=None) -> None:
        """
        Delete all key-value pairs matching the key prefix from a KVS storing
        segmented keys.

        This interface is used to delete an entire range of segmented keys. To do
        this the caller passes a filter with a length equal to the KVS's key prefix
        length. It is not an error if no keys exist matching the filter. If there is
        a filtered iteration in progress, then that iteration can fail if
        ``Kvs.prefix_delete()`` is called with a filter matching the iteration.

        If ``Kvs.prefix_delete()`` is called from a transaction context, it affects
        no key-value mutations that are part of the same transaction. Stated
        differently, for KVS commands issued within a transaction, all calls to
        ``Kvs.prefix_delete()`` are treated as though they were issued serially at
        the beginning of the transaction regardless of the actual order these
        commands appeared in.

        Args:
            pfx: Prefix of keys to delete.
            txn: Transaction context.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef unsigned int cflags = 0
        cdef hse_kvdb_txn *txn_addr = NULL
        cdef const void *pfx_addr = NULL
        cdef size_t pfx_len = 0

        cdef const unsigned char[:] pfx_view = to_bytes(pfx)

        if txn:
            txn_addr = txn._c_hse_kvdb_txn
        if pfx_view is not None:
            pfx_addr = &pfx_view[0]
            pfx_len = pfx_view.shape[0]

        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvs_prefix_delete(self._c_hse_kvs, cflags, txn_addr, pfx_addr, pfx_len)
        if err != 0:
            raise HseException(err)

    IF HSE_PYTHON_EXPERIMENTAL == 1:
        def prefix_probe(
            self,
            pfx: Union[str, bytes],
            unsigned char [:]key_buf=bytearray(limits.HSE_KVS_KEY_LEN_MAX),
            unsigned char [:]value_buf=bytearray(limits.HSE_KVS_VALUE_LEN_MAX),
            KvdbTransaction txn=None,
        ) -> Tuple[KvsPfxProbeCnt, Optional[bytes], int, Optional[bytes], int]:
            """
            Probe for a prefix.

            Given a prefix, outputs how many matches were encountered - zero, one or
            multiple.

            Args:
                pfx: Prefix to be probed.
                key_buf: Buffer which will be populated with contents of first seen key.
                val_buf: Buffer which will be populated with value for ``key_buf``
                txn: Transaction context.

            Returns:
                tuple: Tuple of ``KvsPfxProbeCnt``, key, length of key, value, and length of
                    value.

            Raises:
                HseException: Underlying C function returned a non-zero value.
            """
            cdef hse_kvdb_txn *txn_addr = NULL
            cdef const void *pfx_addr = NULL
            cdef size_t pfx_len = 0
            cdef hse_kvs_pfx_probe_cnt found = HSE_KVS_PFX_FOUND_ZERO
            cdef void *key_buf_addr = NULL
            cdef size_t key_buf_len = 0
            cdef size_t key_len = 0
            cdef void *value_buf_addr = NULL
            cdef size_t value_buf_len = 0
            cdef size_t value_len = 0

            cdef const unsigned char[:] pfx_view = to_bytes(pfx)

            if pfx_view is not None:
                pfx_addr = &pfx_view[0]
                pfx_len = pfx_view.shape[0]
            if key_buf is not None and len(key_buf) > 0:
                key_buf_addr = &key_buf[0]
                key_buf_len = len(key_buf)
            if value_buf is not None and len(value_buf) > 0:
                value_buf_addr = &value_buf[0]
                value_buf_len = len(value_buf)
            if txn:
                txn_addr = txn._c_hse_kvdb_txn

            cdef hse_err_t err = 0
            with nogil:
                err = hse_kvs_prefix_probe(self._c_hse_kvs, 0, txn_addr,
                    pfx_addr, pfx_len, &found, key_buf_addr, key_buf_len, &key_len,
                    value_buf_addr, value_buf_len, &value_len)
            if err != 0:
                raise HseException(err)
            if found == HSE_KVS_PFX_FOUND_ZERO:
                return KvsPfxProbeCnt.ZERO, None, 0, None, 0

            return (
                KvsPfxProbeCnt(found),
                bytes(key_buf)[:key_len] if key_buf is not None and key_len < len(key_buf) else key_buf,
                key_len,
                bytes(value_buf)[:value_len] if value_buf is not None and value_len < len(value_buf) else value_buf,
                value_len
            )

    def cursor(
        self,
        filt: Optional[Union[str, bytes]]=None,
        KvdbTransaction txn=None,
        flags: Optional[CursorCreateFlag]=None,
    ) -> KvsCursor:
        """
        Non-transactional cursors:

        If ``txn`` is None, a non-transactional cursor is created. Non-transactional
        cursors have an ephemeral snapshot view of the KVS at the time it the cursor
        is created. The snapshot view is maintained for the life of the cursor.
        Writes to the KVS (put, deletes, etc.) made after the cursor is created will
        not be visible to the cursor unless ``KvsCursor.update_view()`` is used to
        obtain a more recent snapshot view. Non-transactional cursors can be used on
        transactional and non-transactional KVSs.

        Transactional cursors:

        If ``txn`` is not None, it must be a valid transaction handle or undefined
        behavior will result. If it is a valid handle to a transaction in the ACTIVE
        state, a transactional cursor is created. A transaction cursor's view
        includes the transaction's writes overlaid on the transaction's ephemeral
        snapshot view of the KVS. If the transaction is committed or aborted before
        the cursor is destroyed, the cursor's view reverts to same snaphsot view the
        transaction had when first became active. The cursor will no longer be able
        to see the transaction's writes. Calling ``KvsCursor.update_view()`` on a
        transactional cursor is a no-op and has no effect on the cursor's view.
        Transactional cursors can only be used on transactional KVSs.

        Prefix vs non-prefix cursors:

        Parameter ``filter`` can be used to iterate over the subset
        of keys in the KVS whose first ``len(filter)`` bytes match the first
        ``len(filter)`` bytes pointed to by ``filter``.

        A prefix cursor is created when:
            * KVS was created with ``prefix.length`` > 0 (i.e., it is a prefix KVS), and
            * ``filter`` != None and ``len(filter)`` >= ``prefix.length``.

        Otherwise, a non-prefix cursor is created.

        Applications should arrange their key-value data to avoid the need for
        non-prefix cursors as they are significantly slower and more
        resource-intensive than prefix cursors. Note that simply using a filter
        doesn't create a prefix cursor -- it must meet the two conditions listed
        above.

        This function is thread safe across disparate cursors.

        Args:
            filt: Iteration limited to keys matching this prefix filter.
            txn: Transaction context.
            flags: Flags for operation specialization.

        Returns:
            KvsCursor: A cursor handle.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cursor: KvsCursor = KvsCursor(
            self,
            filt,
            txn=txn,
            flags=flags,
        )

        return cursor


@unique
class KvdbTransactionState(Enum):
    """
    Transaction state.
    """
    INVALID = HSE_KVDB_TXN_INVALID
    ACTIVE = HSE_KVDB_TXN_ACTIVE
    COMMITTED = HSE_KVDB_TXN_COMMITTED
    ABORTED = HSE_KVDB_TXN_ABORTED


@cython.no_gc_clear
cdef class KvdbTransaction:
    """
    The HSE KVDB provides transactions with operations spanning KVSs within a
    single KVDB. These transactions have snapshot isolation (a specific form of
    MVCC) with the normal semantics (see "Concurrency Control and Recovery in
    Database Systems" by PA Bernstein).

    One unusual aspect of the API as it relates to transactions is that the data
    object that is used to hold client-level transaction state is allocated
    separately from the transaction being initiated. As a result, the same object
    handle should be reused again and again.

    In addition, there is very limited coupling between threading and
    transactions. A single thread may have many transactions in flight
    simultaneously. Also operations within a transaction can be performed by
    multiple threads. The latter mode of operation must currently restrict calls
    so that only one thread is actively performing an operation in the context of
    a particular transaction at any particular time.

    The general lifecycle of a transaction is as follows:

                          +----------+
                          | INVALID  |
                          +----------+
                                |
                                v
                          +----------+
        +---------------->|  ACTIVE  |<----------------+
        |                 +----------+                 |
        |  +-----------+    |      |     +----------+  |
        +--| COMMITTED |<---+      +---->| ABORTED  |--+
           +-----------+                 +----------+

    When a transaction is initially allocated, it starts in the INVALID state.
    When ``KvdbTransaction.begin()`` is called with transaction in the INVALID,
    COMMITTED, or ABORTED states, it moves to the ACTIVE state. It is an error to
    call the hse_kvdb_txn_begin() function on a transaction in the ACTIVE state.
    For a transaction in the ACTIVE state, only the functions
    ``KvdbTransaction.commit()`` or``KvdbTransaction.abort()`` may be
    called.

    When a transaction becomes ACTIVE, it establishes an ephemeral snapshot view
    of the state of the KVDB. Any data mutations outside of the transaction's
    context after that point are not visible to the transaction. Similarly, any
    mutations performed within the context of the transaction are not visible
    outside of the transaction unless and until it is committed. All such
    mutations become visible atomically when the transaction commits.

    Within a transaction whenever a write operation e.g., put, delete, etc.,
    encounters a write conflict, that operation returns an error code of
    ECANCELED. The caller is then expected to re-try the operation in a new
    transaction, see ``HseException``.
    """
    def __cinit__(self, Kvdb kvdb):
        self.kvdb = kvdb

        with nogil:
            self._c_hse_kvdb_txn = hse_kvdb_txn_alloc(kvdb._c_hse_kvdb)
        if not self._c_hse_kvdb_txn:
            raise MemoryError()

    def __dealloc__(self):
        if not self.kvdb._c_hse_kvdb:
            return
        if not self._c_hse_kvdb_txn:
            return

        with nogil:
            hse_kvdb_txn_free(self.kvdb._c_hse_kvdb, self._c_hse_kvdb_txn)
            self._c_hse_kvdb_txn = NULL

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]):
        # PEP-343: If exception occurred in with statement, abort transaction
        if exc_tb:
            self.abort()
            return

        if self.state == KvdbTransactionState.ACTIVE:
            self.commit()

        with nogil:
            hse_kvdb_txn_free(self.kvdb._c_hse_kvdb, self._c_hse_kvdb_txn)
            self._c_hse_kvdb_txn = NULL

    def begin(self) -> None:
        """
        Initiate transaction.

        The call fails if the transaction handle refers to an ACTIVE transaction.

        This function is thread safe with different transactions.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvdb_txn_begin(self.kvdb._c_hse_kvdb, self._c_hse_kvdb_txn)
        if err != 0:
            raise HseException(err)

    def commit(self) -> None:
        """
        Commit all the mutations of the referenced transaction.

        The call fails if the referenced transaction is not in the ACTIVE state.

        This function is thread safe with different transactions.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvdb_txn_commit(self.kvdb._c_hse_kvdb, self._c_hse_kvdb_txn)
        if err != 0:
            raise HseException(err)

    def abort(self) -> None:
        """
        Abort/rollback transaction.

        The call fails if the referenced transaction is not in the ACTIVE state.

        This function is thread safe with different transactions.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvdb_txn_abort(self.kvdb._c_hse_kvdb, self._c_hse_kvdb_txn)
        if err != 0:
            raise HseException(err)

    @property
    def state(self) -> KvdbTransactionState:
        """
        Retrieve the state of the referenced transaction.

        This function is thread safe with different transactions.

        Returns:
            KvdbTransactionState: Transaction's state.
        """
        cdef hse_kvdb_txn_state state = HSE_KVDB_TXN_INVALID
        with nogil:
            state = hse_kvdb_txn_state_get(self.kvdb._c_hse_kvdb, self._c_hse_kvdb_txn)
        return KvdbTransactionState(state)


cdef class KvsCursor:
    def __cinit__(
        self,
        Kvs kvs,
        filt: Optional[Union[str, bytes]]=None,
        KvdbTransaction txn=None,
        flags: Optional[CursorCreateFlag]=None,
    ):
        self._eof = False

        cdef unsigned int cflags = int(flags) if flags else 0
        cdef hse_kvdb_txn *txn_addr = NULL
        cdef const void *filt_addr = NULL
        cdef size_t filt_len = 0

        cdef const unsigned char[:] filt_view = to_bytes(filt)

        if txn:
            txn_addr = txn._c_hse_kvdb_txn
        if filt_view is not None:
            filt_addr = &filt_view[0]
            filt_len = filt_view.shape[0]

        with nogil:
            err = hse_kvs_cursor_create(
                kvs._c_hse_kvs,
                cflags,
                txn_addr,
                filt_addr,
                filt_len,
                &self._c_hse_kvs_cursor
            )
        if err != 0:
            raise HseException(err)

    def __dealloc__(self):
        if self._c_hse_kvs_cursor:
            with nogil:
                hse_kvs_cursor_destroy(self._c_hse_kvs_cursor)
            self._c_hse_kvs_cursor = NULL

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]):
        self.destroy()

    def destroy(self):
        """
        Destroy cursor.

        After invoking this function, calling any other cursor functions
        with this handle will result in undefined behavior.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        if self._c_hse_kvs_cursor:
            with nogil:
                hse_kvs_cursor_destroy(self._c_hse_kvs_cursor)
            self._c_hse_kvs_cursor = NULL

    def items(self) -> Iterator[Tuple[bytes, Optional[bytes]]]:
        """
        Convenience function to return an iterator over key-value pairs in a cursor's
        view.

        Args:
            max_count: Limit for the number of results.

        Returns:
            Iterator of key-value pairs.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        def _iter():
            while True:
                key, val = self.read()
                if not self._eof:
                    yield key, val
                else:
                    return

        return _iter()

    def update_view(self) -> None:
        """
        Update a the cursor view.

        This operation updates the snapshot view of a non-transaction cursor. It is a
        no-op on transaction cursors.

        This function is thread safe across disparate cursors.

        Args:
            flags: Flags for operation specialization.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef unsigned int cflags = 0

        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvs_cursor_update_view(self._c_hse_kvs_cursor, cflags)
        if err != 0:
            raise HseException(err)

    def seek(self, key: Union[str, bytes, SupportsBytes]) -> Optional[bytes]:
        """
        Move the cursor to point at the key-value pair at or closest to ``key``.

        The next ``KvsCursor.read()`` will start at this point.

        This function is thread safe across disparate cursors.

        Args:
            key: Key to find.

        Returns:
            bytes: Next key in sequence.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef unsigned int cflags = 0
        cdef const void *key_addr = NULL
        cdef size_t key_len = 0

        cdef const unsigned char [:]key_view = to_bytes(key)

        if key_view is not None:
            key_addr = &key_view[0]
            key_len = key_view.shape[0]

        cdef const void *found = NULL
        cdef size_t found_len = 0
        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvs_cursor_seek(
                self._c_hse_kvs_cursor,
                cflags,
                key_addr,
                key_len,
                &found,
                &found_len
            )
        if err != 0:
            raise HseException(err)

        if not found:
            return None

        return (<char *>found)[:found_len]

    def seek_range(self, filt_min: Optional[Union[str, bytes, SupportsBytes]], filt_max: Optional[Union[str, bytes, SupportsBytes]]) -> Optional[bytes]:
        """
        Move the cursor to the closest match to key, gated by the given filter.

        Keys read from this cursor will belong to the closed interval defined by the
        given filter: [``filt_min``, ``filt_max``]. For KVSs storing segmented keys,
        performance will be enhanced when ``len(filt_min)`` and ``len(filt_max)`` are
        greater than or equal to the KVS key prefix length.

        This is only supported for forward cursors.

        This function is thread safe across disparate cursors.

        Args:
            filt_min: Filter minimum.
            filt_max: Filter maximum.

        Returns:
            bytes: Next key in sequence.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef unsigned int cflags = 0
        cdef const void *filt_min_addr = NULL
        cdef size_t filt_min_len = 0
        cdef const void *filt_max_addr = NULL
        cdef size_t filt_max_len = 0

        cdef const unsigned char[:] filt_min_view = to_bytes(filt_min)
        cdef const unsigned char[:] filt_max_view = to_bytes(filt_max)

        if filt_min_view is not None:
            filt_min_addr = &filt_min_view[0]
            filt_min_len = filt_min_view.shape[0]
        if filt_max_view is not None:
            filt_max_addr = &filt_max_view[0]
            filt_max_len = filt_max_view.shape[0]

        cdef const void *found = NULL
        cdef size_t found_len = 0
        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvs_cursor_seek_range(
                self._c_hse_kvs_cursor,
                cflags,
                filt_min_addr,
                filt_min_len,
                filt_max_addr,
                filt_max_len,
                &found,
                &found_len
            )
        if err != 0:
            raise HseException(err)

        if not found:
            return None

        return (<char *>found)[:found_len]

    def read(self) -> Tuple[Optional[bytes], Optional[bytes]]:
        """
        Iteratively access the elements pointed to by the cursor.

        Read a key-value pair from the cursor, advancing the cursor past its current
        location.

        If the cursor is at EOF, attempts to read from it will not change the
        state of the cursor.

        This function is thread safe across disparate cursors.

        Returns:
            tuple: Key-value pair.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        cdef unsigned int cflags = 0
        cdef const void *key = NULL
        cdef const void *value = NULL
        cdef size_t key_len = 0
        cdef size_t value_len = 0
        cdef cbool eof = False
        cdef hse_err_t err = 0
        with nogil:
            err = hse_kvs_cursor_read(
                self._c_hse_kvs_cursor,
                cflags,
                &key,
                &key_len,
                &value,
                &value_len,
                &eof
            )
        if err != 0:
            raise HseException(err)

        self._eof = eof
        if eof:
            return None, None
        else:
            return (<char *>key)[:key_len], (<char *>value)[:value_len] if value else None

    @property
    def eof(self) -> bool:
        """
        Whether the cursor has more data to read.
        """
        return self._eof


IF HSE_PYTHON_EXPERIMENTAL == 1:
    cdef class KvdbCompactStatus:
        """
        Status of a compaction request.
        """
        @property
        def samp_lwm(self) -> int:
            """
            space amp low water mark (%).
            """
            return self._c_hse_kvdb_compact_status.kvcs_samp_lwm

        @property
        def samp_hwm(self) -> int:
            """
            space amp high water mark (%).
            """
            return self._c_hse_kvdb_compact_status.kvcs_samp_hwm

        @property
        def samp_curr(self) -> int:
            """
            current space amp (%).
            """
            return self._c_hse_kvdb_compact_status.kvcs_samp_curr

        @property
        def active(self) -> int:
            """
            is an externally requested compaction underway.
            """
            return self._c_hse_kvdb_compact_status.kvcs_active

        @property
        def canceled(self) -> int:
            """
            was an externally requested compaction canceled.
            """
            return self._c_hse_kvdb_compact_status.kvcs_canceled


IF HSE_PYTHON_EXPERIMENTAL == 1:
    cdef class KvdbStorageInfo:
        """
        Storage information for a KVDB.
        """
        @property
        def total_bytes(self) -> int:
            """
            total space in the file-system containing this kvdb.
            """
            return self._c_hse_kvdb_storage_info.total_bytes

        @property
        def available_bytes(self) -> int:
            """
            available space in the file-system containing this kvdb.
            """
            return self._c_hse_kvdb_storage_info.available_bytes

        @property
        def allocated_bytes(self) -> int:
            """
            allocated storage space for a kvdb.
            """
            return self._c_hse_kvdb_storage_info.allocated_bytes

        @property
        def used_bytes(self) -> int:
            """
            used storage space for a kvdb.
            """
            return self._c_hse_kvdb_storage_info.used_bytes
