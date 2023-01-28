import re
def minify(data):
    data=data.replace("    ",'')
    data=data.replace('\t','')
    data=data.replace('\n','')
    return data
def valid( s):
      s= minify(s)
      s = re.sub("<", "\n<", s)
      s = re.sub(">", ">\n", s)
      Lines = s.split("\n")
      def smallest_between_two(a, b, text):
           
            return re.findall(re.escape(a)+"(.*?)"+re.escape(b),text)
      
      stack=[]
      for line in Lines:

            size=len(smallest_between_two('<', '>',line ))
      
            if(len(line)==0):
                  continue
            if(size!=0):
                  for tag in smallest_between_two('<', '>',line ):
                        if '?' in tag or '\\' in tag or '!' in tag:
                              continue

                        elif('/' in tag):
                              if(len(stack)==0):

                                    return False
                              else:
                                  temp= stack.pop()
                                  if(not tag[1:] in temp):
                                    return False

                        else:
                              stack.append(tag)
      if( not len(stack)==0):
            return False
      return True
                        
