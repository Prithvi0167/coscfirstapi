from flask_restful import Resource,reqparse
from db import query
from flask_jwt_extended import create_access_token,jwt_required
from werkzeug.security import safe_str_cmp

class Emp(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser() #for taking input from user
        parser.add_argument('empno',type=int,required=True,help="empno cannot be left blank ")
        data=parser.parse_args()
        try:
            return query(f'''select * from testapi.emp where empno={data['empno']}''')
        except:
            return {"msg":"no connection to emp established error occured"},500
            #this 500 is taken as aresponse code
    #for inserting into a table
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('empno',type=int,required=True,help="empno cannot be left blank ")
        parser.add_argument('ename',type=str,required=True,help="ename cannot be left blank ")
        parser.add_argument('job',type=str,required=True,help="job cannot be left blank ")
        parser.add_argument('mgr',type=int,required=True,help="mgr cannot be left blank ")
        parser.add_argument('hiredate',type=str,required=True,help="hiredate cannot be left blank ")
        parser.add_argument('sal',type=str,required=True,help="sal cannot be left blank ")
        parser.add_argument('comm',type=str) #since in database table this is not compulsory to enter
        parser.add_argument('deptno',type=int,required=True,help="deptno cannot be left blank ")
        parser.add_argument('pass',type=str,required=True,help="pass cannot be left blank ")
        data=parser.parse_args()
        #handling the primary key constarints i.e if user enters same empno to insert then this should occur.
        try:
            if len(query(f"""select * from testapi.emp where empno={data['empno']}""",return_json=False)) > 0:
                return "empno already exists",400
        except:
            return {"msg":"error while inserting into database"},500
        #handling foreign key constraint we cannot add a different deptno from emp table
        try:
            if len(query(f"""select * from testapi.emp where deptno={data['deptno']}""",return_json=False))==0:
                return "cannot find such department enter valid department",400
        except:
            return {"msg":"error inserting into database"},500

        if(data['comm']!=None):
            try:
                query(f"""insert into testapi.emp values({data['empno']},
                                                        '{data['ename']}',
                                                        '{data['job']}',
                                                        {data['mgr']},
                                                        '{data['hiredate']}',
                                                        '{data['sal']}',
                                                        '{data['comm']}',
                                                        {data['deptno']},
                                                        '{data['pass']}')""")

            except:
                return {"msg":"no connection to emp established error occured"},500
            return {"msg":"successfully inserted"},201
        else:
            try:
                query(f"""insert into testapi.emp(empno,ename,job,mgr,hiredate,sal,deptno,pass)
                                                        values({data['empno']},
                                                        '{data['ename']}',
                                                        '{data['job']}',
                                                        {data['mgr']},
                                                        '{data['hiredate']}',
                                                        '{data['sal']}',
                                                        {data['deptno']},
                                                        '{data['pass']}')""")  #commision is removed

            except:
                return {"msg":"no connection to emp established error occured"},500
            return {"msg":"successfully inserted"},201

class User():
    def __init__(self,empno,ename,password):
        self.empno=empno
        self.ename=ename
        self.password=password
    @classmethod
    def getUserdetailsbyename(cls,ename):
        result=query(f"""select empno,ename,pass from emp where ename='{ename}'""",return_json=False)
        if len(result)>0:
            return User(result[0]['empno'],result[0]['ename'],result[0]['pass'])
    @classmethod
    def getUserdetailsbyempno(cls,empno):
        ans=query(f"""select empno,ename,pass from emp where empno='{empno}'""",return_json=False)
        if len(ans)>0:
            return User(ans[0]['empno'],ans[0]['ename'],ans[0]['pass'])

class Emplogin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('empname',type=str,required=True,help="empname cannot be left blank ")
        parser.add_argument('pass',type=str,required=True,help="password cannot be left blank ")
        data=parser.parse_args()
        userdetails=User.getUserdetailsbyename(data['empname'])
        if userdetails and safe_str_cmp(userdetails.password,data['pass']) :
            #generate token
            accesstoken=create_access_token(identity=userdetails.empno,expires_delta=False)
            return {'accesstoken':accesstoken},200
        return {"msg":"Invalid Credentials.."},401
