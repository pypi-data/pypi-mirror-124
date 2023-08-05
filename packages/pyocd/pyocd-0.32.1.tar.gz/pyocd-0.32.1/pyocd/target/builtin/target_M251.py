# pyOCD debugger
# Copyright (c) 2019 Nuvoton
# Copyright (c) 2021 Chris Reed
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ...coresight.coresight_target import CoreSightTarget
from ...core.memory_map import (FlashRegion, RamRegion, MemoryMap)
from ...debug.svd.loader import SVDFile

FLASH_ALGO_AP_256 = {
    'load_address' : 0x20000000,
    'instructions': [
    0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
    0xb088b5b0, 0x460c4613, 0x90064605, 0x92049105, 0x90032064, 0x1000f240, 0x0000f2c4, 0x60012159,
    0x60012116, 0x60012188, 0x21016800, 0x93024208, 0x95009401, 0xe7ffd103, 0x90072001, 0xf240e038,
    0xf2c42000, 0x68010000, 0x43112204, 0xf2406001, 0xf2c42004, 0x68010000, 0x60014311, 0x9803e7ff,
    0x91031e41, 0xd0012800, 0xe7f8e7ff, 0x0000f24c, 0x0000f2c4, 0x222d6801, 0x60014311, 0x011cf24c,
    0x0100f2c4, 0x2301680a, 0x600a431a, 0x42186800, 0xe7ffd103, 0x90072001, 0xf24ce00a, 0xf2c40000,
    0x68010000, 0x43112240, 0x20006001, 0xe7ff9007, 0xb0089807, 0xb082bdb0, 0x90014601, 0xe7ff9100,
    0x0010f24c, 0x0000f2c4, 0x21016800, 0xd0014208, 0xe7f5e7ff, 0x0000f24c, 0x0000f2c4, 0x222d6801,
    0x60014391, 0x001cf24c, 0x0000f2c4, 0x22016801, 0x60014391, 0xb0022000, 0xb0854770, 0x4603460a,
    0xa8029003, 0x92017001, 0xe7ff9300, 0x0010f24c, 0x0000f2c4, 0x21016800, 0xd0014208, 0xe7f5e7ff,
    0x0000f24c, 0x0000f2c4, 0x22406801, 0x60014311, 0x000cf24c, 0x0000f2c4, 0x60012122, 0xf24c9803,
    0xf2c40104, 0x60080100, 0x7800a802, 0xd1082800, 0x2000e7ff, 0xf24c43c0, 0xf2c40108, 0x60080100,
    0xf24ce009, 0xf2c40008, 0xf64a0000, 0xf2c02103, 0x60010155, 0xf24ce7ff, 0xf2c40010, 0x21010000,
    0xf3bf6001, 0xe7ff8f6f, 0x0010f24c, 0x0000f2c4, 0x21016800, 0xd0014208, 0xe7f5e7ff, 0x0000f24c,
    0x0000f2c4, 0x21406800, 0xd00b4208, 0xf24ce7ff, 0xf2c40000, 0x68010000, 0x43112240, 0x20016001,
    0xe0029004, 0x90042000, 0x9804e7ff, 0x4770b005, 0xb084b580, 0x90024601, 0x220f9802, 0x40100512,
    0x05522201, 0x91014290, 0xe7ffd10b, 0xf2409802, 0xf6cf0100, 0x184071e0, 0xf7ff2101, 0x9003ff7e,
    0x9802e005, 0xf7ff2100, 0x9003ff78, 0x9803e7ff, 0xbd80b004, 0xb088b580, 0x4603460a, 0x91059006,
    0x90042000, 0x93019202, 0x9804e7ff, 0x42889905, 0xe7ffd210, 0x99049806, 0x92041c4a, 0x58400089,
    0xffc6f7ff, 0x28009003, 0xe7ffd003, 0x90079803, 0xe7eae003, 0x90072000, 0x9807e7ff, 0xbd80b008,
    0xb08ab5b0, 0x460c4613, 0x90084605, 0x92069107, 0x90042000, 0x93029003, 0x95009401, 0xf24ce7ff,
    0xf2c40010, 0x68000000, 0x42082101, 0xe7ffd001, 0xf24ce7f5, 0xf2c40000, 0x68010000, 0x43112240,
    0x98076001, 0x21031cc0, 0x90074388, 0x9807e7ff, 0xd04c2800, 0xa808e7ff, 0x06407800, 0xd10f2800,
    0x9807e7ff, 0xd30b2880, 0x2080e7ff, 0x98089005, 0x9a069905, 0x18d29b04, 0xf83ff000, 0xe0229003,
    0x7800a808, 0x28000640, 0xe7ffd111, 0x28109807, 0xe7ffd30d, 0x210f9807, 0x90054388, 0x99059808,
    0x9b049a06, 0xf00018d2, 0x9003f828, 0x9807e00a, 0x98089005, 0x9a069905, 0x18d29b04, 0xf8e0f000,
    0xe7ff9003, 0x9805e7ff, 0x18089908, 0x98059008, 0x18089904, 0x98059004, 0x1a089907, 0x98039007,
    0xd0032800, 0x2001e7ff, 0xe0039009, 0x2000e7af, 0xe7ff9009, 0xb00a9809, 0xb5b0bdb0, 0x4613b088,
    0x4605460c, 0x91069007, 0x20009205, 0x98059003, 0x98069004, 0x210f300f, 0x90064388, 0x94019302,
    0xe7ff9500, 0x0010f24c, 0x0000f2c4, 0x21016800, 0xd0014208, 0xe7f5e7ff, 0x0000f24c, 0x0000f2c4,
    0x22406801, 0x60014311, 0x210f9807, 0xf24c4388, 0xf2c40104, 0x60080100, 0x000cf24c, 0x0000f2c4,
    0x60012127, 0x99039804, 0x92031c4a, 0x58400089, 0x0180f24c, 0x0100f2c4, 0x98046008, 0x1c4a9903,
    0x00899203, 0xf24c5840, 0xf2c40184, 0x60080100, 0x99039804, 0x92031c4a, 0x58400089, 0x0188f24c,
    0x0100f2c4, 0x98046008, 0x1c4a9903, 0x00899203, 0xf24c5840, 0xf2c4018c, 0x60080100, 0x0010f24c,
    0x0000f2c4, 0x60012101, 0x38109806, 0xe7ff9006, 0x28009806, 0xe7ffd046, 0xf24ce7ff, 0xf2c400c0,
    0x68000000, 0x42082130, 0xe7ffd001, 0x9804e7f5, 0x1c4a9903, 0x00899203, 0xf24c5840, 0xf2c40180,
    0x60080100, 0x99039804, 0x92031c4a, 0x58400089, 0x0184f24c, 0x0100f2c4, 0xe7ff6008, 0x00c0f24c,
    0x0000f2c4, 0x21c06800, 0xd0014208, 0xe7f5e7ff, 0x99039804, 0x92031c4a, 0x58400089, 0x0188f24c,
    0x0100f2c4, 0x98046008, 0x1c4a9903, 0x00899203, 0xf24c5840, 0xf2c4018c, 0x60080100, 0x38109806,
    0xe7b59006, 0xf24ce7ff, 0xf2c40010, 0x68000000, 0x42082101, 0xe7ffd001, 0x2000e7f5, 0xbdb0b008,
    0xb087b5b0, 0x460c4613, 0x90054605, 0x92039104, 0x1cc09804, 0x43882103, 0x93029004, 0x95009401,
    0xf24ce7ff, 0xf2c40010, 0x68000000, 0x42082101, 0xe7ffd001, 0xf24ce7f5, 0xf2c40000, 0x68010000,
    0x43112240, 0xf24c6001, 0xf2c4000c, 0x21210000, 0xe7ff6001, 0x28009804, 0xe7ffd040, 0x21039805,
    0xf24c4388, 0xf2c40104, 0x60080100, 0x68009803, 0x0108f24c, 0x0100f2c4, 0xf24c6008, 0xf2c40010,
    0x21010000, 0xf3bf6001, 0xe7ff8f6f, 0x0010f24c, 0x0000f2c4, 0x21016800, 0xd0014208, 0xe7f5e7ff,
    0x0000f24c, 0x0000f2c4, 0x21406800, 0xd00b4208, 0xf24ce7ff, 0xf2c40000, 0x68010000, 0x43112240,
    0x20016001, 0xe00c9006, 0x1d009805, 0x98039005, 0x90031d00, 0x1f009804, 0xe7bb9004, 0x90062000,
    0x9806e7ff, 0xbdb0b007, 0xb087b5b0, 0x460c4613, 0x90054605, 0x92039104, 0x1cc09804, 0x43882103,
    0x93029004, 0x95009401, 0xf24ce7ff, 0xf2c40010, 0x68000000, 0x42082101, 0xe7ffd001, 0xf24ce7f5,
    0xf2c40000, 0x68010000, 0x43112240, 0xf24c6001, 0xf2c4000c, 0x21000000, 0xe7ff6001, 0x28009804,
    0xe7ffd04c, 0x21039805, 0xf24c4388, 0xf2c40104, 0x60080100, 0x0008f24c, 0x0000f2c4, 0x60012100,
    0x0010f24c, 0x0000f2c4, 0x60012101, 0x8f6ff3bf, 0xf24ce7ff, 0xf2c40010, 0x68000000, 0x42082101,
    0xe7ffd001, 0xf24ce7f5, 0xf2c40000, 0x68000000, 0x42082140, 0xe7ffd00b, 0x0000f24c, 0x0000f2c4,
    0x22406801, 0x60014311, 0x90062001, 0xf24ce019, 0xf2c40008, 0x68000000, 0x68099903, 0xd0034288,
    0x2001e7ff, 0xe00c9006, 0x1d009805, 0x98039005, 0x90031d00, 0x1f009804, 0xe7af9004, 0x90062000,
    0x9806e7ff, 0xbdb0b007, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x20000021,
    'pc_unInit': 0x200000d7,
    'pc_program_page': 0x20000281,
    'pc_erase_sector': 0x200001f1,
    'pc_eraseAll': 0x0,

    'static_base' : 0x20000000 + 0x00000020 + 0x000006c8,
    'begin_stack' : 0x20000900,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x200,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20001200],   # Enable double buffering
    'min_program_length' : 0x200,

    # Flash information
    'flash_start': 0x0,
    'flash_size': 0x40000,
    'sector_sizes': (
        (0x0, 0x200),
    )
}

FLASH_ALGO_LD_4 = {
    'load_address' : 0x20000000,
    'instructions': [
    0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
    0xb089b5b0, 0x460c4613, 0x90074605, 0x92059106, 0x90032064, 0x1000f240, 0x0000f2c4, 0x60012159,
    0x60012116, 0x60012188, 0x21016800, 0x93024208, 0x95009401, 0xe7ffd103, 0x90082001, 0xf240e044,
    0xf2c42000, 0x68010000, 0x43112204, 0xf2406001, 0xf2c42004, 0x68010000, 0x60014311, 0x9803e7ff,
    0x91031e41, 0xd0012800, 0xe7f8e7ff, 0x0000f24c, 0x0000f2c4, 0x222d6801, 0x60014311, 0x011cf24c,
    0x0100f2c4, 0x2301680a, 0x600a431a, 0x42186800, 0xe7ffd103, 0x90082001, 0xf24ce016, 0xf2c40000,
    0x68000000, 0x42082120, 0xe7ffd103, 0x90082001, 0xf24ce00a, 0xf2c40000, 0x68010000, 0x43112240,
    0x20006001, 0xe7ff9008, 0xb0099808, 0xb082bdb0, 0x90014601, 0xe7ff9100, 0x0010f24c, 0x0000f2c4,
    0x21016800, 0xd0014208, 0xe7f5e7ff, 0x0000f24c, 0x0000f2c4, 0x222d6801, 0x60014391, 0x001cf24c,
    0x0000f2c4, 0x22016801, 0x60014391, 0xb0022000, 0xb5b04770, 0x4613b086, 0x4605460c, 0x91049005,
    0x7002a803, 0x93022001, 0x95009401, 0xbdb0b006, 0x460ab085, 0x90034603, 0x7001a802, 0x93009201,
    0xf24ce7ff, 0xf2c40010, 0x68000000, 0x42082101, 0xe7ffd001, 0xf24ce7f5, 0xf2c40000, 0x68010000,
    0x43112240, 0xf24c6001, 0xf2c4000c, 0x21220000, 0x98036001, 0x0104f24c, 0x0100f2c4, 0xa8026008,
    0x28007800, 0xe7ffd108, 0x43c02000, 0x0108f24c, 0x0100f2c4, 0xe0096008, 0x0008f24c, 0x0000f2c4,
    0x2103f64a, 0x0155f2c0, 0xe7ff6001, 0x0010f24c, 0x0000f2c4, 0x60012101, 0x8f6ff3bf, 0xf24ce7ff,
    0xf2c40010, 0x68000000, 0x42082101, 0xe7ffd001, 0xf24ce7f5, 0xf2c40000, 0x68000000, 0x42082140,
    0xe7ffd00b, 0x0000f24c, 0x0000f2c4, 0x22406801, 0x60014311, 0x90042001, 0x2000e002, 0xe7ff9004,
    0xb0059804, 0xb5804770, 0x4601b084, 0x98029002, 0x0512220f, 0x22014010, 0x42900552, 0xd10b9101,
    0x9802e7ff, 0x0100f240, 0x71e0f6cf, 0x21011840, 0xff7ef7ff, 0xe0059003, 0x21009802, 0xff78f7ff,
    0xe7ff9003, 0xb0049803, 0xb580bd80, 0x460ab088, 0x90064603, 0x20009105, 0x92029004, 0xe7ff9301,
    0x99059804, 0xd2104288, 0x9806e7ff, 0x1c4a9904, 0x00899204, 0xf7ff5840, 0x9003ffc6, 0xd0032800,
    0x9803e7ff, 0xe0039007, 0x2000e7ea, 0xe7ff9007, 0xb0089807, 0xb5b0bd80, 0x4613b08a, 0x4605460c,
    0x91079008, 0x20009206, 0x90039004, 0x94019302, 0xe7ff9500, 0x0010f24c, 0x0000f2c4, 0x21016800,
    0xd0014208, 0xe7f5e7ff, 0x0000f24c, 0x0000f2c4, 0x22406801, 0x60014311, 0x1cc09807, 0x43882103,
    0xe7ff9007, 0x28009807, 0xe7ffd04c, 0x7800a808, 0x28000640, 0xe7ffd10f, 0x28809807, 0xe7ffd30b,
    0x90052080, 0x99059808, 0x9b049a06, 0xf00018d2, 0x9003f83f, 0xa808e022, 0x06407800, 0xd1112800,
    0x9807e7ff, 0xd30d2810, 0x9807e7ff, 0x4388210f, 0x98089005, 0x9a069905, 0x18d29b04, 0xf828f000,
    0xe00a9003, 0x90059807, 0x99059808, 0x9b049a06, 0xf00018d2, 0x9003f8e0, 0xe7ffe7ff, 0x99089805,
    0x90081808, 0x99049805, 0x90041808, 0x99079805, 0x90071a08, 0x28009803, 0xe7ffd003, 0x90092001,
    0xe7afe003, 0x90092000, 0x9809e7ff, 0xbdb0b00a, 0xb088b5b0, 0x460c4613, 0x90074605, 0x92059106,
    0x90032000, 0x90049805, 0x300f9806, 0x4388210f, 0x93029006, 0x95009401, 0xf24ce7ff, 0xf2c40010,
    0x68000000, 0x42082101, 0xe7ffd001, 0xf24ce7f5, 0xf2c40000, 0x68010000, 0x43112240, 0x98076001,
    0x4388210f, 0x0104f24c, 0x0100f2c4, 0xf24c6008, 0xf2c4000c, 0x21270000, 0x98046001, 0x1c4a9903,
    0x00899203, 0xf24c5840, 0xf2c40180, 0x60080100, 0x99039804, 0x92031c4a, 0x58400089, 0x0184f24c,
    0x0100f2c4, 0x98046008, 0x1c4a9903, 0x00899203, 0xf24c5840, 0xf2c40188, 0x60080100, 0x99039804,
    0x92031c4a, 0x58400089, 0x018cf24c, 0x0100f2c4, 0xf24c6008, 0xf2c40010, 0x21010000, 0x98066001,
    0x90063810, 0x9806e7ff, 0xd0462800, 0xe7ffe7ff, 0x00c0f24c, 0x0000f2c4, 0x21306800, 0xd0014208,
    0xe7f5e7ff, 0x99039804, 0x92031c4a, 0x58400089, 0x0180f24c, 0x0100f2c4, 0x98046008, 0x1c4a9903,
    0x00899203, 0xf24c5840, 0xf2c40184, 0x60080100, 0xf24ce7ff, 0xf2c400c0, 0x68000000, 0x420821c0,
    0xe7ffd001, 0x9804e7f5, 0x1c4a9903, 0x00899203, 0xf24c5840, 0xf2c40188, 0x60080100, 0x99039804,
    0x92031c4a, 0x58400089, 0x018cf24c, 0x0100f2c4, 0x98066008, 0x90063810, 0xe7ffe7b5, 0x0010f24c,
    0x0000f2c4, 0x21016800, 0xd0014208, 0xe7f5e7ff, 0xb0082000, 0xb5b0bdb0, 0x4613b087, 0x4605460c,
    0x91049005, 0x98049203, 0x21031cc0, 0x90044388, 0x94019302, 0xe7ff9500, 0x0010f24c, 0x0000f2c4,
    0x21016800, 0xd0014208, 0xe7f5e7ff, 0x0000f24c, 0x0000f2c4, 0x22406801, 0x60014311, 0x000cf24c,
    0x0000f2c4, 0x60012121, 0x9804e7ff, 0xd0402800, 0x9805e7ff, 0x43882103, 0x0104f24c, 0x0100f2c4,
    0x98036008, 0xf24c6800, 0xf2c40108, 0x60080100, 0x0010f24c, 0x0000f2c4, 0x60012101, 0x8f6ff3bf,
    0xf24ce7ff, 0xf2c40010, 0x68000000, 0x42082101, 0xe7ffd001, 0xf24ce7f5, 0xf2c40000, 0x68000000,
    0x42082140, 0xe7ffd00b, 0x0000f24c, 0x0000f2c4, 0x22406801, 0x60014311, 0x90062001, 0x9805e00c,
    0x90051d00, 0x1d009803, 0x98049003, 0x90041f00, 0x2000e7bb, 0xe7ff9006, 0xb0079806, 0xb5b0bdb0,
    0x4613b087, 0x4605460c, 0x91049005, 0x98049203, 0x21031cc0, 0x90044388, 0x94019302, 0xe7ff9500,
    0x0010f24c, 0x0000f2c4, 0x21016800, 0xd0014208, 0xe7f5e7ff, 0x0000f24c, 0x0000f2c4, 0x22406801,
    0x60014311, 0x000cf24c, 0x0000f2c4, 0x60012100, 0x9804e7ff, 0xd04c2800, 0x9805e7ff, 0x43882103,
    0x0104f24c, 0x0100f2c4, 0xf24c6008, 0xf2c40008, 0x21000000, 0xf24c6001, 0xf2c40010, 0x21010000,
    0xf3bf6001, 0xe7ff8f6f, 0x0010f24c, 0x0000f2c4, 0x21016800, 0xd0014208, 0xe7f5e7ff, 0x0000f24c,
    0x0000f2c4, 0x21406800, 0xd00b4208, 0xf24ce7ff, 0xf2c40000, 0x68010000, 0x43112240, 0x20016001,
    0xe0199006, 0x0008f24c, 0x0000f2c4, 0x99036800, 0x42886809, 0xe7ffd003, 0x90062001, 0x9805e00c,
    0x90051d00, 0x1d009803, 0x98049003, 0x90041f00, 0x2000e7af, 0xe7ff9006, 0xb0079806, 0x0000bdb0,
    0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x20000021,
    'pc_unInit': 0x200000ef,
    'pc_program_page': 0x200002b7,
    'pc_erase_sector': 0x20000227,
    'pc_eraseAll': 0x0,

    'static_base' : 0x20000000 + 0x00000020 + 0x00000700,
    'begin_stack' : 0x20000a00,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x200,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20001200],   # Enable double buffering
    'min_program_length' : 0x200,

    # Flash information
    'flash_start': 0x100000,
    'flash_size': 0x1000,
    'sector_sizes': (
        (0x0, 0x200),
    )
}

class M252KG6AE(CoreSightTarget):
    VENDOR = "Nuvoton"

    MEMORY_MAP = MemoryMap(
        FlashRegion( start=0x00000000, length=0x40000,  sector_size=0x0200,
                                                        page_size=0x0200,
                                                        is_boot_memory=True,
                                                        algo=FLASH_ALGO_AP_256),
        FlashRegion( start=0x00100000, length=0x1000,   sector_size=0x0200,
                                                        page_size=0x0200,
                                                        algo=FLASH_ALGO_LD_4),
        RamRegion(   start=0x20000000, length=0x8000)
        )

    def __init__(self, session):
        super(M252KG6AE, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("M251_v1.svd")
