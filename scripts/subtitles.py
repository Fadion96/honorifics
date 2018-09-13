#!/usr/bin/env python3
import sys
sys.path.insert(0, '../')

from honorifics.textswapper import TextSwapperInMark


swapper = TextSwapperInMark()

for line in sys.stdin:
    sys.stdout.write(swapper.swap(line))
