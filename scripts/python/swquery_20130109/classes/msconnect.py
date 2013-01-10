from sqlalchemy import create_engine
import os, cPickle, base64

class MSSQLConnect():
	def __init__(self):
		self.mypath = os.path.dirname( os.path.realpath( __file__) )
		self.savefile = os.path.join(self.mypath, '../data/data.p')
		self.return_query = "SELECT Name, IP FROM NodeObjectTable WHERE Primary_User='PUser'"
		self.data = []
		self.server_ip = "192.168.1.100"
		self.server_db = "SWDB"
		self.user = "viewonly"
		self.passwd = "password"

	def load_data(self):
		#Try to grab data from sql database
		try:
			print "Connecting to the database...\n"
			engine = create_engine("mssql://%s:%s@%s/%s" % (self.user, self.passwd, self.server_ip, self.server_db)) 
			for row in engine.execute(self.return_query):
				self.data.append([row.Name, row.IP])
			try:
				print "Saving data to savefile: %s" % self.savefile
				f = open(self.savefile, 'wb')
				f.write(base64.b64encode(cPickle.dumps(self.data)))
				f.close()
				print "Data saved to %s" % self.savefile
			except:
				print "Could not save data."

		#If it fails, load from save file.
		except:
			print "Could not connect to database or bad username/password combination."
			try:
				print "Loading from savefile: %s" % self.savefile
				f = open(self.savefile, 'rb')
				obj = f.read()
				self.data = cPickle.loads(base64.b64decode(obj))
				f.close()
				for en in self.data:
					print en
			except:
				print "No data loaded. Does %s exists?" % self.savefile
				
	def get_data(self):
		return self.data