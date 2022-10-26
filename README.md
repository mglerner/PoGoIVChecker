# PoGoIVChecker

Check IVs to see what to keep for PVP

This is based HUGELY on two things I did not write:

* All of Ryan Swag's PVP IV [Deep Dives](https://gamepress.gg/pokemongo/pvp-iv-deep-dive-full-series)
* Lots of stats and move data from [PvPoke](https://pvpoke.com/)

This grew out of my Discord quiz bot (https://github.com/mglerner/PoGoQuizBot)

I'll try to document things more later, but you'll need to be able to install python and jupyter notebooks to make the most of this.

1. Clone this repository.

## Notes for me

You add a subtree wtih

`git subtree add --prefix external/pvpoke git@github.com:pvpoke/pvpoke.git master --squash`

And you update it with

`git subtree pull --prefix external/pvpoke git@github.com:pvpoke/pvpoke.git master --squash`

(read [this](https://www.atlassian.com/git/tutorials/git-subtree) for more info on subtrees)

## Other data

[PvPoke](https://pvpoke.com/) is an amazing resource, and it's all available as an open-source [github repo](https://github.com/pvpoke/pvpoke).

This code uses PvPoke's move data, stats, etc. Since PvPoke uses the MIT License, I've included a copy of that license below.

### MIT License, as it applies to the pvpoke code included in this repository.

MIT License

Copyright (c) 2019 pvpoke

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
