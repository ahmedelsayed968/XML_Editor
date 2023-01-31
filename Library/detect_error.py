import re

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class stack:
    def __init__(self):
        self.head = Node("head")
        self.size = 0
    def getSize(self):
        return self.size
    def isEmpty(self):
        return bool(self.size == 0)
    def peek(self):
        if self.isEmpty():
            raise Exception("Peeking from an empty stack")
        return self.head.next.value
    def push(self, value):
        node = Node(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1
    def pop(self):
        if self.isEmpty():
            raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value
        
def get_closed_tags(string):
    pattern = r'</(.+?)>'
    match = re.findall(pattern, string)
    return match

def get_words_between_angle_brackets(string):
    pattern = r'<([^\\?!/]+?)>'
    match = re.findall(pattern, string)
    return match


def detect_error(xml_string):
    open_tag=get_words_between_angle_brackets(xml_string)


    close_tag=get_closed_tags(xml_string)

    # convert list1 and list2 to sets
    set1 = set(open_tag)
    set2 = set(close_tag)

    # use union method to combine the two sets into one without duplicates
    result_set = set1.union(set2)

    # convert the set back to a list
    opening_words= list(result_set)
    opening_words=[i for i in opening_words if not re.search(r"atrr=", i)]
    closing_words = ['/'+i for i in opening_words ]

    Lines = xml_string.split('\n')

    
    count=0

    stack1 = stack()   #temp stack
    open_tag_error=stack()     #close tag error
    close_tag_error=stack()     #open tag error 
    data_error=stack()
    line_words=[]
    pastline=[]
    statement=""
            
            

    for line in Lines:
        
        word_count=0
        if line.isspace() or line=='' :
            count=count +1
            continue 
        result = re.findall(r'<.*?>|[^<>]+', line)
        pastpast=pastline
        pastline=line_words
        line_words = []
        
        for val in result:
                val = val.replace("<", "").replace(">", "")
                if("=" in val and not("?" in val)):
                    val=val.split(" ")[0][:]
                    
                line_words.append(val)
        count=count +1
        line_words=[x for x in line_words if x.strip()]
        for line in line_words:
            
            word_count=word_count+1
            if(not("/" in line)):
                for opening_word in opening_words:
                    if (opening_word == line):
                        if(word_count>1):
                            
                            if(line_words[word_count-2]not in opening_words and line_words[word_count-2] not in closing_words ):
                                
                                if(word_count-3 >-1):
                                    if(line_words[word_count-3] in opening_words):
                                            
                                        
                                            close_tag_error.push(count)
                                            close_tag_error.push(line_words[word_count-3])
                                            stack1.pop()
                                            stack1.pop()


                                    else:
                    
                                            if(pastline[len(pastline)-1] in opening_words):
                            
                                                
                                                close_tag_error.push(count)
                                                close_tag_error.push(pastline[len(pastline)-1])
                                            
                                                stack1.pop()
                                                stack1.pop()

                        


                                        
                        else:
                            if((word_count==1 ) and count>2):

                                if(pastline[len(pastline)-1]not in opening_words and pastline[len(pastline)-1] not in closing_words): 

                                    if((len(pastline)-2)>-1):
                                    

                                        if(pastline[len(pastline)-2] in opening_words ):
                                            
                                            close_tag_error.push(count-1)
                                            close_tag_error.push(pastline[len(pastline)-2])
                                            stack1.pop()
                                            stack1.pop()
    
                                    else:
                                        
                                        if(pastpast[len(pastpast)-1] in opening_words   ):
                                            close_tag_error.push(count-1)
                                            
                                            close_tag_error.push(pastpast[len(pastpast)-1])
                                            stack1.pop()
                                            stack1.pop()

                                        
                                
                        stack1.push(count)
                        stack1.push(opening_word)
                        break

                            
                
            else:
                
                for closing_word in closing_words: 
                    
                    if (closing_word == line):


                                
                        if( stack1.isEmpty() ):
                            
                            open_tag_error.push(count)
                            open_tag_error.push(closing_word)
                            break
                    
                        else:
                            #print(stack1.peek())
                            #print(line)
                            
                            temp='/'+stack1.peek()
                            
                            if (temp!=closing_word ):

                                tag=stack1.pop()
                                count_tag=stack1.pop()
                                if(not stack1.isEmpty()):
                                    if(stack1.peek()==closing_word[1:]):
                                        
                                        
                                        close_tag_error.push(count_tag)
                                        close_tag_error.push(tag)
                                        stack1.pop()
                                        stack1.pop()
                                    else:
                                    
                                        open_tag_error.push(count)
                                        open_tag_error.push(closing_word[1:])
                                        stack1.push(count_tag)
                                        stack1.push(tag)

                                elif(stack1.isEmpty()):
                                    open_tag_error.push(count)
                                    open_tag_error.push(closing_word[1:])
                                    close_tag_error.push(count_tag)
                                    close_tag_error.push(tag)

                                    
                                break
                                        
        
                                    
                            else:
                            
                                
                                stack1.pop()
                                stack1.pop()
                                break
                        
            

        

    while stack1.getSize() !=0:    
        temp=stack1.peek()
        stack1.pop()
        close_tag_error.push(stack1.peek())
        stack1.pop()
        close_tag_error.push(temp)


    while close_tag_error.getSize()!=0:
        statement +="missing close tag for the open tag  "+str(close_tag_error.peek())
        close_tag_error.pop()
        statement+=" which in  line  "+str(close_tag_error.peek())+"\n"
        close_tag_error.pop()

    while open_tag_error.getSize() !=0:
        
        statement +="missing or incorret open tag for close tag "+str(open_tag_error.peek())
        open_tag_error.pop()
        statement+=" which in line "+str(open_tag_error.peek())+"\n"
        open_tag_error.pop()
    return statement

if __name__ == "__main__":
    xml_string="""<users>
    
        1</id>
        Ahmed Ali</name>
        <posts>
            <post>
                <body>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                
                
                    
                        economy
                    </topic>
                    <topic>
                        finance
                    </topic>
                </topics>
            </post>
            <post>
                <body>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </body>
                <topics>
                    <topic>
                        solar_energy
                    </topic>
                </topics>
            </post>
        </posts>
        <followers>
            <follower>
                <id>2</id>
            
            <follower>
                <id>3</id>
            </follower>
        </followers>
    </user>
    <user>
        <id>2</id>
        <name>Yasser Ahmed
        <posts>
            <post>
                <body>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </body>
                <topics>
                    <topic>
                        education
                    </topic>
               
            </post>
        </posts>
        <followers>
            <follower>
                <id>1</id>
            </follower>
        </followers>
    </user>
    <user>
        3</id>
        Mohamed Sherif</name>
        <posts>
            <post>
                <body>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </body>
                <topics>
                    <topic>
                        sports
                    </topic>
                </topics>
            </post>
        </posts>
        <followers>
            <follower>
                <id>1</id>
            </follower>
        </followers>
    </user>
</users>"""
   # print(detect_error(xml_string))