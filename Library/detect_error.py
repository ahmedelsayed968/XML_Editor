import re

class Node:
    """Node for linked list implementation of stack"""
    def __init__(self, value):
        """
        Initialize the node with value

        Parameters:
        value (Any): The value to be stored in the node
        """
        self.value = value
        self.next = None

class stack:
    # mplementation of a stack data structure using linked list
    def __init__(self):
        # Initialize the stack
        self.head = Node("head")
        self.size = 0
    def getSize(self):
        # Returns the size of the stack
        return self.size
    def isEmpty(self):
        # Checks if the stack is empty
        return bool(self.size == 0)
    def peek(self):
        # Returns the top element of the stack without removing it
        if self.isEmpty():
            raise Exception("Peeking from an empty stack")
        return self.head.next.value
    def push(self, value):
        # Pushes an element onto the top of the stack
        node = Node(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1
    def pop(self):
        # Pops the top element off the stack
        if self.isEmpty():
            raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value
        
def get_closed_tags(string):
    #to extract words between </>
    pattern = r'</(.+?)>'
    match = re.findall(pattern, string)
    return match

def get_words_between_angle_brackets(string):
    #to extract words between <> and not include  comments tag or self-close tag  
    pattern = r'<([^\\?!/]+?)>'
    match = re.findall(pattern, string)
    return match


def detect_error(xml_string):
    # Extract all words between angle brackets in the xml string
    open_tag=get_words_between_angle_brackets(xml_string)

    # Get all closing tags in the xml string
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

    #split data into lines

    Lines = xml_string.split('\n')

    # Initialize stacks for temporary data, open tag errors, close tag errors, and count
    count=0

    stack1 = stack()   #temp stack
    open_tag_error=stack()     #close tag error
    close_tag_error=stack()     #open tag error 
    data_error=stack()
    line_words=[]
    pastline=[]
    statement=""
            
            
# Iterate through each line in the xml string
    for line in Lines:
        
        word_count=0
        # Skip any empty or whitespace lines
        if line.isspace() or line=='' :
            count=count +1
            continue 
        # Extract all elements between angle brackets and all other characters
        result = re.findall(r'<.*?>|[^<>]+', line)
        pastpast=pastline
        pastline=line_words
        line_words = []
        
        for val in result:
             # Remove angle brackets from the element
                val = val.replace("<", "").replace(">", "")
                if("=" in val and not("?" in val)):
                    #for open tag with attr
                    val=val.split(" ")[0][:]
                    
                line_words.append(val)
        count=count +1
         # Remove any whitespace elements from the line words list
        line_words=[x for x in line_words if x.strip()]
        # Iterate through each word in the line
        for line in line_words:
            
            word_count=word_count+1
            # if does not  have slash mean it is open tag or data
            if(not("/" in line)):
                for opening_word in opening_words:
                    if (opening_word == line):
                        if(word_count>1):
                            
                            if(line_words[word_count-2]not in opening_words and line_words[word_count-2] not in closing_words ):
                                #if we have data and before it a close tag that means error in open tag 
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


                         #if it empty that means error in open tag for the recent close tag       
                        if( stack1.isEmpty() ):
                            
                            open_tag_error.push(count)
                            open_tag_error.push(closing_word)
                            break
                    
                        else:
                            #print(stack1.peek())
                            #print(line)
                            
                            temp='/'+stack1.peek()
                            #if not match with the open tag in the stack we see the past open tag if match that means error close tag 
                            # for the unmatched open tag if not that means error in both tag 
                            if (temp!=closing_word ):
                                flag=False
                                temp_stack=stack()
                                while(not flag):
                                    if(stack1.isEmpty()):
                                        break
                                    if(stack1.peek()==closing_word[1:]):
                                        stack1.pop()
                                        stack1.pop()
                                        flag=True
                                        break
                                    else:
                                        temp_stack.push(stack1.pop())
                                        temp_stack.push(stack1.pop())

                                if(flag):
                                    while(not temp_stack.isEmpty()):
                                        close_tag_error.push(temp_stack.pop())
                                        close_tag_error.push(temp_stack.pop())

                                else:
                                    while(not temp_stack.isEmpty()):
                                        stack1.push(temp_stack.pop())
                                        stack1.push(temp_stack.pop())
                                    open_tag_error.push(count)
                                    open_tag_error.push(closing_word[1:])
         
                                break
                                        
        
                                    
                            else:
                            
                                
                                stack1.pop()
                                stack1.pop()
                                break
                        
            

        
    #check if the stack empty if not this means error in clos tag 
    while stack1.getSize() !=0:    
        temp=stack1.peek()
        stack1.pop()
        close_tag_error.push(stack1.peek())
        stack1.pop()
        close_tag_error.push(temp)

    # restore errors in one varible called statement
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


# if __name__ == "__main__":
#     xml_string="""<users>
    
#         1</id>
#         Ahmed Ali</name>
#         <posts>
#             <post>
#                 <body>
#                     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                
                
                    
#                         economy
#                     </topic>
#                     <topic>
#                         finance
#                     </topic>
#                 </topics>
#             </post>
#             <post>
#                 <body>
#                     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
#                 </body>
#                 <topics>
#                     <topic>
#                         solar_energy
#                     </topic>
#                 </topics>
#             </post>
#         </posts>
#         <followers>
#             <follower>
#                 <id>2</id>
            
#             <follower>
#                 <id>3</id>
#             </follower>
#         </followers>
#     </user>
#     <user>
#         <id>2</id>
#         <name>Yasser Ahmed
#         <posts>
#             <post>
#                 <body>
#                     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
#                 </body>
#                 <topics>
#                     <topic>
#                         education
#                     </topic>
               
#             </post>
#         </posts>
#         <followers>
#             <follower>
#                 <id>1</id>
#             </follower>
#         </followers>
#     </user>
#     <user>
#         3</id>
#         Mohamed Sherif</name>
#         <posts>
#             <post>
#                 <body>
#                     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
#                 </body>
#                 <topics>
#                     <topic>
#                         sports
#                     </topic>
#                 </topics>
#             </post>
#         </posts>
#         <followers>
#             <follower>
#                 <id>1</id>
#             </follower>
#         </followers>
#     </user>
# </users>"""
#     print(detect_error(xml_string))