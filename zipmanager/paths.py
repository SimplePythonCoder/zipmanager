from collections import defaultdict

SPACE = '    '
BRANCH = '│   '
TEE = '├── '
LAST = '└── '


def build_tree_dict(paths):
    tree = lambda: defaultdict(tree)
    root = tree()
    for path in paths.keys():
        parts = path.strip('/').split('/')
        is_directory = paths[path].is_folder
        parts = [f'{p}/' if (i < len(parts)-1 or is_directory) else p for i, p in enumerate(parts)]
        current = root
        for i, part in enumerate(parts):
            if not part:
                continue
            current = current[part]
    return root


def tree_from_dict(tree_dict, prefix=''):
    contents = sorted(tree_dict.keys())
    pointers = [TEE] * (len(contents) - 1) + [LAST]
    for pointer, name in zip(pointers, contents):
        yield prefix + pointer + name
        extension = BRANCH if pointer == TEE else SPACE
        yield from tree_from_dict(tree_dict[name], prefix=prefix + extension)