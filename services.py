from flask_restful import Resource, reqparse
from database import DataBase
db = DataBase()
parser = reqparse.RequestParser()

class Services(Resource):
    columns_for_roles = 's.doctorid, d.firstname as doc_first, d.lastname as doc_last, s.patientid, p.firstname as pat_first, p.lastname as pat_last, '
    table_join = '{}s as s left join doctors as d on s.doctorid=d.id left join patients as p on s.patientid=p.id '

    def get(self, role=None):
        if role==None:
            parser.add_argument('doctorid')
            parser.add_argument('patientid')
            args = parser.parse_args()
            query = 'select ' + self.columns_for_roles + self.columns_for_service + 'from ' + self.table_join + 'where d.id=\'{}\' and p.id=\'{}\''.format(args['doctorid'], args['patientid'])
        else:
            parser.add_argument('roleid')
            roleid = parser.parse_args()['roleid']
            query = 'select ' + self.columns_for_roles + self.columns_for_service + 'from ' + self.table_join + 'where {}.id=\'{}\''.format('d' if role=='doctor' else 'p', roleid)
        return db.execute(query)

class Prescriptions(Services):
    category = 'prescription'
    columns_for_service = 'm.name, s.dose::text, s.dose_unit, s.dose_freq, s.start_date::text, s.duration::text, s.create_date::text '
    def __init__(self):
        self.table_join = self.table_join.format(self.category) + 'left join medicines as m on s.medicineid=m.id '

    def post(self):
        parser.add_argument('doctorid')
        parser.add_argument('patientid')
        parser.add_argument('medicineid')
        parser.add_argument('dose')
        parser.add_argument('unit')
        parser.add_argument('freq')
        parser.add_argument('startdate')
        parser.add_argument('duration')
        args = parser.parse_args()
        docid, start, unit = args['doctorid'], args['startdate'], args['unit']
        query = 'insert into prescriptions values (uuid_generate_v3(\'{}\', \'{}\'), \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')'.format(docid, start + unit, docid, args['patientid'], args['medicineid'], args['dose'], unit, args['freq'], start, args['duration'])
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res}

class Appointments(Services):
    category = 'appointment'
    columns_for_service = 's.status, to_char(s.date, \'yyyy-mm-dd\') as date, to_char((s.starttime at time zone \'utc\')::time, \'hh24:mi:ss\') as starttime, to_char((s.endtime at time zone \'utc\')::time, \'hh24:mi:ss\') as endtime '
    def __init__(self):
        self.table_join = self.table_join.format(self.category)

    def post(self):
        parser.add_argument('doctorid')
        parser.add_argument('patientid')
        parser.add_argument('date')
        parser.add_argument('start')
        parser.add_argument('end')
        args = parser.parse_args()
        query = 'insert into appointments values (\'{}\', \'{}\', 1, \'{}\', \'{}\', \'{}\')'.format(args['doctorid'], args['patientid'], args['date'], args['start'], args['end'])
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res}

    def put(self, status):
        parser.add_argument('doctorid')
        parser.add_argument('date')
        parser.add_argument('start')
        args = parser.parse_args()
        statusdict = {'finished':2, 'unattended':0, 'booked':1}
        query = 'update appointments set status={} where doctorid=\'{}\' and date=\'{}\' and starttime=\'{}\''.format(statusdict[status], args['doctorid'], args['date'], args['start'])
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res}

    def delete(self):
        parser.add_argument('doctorid')
        parser.add_argument('date')
        parser.add_argument('start')
        args = parser.parse_args()
        query = 'delete from appointments where doctorid=\'{}\' and date=\'{}\' and starttime=\'{}\''.format(args['doctorid'], args['date'], args['start'])
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res}

class Slots(Resource):
    def get(self, doctorid):
        query = """SELECT '{}' as doctorid, s.starttime::text, (s.starttime + interval '15 minute')::text as endtime
FROM (SELECT date_trunc('HOUR', now()) + make_interval(mins => date_part('MINUTE', now())::int/15+1+Number) * 15 as starttime from Numbers) as s
WHERE
    date_part('HOUR', s.starttime) >= 9
        AND
    date_part('HOUR', s.starttime + interval '14 minute') <= 16
        AND
    NOT EXISTS (SELECT 1 FROM appointments AS a WHERE s.starttime::time < a.endtime AND endtime::time > a.starttime AND a.doctorid = doctorid AND a.date = date_trunc('day', s.starttime))
        AND
    extract(dow from s.starttime) not in (0,6)
        AND
    s.starttime <= now() + interval '10 days' - interval '15 minute'
ORDER BY s.starttime""".format(doctorid)
        return db.execute(query)
