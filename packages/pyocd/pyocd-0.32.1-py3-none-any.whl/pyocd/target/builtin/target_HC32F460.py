# pyOCD debugger
# Copyright (c) 2021 Huada Semiconductor Corporation
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


class DBGMCU:
    STCTL = 0xE0042020
    STCTL_VALUE = 0x3

    TRACECTL = 0xE0042024
    TRACECTL_VALUE = 0x0

FLASH_ALGO = { 'load_address' : 0x20000000,
               'instructions' : [
    0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
    0x4770ba40, 0x4770bac0, 0x0030ea4f, 0x00004770, 0x5001f24a, 0x8008490a, 0x7800480a, 0x0007f020,
    0x39264908, 0x0026f881, 0x68004807, 0x00f0f020, 0x60084905, 0x49032001, 0x70081d09, 0x00004770,
    0x4005440e, 0x40054026, 0x40010408, 0x5101f24a, 0x80114a16, 0x6a094916, 0x0170f021, 0x4a143110,
    0xf2406211, 0x68094104, 0x0001f001, 0x4911b150, 0x60114a11, 0x68094911, 0x01f0f021, 0x4a0f3140,
    0xe0096011, 0x4a0c490e, 0x490c6011, 0xf0216809, 0x315001f0, 0x60114a09, 0x4a052100, 0x7011322a,
    0x4a032105, 0x1026f882, 0x00004770, 0x4005440e, 0x40054000, 0x10102781, 0x4005410c, 0x40010408,
    0x10101f81, 0xf241b53e, 0x90022034, 0xffa0f7ff, 0x30fff04f, 0xab022101, 0xe9cd2210, 0x20051000,
    0xf8c4f000, 0xf7ff4604, 0x4620ffb1, 0xb53ebd3e, 0xf2414604, 0x90022034, 0xff8af7ff, 0x30fff04f,
    0xab022101, 0xe9cd4622, 0x20041000, 0xf8aef000, 0xf7ff4605, 0x4628ff9b, 0x0000bd3e, 0x4604b570,
    0x4616460d, 0x49124811, 0x48126008, 0x48106008, 0x6800300c, 0x7080f420, 0x7080f500, 0x310c490c,
    0xf24a6008, 0x490c5001, 0x480c8008, 0xf4206a00, 0xf50040e0, 0x490940c0, 0xf44f6208, 0x49064025,
    0xf0008008, 0x2000f939, 0x0000bd70, 0xffff0123, 0x40010400, 0xffff3210, 0x4005440e, 0x40054000,
    0x4df0e92d, 0x4607b086, 0x4690460c, 0xf924f000, 0xea4f46c2, 0xf0040b94, 0xf04f0503, 0x900530ff,
    0x44401b60, 0xf0009004, 0x2600f917, 0x9804e004, 0xa9055d80, 0x1c765588, 0xd3f842ae, 0x2000b955,
    0x463a4653, 0xe9cd2101, 0x2002b000, 0xf84ef000, 0xe0159003, 0x46532000, 0x4601463a, 0xb000e9cd,
    0xf0002002, 0x9003f843, 0x44071b60, 0x21012000, 0x463aab05, 0x1000e9cd, 0xf000200f, 0x9003f837,
    0xb0069803, 0x8df0e8bd, 0x4604b510, 0xf8e4f000, 0x68004808, 0x7080f420, 0x60084906, 0x60082001,
    0x60082000, 0x49031e40, 0x6008390c, 0xf8d4f000, 0xbd102000, 0x4001040c, 0x41f0e92d, 0x460e4605,
    0xf04f4617, 0x46a80800, 0xe0082400, 0xf8c4f000, 0x1b01f818, 0x42815d38, 0xe002d000, 0x42b41c64,
    0xbf00d3f4, 0xe8bd1928, 0x000081f0, 0x4df8e92d, 0x468a4606, 0x469b4614, 0x90002000, 0xf8acf000,
    0xd0122e0f, 0x6800482d, 0x0001f020, 0x492b1c40, 0x46086008, 0xf3666800, 0x60081006, 0x68004608,
    0x7080f420, 0x7080f500, 0xf0006008, 0x2500f895, 0xf85be02c, 0x60200025, 0xbf004f21, 0xf88cf000,
    0x481e1e7f, 0x68001d00, 0x7080f400, 0x2f00b908, 0xb917d1f4, 0x9000201f, 0x980ae01b, 0x4817b960,
    0x68001d00, 0x080ff000, 0x0f00f1b8, 0xf000d00c, 0xf8cdf873, 0xe00c8000, 0x8000f8d4, 0x4580980a,
    0x203fd002, 0xe0049000, 0x1c6d1d24, 0x42859809, 0xbf00d3cf, 0xf860f000, 0x0f01f1ba, 0x4807d10a,
    0xf0206800, 0x49050070, 0x46086008, 0xf0206800, 0x60080001, 0xe8bd9800, 0x00008df8, 0x4001040c,
    0x00030d40, 0x1e01bf00, 0x0001f1a0, 0x4770d1fb, 0x481fb510, 0x481f6802, 0xf3c06800, 0x481d0481,
    0xf3c06800, 0xb90c2303, 0xe0081192, 0xd1012c01, 0xe0041292, 0xd1012c02, 0xe0001312, 0xb10b1392,
    0xd1022b0f, 0xf83af000, 0xf003e020, 0xb1180001, 0xf000b9e2, 0xe019f833, 0x0002f003, 0xd1042802,
    0xd1132a01, 0xf82af000, 0xf003e010, 0x28040004, 0x2a02d104, 0xf000d10a, 0xe007f821, 0x0008f003,
    0xd1032808, 0xd1012a03, 0xf818f000, 0x0000bd10, 0x40049404, 0x40010680, 0x4807b500, 0xf3c06800,
    0xb9084000, 0xf816f000, 0x68004803, 0x0001f000, 0xf7ffb908, 0xbd00ffad, 0x40010680, 0x49034802,
    0x48036008, 0x47706008, 0xffff0123, 0x40049408, 0xffff3210, 0x481fb510, 0xb2926842, 0x6800481e,
    0x4481f3c0, 0x6800481c, 0x6303f3c0, 0x1192b90c, 0x2c01e008, 0x1292d101, 0x2c02e004, 0x1312d101,
    0x1392e000, 0x2b0fb10b, 0xf000d102, 0xe020f827, 0x0001f003, 0xb9e2b118, 0xf820f000, 0xf003e019,
    0x28020002, 0x2a01d104, 0xf000d113, 0xe010f817, 0x0004f003, 0xd1042804, 0xd10a2a02, 0xf80ef000,
    0xf003e007, 0x28080008, 0x2a03d103, 0xf000d101, 0xbd10f805, 0x40049000, 0x40010680, 0x49034802,
    0x48036088, 0x47706088, 0xffff0123, 0x40049000, 0xffff3210, 0x00000000
    ],

    'pc_init': 0x2000013d,
    'pc_unInit': 0x20000229,
    'pc_program_page': 0x200001a1,
    'pc_erase_sector': 0x2000010f,
    'pc_eraseAll': 0x200000e5,

    'static_base' : 0x20000000 + 0x00000020 + 0x000004b0,
    'begin_stack' : 0x20000700,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x200,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x20001200],   # Enable double buffering
    'min_program_length' : 0x200,
}


FLASH_ALGO_OTP = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
    0x4770ba40, 0x4770bac0, 0x0030ea4f, 0x00004770, 0x5001f24a, 0x8008490a, 0x7800480a, 0x0007f020,
    0x39264908, 0x0026f881, 0x68004807, 0x00f0f020, 0x60084905, 0x49032001, 0x70081d09, 0x00004770,
    0x4005440e, 0x40054026, 0x40010408, 0x5101f24a, 0x80114a16, 0x6a094916, 0x0170f021, 0x4a143110,
    0xf2406211, 0x68094104, 0x0001f001, 0x4911b150, 0x60114a11, 0x68094911, 0x01f0f021, 0x4a0f3140,
    0xe0096011, 0x4a0c490e, 0x490c6011, 0xf0216809, 0x315001f0, 0x60114a09, 0x4a052100, 0x7011322a,
    0x4a032105, 0x1026f882, 0x00004770, 0x4005440e, 0x40054000, 0x10102781, 0x4005410c, 0x40010408,
    0x10101f81, 0x47702000, 0x20004601, 0x00004770, 0x4604b570, 0x4616460d, 0x49124811, 0x48126008,
    0x48106008, 0x6800300c, 0x7080f420, 0x7080f500, 0x310c490c, 0xf24a6008, 0x490c5001, 0x480c8008,
    0xf4206a00, 0xf50040e0, 0x490940c0, 0xf44f6208, 0x49064025, 0xf0008008, 0x2000f8f7, 0x0000bd70,
    0xffff0123, 0x40010400, 0xffff3210, 0x4005440e, 0x40054000, 0x45f0e92d, 0x460e4605, 0xf8df4614,
    0xf00080b8, 0x482df8e1, 0xf0206800, 0x1c400001, 0x6008492a, 0x68004608, 0x0070f020, 0x60083020,
    0x68004608, 0x7080f420, 0x7080f500, 0x46aa6008, 0xf000bf00, 0x2700f8c9, 0xf000e02a, 0xf8dff8c5,
    0x68208078, 0x0000f8ca, 0x0a04f10a, 0xf0001d24, 0xe001f8bb, 0xf8b8f000, 0x1d004818, 0xf4006800,
    0xb9207080, 0x0001f1a8, 0x0800f1b0, 0xf1b8d1f2, 0xd1020f00, 0xe8bd2001, 0x481085f0, 0x68001d00,
    0x000ff000, 0xf000b118, 0x2001f89f, 0x1c7fe7f3, 0x0f96ebb7, 0xf000d3d1, 0x4808f897, 0xf0206800,
    0x49060070, 0x46086008, 0xf0206800, 0x60080001, 0xf88af000, 0xe7de2000, 0x00030d40, 0x4001040c,
    0x4604b510, 0xf880f000, 0x68004808, 0x7080f420, 0x60084906, 0x60082001, 0x60082000, 0x49031e40,
    0x6008390c, 0xf870f000, 0xbd102000, 0x4001040c, 0x41f0e92d, 0x460e4605, 0xf04f4617, 0x46a80800,
    0xe0082400, 0xf860f000, 0x1b01f818, 0x42815d38, 0xe002d000, 0x42b41c64, 0xbf00d3f4, 0xe8bd1928,
    0xbf0081f0, 0xf1a01e01, 0xd1fb0001, 0x00004770, 0x4823b510, 0x48236802, 0xf3c06800, 0x48210481,
    0xf3c06800, 0xb90c2303, 0xe0081192, 0xd1012c01, 0xe0041292, 0xd1012c02, 0xe0001312, 0xb90b1392,
    0xe0002001, 0x2b0f2000, 0x2101d101, 0x2100e000, 0xb1104308, 0xf83af000, 0xf003e020, 0xb1180001,
    0xf000b9e2, 0xe019f833, 0x0002f003, 0xd1042802, 0xd1132a01, 0xf82af000, 0xf003e010, 0x28040004,
    0x2a02d104, 0xf000d10a, 0xe007f821, 0x0008f003, 0xd1032808, 0xd1012a03, 0xf818f000, 0x0000bd10,
    0x40049404, 0x40010680, 0x4807b500, 0xf3c06800, 0xb9084000, 0xf816f000, 0x68004803, 0x0001f000,
    0xf7ffb908, 0xbd00ffa5, 0x40010680, 0x49034802, 0x48036008, 0x47706008, 0xffff0123, 0x40049408,
    0xffff3210, 0x4823b510, 0xb2926842, 0x68004822, 0x4481f3c0, 0x68004820, 0x6303f3c0, 0x1192b90c,
    0x2c01e008, 0x1292d101, 0x2c02e004, 0x1312d101, 0x1392e000, 0x2001b90b, 0x2000e000, 0xd1012b0f,
    0xe0002101, 0x43082100, 0xf000b110, 0xe020f827, 0x0001f003, 0xb9e2b118, 0xf820f000, 0xf003e019,
    0x28020002, 0x2a01d104, 0xf000d113, 0xe010f817, 0x0004f003, 0xd1042804, 0xd10a2a02, 0xf80ef000,
    0xf003e007, 0x28080008, 0x2a03d103, 0xf000d101, 0xbd10f805, 0x40049000, 0x40010680, 0x49034802,
    0x48036088, 0x47706088, 0xffff0123, 0x40049000, 0xffff3210, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x200000f1,
    'pc_unInit': 0x20000221,
    'pc_program_page': 0x20000155,
    'pc_erase_sector': 0x200000e9,
    'pc_eraseAll': 0x200000e5,

    'static_base' : 0x20000000 + 0x00000020 + 0x000003f4,
    'begin_stack' : 0x20000700,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x3fc,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    'page_buffers' : [0x20001000, 0x200013fc],   # Enable double buffering
    'min_program_length' : 0x3fc,

    # Flash information
    'flash_start': 0x3000c00,
    'flash_size': 0x3fc,
    'sector_sizes': (
        (0x0, 0x3fc),
    )
}


class HC32F460xC(CoreSightTarget):

    VENDOR = "HDSC"

    MEMORY_MAP = MemoryMap(
        FlashRegion( start=0x00000000, length=0x40000, page_size=0x200, sector_size=0x2000,
                        is_boot_memory=True,
                        algo=FLASH_ALGO),
        FlashRegion( start=0x03000C00, length=0x3FC, sector_size=0x3FC,
                        is_boot_memory=False,
                        is_default=False,
                        algo=FLASH_ALGO_OTP),
        RamRegion(   start=0x1FFF8000, length=0x2F000),
        RamRegion(   start=0x200F0000, length=0x1000)
        )

    def __init__(self, session):
        super(HC32F460xC, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("HC32F460.svd")

    def post_connect_hook(self):
        self.write32(DBGMCU.STCTL, DBGMCU.STCTL_VALUE)
        self.write32(DBGMCU.TRACECTL, DBGMCU.TRACECTL_VALUE)


class HC32F460xE(CoreSightTarget):

    VENDOR = "HDSC"

    MEMORY_MAP = MemoryMap(
        FlashRegion( start=0x00000000, length=0x80000, page_size=0x200, sector_size=0x2000,
                        is_boot_memory=True,
                        algo=FLASH_ALGO),
        FlashRegion( start=0x03000C00, length=0x3FC, sector_size=0x3FC,
                        is_boot_memory=False,
                        is_default=False,
                        algo=FLASH_ALGO_OTP),
        RamRegion(   start=0x1FFF8000, length=0x2F000),
        RamRegion(   start=0x200F0000, length=0x1000)
        )

    def __init__(self, session):
        super(HC32F460xE, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("HC32F460.svd")

    def post_connect_hook(self):
        self.write32(DBGMCU.STCTL, DBGMCU.STCTL_VALUE)
        self.write32(DBGMCU.TRACECTL, DBGMCU.TRACECTL_VALUE)

