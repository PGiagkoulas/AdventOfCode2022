from dataclasses import dataclass, field


COMMAND_SYMBOL = '$'
COMMAND_LS = 'ls'
COMMAND_CD = 'cd'


@dataclass
class DirectoryTree:
    root:       'DirectoryNode' = field(default=None)
    current:    'DirectoryNode' = field(default=None)
    nodes:      list['DirectoryNode'] = field(default_factory=list)

    def is_node_in_tree(self, node: 'DirectoryNode') -> bool:
        return node in self.nodes

    def add_node(self, new_node: 'DirectoryNode') -> None:
        self.nodes.append(new_node)

    def update_current(self, new_node: 'DirectoryNode') -> None:
        self.current = new_node

    def insert_update_single_node_to_current(self, new_node: 'DirectoryNode') -> None:
        self.add_node(new_node)
        self.current.add_single_child_node(new_node)
        self.update_current(new_node)

    def insert_single_node_to_current(self, new_node: 'DirectoryNode') -> None:
        self.add_node(new_node)
        self.current.add_single_child_node(new_node)

    def insert_multiple_nodes_to_current(self, new_nodes: list['DirectoryNode']) -> None:
        for new_node in new_nodes:
            self.insert_single_node_to_current(new_node)

    def go_to_node(self, node: 'DirectoryNode') -> None:
        if self.is_node_in_tree(node):
            self.update_current(self.nodes[self.nodes.index(node)])

    def calculate_directory_sizes(self) -> None:
        for node in reversed(self.nodes):
            if not node.is_file:
                node.size = sum(n.size for n in node.children)


@dataclass
class DirectoryNode:
    name:       str = field(compare=True)
    is_file:    bool = field(compare=True)
    size:       int = field(default=0, compare=False)
    parent:     'DirectoryNode' = field(default=None, compare=True)
    children:   list['DirectoryNode'] = field(default_factory=list, compare=False)

    def update_parent(self, parent_node: 'DirectoryNode'):
        self.parent = parent_node

    def add_single_child_node(self, new_node: 'DirectoryNode') -> None:
        new_node.update_parent(self)
        self.children.append(new_node)

    def add_child_nodes(self, new_nodes: list['DirectoryNode']) -> None:
        for new_node in new_nodes:
            new_node.update_parent(self)
        self.children.extend(new_nodes)


def is_command(line):
    return (COMMAND_SYMBOL in line) and (line[0] == COMMAND_SYMBOL)  # redundant? different?


if __name__ == '__main__':
    with open('d7-input.txt') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    directory_tree_object = None
    index = 0
    while index < len(lines):
        if is_command(lines[index]):
            if COMMAND_LS in lines[index]:
                index += 1
                child_nodes = []
                while index < len(lines) and not is_command(lines[index]):
                    node_name = lines[index].split(' ')[-1]
                    is_file = lines[index].split(' ')[0] != 'dir'
                    if is_file:
                        size = int(lines[index].split(' ')[0])
                    else:
                        size = 0
                    # create nodes and add them for all following dirs/files
                    child_nodes.append(DirectoryNode(name=node_name, is_file=is_file, size=size,
                                                     parent=directory_tree_object.current))
                    index += 1
                directory_tree_object.insert_multiple_nodes_to_current(child_nodes)
            elif COMMAND_CD in lines[index]:
                curr_dir = lines[index].split(' ')[-1]
                if curr_dir == '..':
                    directory_tree_object.go_to_node(directory_tree_object.current.parent)
                else:
                    if not directory_tree_object:
                        curr_node = DirectoryNode(name=curr_dir, is_file=False)
                        directory_tree_object = DirectoryTree(root=curr_node, current=curr_node, nodes=[curr_node])
                    else:
                        curr_node = DirectoryNode(name=curr_dir, is_file=False, parent=directory_tree_object.current)
                        if directory_tree_object.is_node_in_tree(curr_node):
                            directory_tree_object.go_to_node(curr_node)
                        else:
                            directory_tree_object.insert_update_single_node_to_current(curr_node)
                index += 1
        else:
            print('[!] ERROR @&%@!')
    directory_tree_object.calculate_directory_sizes()
    a = [n for n in directory_tree_object.nodes if not n.is_file and n.size <= 100000]
    print()
