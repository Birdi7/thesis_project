def omit(d, blacklist=None):
    blacklist = blacklist or []
    return {k: v for k, v in d.items() if k not in blacklist}
