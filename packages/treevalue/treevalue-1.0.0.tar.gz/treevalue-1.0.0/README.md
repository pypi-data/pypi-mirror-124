# treevalue

[![PyPI](https://img.shields.io/pypi/v/treevalue)](https://pypi.org/project/treevalue/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/treevalue)
![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/ff0bc026423888cd7c4f287eaed4b3f5/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/ff0bc026423888cd7c4f287eaed4b3f5/raw/comments.json)


[![Docs Deploy](https://github.com/opendilab/treevalue/workflows/Docs%20Deploy/badge.svg)](https://github.com/opendilab/treevalue/actions?query=workflow%3A%22Docs+Deploy%22)
[![Code Test](https://github.com/opendilab/treevalue/workflows/Code%20Test/badge.svg)](https://github.com/opendilab/treevalue/actions?query=workflow%3A%22Code+Test%22)
[![Badge Creation](https://github.com/opendilab/treevalue/workflows/Badge%20Creation/badge.svg)](https://github.com/opendilab/treevalue/actions?query=workflow%3A%22Badge+Creation%22)
[![Package Release](https://github.com/opendilab/treevalue/workflows/Package%20Release/badge.svg)](https://github.com/opendilab/treevalue/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/opendilab/treevalue/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/opendilab/treevalue)

[![GitHub stars](https://img.shields.io/github/stars/opendilab/treevalue)](https://github.com/opendilab/treevalue/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/opendilab/treevalue)](https://github.com/opendilab/treevalue/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/opendilab/treevalue)
[![GitHub issues](https://img.shields.io/github/issues/opendilab/treevalue)](https://github.com/opendilab/treevalue/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/opendilab/treevalue)](https://github.com/opendilab/treevalue/pulls)
[![Contributors](https://img.shields.io/github/contributors/opendilab/treevalue)](https://github.com/opendilab/treevalue/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/opendilab/treevalue)](https://github.com/opendilab/treevalue/blob/master/LICENSE)

`TreeValue` is a generalized tree-based data structure mainly developed by [OpenDILab Contributors](https://github.com/opendilab).

Almost all the operation can be supported in form of trees in a convenient way to simplify the structure processing when the calculation is tree-based.

## Installation

You can simply install it with `pip` command line from the official PyPI site.

```shell
pip install treevalue
```

For more information about installation, you can refer to [Installation](https://opendilab.github.io/treevalue/main/tutorials/installation/index.html#).

## Documentation

The detailed documentation are hosted on [https://opendilab.github.io/treevalue](https://opendilab.github.io/treevalue/).

Only english version is provided now, the chinese documentation is still under development.

## Quick Start

You can easily create a tree value object based on `FastTreeValue`.

```python
from treevalue import FastTreeValue

if __name__ == '__main__':
    t = FastTreeValue({
        'a': 1,
        'b': 2.3,
        'x': {
            'c': 'str',
            'd': [1, 2, None],
            'e': b'bytes',
        }
    })
    print(t)

```

The result should be

```text
<FastTreeValue 0x7f6c7df00160 keys: ['a', 'b', 'x']>
├── 'a' --> 1
├── 'b' --> 2.3
└── 'x' --> <FastTreeValue 0x7f6c81150860 keys: ['c', 'd', 'e']>
    ├── 'c' --> 'str'
    ├── 'd' --> [1, 2, None]
    └── 'e' --> b'bytes'
```

And `t` is structure should be like this

![](https://opendilab.github.io/treevalue/main/_images/simple_demo.dat.svg)

For more quick start explanation and further usage, take a look at:

* [Quick Start](https://opendilab.github.io/treevalue/main/tutorials/quick_start/index.html)
* [Basic Usage](https://opendilab.github.io/treevalue/main/tutorials/basic_usage/index.html)
* [Advanced Usage](https://opendilab.github.io/treevalue/main/tutorials/advanced_usage/index.html)

## Contribution

We appreciate all contributions to improve treevalue, both logic and system designs. Please refer to CONTRIBUTING.md for more guides.

And users can join our [slack communication channel](https://join.slack.com/t/opendilab/shared_invite/zt-v9tmv4fp-nUBAQEH1_Kuyu_q4plBssQ), or contact the core developer [HansBug](https://github.com/HansBug) for more detailed discussion.

## License

`treevalue` released under the Apache 2.0 license.
