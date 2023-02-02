# XML_Editor
## Table of Contents

| **Feature** | **Description** |
| ------- | ----------- |
| [**1. Checking XML consistency**](https://github.com/ahmedelsayed968/XML_Editor/edit/main/README.md#1-checking-xml-consistency) | Validate input XML for consistency |
| [**2. Formatting XML**](https://github.com/ahmedelsayed968/XML_Editor/edit/main/README.md#2-formatting-xmlformatting-xml) | Prettify the XML file with proper indentation |
| [**3. Converting XML to JSON**](https://github.com/ahmedelsayed968/XML_Editor/edit/main/README.md#3-converting-xml-to-json) | Convert XML data to JSON format |
| [**4. Minifying XML file**](https://github.com/ahmedelsayed968/XML_Editor/edit/main/README.md#4-minifying-xml-file) | Reduce the size of XML by removing unnecessary whitespaces and lines|
| [**5. Compressing XML/JSON data**](https://github.com/ahmedelsayed968/XML_Editor/edit/main/README.md#5-compressing-xmljson-data) | Compress the data in the XML/JSON file |
| [**6. Decompressing compressed data**](https://github.com/ahmedelsayed968/XML_Editor/edit/main/README.md#6-decompressing-compressed-data) | Return the compressed data to its original format |
| [**7. Network analysis**](https://github.com/ahmedelsayed968/XML_Editor/edit/main/README.md#7-network-analysis) | Analyze the data represented in the network |
| [**8. Post search**](https://github.com/ahmedelsayed968/XML_Editor/edit/main/README.md#8-post-search) | Search posts in the XML data |
| [**9. Graph visualization**](https://github.com/ahmedelsayed968/XML_Editor/edit/main/README.md#9-graph-visualization) | Visualize the data in a graph  |

----
## Features

### 1. Checking XML consistency
Validate input XML for consistency

----
### 2. Formatting XML
Prettify the XML file with proper indentation

----
### 3. Converting XML to JSON
Convert XML data to JSON format

----
### 4. Minifying XML file
Reduce the size of XML by removing unnecessary whitespaces and lines

----
### 5. Compressing XML/JSON data
Huffman coding is a **data compression technique** that is used to represent the data in an efficient way. It is a *lossless compression algorithm* that works by constructing a **binary tree** that assigns codes to each character in the text. These codes are chosen based on the *frequency of the characters*, with more frequent characters getting shorter codes and less frequent characters getting longer codes. The main goal of Huffman coding is to *minimize the average length of the codes assigned to the characters*, resulting in more efficient storage of the text, which resulting a *significantly reduce the size of the data without losing any of the original information*.
* Here is an example of representing the sentence **"Data Structures Project"** in Tree 
![Compression Tree](https://serving.photos.photobox.com/64998938a5d89edffa6fa5ef241e4df50e78719d58778f1975d1c8386a8b82f05d72b7a5.jpg)

* And here is the frequency dictionary of the sentence 

![Frequency dictionary](https://www.linkpicture.com/q/Compression-Dictionary-1.png)

----
### 6. Decompressing compressed data
* Return the compressed data to its **original format**
* Simply , Decompression works by **reversing** the process of compression,the compressed text is read bit by bit then look up the corresponding symbol in the reverse Huffman coding dictionary. The decoded symbols are concatenated to form the original data.
----
### 7. Network analysis
* **Analyze** the data represented in the network
* The data of users that extracted from xml is represented by graph as following :
  * **{1 : [2,3] , 2 : [1] , 3 : [1] }**
  * Where user with ID = 1 has followers with ID =[2,3]
  * So *user2* , *user3* are following *user1*
 
#### By this representation, it is easy now to extract the following :

   #### Most Influencer User
   * It returns the user who has the **most followers** on the network
   #### Most Active User
   * It return the user who follows the biggest number of users

   #### Mutual Friends
   * The mutual followers between two users are the users who follow both of them.

   #### Suggested Friends
   * For each user, a list of users to follow can be suggested based on the followers of their followers.
   
   ##### Here is an example for a certain network
   ![Network analysis](https://gcdnb.pbrd.co/images/8YSwO3DZ09QU.png?o=1)
---

 

### 8. Post search
* Searching is simply done by checking the post's **body** text and **topics** for the word to be found, and adds a string with the user's name and relevant information (the body or topic) to the list to be returned if found.


---
### 9. Graph visualization
* Graph Visualization is done using :
  * NetworkX 
  * Matplotlib

* it represents how users are connected to each other in a visual graph

### ![visualization](https://gcdnb.pbrd.co/images/ahsJ4OiseLOo.jpg?o=1)
### 10. How to open exe file 
*from exe_file folder open dist folder and then press on exe file 
 

---
