from django.test import TestCase
from home.services import gen_rand_id

class ViewsTest(TestCase):
	def test_f(self):
		result = []
		for i in range(30):
			result.append(gen_rand_id(15))
		for i in result:
			self.assertEqual(1,result.count(i))