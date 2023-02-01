import re

def add_new_lines(minifystring):
    """
    Add new line before "<" and after ">" in the minifystring
    
    Parameters:
    minifystring (str): A string which needs to be formatted.

    Returns:
    str: Returns a formatted string with new line added before "<" and after ">".
    """
    minifystring = re.sub("<", "\n<", minifystring)
    minifystring = re.sub(">", ">\n", minifystring)
    return minifystring

def smallest_between_two(a, b, text):
    """
    Find the smallest sub-string between a and b in the text
    
    Parameters:
    a (str): Starting string.
    b (str): Ending string.
    text (str): A string which needs to be processed.

    Returns:
    list: Returns a list of sub-strings between a and b.
    """
    return re.findall(re.escape(a)+"(.*?)"+re.escape(b),text)


def minify(string):
    """
    Remove extra spaces between ">" and "<" in the string
    
    Parameters:
    string (str): A string which needs to be minified.

    Returns:
    str: Returns a minified string with spaces removed between ">" and "<".
    """
    new_string = re.sub(r"(>\s+<)", "><", string)
    return new_string

def prettify(string):
    """
    Prettify the string to make it more readable
    
    Parameters:
    string (str): A string which needs to be prettified.

    Returns:
    str: Returns a prettified string with proper indention.
    """
    minifystring=minify(string)
    print(minifystring)
    minifystring=add_new_lines(string)
    Lines = minifystring.split("\n")
    string_output=""  
    count=-1
    flag_close=False
    flag_data=True
    for line in Lines:
        flag_data=True
        flag_close=False
        size=len(smallest_between_two('<', '>',line ))
        if(len(line)==0):
            continue
        if(size!=0):
            for tag in smallest_between_two('<', '>',line ):
                flag_data=False 
                if("/" in tag):
                    flag_close=True
                else:
                    count+=1
        if(flag_data):
            count+=1
        string_output=string_output+ "\t"*count+line+"\n"
        if(flag_close or flag_data):
            count=count-1
    return string_output


string="\n\n\n<users>\n\n\n\n<user>\n<id>1</id>\n\n\n<name>Ahmed Ali</name>\n<posts>\n<post>\n<body>\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n</body>\n<topics>\n<topic>\nsolar_energy\n</topic>\n</topics>\n</post>\n</posts>\n<followers>\n<follower>\n<id>2</id>\n</follower>\n<follower>\n<id>3</id>\n</follower>\n</followers>\n</user>\n</uses>"
print(prettify(string))