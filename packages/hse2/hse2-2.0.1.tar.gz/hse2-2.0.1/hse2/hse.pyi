# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2020-2021 Micron Technology, Inc. All rights reserved.

import os
from enum import Enum, IntFlag
from types import TracebackType
from typing import Iterator, List, Optional, SupportsBytes, Tuple, Type, Any, Union

def init(config: Optional[Union[str, os.PathLike[str]]] = ..., *params: str) -> None:
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
    ...

def fini() -> None:
    """
    Shutdown the HSE subsystem.

    This function cleanly finalizes a range of different internal HSE structures.
    It should be called prior to application exit.

    After invoking this function, calling any other HSE functions will
    result in undefined behavior unless HSE is re-initialized.

    This function is not thread safe.
    """
    ...

class HseException(Exception):
    """
    Raised when HSE encounters an error. Wrapper around ``hse_err_t``.

    Attributes:
        returncode: Errno value returned by HSE.
    """

    returncode: int
    def __init__(self, returncode: int) -> None: ...

class KvdbSyncFlag(IntFlag):
    """
    Attributes:
        ASYNC: Return immediately after initiating operation
    """

    ASYNC = ...

class Kvdb:
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
        ...
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
        ...
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
        ...
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
        ...
    @property
    def kvs_names(self) -> List[str]:
        """
        Get the names of the KVSs within the given KVDB.

        Key-value stores (KVSs) are opened by name. This function allocates a vector
        of allocated strings.

        Returns:
            List[str]: List of KVS names.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        ...
    def kvs_create(self, name: str, *params: str) -> None:
        """
        Create a new KVS within the referenced KVDB.

        This function is not thread safe.

        Args:

        name: KVS name.
        params: List of parameters in key=value format.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        ...
    def kvs_drop(self, name: str) -> None:
        """
        Drop a KVS from the referenced KVDB.

        It is an error to call this function on a KVS that is open.

        This function is not thread safe.

        Args:
            name: KVS name.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        ...
    def kvs_open(self, name: str, *params: str) -> Kvs:
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
        ...
    def sync(self, flags: Optional[KvdbSyncFlag] = ...) -> None:
        """
        Sync data in all of the referenced KVDB's KVSs to stable media.

        Args:
            flags: Flags for operation specialization.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        ...
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
        ...
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
        ...
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
        ...
    # endif
    @staticmethod
    def storage_add(kvdb_home: Union[str, "os.PathLike[str]"], params: str) -> None:
        """
        Add a new media class storage to an existing offline KVDB.

        This function is not thread safe.

        Args:
            kvdb_home: KVDB home directory.
            params: List of parameters in key=value format.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
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
        ...

class KvsPutFlag(IntFlag):
    """
    Attributes:
        PRIO: Operation will not be throttled
        VCOMP_OFF: Value will not be compressed
    """

    PRIO = ...
    VCOMP_OFF = ...

class CursorCreateFlag(IntFlag):
    """
    Attributes:
        REV: iterate in reverse lexicographical order
    """

    REV = ...

    """
    Number of keys found from a prefix probe operation.

    Attributes:
        ZERO: Zero keys found with prefix.
        ONE: One key found with prefix.
        MUL: Multiple keys found with prefix.
    """

    ZERO = ...
    ONE = ...
    MUL = ...

# endif

class Kvs:
    def close(self) -> None:
        """
        Close an open KVS.

        After invoking this function, calling any other KVS functions will
        result in undefined behavior unless the KVS is re-opened.

        This function is not thread safe.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        ...
    def put(
        self,
        key: Union[str, bytes, SupportsBytes],
        value: Optional[Union[str, bytes, SupportsBytes]],
        txn: Optional[KvdbTransaction] = ...,
        flags: Optional[KvsPutFlag] = ...,
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
        ...
    def get(
        self,
        key: Union[str, bytes, SupportsBytes],
        txn: Optional[KvdbTransaction] = ...,
        buf: Optional[bytearray] = ...,
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
        ...
    def delete(
        self,
        key: Union[str, bytes, SupportsBytes],
        txn: Optional[KvdbTransaction] = ...,
    ) -> None:
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
        ...
    def prefix_delete(
        self, pfx: Union[str, bytes], txn: Optional[KvdbTransaction] = ...
    ) -> None:
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
        ...
        self,
        pfx: Union[str, bytes],
        key_buf: bytearray = ...,
        value_buf: Optional[bytearray] = ...,
        txn: Optional[KvdbTransaction] = ...,
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
        ...
    # endif
    def cursor(
        self,
        filt: Optional[Union[str, bytes]] = ...,
        txn: Optional[KvdbTransaction] = ...,
        flags: Optional[CursorCreateFlag] = ...,
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
        ...

class KvdbTransactionState(Enum):
    """
    Transaction state.
    """

    INVALID: int
    ACTIVE: int
    COMMITTED: int
    ABORTED: int

class KvdbTransaction:
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

    def __enter__(self) -> KvdbTransaction: ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[Any],
        exc_tb: Optional[TracebackType],
    ) -> None: ...
    def begin(self) -> None:
        """
        Initiate transaction.

        The call fails if the transaction handle refers to an ACTIVE transaction.

        This function is thread safe with different transactions.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        ...
    def commit(self) -> None:
        """
        Commit all the mutations of the referenced transaction.

        The call fails if the referenced transaction is not in the ACTIVE state.

        This function is thread safe with different transactions.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        ...
    def abort(self) -> None:
        """
        Abort/rollback transaction.

        The call fails if the referenced transaction is not in the ACTIVE state.

        This function is thread safe with different transactions.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        ...
    @property
    def state(self) -> KvdbTransactionState:
        """
        Retrieve the state of the referenced transaction.

        This function is thread safe with different transactions.

        Returns:
            KvdbTransactionState: Transaction's state.
        """
        ...

class KvsCursor:
    def __enter__(self) -> KvsCursor: ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[Any],
        exc_tb: Optional[TracebackType],
    ) -> None: ...
    @property
    def eof(self) -> bool:
        """
        Whether the cursor has more data to read.
        """
        ...
    def destroy(self) -> None:
        """
        Destroy cursor.

        After invoking this function, calling any other cursor functions
        with this handle will result in undefined behavior.

        Raises:
            HseException: Underlying C function returned a non-zero value.
        """
        ...
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
        ...
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
        ...
    def update_view(
        self,
        txn: Optional[KvdbTransaction] = ...,
    ) -> None:
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
        ...
    def seek(self, key: Optional[Union[str, bytes, SupportsBytes]]) -> Optional[bytes]:
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
        ...
    def seek_range(
        self,
        filt_min: Optional[Union[str, bytes, SupportsBytes]],
        filt_max: Optional[Union[str, bytes, SupportsBytes]],
    ) -> Optional[bytes]:
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
        ...

    """
    Status of a compaction request.
    """

    @property
    def samp_lwm(self) -> int:
        """
        space amp low water mark (%).
        """
        ...
    @property
    def samp_hwm(self) -> int:
        """
        space amp high water mark (%).
        """
        ...
    @property
    def samp_curr(self) -> int:
        """
        current space amp (%).
        """
        ...
    @property
    def active(self) -> int:
        """
        is an externally requested compaction underway.
        """
        ...
    @property
    def canceled(self) -> int:
        """
        was an externally requested compaction canceled.
        """
        ...

# endif

class KvdbStorageInfo:
    """
    Storage information for a KVDB.
    """

    @property
    def total_bytes(self) -> int:
        """
        total space in the file-system containing this kvdb.
        """
        ...
    @property
    def available_bytes(self) -> int:
        """
        available space in the file-system containing this kvdb.
        """
        ...
    @property
    def allocated_bytes(self) -> int:
        """
        allocated storage space for a kvdb.
        """
        ...
    @property
    def used_bytes(self) -> int:
        """
        used storage space for a kvdb.
        """
        ...
