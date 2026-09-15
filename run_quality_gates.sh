#!/bin/bash
#
# @brief   mecharmory
# @version 1.0.0
# @date    Mon Sep 14 15:20:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 gates/gates/interfaces_checker.py mecharmory
python3 gates/gates/isp_checker.py mecharmory
python3 gates/gates/limits_checker.py mecharmory
python3 gates/gates/srp_checker.py mecharmory

echo "Done"
