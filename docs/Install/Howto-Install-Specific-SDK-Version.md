# How to install specific Sentinel Python SDK version from GitHub

The supported schemes are git+https and git+ssh. Here are some of the supported forms:

- git+ssh://git@github.com:haas-labs/ext-sentinel-py-sdk.git

It is also possible to specify a “git ref” such as branch name, a commit hash or a tag name:

- git+ssh://git@github.com/haas-labs/ext-sentinel-py-sdk.git@main
- git+ssh://git@github.com/haas-labs/ext-sentinel-py-sdk.git@v0.3.5
- git+ssh://git@github.com/haas-labs/ext-sentinel-py-sdk.git@da39a3ee5e6b4b0d3255bfef95601890afd80709
- git+ssh://git@github.com/haas-labs/ext-sentinel-py-sdk.git@refs/pull/123/head

When passing a commit hash, specifying a full hash is preferable to a partial hash because a full hash allows pip to operate more efficiently (e.g. by making fewer network calls).

## References

- [Pip documentation, VCS Support](https://pip.pypa.io/en/stable/topics/vcs-support/)