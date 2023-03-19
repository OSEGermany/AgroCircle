/*
 * SPDX-FileCopyrightText: 2014 Stefan Raabe <raabe.stefan@googlemail.com>
 * SPDX-FileCopyrightText: 2014 Thomas Kalka <thomas.kalka@co-buero.de>
 * SPDX-FileCopyrightText: 2017 Jan R.I. B.F. v.W. v.Z. (faerietree) <radagast@ciry.at>
 * SPDX-FileCopyrightText: 2020 hoijui <hoijui.quaero@gmail.com>
 * SPDX-FileCopyrightText: 2023 Robin Vobruba <hoijui.quaero@gmail.com>
 *
 * SPDX-License-Identifier: CC-BY-SA-4.0
 */

// all units in cm
h = 80;    // heigth above ground

use <utils.scad>;
use <traverse.scad>;

$fn = 60;
//rotate([0,90,0]) rotate([0,0,180+120])

tube(h,10,0.5);
translate([0,0,h]) traverse();
