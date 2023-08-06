# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2020 Micron Technology, Inc. All rights reserved.

"""

Maximum number of KVSs contained within one KVDB

Maximum key length.

A common requirement clients have for key length is 1024.
Combined with a discriminant and (potentially) a chunk key, this pushes us to
1030 bytes keys. Looking at the packing for the on-media format for data, we
can have at most 3 keys of such large size in a 4k page. Lopping off 64-bytes
for other data, and we can have 3 keys of 1344 bytes.

Max value length is 1MiB.

Max key prefix length.

Maximum length of a KVS name.

KVS names are NULL-terminated strings. The string plus the NULL-terminator
must fit into a ``KVS_NAME_LEN_MAX`` byte buffer.
"""

cimport limits

KVS_COUNT_MAX = limits.HSE_KVS_COUNT_MAX
KVS_KEY_LEN_MAX = limits.HSE_KVS_KEY_LEN_MAX
KVS_VALUE_LEN_MAX = limits.HSE_KVS_VALUE_LEN_MAX
KVS_PFX_LEN_MAX = limits.HSE_KVS_PFX_LEN_MAX
KVS_NAME_LEN_MAX = limits.HSE_KVS_NAME_LEN_MAX
