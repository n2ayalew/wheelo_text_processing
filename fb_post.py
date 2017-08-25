import re
class FBPost:
	
	def __init__(self, msg, up_time, post_id):
		self.msg = msg
		self.up_time = up_time
		self.post_id = post_id
		self.driver_post = None
		self.round_trip = None
		self.price = None
		self.dest = None
		self.origin = None
		self.other_locs = None
		self.date = None
		self.time = None
		self.err_post = False

	def set_type(self):
		"""
		Determines if the post intends to be a driver in a carpool or a rider.
		If the post can't be classified as either a DRIVER or RIDER it is assigned a
		type of 'OTHER'.
		"""
		count = 0
		s = self.msg
		dregs = (r'driving', r'\$', r'offering|providing')
		rregs = (r'looking', r'\?')
		
		count = count+2 if re.search(dregs[0], s, re.I) else count
		count = count+1 if re.search(dregs[1], s, re.I) else count
		count = count+1 if re.search(dregs[2], s, re.I) else count
		count = count-2 if re.search(rregs[0], s, re.I) else count
		count = count-1 if re.search(rregs[1], s, re.I) else count

		if (count > 0):
#			print 'DRIVER POST'
			self.driver_post = 1
		elif (count < 0):
#			print 'RIDER POST'
			self.driver_post = -1
		else:
#			print 'OTHER POST'
			self.driver_post = 0
			self.err_post = True
		return


