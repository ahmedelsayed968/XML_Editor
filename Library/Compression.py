#Huffman Compression
import heapq


def minify(data):
    
    data=data.replace("    ",'')
    data=data.replace('\t','')
    data=data.replace('\n','')
    return data


class HuffmanCode:
	def __init__(self,data:str):
		self.data = minify(data)
		self.heap = []
		self.codes = {} 
		self.reversecode = {}

	class BinaryTreeNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		# less_than Method
		def __lt__(self, other):
			return self.freq < other.freq

		#equals method
		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other, BinaryTreeNode)):
				return False
			return self.freq == other.freq

	# functions for compression:

	#method that builds the frequency of each char. in xml file and store them in hashmap 
	def __freq_dict_builder(self, xml_text):
		frequency = {}
		for character in xml_text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	
	# build heap , push minimum nodes into heap
	def __heap_builder(self, frequency):
		for key in frequency:
			node = self.BinaryTreeNode(key, frequency[key])
			heapq.heappush(self.heap, node)
		
	#build binary tree by mergeing 2 minimum nodes each time
	def __binary_tree_builder(self):
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = self.BinaryTreeNode(None, node1.freq + node2.freq)
			merged.left,merged.right = node1,node2

			heapq.heappush(self.heap, merged)

	#this method is responsible for assigning 0's to left nodes and 1's for right nodes
	def __codes_generator_helper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reversecode[current_code] = root.char
			return

		self.__codes_generator_helper(root.left, current_code + '0')
		self.__codes_generator_helper(root.right, current_code + '1')


	def __codes_generator(self):
		root = heapq.heappop(self.heap)
		self.__codes_generator_helper(root,'')


	def __encoded_text_builder(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text

	#add padding in case of total bits not multiple of 8
	def __padding_builder(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"
		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text
	#put bits in form of bytes for output binary file
	def __bytes_list_bulder(self, padded_encoded_text):
		bytes_list = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			bytes_list.append(int(byte, 2))
		return bytes_list

	"""-------------Compression---------------"""
	def compress(self):
		data = self.data
		data = data.rstrip()
		frequency = self.__freq_dict_builder(data)
		self.__heap_builder(frequency)
		self.__binary_tree_builder()
		self.__codes_generator()

		encoded_text = self.__encoded_text_builder(data)
		padded_encoded_bits = self.__padding_builder(encoded_text)

		compressed_data=[padded_encoded_bits[8*i:8*(i+1)] for i in range(len(padded_encoded_bits)//8)]

		compressed_data=[int(i,2) for i in compressed_data]

		compressed_data=''.join(chr(i) for i in compressed_data)		


		print("Compressed")
		return compressed_data


		"""----------Decompression------------"""

	#remove the added padding in encoded text
	def __remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text
	#decode the encoded text
	def __xml_text_decoder(self, encoded_text):
		current_code = ""
		decoded_xml_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reversecode):
				character = self.reversecode[current_code]
				decoded_xml_text += character
				current_code = ""

		return decoded_xml_text


	def decompress(self, input_data):
		#convert string to utf-8
		#utf-8 to bits
		byte_arr = bytearray(input_data, 'utf-8')
		byte_arr=bytes(byte_arr)
		byte_arr=byte_arr.decode("utf-8") 
		bytes_as_bits = ''.join(format(ord(byte), '08b') for byte in byte_arr)

		encoded_text = self.__remove_padding(bytes_as_bits)
		decompressed_text = self.__xml_text_decoder(encoded_text)



		print("Decompressed")
		return decompressed_text
	