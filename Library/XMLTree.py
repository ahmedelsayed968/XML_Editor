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
    Space = '\t\t'

    def __init__(self):
        self.root = None            # point to the root of the xml file
        self.created_nodes = None   # contains the remaining tags after parsing

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
                    end_tag_node.is_valid = True
                    xmlTagsSt.append(end_tag_node)
        else:
            end_tag_node.is_valid = False
            xmlTagsSt.append(end_tag_node)

    def __data_node(self, stackTags: list[Node], dataNode: Node):
        if stackTags:
            top = stackTags[-1]
            if top.is_open_tag:
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
        length_file_string = len(file_string)
        index = 0
        xmlTagsSt = []
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
                value_node.value = data
                # value_node.hasValue = data
                self.__data_node(xmlTagsSt, value_node)
        self.created_nodes = xmlTagsSt

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
        for child in root.children:
            self.__printTree(child, level + 1)
        # if root == self.root:
        #     print(f'{sep}</{root.tag_name}>')
    def __printJSON(self, root: Node, level=0, temp:list =[],temp1:list =[]):
        sep = level * "\t"
        flag_list_close=False
        flag_set_close=False
        length=len(root.children)
        if not root:
            return
        if(length==0):
            if(len(temp)==1 and root.tag_name==temp[0] ):
                temp.pop()
                print(sep+" ]")
                print("}") 
            else:
                for tags in temp:
                    if(root.tag_name==tags):
                        temp.pop()
                        flag_list_close=True     
                if(flag_list_close):
                    print(sep+" ]")
                    flag_list_close=False 
                for tags in temp1:
                    if(root.tag_name==tags):
                        temp1.pop()
                        flag_set_close=True
                if(flag_set_close):
                    print(sep+" }")
                    flag_set_close=False     
        elif(length==1 ):
            if(root.children[0].value!=None):
                    print(sep+"\""+root.tag_name +"\":\"",end=" ")
                    if root.has_attribute:
                        print("{\""+root.attribute_name+"\":"+root.attribute_value+"}")
                    else:
                        print(root.children[0].value+"\",")
        elif(length>2):
            if(level==0):
                print("{\""+root.tag_name+"\"[")
                temp.append(root.tag_name)
            elif(root.children[0].tag_name!=root.children[2].tag_name):
                    print(sep+"\""+root.tag_name +"\":",end=" ")
                    if root.has_attribute:
                        print("{\""+root.attribute_name+"\":"+root.attribute_value+"}{")
                    else:
                        print(root.children[0].value,end=" ")
                        print("{")
                    temp1.append(root.tag_name)
            else:   
                if root.is_open_tag:
                    print(sep+"\""+root.tag_name +"\":",end=" ")
                    if root.has_attribute:
                        print("{\""+root.attribute_name+"\":"+root.attribute_value+"}{")
                    else:
                        print(root.children[0].value,end='')
                        print("[")
                        temp.append(root.tag_name)

        elif root.self_close:
                print(sep+"\""+root.tag_name+"\"")
        elif root.comment:
                pass
        elif root.xml_version:
                pass
        for child in root.children:
            self.__printJSON(child, level + 1,temp,temp1)
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

                # TODO Uncomment this
                # should be correct in case of close tags!
                # elif root.is_close_tag:
                #     root.is_valid = True
                #     open_tag_node = Node()
                #     open_tag_node.tag_name = root.tag_name
                #     open_tag_node.is_tag = True
                #     open_tag_node.is_open_tag = True
                #     open_tag_node.is_valid = True
                #     index_end = perent.children.index(root)
                #     perent.children.insert(index_end, open_tag_node)

                # TODO add condition for the data tag!

        for child in root.children:
            self.__correctionTree(child, root)

    # def def_validation(self,node):

    def correter_XML(self):
        for node in self.created_nodes:
            if node is self.root:
                if not node.is_valid:
                    # correct the root node before going to its children
                    end_tag_root = Node()
                    end_tag_root.tag_name = self.root.tag_name
                    end_tag_root.is_close_tag = True
                    self.__check_tag(self.created_nodes, end_tag_root)

                for child in node.children:
                    self.__correctionTree(child, node)

    def visualizeXML(self):
        for nodes in self.created_nodes:
            self.__printTree(nodes)
    def visualizeJSON(self):
        for nodes in self.created_nodes:
            self.__printJSON(nodes)


if __name__ == '__main__':
    file_string = """
<?xml version="1.0"?>
<catalog>
   <book id="bk101">
      <author>Gambardella, Matthew</author>
      <title>XML Developer's Guide</title>
      <genre>Computer</genre>
      <price>44.95</price>
      <publish_date>2000-10-01</publish_date>
      <description>An in-depth look at creating applications 
      with XML.</description>
   </book>
   <book id="bk102">
      <author>Ralls, Kim</author>
      <title>Midnight Rain</title>
      <genre>Fantasy</genre>
      <price>5.95</price>
      <publish_date>2000-12-16</publish_date>
      <description>A former architect battles corporate zombies, 
      an evil sorceress, and her own childhood to become queen 
      of the world.</description>
   </book>
   <book id="bk103">
      <author>Corets, Eva</author>
      <title>Maeve Ascendant</title>
      <genre>Fantasy</genre>
      <price>5.95</price>
      <publish_date>2000-11-17</publish_date>
      <description>After the collapse of a nanotechnology 
      society in England, the young survivors lay the 
      foundation for a new society.</description>
   </book>
   <book id="bk104">
      <author>Corets, Eva</author>
      <title>Oberon's Legacy</title>
      <genre>Fantasy</genre>
      <price>5.95</price>
      <publish_date>2001-03-10</publish_date>
      <description>In post-apocalypse England, the mysterious 
      agent known only as Oberon helps to create a new life 
      for the inhabitants of London. Sequel to Maeve 
      Ascendant.</description>
   </book>
   <book id="bk105">
      <author>Corets, Eva</author>
      <title>The Sundered Grail</title>
      <genre>Fantasy</genre>
      <price>5.95</price>
      <publish_date>2001-09-10</publish_date>
      <description>The two daughters of Maeve, half-sisters, 
      battle one another for control of England. Sequel to 
      Oberon's Legacy.</description>
   </book>
   <book id="bk106">
      <author>Randall, Cynthia</author>
      <title>Lover Birds</title>
      <genre>Romance</genre>
      <price>4.95</price>
      <publish_date>2000-09-02</publish_date>
      <description>When Carla meets Paul at an ornithology 
      conference, tempers fly as feathers get ruffled.</description>
   </book>
   <book id="bk107">
      <author>Thurman, Paula</author>
      <title>Splish Splash</title>
      <genre>Romance</genre>
      <price>4.95</price>
      <publish_date>2000-11-02</publish_date>
      <description>A deep sea diver finds true love twenty 
      thousand leagues beneath the sea.</description>
   </book>
   <book id="bk108">
      <author>Knorr, Stefan</author>
      <title>Creepy Crawlies</title>
      <genre>Horror</genre>
      <price>4.95</price>
      <publish_date>2000-12-06</publish_date>
      <description>An anthology of horror stories about roaches,
      centipedes, scorpions  and other insects.</description>
   </book>
   <book id="bk109">
      <author>Kress, Peter</author>
      <title>Paradox Lost</title>
      <genre>Science Fiction</genre>
      <price>6.95</price>
      <publish_date>2000-11-02</publish_date>
      <description>After an inadvertant trip through a Heisenberg
      Uncertainty Device, James Salway discovers the problems 
      of being quantum.</description>
   </book>
   <book id="bk110">
      <author>O'Brien, Tim</author>
      <title>Microsoft .NET: The Programming Bible</title>
      <genre>Computer</genre>
      <price>36.95</price>
      <publish_date>2000-12-09</publish_date>
      <description>Microsoft's .NET initiative is explored in 
      detail in this deep programmer's reference.</description>
   </book>
   <book id="bk111">
      <author>O'Brien, Tim</author>
      <title>MSXML3: A Comprehensive Guide</title>
      <genre>Computer</genre>
      <price>36.95</price>
      <publish_date>2000-12-01</publish_date>
      <description>The Microsoft MSXML3 parser is covered in 
      detail, with attention to XML DOM interfaces, XSLT processing, 
      SAX and more.</description>
   </book>
   <book id="bk112">
      <author>Galos, Mike</author>
      <title>Visual Studio 7: A Comprehensive Guide</title>
      <genre>Computer</genre>
      <price>49.95</price>
      <publish_date>2001-04-16</publish_date>
      <description>Microsoft Visual Studio 7 is explored in depth,
      looking at how Visual Basic, Visual C++, C#, and ASP+ are 
      integrated into a comprehensive development 
      environment.</description>
   </book>
</catalog>
  """
    xmlTree = Tree()
    xmlTree.parser(file_string)
    xmlTree.visualizeJSON()
