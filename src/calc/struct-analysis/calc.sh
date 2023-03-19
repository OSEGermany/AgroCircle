#!/bin/bash

# SPDX-FileCopyrightText: 2014 Thomas Kalka <thomas.kalka@co-buero.de>
# SPDX-FileCopyrightText: 2014 toka <toka@brutus.co-buero.de>
# SPDX-FileCopyrightText: 2020 hoijui <hoijui.quaero@gmail.com>
# SPDX-FileCopyrightText: 2023 Robin Vobruba <hoijui.quaero@gmail.com>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

set -e

python traverse.py > traverse.in
rm -f traverse.out
frame3dd traverse.in traverse.out
