# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import warnings
from pathlib import Path
from typing import Union

from framefile import Format
from framefile._base import filename_to_pattern


def filename_to_pct_pattern(filename: Union[str, Path], min_length=2) -> str:
    warnings.warn("Use filename_to_pattern", DeprecationWarning)  # 2021-10
    return filename_to_pattern(Format.percent, filename, min_length=min_length)


def filename_to_hash_pattern(filename: Union[str, Path], min_length=2) -> str:
    warnings.warn("Use filename_to_pattern", DeprecationWarning)  # 2021-10
    return filename_to_pattern(Format.hash, filename, min_length=min_length)