from django.shortcuts import render_to_response
from django.db import connection
from forms import *
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
import sys
import json
import hashlib
#from models import Person
# Create your views here.

def login(Request):
    msg = "Please log in !"
    if Request.method == 'POST':
        login_name = Request.POST.get('name','')
        pwd = Request.POST.get('pwd','')
        if login_name != "":
            cursor = connection.cursor()
            sql = '''SELECT person_id, `password`, role FROM `person` WHERE `name` = '%(name)s';
            '''%{"name":login_name}
            cursor.execute(sql)
            llist = cursor.fetchall()
            plist = []
            for l in llist:
                d={"id":l[0],"pwd":l[1],"role":l[2]}
                plist.append(d)
            pid = plist[0]["id"]
            role = plist[0]["role"]
            mpwd = plist[0]["pwd"]
            value = hashlib.md5(pwd).hexdigest()
            print value
            if mpwd == value:
                Request.session['pid']=pid
                Request.session['loginName']=login_name
                Request.session['role']=role
                return HttpResponseRedirect('/person/')
            else:
                msg = "Wrong password,please log in again !"
                return render_to_response('login.html',{'msg':msg})
        else:
            msg = "Please enter the login name !"
            return render_to_response('login.html',{'msg':msg})
    else:
        Request.session.clear()
        return render_to_response('login.html',{'msg':msg})

def person(Request):
    if 'loginName' in Request.session and Request.session['loginName'] != '':
        lname = Request.session['loginName']
    else:
        return HttpResponseRedirect('/login/')
    cursor = connection.cursor()
    flag = 0
    if Request.method == 'POST':
        status = Request.POST.get('position','')
        name = Request.POST.get('name','')
        department = Request.POST.get('department','')
        title = Request.POST.get('title','')
        remark = Request.POST.get('remark','')
        if status == '':
            sql='''insert into person(`name`,`password`,department,
                     title,role,`status`,remark)
                     values('%(name)s',md5('123456'),'%(department)s',
                     '%(title)s','employee','1','%(remark)s');
                '''%{'name':name,'department':department,
                 'title':title,'remark':remark}
        else:
            uid = Request.POST.get('id','')
            if uid != '':
                sql = '''update person set name='%(name)s',department='%(department)s',
                         title='%(title)s',remark='%(remark)s',`status`='%(status)s'
                         where person_id = '%(id)s';
                '''%{'id':uid,'name':name,'department':department,
                     'title':title,'remark':remark,'status':status}
            else:
                flag = 1
        if flag == 0:
            try:
                cursor.execute(sql)
            except:
                type, value, traceback = sys.exc_info()
                print value

    if 'order' in Request.GET and Request.GET['order'] and 'mission' in Request.GET and Request.GET['mission']:
        id = int(Request.GET['mission'])
        order = int(Request.GET['order'])
        sql='''select p.person_id,p.name `name`,department,title,remark,p.`status`,c.name position
                 from person p join `code` c
                 on p.`status`=c.`value`
                 join submission_to_person s
                 on p.person_id=s.person_id
                 where c.key=
                 (
	              select `value` from `code`
	              where `name`='person'
                 )
                 and s.mission_id=%(mission)d
                 and s.mission_order_id=%(order)d;
        '''%{'mission':id,'order':order}
    elif 'role' in Request.session and Request.session['role'] != '':
        role = Request.session['role']
        if role == "employee":
            pid =int(Request.session['pid'])
            sql = '''select person_id,p.name `name`,department,title,remark,p.`status`,c.name position
                from person p join `code` c
                on p.`status`=c.`value`
                where c.key=
                (
                  select `value` from `code`
                  where `name`='person'
                ) and p.person_id = %(pid)d;
            '''%{'pid':pid}
        else:
           sql='''select person_id,p.name `name`,department,title,remark,p.`status`,c.name position
                from person p join `code` c
                on p.`status`=c.`value`
                where c.key=
                (
                  select `value` from `code`
                  where `name`='person'
                );
            '''
    else:
        return HttpResponseRedirect('/login/')

    cursor.execute(sql)
    personList = cursor.fetchall()
    list = []
    for p in personList:
        d = {"id":p[0],"name":p[1],"department":p[2],"title":p[3],"remark":p[4],"position":p[6]}
        list.append(d)
    statusList = get_person_status(cursor)
    cursor.close()
    form = NewPerson()

    return render_to_response('person.html',
                                  {'personlist':list,
                                   'statuslist':statusList,
                                   'form':form,
                                   'loginName':lname})

def mission(Request):
    if 'loginName' in Request.session and Request.session['loginName'] != '':
        lname = Request.session['loginName']
    else:
        return HttpResponseRedirect('/login/')

    cursor = connection.cursor()
    flag = 0
    r = 0
    if Request.method == 'POST':
        mid = Request.POST.get('mission_id','')
        order = Request.POST.get('order','')
        if mid != '' and order == '': #add submission
            content = Request.POST.get('content','')
            remark = Request.POST.get('remark','')
            pid = Request.POST.get('person','')
            sql = '''insert into submission(mission_id,mission_order_id,`status`,content,remark)
                     select %(mid)s,ifnull(max(mission_order_id)+1,1),1,'%(content)s','%(remark)s'
                     from submission where mission_id =%(mid)s;
            '''%{"mid":mid,"content":content,"remark":remark}
            sql1 = '''insert into submission_to_person(person_id,mission_id,mission_order_id)
                      select %(pid)s,%(mid)s,ifnull(max(mission_order_id),1)
                      from submission where mission_id =%(mid)s;
            '''%{'pid':pid,'mid':mid}
            r = 1
        else:
            if mid != '' and order != '': #edit
                content = Request.POST.get('content','')
                name = Request.POST.get('name','')
                status = Request.POST.get('status','')
                mremark = Request.POST.get('mremark','')
                sremark = Request.POST.get('sremark','')
                #pid = Request.POST.get('person','')
                sql = '''update mission set mission_name = '%(name)s',
                         remark ='%(mremark)s' where mission_id = %(mid)s;
                         '''%{'mid':mid,'order':order,
                              'name':name,'mremark':mremark }

                sql1 = '''update submission set content='%(content)s',
                         remark='%(sremark)s',`status`='%(status)s'
                         where mission_id = %(mid)s
                         and mission_order_id='%(order)s';
                       '''%{'mid':mid,'order':order,'status':status,
                            'content':content,'sremark':sremark}
                r = 1
            else:
                if mid == '': #add misssion
                    name = Request.POST.get('name','')
                    remark = Request.POST.get('remark','')
                    sql='''insert into mission(mission_name,remark)
                           values('%(name)s','%(remark)s');
                        '''%{'name':name,'remark':remark}
                else:
                    flag = 1
        if flag == 0:
            try:
                cursor.execute(sql)
                if r == 1:
                    cursor.execute(sql1)
            except:
                type, value, traceback = sys.exc_info()
                print value

    if 'person' in Request.GET and Request.GET['person']:
        id = int(Request.GET['person'])
        sql='''select m.mission_id,m.mission_name,m.remark,
                ss.mission_order_id,ss.`status`,ss.content,
                ss.remark,ss.`name`
               from mission m left join (
                  select * from submission s
                  join `code` c on s.`status`=c.`value`
                  where c.`key` in(
	                select `value` from `code`
	                where `name`='submission'
                  )
               ) ss on ss.mission_id = m.mission_id
               left join submission_to_person st on
               st.mission_id= m.mission_id
               and st.mission_order_id = ss.mission_order_id
               where st.person_id = %d
               order by m.mission_id,ss.mission_order_id;
            '''% id
    elif 'role' in Request.session and Request.session['role'] != '':
        role = Request.session['role']
        if role == 'employee':
            id = int(Request.session['pid'])
            sql='''select m.mission_id,m.mission_name,m.remark,
                ss.mission_order_id,ss.`status`,ss.content,
                ss.remark,ss.`name`
               from mission m left join (
                  select * from submission s
                  join `code` c on s.`status`=c.`value`
                  where c.`key` in(
	                select `value` from `code`
	                where `name`='submission'
                  )
               ) ss on ss.mission_id = m.mission_id
               left join submission_to_person st on
               st.mission_id= m.mission_id
               and st.mission_order_id = ss.mission_order_id
               where st.person_id = %d
               order by m.mission_id,ss.mission_order_id;
            '''% id
        else:
            sql='''select m.mission_id,m.mission_name,m.remark,
                  ss.mission_order_id,ss.`status`,ss.content,ss.remark,ss.`name`
               from mission m left join (
                  select * from submission s
                  join `code` c on s.`status`=c.`value`
                  where c.`key` in(
	                select `value` from `code`
	                where `name`='submission'
                  )
                ) ss on ss.mission_id = m.mission_id
               order by m.mission_id,ss.mission_order_id;
            '''
    else:
        return HttpResponseRedirect('/login/')

    cursor.execute(sql)
    missionList = cursor.fetchall()
    list = []
    for p in missionList:
        d = {"id":p[0],"name":p[1],"remark":p[2],"order":p[3],"content":p[5],"subremark":p[6],"status":p[7]}
        list.append(d)
    sstatus = get_submission_status(cursor)
    plist = get_all_person(cursor)

    cursor.close()

    form = NewMission()
    subform = NewSubmission()

    return render_to_response('mission.html',
                              {"missionlist":list,
                               "substatus":sstatus,
                               "personList":plist,
                               "form":form,
                               "subform":subform,
                               "loginName":lname})

def daily_report(Request):
    if 'loginName' in Request.session and Request.session['loginName'] != '':
        lname = Request.session['loginName']
    else:
        return HttpResponseRedirect('/login/')

    cursor = connection.cursor()
    if Request.method == 'POST':
        date = Request.POST.get('date','')
        pid = Request.POST.get('name','')
        n = int(Request.POST.get('ordern',''))
        if date != '':

            sql = '''insert into daily_report(report_date,person_id)
                     values('%(date)s',%(pid)s)
            '''%{'date':date,'pid':pid}

            try:
                cursor.execute(sql)
            except:
                type, value, traceback = sys.exc_info()
                print value

            for i in range(1,n+1):
                content = Request.POST.get('text_'+str(n),'')
                mm_id = str(Request.POST.get('mission_'+str(n),''))
                ml = mm_id.split('_')
                m_id = int(ml[0])
                order_id = int(ml[1])
                ssql = '''insert into report_describe
                          (report_id,report_order_id,mission_id,
                          mission_order_id,content)
                          select max(report_id),%(n)d,%(m_id)d,%(order)d,'%(content)s'
                          from daily_report;
                '''%{'n':i,'m_id':m_id,'order':order_id,'content':content}
                try:
                    cursor.execute(ssql)
                except:
                    type, value, traceback = sys.exc_info()
                    print value

    if 'person' in Request.GET and Request.GET['person']:
        id = int(Request.GET['person'])
        sql='''select d.report_id,r.report_order_id,d.report_date,
	            r.content,r.mission_id,r.mission_order_id,
	            p.name,m.mission_name
	            from daily_report d join report_describe r
	            on d.report_id = r.report_id
	            join person p on p.person_id = d.person_id
	            join mission m on m.mission_id=r.mission_id
	            where p.person_id = %d
	            order by d.report_id,r.report_order_id;
	        '''%id
    else:
        if 'order' in Request.GET and Request.GET['order'] and 'mission' in Request.GET and Request.GET['mission']:
            m_id = int(Request.GET['mission'])
            o_id = int(Request.GET['order'])
            sql='''select d.report_id,r.report_order_id,d.report_date,
	                r.content,r.mission_id,r.mission_order_id,
	                p.name,m.mission_name
	                from daily_report d join report_describe r
	                on d.report_id = r.report_id
	                join person p on p.person_id = d.person_id
	                join mission m on m.mission_id=r.mission_id
	                join submission sm on sm.mission_id=r.mission_id
	                and sm.mission_order_id = r.mission_order_id
	                where r.mission_id = %(m_id)d
	                and r.mission_order_id = %(o_id)d
	                order by d.report_id,r.report_order_id;
	            '''%{'m_id':m_id,'o_id':o_id}
        else:
            if 'role' in Request.session and Request.session['role'] != '':
                role = Request.session['role']
                id = int(Request.session['pid'])
                sql='''select d.report_id,r.report_order_id,d.report_date,
	                r.content,r.mission_id,r.mission_order_id,
	                p.name,m.mission_name
	                from daily_report d join report_describe r
	                on d.report_id = r.report_id
	                join person p on p.person_id = d.person_id
	                join mission m on m.mission_id=r.mission_id
	                where p.person_id = %d
	                order by d.report_id,r.report_order_id;
	            '''%id
            else:
                sql='''select d.report_id,r.report_order_id,d.report_date,
	                r.content,r.mission_id,r.mission_order_id,
	                p.name,m.mission_name
	                from daily_report d join report_describe r
	                on d.report_id = r.report_id
	                join person p on p.person_id = d.person_id
	                join mission m on m.mission_id=r.mission_id
	                order by d.report_id,r.report_order_id;
	            '''

    cursor.execute(sql)
    reportList = cursor.fetchall()
    list = []
    for p in reportList:
        d = {"id":p[0],"date":p[2],"name":p[6],"order":p[1],"content":p[3],"missionName":p[7],"missionOrder":p[5]}
        list.append(d)

    allperson = get_all_person(cursor)
    cursor.close()

    return render_to_response('daily_report.html',{"reportlist":list,
                                                   "person":allperson,
                                                   "loginName":lname})

def load(Request):
    if 'id' in Request.GET and Request.GET['id']:
        pid = int(Request.GET['id'])
        cursor = connection.cursor()
        smissionlist = get_submission_by_person(cursor,pid)
        j = json.dumps(smissionlist)
        return HttpResponse(j)

def get_person_status(cursor):
    sql = '''select `name`,`value` from `code`
              where `key` = (
	            select `value` from `code`
	            where `key`=0 and `name`='person'
              );'''
    cursor.execute(sql)
    statuslist = cursor.fetchall()
    list = []
    for s in statuslist:
        d = {"id":s[1],"status":s[0]}
        list.append(d)
    return list

def get_person(cursor,person_id):
    sql = '''select person_id,name,department,title,`status`,remark
             from person
             where person_id = %d
    '''%person_id
    cursor.execute(sql)
    personlist = cursor.fetchall()
    list = []
    for p in personlist:
        d = {"id":p[0],"name":p[1],"department":p[2],"title":p[3],"status":p[4],"remark":p[5]}
        list.append(d)
    return list

def get_all_person(cursor):
    sql = '''select person_id,name from person
        '''
    cursor.execute(sql)
    personlist = cursor.fetchall()
    list = []
    for p in personlist:
        d = {"id":p[0],"name":p[1]}
        list.append(d)
    return list

def get_submission_by_person(cursor,person_id):
    sql='''select s.mission_id,s.mission_order_id,content
            from submission s join submission_to_person st
            on s.mission_id=st.mission_id
            and s.mission_order_id =st.mission_order_id
            where st.person_id = %d
        '''%person_id
    cursor.execute(sql)
    sublist = cursor.fetchall()
    list = []
    for p in sublist:
        d = {"m_id":p[0],"m_order":p[1],"content":p[2]}
        list.append(d)
    return list

def get_submission_status(cursor):
    sql = '''select `name`,`value` from `code`
              where `key` = (
	            select `value` from `code`
	            where `key`=0 and `name`='submission'
              );'''
    cursor.execute(sql)
    statuslist = cursor.fetchall()
    list = []
    for s in statuslist:
        d = {"id":s[1],"status":s[0]}
        list.append(d)
    return list