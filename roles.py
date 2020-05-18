from hashlib import pbkdf2_hmac
from flask_restful import Resource, reqparse
from database import DataBase
db = DataBase()
parser = reqparse.RequestParser()

class Roles(Resource):
    def get(self):
        query = 'select * from {}s'.format(self.category)
        return db.execute(query)

    def post(self):
        parser.add_argument('firstname', type=str)
        parser.add_argument('lastname', type=str)
        if self.category == 'patient':
            parser.add_argument('username', type=str)
            parser.add_argument('password', type=str)
        args = parser.parse_args()
        firstname, lastname, username, password = args['firstname'], args['lastname'], args['username'], pbkdf2_hmac('sha256', args['password'].encode('utf-8'), '?AzP7@0'.encode('utf-8'), 100000).decode('latin')
        newid = db.execute("select uuid_generate_v3(uuid_generate_v1(),\'{}\')".format(firstname))[0]['uuid_generate_v3']
        insvals = '\'{}\', {}\'{}\', \'{}\''.format(newid, '\'{}\', \'{}\', '.format(username, password) if self.category == 'patient' else '', firstname, lastname)
        query = 'insert into {}s values ({})'.format(self.category, insvals)
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res, 'id': newid}

    def delete(self):
        parser.add_argument('roleid', type=str)
        roleid = parser.parse_args()['roleid']
        res = db.execute('delete from prescriptions where {}id=\'{}\''.format(self.category, roleid), post=True)
        if isinstance(res, int) or res == "no results to fetch":
            res = db.execute('delete from appointments where {}id=\'{}\''.format(self.category, roleid), post=True)
            if isinstance(res, int) or res == "no results to fetch":
                res = db.execute('delete from {}s where id=\'{}\''.format(self.category, roleid), post=True)
        success = res==1
        return {'success': success, 'affectedrows': res}, 200 if success else 401

    def put(self):
        parser.add_argument('id', required=True)
        parser.add_argument('firstname')
        parser.add_argument('lastname')
        args = parser.parse_args()
        first, last = args['firstname'], args['lastname']
        query = ('update {}s set '.format(self.category)) + ('firstname=\'{}\' '.format(first) if first else '') + ('and ' if first and last else '') + ('lastname=\'{}\' '.format(last) if last else '') + 'where id=\'{}\''.format(args['id'])
        print(query)
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res}

class Patients(Roles):
    category = 'patient'

class Login(Resource):
    def post(self):
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()
        user, pw = args['username'], pbkdf2_hmac('sha256', args['password'].encode('utf-8'), '?AzP7@0'.encode('utf-8'), 100000).decode('latin')
        pws = {row['password']:row for row in db.execute('select * from patients where username = \'{}\''.format(user))}
        return {'success': pw in pws, 'user': None if pw not in pws else pws[pw]}

class Doctors(Roles):
    category = 'doctor'
