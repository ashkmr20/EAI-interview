import requests
import unittest

class Test_contacts_api(unittest.TestCase):
	def setUp(self):
		#lists to create dummy values
		self.test_name=['a' for i in range(10)]
		self.test_phone= ['0' for i in range(10)]
	def test_post_multiple_ele(self):	
		for i in range(50):
			num_range= int(i/9)
			char_range=int(i/25)
			name=""
			phone_no=""
			self.test_phone[-1-num_range]= str(int(self.test_phone[-1-num_range])+1)
			self.test_name[-1-char_range]= chr(ord(self.test_name[-1-char_range])+1)
			for i in self.test_phone:
				phone_no=phone_no+i
			for i in self.test_name:
				name=name+i
			#name, phone aaaaa, 00000 and increase similarly
			r = requests.post('http://127.0.0.1:5000/contact', data = {'name':name, 'phone_no': phone_no})
			self.assertEqual(r.status_code, 200)
	def test_update(self):
		r = requests.put('http://127.0.0.1:5000/contact/aaaaaaaaat', data = {})
		self.assertEqual(r.status_code, 200)
	def test_delete_absent_name(self):
		r = requests.delete('http://127.0.0.1:5000/contact/190293')
		print(r.status_code) 
		self.assertEqual(r.status_code, 400)


if __name__ == '__main__':
    unittest.main()