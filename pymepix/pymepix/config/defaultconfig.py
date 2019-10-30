##############################################################################
##
# This file is part of Pymepix
#
# https://arxiv.org/abs/1905.07999
#
#
# Pymepix is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pymepix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pymepix.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from .timepixconfig import TimepixConfig

class DefaultConfig(TimepixConfig):

    def __init__(self):
        pass
    

    def dacCodes(self):
        codes = [('IBIAS_PREAMP_ON',       1,  128) # [0-255]
                ,('TPX3_IBIAS_PREAMP_OFF', 2,    8) # [0-15]
                ,('TPX3_VPREAMP_NCAS',     3,  128) # [0-255]
                ,('TPX3_IBIAS_IKRUM',      4,  128) # [0-255]
                ,('TPX3_VFBK',             5,  128) # [0-255]
                ,('TPX3_VTHRESH_FINE',     6,  256) # [0-512]
                ,('TPX3_VTHRESH_COARSE',   7,    8) # [0-15]
                ,('TPX3_IBIAS_DISCS1_ON',  8,  128) # [0-255]
                ,('TPX3_IBIAS_DISCS1_OFF', 9,    8) # [0-15]
                ,('TPX3_IBIAS_DISCS2_ON',  10, 128) # [0-255]
                ,('TPX3_IBIAS_DISCS2_OFF', 11,   8) # [0-15]
                ,('TPX3_IBIAS_PIXELDAC',   12, 128) # [0-255]
                ,('TPX3_IBIAS_TPBUFIN',    13, 128) # [0-255]
                ,('TPX3_IBIAS_TPBUFOUT',   14, 128) # [0-255]
                ,('TPX3_VTP_COARSE',       15, 128) # [0-255]
                ,('TPX3_VTP_FINE',         16, 256) # [0-512]
                ,('TPX3_IBIAS_CP_PLL',     17, 128) # [0-255]
                ,('PLL_Vcntrl',            18, 128)]# [0-255]
        return codes
