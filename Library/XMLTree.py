import enum


class Status(enum.Enum):
    initial_status = 0
    prettifying = 1
    minifying = 2
    correction = 3


class Node:
    def __init__(self):
        self.children = []
        self.is_valid = False
        self.xml_version = False
        self.tag_name = str()
        self.self_close = False
        self.comment = False
        self.hasValue = False
        self.value = str()
        self.attribute_name = str()
        self.attribute_value = str()
        self.has_attribute = False
        self.is_tag = True
        self.is_open_tag = False
        self.is_close_tag = False
        self.num_child = 0
        self.num_attributes = 0


class Tree:
    def __init__(self):
        self.root = None  # point to the root of the xml file
        self.created_nodes = None  # contains the remaining tags after parsing
        self.file_state_xml = None  # should be updated while the user keep editing the file!
        self.json_file = None  # TODO store the the json file that was created after conversion! @Sara
        self.passed_file = None

    def __check_tag(self, xmlTagsSt: list[Node], end_tag_node: Node):
        temp_stack = []
        if xmlTagsSt:
            if xmlTagsSt[-1].tag_name == end_tag_node.tag_name:
                xmlTagsSt[-1].is_valid = True
                end_tag_node.is_valid = True
                xmlTagsSt.append(end_tag_node)
            else:
                while xmlTagsSt and xmlTagsSt[-1].tag_name != end_tag_node.tag_name:
                    current_top_tag = xmlTagsSt.pop()
                    if not current_top_tag.is_valid:  # could be a redundant  check  REVIEW!!
                        current_top_tag.is_valid = False
                    temp_stack.append(current_top_tag)

                if not xmlTagsSt:  # the main stack became empty then the end tag is not valid for any open tag
                    while temp_stack:  # return all nodes to the main stack
                        xmlTagsSt.append(temp_stack.pop())
                    end_tag_node.is_valid = False
                    xmlTagsSt.append(end_tag_node)
                else:
                    found_open_tag = xmlTagsSt[-1]
                    found_open_tag.is_valid = True
                    while temp_stack:
                        current_node_in_temp = temp_stack.pop()
                        found_open_tag.children.append(current_node_in_temp)
                        found_open_tag.num_child += 1
                    end_tag_node.is_valid = True
                    xmlTagsSt.append(end_tag_node)
        else:
            end_tag_node.is_valid = False
            xmlTagsSt.append(end_tag_node)

    def __data_node(self, stackTags: list[Node], dataNode: Node):
        if stackTags:
            top = stackTags[-1]
            if top.is_open_tag and self.root is not top:
                top.hasValue = True
                dataNode.is_valid = True
                top.children.append(dataNode)
            else:
                dataNode.is_valid = False
                stackTags.append(dataNode)

        else:
            dataNode.is_valid = False
            stackTags.append(dataNode)

    def __get_atrribute_value(self, data: str):
        list_ = data.split('=')
        return list_

    def parser(self, file_string: str):
        self.passed_file = file_string
        length_file_string = len(file_string)
        index = 0
        xmlTagsSt = []
        trash = ""
        while index < length_file_string and file_string[index] != '<':
            trash += file_string[index]
            index += 1
        trash = trash.strip()

        if trash != "":
            data_node = Node()
            data_node.is_valid = False
            data_node.is_tag = False
            data_node.value = trash
            xmlTagsSt.append(data_node)

        # assuming the start of the file with <
        while index < length_file_string:
            if file_string[index] == '<':
                # then get the data between < and  >
                index += 1
                data = str()
                while index < length_file_string and file_string[index] != '>':
                    data += file_string[index]
                    index += 1

                index += 1
                if data:
                    if data[0] == '!':  # then this a comment!
                        comment_node = Node()
                        comment_node.comment = True
                        comment_node.is_valid = True
                        comment_node.is_tag = True
                        comment_node.hasValue = True
                        comment_node.value = data[1:]
                        # push the comment on the stack till find its parent
                        xmlTagsSt.append(comment_node)

                    elif data[0] == '?':  # is xml_version tag
                        xml_version = Node()
                        xml_version.xml_version = True
                        xml_version.is_tag = True
                        xml_version.is_valid = True
                        xml_version.value = data[1:]
                        # if not self.root:
                        #     self.root = xml_version
                        xmlTagsSt.append(xml_version)

                    elif data[0] == '/':  # end tag
                        data = data[1:]
                        end_tag_node = Node()
                        end_tag_node.tag_name = data
                        end_tag_node.is_tag = True
                        end_tag_node.is_close_tag = True
                        self.__check_tag(xmlTagsSt, end_tag_node)

                    elif data[-1] == '/':  # self close tag
                        # Note that we can't set the self_closed tag to be the root
                        # if the root was not assigned to any value yet
                        # and the self closed tag is in the top of the file
                        # then its may be non-valid if and only if the file has another tags
                        # otherwise set the self closed tag as the root
                        data = data[0:-1]
                        self_closed_node = Node()
                        self_closed_node.self_close = True
                        self_closed_node.is_valid = True
                        if not self.root:
                            # we should make sure there exist another tags in the file
                            index_temp = index
                            flag = False
                            while index_temp < length_file_string:
                                if file_string[index_temp] == '<':
                                    flag = True
                                    break
                                index_temp += 1

                            if flag:
                                self_closed_node.is_valid = False

                        if '=' in data:  # then will have an attribute
                            tag_name, attr = data.split()
                            attr_name, attr_value = self.__get_atrribute_value(attr)
                            self_closed_node.has_attribute = True
                            self_closed_node.tag_name = tag_name.strip()
                            self_closed_node.attribute_name = attr_name.strip()
                            self_closed_node.attribute_value = attr_value.strip()
                        else:
                            self_closed_node.tag_name = data.strip()
                        xmlTagsSt.append(self_closed_node)

                    else:  # this is an open tag
                        open_tag = Node()
                        open_tag.is_tag = True
                        open_tag.is_open_tag = True
                        if '=' in data:
                            tag_name, attr = data.split()
                            attr_name, attr_value = self.__get_atrribute_value(attr)
                            open_tag.tag_name = tag_name.strip()
                            open_tag.has_attribute = True
                            open_tag.attribute_name = attr_name
                            open_tag.attribute_value = attr_value
                        else:
                            data = data.strip()
                            open_tag.tag_name = data

                        if not self.root:
                            self.root = open_tag
                        xmlTagsSt.append(open_tag)
                        data = ""

            # iterate until find <
            data = ""
            while index < length_file_string and file_string[index] != '<':
                data += file_string[index]
                index += 1
            data = data.strip()
            if data:
                value_node = Node()
                value_node.is_tag = False
                data = " ".join(list(data.split()))
                value_node.value = data
                self.__data_node(xmlTagsSt, value_node)
        self.created_nodes = xmlTagsSt
        self.update_file_state(Status.prettifying)

    def __printTree(self, root: Node, level=0):
        sep = level * "\t"
        if not root:
            return
        if root.is_open_tag:
            print(f'{sep}<{root.tag_name}', end='')
            if root.has_attribute:
                print(f' {root.attribute_name}={root.attribute_value}>')
            else:
                print('>')
            if root.hasValue and root.children:
                another_sep = sep + '\t'
                print(f'{another_sep}{root.children[0].value}')
        elif root.is_close_tag:
            print(f'{sep}</{root.tag_name}>')
        elif root.self_close:
            print(f'{sep}<{root.tag_name}/>')
        elif root.comment:
            print(f'{sep}<!{root.value}>')
        elif root.xml_version:
            print(f'{sep}<?{root.value}>')
        elif not root.is_valid:
            print(f'{sep}{root.value}')
        for child in root.children:
            self.__printTree(child, level + 1)

    def __printJSON(self, root: Node, level=0, temp: list = [], temp1: list = []):
        sep = level * "\t"
        flag_list_close = False
        flag_set_close = False
        length = len(root.children)
        if not root:
            return
        if (length == 0):
            if (len(temp) == 1 and root.tag_name == temp[0]):
                temp.pop()
                print(sep + " ]")
                print("}")
            else:
                for tags in temp:
                    if (root.tag_name == tags):
                        temp.pop()
                        flag_list_close = True
                if (flag_list_close):
                    print(sep + " ]")
                    flag_list_close = False
                for tags in temp1:
                    if (root.tag_name == tags):
                        temp1.pop()
                        flag_set_close = True
                if (flag_set_close):
                    print(sep + " }")
                    flag_set_close = False
        elif (length == 1):
            if (root.children[0].value != None):
                print(sep + "\"" + root.tag_name + "\":\"", end=" ")
                if root.has_attribute:
                    print("{\"" + root.attribute_name + "\":" + root.attribute_value + "}")
                else:
                    print(root.children[0].value + "\",")
        elif (length > 2):
            if (level == 0):
                print("{\"" + root.tag_name + "\"[")
                temp.append(root.tag_name)
            elif (root.children[0].tag_name != root.children[2].tag_name):
                print(sep + "\"" + root.tag_name + "\":", end=" ")
                if root.has_attribute:
                    print("{\"" + root.attribute_name + "\":" + root.attribute_value + "}{")
                else:
                    print(root.children[0].value, end=" ")
                    print("{")
                temp1.append(root.tag_name)
            else:
                if root.is_open_tag:
                    print(sep + "\"" + root.tag_name + "\":", end=" ")
                    if root.has_attribute:
                        print("{\"" + root.attribute_name + "\":" + root.attribute_value + "}{")
                    else:
                        print(root.children[0].value, end='')
                        print("[")
                        temp.append(root.tag_name)

        elif root.self_close:
            print(sep + "\"" + root.tag_name + "\"")
        elif root.comment:
            pass
        elif root.xml_version:
            pass
        for child in root.children:
            self.__printJSON(child, level + 1, temp, temp1)

    # need to edit
    def __correctionTree(self, root: Node, parent: Node):
        if not root.is_valid:
            if root.is_tag:
                if root.is_open_tag and root.hasValue:
                    root.is_valid = True
                    end_tag_node = Node()
                    end_tag_node.tag_name = root.tag_name
                    end_tag_node.is_tag = True
                    end_tag_node.is_close_tag = True
                    end_tag_node.is_valid = True
                    index = parent.children.index(root)
                    parent.children.insert(index + 1, end_tag_node)

                elif root.is_open_tag and not root.hasValue:
                    root.is_valid = True
                    end_tag_node = Node()
                    end_tag_node.tag_name = root.tag_name
                    end_tag_node.is_tag = True
                    end_tag_node.is_close_tag = True
                    end_tag_node.is_valid = True
                    queue = []
                    index = parent.children.index(root)
                    i = index + 1

                    while i < len(parent.children):
                        current = parent.children[i]
                        queue.append(current)
                        i = i + 1

                    parent.children = parent.children[0:index + 1]

                    while (queue):
                        root.children.append(queue.pop(0))
                    parent.children.append(end_tag_node)

                # should be correct in case of close tags!

                elif root.is_close_tag:
                    root.is_valid = True
                    open_tag_node = Node()
                    open_tag_node.tag_name = root.tag_name
                    open_tag_node.is_tag = True
                    open_tag_node.is_open_tag = True
                    open_tag_node.is_valid = True
                    index_end = parent.children.index(root)
                    parent.children.insert(index_end, open_tag_node)
                    # if (not parent.children[index_end - 1].is_tag):
                    #     open_tag_node.hasValue = True
                    #     parent.children[index_end - 1].is_valid = True
                    #     open_tag_node.children.append(parent.children.pop(index_end - 1))
                    #     parent.children.insert(index_end - 1, open_tag_node)
                    # # to_do handle case open tag missing without data
                    # else:
                    #     open_tag_node.hasValue = False
                    #     queue = []
                    #     i = 0
                    #     if (open_tag_node.tag_name[-1] == 's'):
                    #         while i < index_end:
                    #             if (parent.children[i].is_tag):
                    #                 if open_tag_node.tag_name[0:len(open_tag_node.value) - 1] in parent.children[
                    #                     i].tag_name:
                    #                     current = parent.children.pop(i)
                    #                     i -= 1
                    #                     index_end -= 1
                    #                     queue.append(current)
                    #             i = i + 1
                    #     else:
                    #         while i < index_end:
                    #             current = parent.children.pop(0)
                    #             queue.append(current)
                    #             i = i + 1
                    #     while (queue):
                    #         open_tag_node.children.append(queue.pop(0))
                    #     index_end = parent.children.index(root)
                    #     parent.children.insert(index_end, open_tag_node)
            else:
                # this not a tag so will be data
                index_data = parent.children.index(root)
                length_children = len(parent.children)
                if index_data + 1 < length_children and parent.children[index_data + 1].is_close_tag:
                    root.is_valid = True
                    open_created_tag = Node()
                    open_created_tag.is_open_tag = True
                    open_created_tag.is_valid = True
                    open_created_tag.tag_name = parent.children[index_data + 1].tag_name
                    parent.children[index_data + 1].is_valid = True  # set close tag to be valid
                    open_created_tag.children.append(parent.children.pop(index_data))
                    parent.children.insert(index_data, open_created_tag)  # insert the open tag to the parent!
                    open_created_tag.hasValue = True
                else:
                    # remove undefined data!
                    return root

        for child in root.children:
            self.__correctionTree(child, root)

    def __delete_data(self, root: Node, parent: Node):
        if not root.is_tag:
            if not root.is_valid:
                index = parent.children.index(root)
                parent.children.pop(index)
        for child in root.children:
            self.__delete_data(child, root)

    def correter_XML(self):
        nodes_to_remove = []
        for index, node in enumerate(self.created_nodes):
            if node is self.root:
                remove_from_root = []
                if not node.is_valid:
                    # correct the root node before going to its children
                    end_tag_root = Node()
                    end_tag_root.tag_name = self.root.tag_name
                    end_tag_root.is_close_tag = True
                    self.__check_tag(self.created_nodes, end_tag_root)
                for child in node.children:
                    returned_node = self.__correctionTree(child, node)
                    if returned_node:
                        remove_from_root.append(returned_node)

                for n in remove_from_root:
                    self.root.children.remove(n)


            # in case non-valid self closed tag
            # the tag should be removed due to the file shouldn't contain multiple roots!
            elif node.self_close and not node.is_valid:
                nodes_to_remove.append(node)
            elif not node.is_tag and not node.is_valid:
                nodes_to_remove.append(node)

        # delete non-valid tags
        for node in nodes_to_remove:
            self.created_nodes.remove(node)

        self.update_file_state(Status.correction)  # update the file

    def visualizeXML(self):
        for nodes in self.created_nodes:
            self.__printTree(nodes)

    def visualizeJSON(self):
        for nodes in self.created_nodes:
            self.__printJSON(nodes)

    def __edit_prettifying(self, root: Node, level=0):
        sep = level * "\t"
        new_line = ""
        if not root:
            return
        if root.is_open_tag:
            new_line = f'{sep}<{root.tag_name}'
            if root.has_attribute:
                new_line += f' {root.attribute_name}={root.attribute_value}>\n'
            else:
                new_line += '>\n'
            if root.hasValue and root.children:
                another_sep = sep + '\t'
                new_line += f'{another_sep}{root.children[0].value}' + '\n'
        elif root.is_close_tag:
            new_line = f'{sep}</{root.tag_name}>\n'
        elif root.self_close:
            new_line = f'{sep}<{root.tag_name}/>\n'
        elif root.comment:
            new_line = f'{sep}<!{root.value}>\n'
        elif root.xml_version:
            new_line = f'{sep}<?{root.value}>\n'
        elif not root.is_valid:
            new_line = f'{sep}{root.value}\n'
        self.file_state_xml += new_line
        for child in root.children:
            self.__edit_prettifying(child, level + 1)

    def __prettifying(self):
        self.file_state_xml = ""
        for node in self.created_nodes:
            self.__edit_prettifying(node)

    def __edit_minifying(self, root: Node):
        new_line = ""
        if not root:
            return
        if root.is_open_tag:
            new_line += f'<{root.tag_name}'
            if root.has_attribute:
                new_line += f' {root.attribute_name}={root.attribute_value}>'
            else:
                new_line += '>'
            if root.hasValue and root.children:
                new_line += f'{root.children[0].value}'
        elif root.is_close_tag:
            new_line = f'</{root.tag_name}>'
        elif root.self_close:
            new_line = f'<{root.tag_name}/>'
        elif root.comment:
            new_line = f'<!{root.value}>'
        elif root.xml_version:
            new_line = f'<?{root.value}>'
        if self.file_state_xml:
            if len(self.file_state_xml) % 30 == 0:
                self.file_state_xml += '\n'
        self.file_state_xml += new_line
        for child in root.children:
            self.__edit_minifying(child)

    def __minifying(self):
        self.file_state_xml = ""
        for node in self.created_nodes:
            self.__edit_minifying(node)

    # update the file after every change occurred!
    # changes such as -> prettifying , minifying , correction, initial_state
    def update_file_state(self, status: Status):
        if status == Status.prettifying:
            self.__prettifying()
        elif status == Status.minifying:
            self.__minifying()
        elif status == Status.correction:
            # after correction, we should show the formatted version!
            self.__prettifying()
        elif status == Status.initial_status:
            self.file_state_xml = self.passed_file

    def __check_node(self, node, non_valid_lines: list[int], line=1):
        if not node.is_valid:
            non_valid_lines.append(line)
            line += 1
        if node.children:
            for child in node.children:
                line = self.__check_node(child, non_valid_lines, line + 1)
        elif node.is_valid:
            line += 1

        return line

    # get list of unValid lines!
    def check_validation(self):
        line = 1
        non_valid_lines = []
        for node in self.created_nodes:
            line = self.__check_node(node,  non_valid_lines,line)
        return non_valid_lines


if __name__ == '__main__':
    test = """11
    <users>
        Ahmed Ali</name>
        11
        11
        11<id>
        <posts><post>
                """
    xmlTree = Tree()
    xmlTree.parser(test)
    print(xmlTree.file_state_xml)
    print(xmlTree.check_validation())
    xmlTree.correter_XML()
    # xmlTree.visualizeJSON()
    xmlTree.visualizeXML()
    # xmlTree.update_file_state(Status.prettifying)
