import cx_Oracle

from flask import Flask, jsonify, request
from config import config

app = Flask(__name__)
connection=cx_Oracle.connect(
    user=config['development'].DB_USERNAME,
    password=config['development'].DB_PASSWORD,
    dsn=config['development'].DB_DSN,
    encoding=config['development'].DB_ENCODING
    )

# Main page
@app.route("/")
def index():
    return "My APIs with Python - Marco Neira"

# List all employees
@app.route("/employee/list",methods=['GET'])
def list_employee():
    try:
        cursor=connection.cursor()
        cursor.execute("SELECT empno, ename, job, sal from emp")
        rows=cursor.fetchall()
        employees=[]
        for row in rows:
            employee ={'empno':row[0],'ename':row[1],'job':row[2],'sal':row[3]}
            employees.append(employee)
            #print(row)
        return jsonify({'employees':employees,'message':'Employees listed successfully'})
    except Exception as e:
        return jsonify({'message':'Error'})

# List One employee
@app.route("/employee/listone/<empno>",methods=['GET'])
def list_one(empno):
    try:
        cursor=connection.cursor()
        cursor.execute("SELECT empno, ename, job, sal from emp where empno='{0}'".format(empno))
        row=cursor.fetchone()
        if row!=None:
            employee ={'empno':row[0],'ename':row[1],'job':row[2],'sal':row[3]}
            return jsonify({'employee':employee,'message':'Employee found'})
        else:
            return jsonify({'message':'Employee NOT found'})
    except Exception as e:
        return jsonify({'message':'Error'})

# Register new employee
@app.route("/employee/register",methods=['POST'])
def register_employee():
    try:
        cursor=connection.cursor()
        sql="""INSERT INTO emp (empno, ename, job, mgr, hiredate, sal, comm, deptno) 
        VALUES (:n, :n, :n, :n, to_date(:n, 'yyyy-mm-dd'), :n, :n, :n)"""
        values = (request.json['empno'], request.json['ename'], request.json['job'], request.json['mgr'], 
                  request.json['hiredate'], request.json['sal'], request.json['comm'], request.json['deptno'])
        cursor.execute(sql, values)
        connection.commit()
        return jsonify({'message':'Employee has been registered'})
    except Exception as e:
        print(str(e))
        return jsonify({'message':'Error'})


# Update employee information (name, job, salary and commision)
@app.route("/employee/update/<empno>",methods=['PUT'])
def update_employee(empno):
    try:
        cursor=connection.cursor()
        sql="""UPDATE emp 
        SET ename = :n, 
            job = :n, 
            sal = :n, 
            comm = :n
        WHERE empno = :n"""
        values = (request.json['ename'], request.json['job'], request.json['sal'], request.json['comm'],empno)
        cursor.execute(sql, values)
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message':'No employee was modified with empno = {}'.format(empno)})
        else:
            return jsonify({'message':'Employee with empno = {} has been modified'.format(empno)})
    except Exception as e:
        print(str(e))
        return jsonify({'message':'Error'})


# Delete employee
@app.route("/employee/delete",methods=['DELETE'])
def delete_employee():
    try:
        cursor=connection.cursor()
        sql="""DELETE emp WHERE empno = :n"""
        values = (request.json['empno'],)
        cursor.execute(sql, values)
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message':'No employee was deleted with empno = {}'.format(request.json['empno'])})
        else:
            return jsonify({'message':'Employee with empno = {} has been deleted'.format(request.json['empno'])})
    except Exception as e:
        print(str(e))
        return jsonify({'message':'Error'})

# Page not found
def page_not_found(error):
    return "<h1>The page you are trying to access does NOT exist</h1>",404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,page_not_found)
    app.run()
