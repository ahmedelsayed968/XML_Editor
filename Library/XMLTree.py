from inspect import stack


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


class Tree:
    def __init__(self):
        self.root = None

    def __check_tag(self, xmlTagsSt: [Node], end_tag_node: Node):
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
                    end_tag_node.is_valid = True
                    xmlTagsSt.append(end_tag_node)
        else:
            end_tag_node.is_valid  = False
            xmlTagsSt.append(end_tag_node)

    def __data_node(self, stackTags: list[Node], dataNode: Node):
        if stackTags:
            top = stackTags[-1]
            if top.is_open_tag:
                top.hasValue = True
                dataNode.is_valid = True
            else:
                dataNode.is_valid = False
        else:
            dataNode.is_valid = False
        stackTags.append(dataNode)

    def __get_atrribute_value(self, data: str):
        list_ = data.split('=')
        list_[-1] = list_[-1][1:-1]
        return list_

    def parser(self, file_string: str):
        length_file_string = len(file_string)
        index = 0
        xmlTagsSt = []
        while index < length_file_string:
            if file_string[index] == '<':
                # then get the data between < and  >
                index +=1
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
                        # if there is no root yet!
                        if not self.root:
                            self.root = comment_node
                        # push the comment on the stack till find its parent
                        xmlTagsSt.append(comment_node)

                    elif data[0] == '?':  # is xml_version tag
                        xml_version = Node()
                        xml_version.xml_version = True
                        xml_version.is_tag = True
                        xml_version.is_valid = True
                        xml_version.value = data[1:]
                        if not self.root:
                            self.root = xml_version
                        xmlTagsSt.append(xml_version)

                    elif data[0] == '/':  # end tag
                        data = data[1:]
                        end_tag_node = Node()
                        end_tag_node.tag_name = data
                        end_tag_node.is_tag = True
                        end_tag_node.is_close_tag = True
                        self.__check_tag(xmlTagsSt, end_tag_node)

                    elif data[-1] == '/':  # self close tag
                        data = data[0:-1]
                        self_closed_node = Node()
                        self_closed_node.self_close = True
                        self_closed_node.is_valid = True
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
                        # Note that we can't set the self_closed tag to be the root

                    else:   # this is an open tag
                        open_tag = Node()
                        open_tag.is_tag = True
                        open_tag.is_open_tag = True
                        if '=' in data:
                            tag_name,attr = data.split()
                            attr_name,attr_value = self.__get_atrribute_value(attr)
                            open_tag.tag_name = tag_name
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
                value_node.value = data
                # value_node.hasValue = data
                self.__data_node(xmlTagsSt,value_node)





if __name__ == '__main__':
    file_string = """<users>
    <user/>
    <user atrr="ahmed">
<!--hi        -->
        <id>1</id>
        <name>ahmed</name>
    </user>
    <easy/>
</users>"""
    xmlTree = Tree()
    xmlTree.parser(file_string)
    if xmlTree.root:
        print(xmlTree.root.tag_name)
        children = xmlTree.root.children
        print(len(children))
        print(children[0].tag_name)
        print(children[1].tag_name)
        # print(children[1].attribute_value)
        print(children[2].tag_name)
        print(children[3].tag_name)

    # xmlTree.root
