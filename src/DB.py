from flask import flash, Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'JEWeR6NqFE-6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:xuaokke569@127.0.0.1:3306/lab3'
db = SQLAlchemy(app)


class Course(db.Model):
    CID = db.Column(db.String(32), primary_key=True)
    CName = db.Column(db.String(128))
    CHours = db.Column(db.Integer)
    CType = db.Column(db.Integer)


class Teacher(db.Model):
    TID = db.Column(db.String(5), primary_key=True)
    TName = db.Column(db.String(32))
    TSex = db.Column(db.Integer)
    TTitle = db.Column(db.Integer)


class Project(db.Model):
    ProID = db.Column(db.String(32), primary_key=True)
    ProName = db.Column(db.String(128))
    ProSource = db.Column(db.String(128))
    ProType = db.Column(db.Integer)
    ProBudget = db.Column(db.Float)
    ProStart = db.Column(db.Integer)
    ProEnd = db.Column(db.Integer)


class Paper(db.Model):
    PaID = db.Column(db.Integer, primary_key=True)
    PaName = db.Column(db.String(128))
    PaSource = db.Column(db.String(128))
    PaDate = db.Column(db.Integer)
    PaType = db.Column(db.Integer)
    PaLevel = db.Column(db.Integer)


class TeacherPaper(db.Model):
    TID = db.Column(db.String(5), db.ForeignKey('teacher.TID'), primary_key=True)
    PaID = db.Column(db.Integer, db.ForeignKey('paper.PaID'), primary_key=True)
    TPaRanking = db.Column(db.Integer)
    TPaCA = db.Column(db.Boolean)


class TeacherCourse(db.Model):
    TID = db.Column(db.String(5), db.ForeignKey('teacher.TID'), primary_key=True)
    CID = db.Column(db.String(32), db.ForeignKey('course.CID'), primary_key=True)
    TCDate = db.Column(db.Integer, primary_key=True)
    TCTerm = db.Column(db.Integer, primary_key=True)
    TCHour = db.Column(db.Integer)


class TeacherProject(db.Model):
    TID = db.Column(db.String(5), db.ForeignKey('teacher.TID'), primary_key=True)
    ProID = db.Column(db.String(32), db.ForeignKey('project.ProID'), primary_key=True)
    TProRanking = db.Column(db.Integer)
    TProBudget = db.Column(db.Float)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/paper')
def paper():
    return render_template('paper.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/course')
def course():
    return render_template('course.html')


# 添加 paper
@app.route('/add_paper', methods=['POST'])
def add_paper():
    if request.method == 'POST':
        paper_ID = request.form['paper_ID']
        paper_name = request.form['paper_name']
        paper_source = request.form['paper_source']
        paper_date = request.form['paper_date']
        paper_type = request.form['paper_type']
        paper_level = request.form['paper_level']
        # 如果传过来的信息不完整，则返回错误信息
        if not paper_ID or not paper_name or not paper_source or not paper_date or not paper_type or not paper_level:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('paper'))
        paper_date = int(request.form['paper_date'])
        paper_type = int(request.form['paper_type'])
        paper_level = int(request.form['paper_level'])
        # 如果论文已经存在于数据库中，则返回错误信息
        if Paper.query.get(paper_ID):
            flash("Error: The paper already exists.")
            return redirect(url_for('paper'))
        # 创建一个新的 Paper 对象
        new_paper = Paper(
            PaID=paper_ID,
            PaName=paper_name,
            PaSource=paper_source,
            PaDate=paper_date,
            PaType=paper_type,
            PaLevel=paper_level
        )
        # 将新创建的 Paper 对象添加到数据库会话中
        db.session.add(new_paper)
        # 提交数据库会话
        db.session.commit()
        flash("Success: The paper has been added successfully.")
        return redirect(url_for('paper'))


# 删除论文
@app.route('/delete_paper', methods=['POST'])
def delete_paper():
    if request.method == 'POST':
        paper_ID = request.form['paper_ID']
        # 如果传过来的信息不完整，则返回错误信息
        if not paper_ID:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('paper'))
        # 根据 paper_ID 从数据库中查询对应的论文记录
        paper = Paper.query.get(paper_ID)
        # 如果论文不存在于数据库中，则返回错误信息
        if not paper:
            flash("Error: The paper does not exist.")
            return redirect(url_for('paper'))
        # 如果 teacher_paper 表中存在这个论文，则先删除 teacher_paper 表中的涉及该论文的全部记录
        while TeacherPaper.query.filter_by(PaID=paper_ID).first():
            TeacherPaper.query.filter_by(PaID=paper_ID).delete()
        # 从数据库会话中删除论文记录
        db.session.delete(paper)
        # 提交数据库会话
        db.session.commit()
        flash("Success: The paper has been deleted successfully.")
        return redirect(url_for('paper'))


# 修改论文
@app.route('/update_paper', methods=['POST'])
def update_paper():
    if request.method == 'POST':
        paper_ID = request.form['paper_ID']
        paper_name = request.form['paper_name']
        paper_source = request.form['paper_source']
        paper_date = request.form['paper_date']
        paper_type = request.form['paper_type']
        paper_level = request.form['paper_level']
        # 如果传过来的信息不完整，则返回错误信息
        if not paper_ID or not paper_name or not paper_source or not paper_date or not paper_type or not paper_level:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('paper'))
        paper_date = int(request.form['paper_date'])
        paper_type = int(request.form['paper_type'])
        paper_level = int(request.form['paper_level'])
        # 根据 paper_ID 从数据库中查询对应的论文记录
        paper = Paper.query.get(paper_ID)
        # 如果论文不存在于数据库中，则返回错误信息
        if not paper:
            flash("Error: The paper does not exist.")
            return redirect(url_for('paper'))
        # 更新论文记录
        paper.PaName = paper_name
        paper.PaSource = paper_source
        paper.PaDate = paper_date
        paper.PaType = paper_type
        paper.PaLevel = paper_level
        # 提交数据库会话
        db.session.commit()
        flash("Success: The paper has been updated successfully.")
        return redirect(url_for('paper'))


# 查询论文
@app.route('/query_paper', methods=['POST'])
def query_paper():
    if request.method == 'POST':
        paper_ID = request.form['paper_ID']
        # 如果传过来的信息不完整，则返回错误信息
        if not paper_ID:
            return jsonify({'error': 'Please enter all the fields.'})
        paper = Paper.query.get(paper_ID)
        if not paper:
            return jsonify({'error': 'The paper does not exist.'})
        paper_data = {
            'PaID': paper.PaID,
            'PaName': paper.PaName,
            'PaSource': paper.PaSource,
            'PaDate': paper.PaDate,
            'PaType': paper.PaType,
            'PaLevel': paper.PaLevel
        }
        return jsonify(paper_data)


# 添加 project
@app.route('/add_project', methods=['POST'])
def add_project():
    if request.method == 'POST':
        pro_ID = request.form['pro_ID']
        pro_name = request.form['pro_name']
        pro_source = request.form['pro_source']
        pro_type = request.form['pro_type']
        pro_budget = request.form['pro_budget']
        pro_start = request.form['pro_start']
        pro_end = request.form['pro_end']
        # 如果传过来的信息不完整，则返回错误信息
        if not pro_ID or not pro_name or not pro_source or not pro_type or not pro_budget or not pro_start or not pro_end:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('project'))
        pro_type = int(request.form['pro_type'])
        pro_budget = float(request.form['pro_budget'])
        pro_start = int(request.form['pro_start'])
        pro_end = int(request.form['pro_end'])
        # 如果已经存在于数据库中，则返回错误信息
        if Project.query.get(pro_ID):
            flash("Error: The project already exists.")
            return redirect(url_for('project'))
        # 创建一个新的 Project 对象
        new_project = Project(
            ProID=pro_ID,
            ProName=pro_name,
            ProSource=pro_source,
            ProType=pro_type,
            ProBudget=pro_budget,
            ProStart=pro_start,
            ProEnd=pro_end
        )
        # 将新创建的 Project 对象添加到数据库会话中
        db.session.add(new_project)
        # 提交数据库会话
        db.session.commit()
        flash("Success: The project has been added successfully.")
        return redirect(url_for('project'))


# 删除 project
@app.route('/delete_project', methods=['POST'])
def delete_project():
    if request.method == 'POST':
        pro_ID = request.form['pro_ID']
        # 如果传过来的信息不完整，则返回错误信息
        if not pro_ID:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('project'))
        # 根据 pro_ID 从数据库中查询对应的项目记录
        project = Project.query.get(pro_ID)
        # 如果项目不存在于数据库中，则返回错误信息
        if not project:
            flash("Error: The project does not exist.")
            return redirect(url_for('project'))
        # 如果 teacher_project 表中存在这个项目，则先删除 teacher_project 表中的涉及该项目的全部记录
        while TeacherProject.query.filter_by(ProID=pro_ID).first():
            TeacherProject.query.filter_by(ProID=pro_ID).delete()
        # 从数据库会话中删除项目记录
        db.session.delete(project)
        # 提交数据库会话
        db.session.commit()
        flash("Success: The project has been deleted successfully.")
        return redirect(url_for('project'))


# 修改 Project
@app.route('/update_project', methods=['POST'])
def update_project():
    if request.method == 'POST':
        pro_ID = request.form['pro_ID']
        pro_name = request.form['pro_name']
        pro_source = request.form['pro_source']
        pro_type = request.form['pro_type']
        pro_budget = request.form['pro_budget']
        pro_start = request.form['pro_start']
        pro_end = request.form['pro_end']
        # 如果传过来的信息不完整，则返回错误信息
        if not pro_ID or not pro_name or not pro_source or not pro_type or not pro_budget or not pro_start or not pro_end:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('project'))
        pro_type = int(request.form['pro_type'])
        pro_budget = float(request.form['pro_budget'])
        pro_start = int(request.form['pro_start'])
        pro_end = int(request.form['pro_end'])
        # 根据 pro_ID 从数据库中查询对应的项目记录
        project = Project.query.get(pro_ID)
        # 如果项目不存在于数据库中，则返回错误信息
        if not project:
            flash("Error: The project does not exist.")
            return redirect(url_for('project'))
        # 更新项目记录
        project.ProName = pro_name
        project.ProSource = pro_source
        project.ProType = pro_type
        project.ProBudget = pro_budget
        project.ProStart = pro_start
        project.ProEnd = pro_end
        # 提交数据库会话
        db.session.commit()
        flash("Success: The project has been updated successfully.")
        return redirect(url_for('project'))


# 查询 project
@app.route('/query_project', methods=['POST'])
def query_project():
    if request.method == 'POST':
        pro_ID = request.form['pro_ID']
        # 如果传过来的信息不完整，则返回错误信息
        if not pro_ID:
            return jsonify({'error': 'Please enter all the fields.'})
        # 根据 pro_ID 从数据库中查询对应的项目记录
        project = Project.query.get(pro_ID)
        # 如果项目不存在于数据库中，则返回错误信息
        if not project:
            return jsonify({'error': 'The project does not exist.'})
        # 将查询到的项目记录返回
        project_data = {
            'ProID': project.ProID,
            'ProName': project.ProName,
            'ProSource': project.ProSource,
            'ProType': project.ProType,
            'ProBudget': project.ProBudget,
            'ProStart': project.ProStart,
            'ProEnd': project.ProEnd
        }
        return jsonify(project_data)

# 添加老师和论文的关系
@app.route('/add_relation_TPa', methods=['POST'])
def add_relation_TPa():
    if request.method == 'POST':
        tid = request.form['tid']
        pid = request.form['pid']
        ranking = request.form['ranking']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid or not pid or not ranking:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('paper'))
        ranking = int(request.form['ranking'])
        ca = 'ca' in request.form
        # 检查教师和论文是否存在
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            flash("Error: The teacher does not exist.")
            return redirect(url_for('paper'))
        existing_paper = Paper.query.get(pid)
        if existing_paper is None:
            flash("Error: The paper does not exist.")
            return redirect(url_for('paper'))
        # 检查是否已经存在相同的教师和论文关系
        existing_relation = TeacherPaper.query.filter_by(TID=tid, PaID=pid).first()
        if existing_relation is not None:
            flash("Error: The teacher-paper relation already exists.")
            return redirect(url_for('paper'))
        # 检查是否已经有通讯作者
        if ca:
            existing_ca = TeacherPaper.query.filter_by(PaID=pid, TPaCA=True).first()
            if existing_ca is not None:
                flash("Error: The paper already has a corresponding author.")
                return redirect(url_for('paper'))
        # 检查是否已经有相同的作者排名
        existing_ranking = TeacherPaper.query.filter_by(PaID=pid, TPaRanking=ranking).first()
        if existing_ranking is not None:
            flash("Error: The author ranking is already taken.")
            return redirect(url_for('paper'))
        # 如果所有检查都通过，创建新的关系并保存到数据库
        new_relation = TeacherPaper(
            TID=tid,
            PaID=pid,
            TPaRanking=ranking,
            TPaCA=ca
        )
        db.session.add(new_relation)
        db.session.commit()
        flash("Success: The teacher-paper relation has been added successfully.")
        return redirect(url_for('paper'))


# 删除老师和论文的关系
@app.route('/delete_relation_TPa', methods=['POST'])
def delete_relation_TPa():
    if request.method == 'POST':
        tid = request.form['tid']
        pid = request.form['pid']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid or not pid:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('paper'))
        # 检查教师和论文是否存在
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            flash("Error: The teacher does not exist.")
            return redirect(url_for('paper'))
        existing_paper = Paper.query.get(pid)
        if existing_paper is None:
            flash("Error: The paper does not exist.")
            return redirect(url_for('paper'))
        # 检查是否存在相同的教师和论文关系
        existing_relation = TeacherPaper.query.filter_by(TID=tid, PaID=pid).first()
        if existing_relation is None:
            flash("Error: The teacher-paper relation does not exist.")
            return redirect(url_for('paper'))
        # 如果所有检查都通过，删除关系并保存到数据库
        db.session.delete(existing_relation)
        db.session.commit()
        flash("Success: The teacher-paper relation has been deleted successfully.")
        return redirect(url_for('paper'))


# 更改teacher和paper的关系
@app.route('/update_relation_TPa', methods=['POST'])
def update_relation_TPa():
    if request.method == 'POST':
        tid = request.form['tid']
        pid = request.form['pid']
        ranking = request.form['ranking']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid or not pid or not ranking:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('paper'))
        ranking = int(request.form['ranking'])
        ca = 'ca' in request.form
        # 检查教师和论文是否存在
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            flash("Error: The teacher does not exist.")
            return redirect(url_for('paper'))
        existing_paper = Paper.query.get(pid)
        if existing_paper is None:
            flash("Error: The paper does not exist.")
            return redirect(url_for('paper'))
        # 检查是否存在教师和论文关系
        existing_relation = TeacherPaper.query.filter_by(TID=tid, PaID=pid).first()
        if existing_relation is None:
            flash("Error: The teacher-paper relation does not exist.")
            return redirect(url_for('paper'))
        # 检查是否发生更改
        if existing_relation.TPaRanking == ranking and existing_relation.TPaCA == ca:
            flash("Error: Nothing changed.")
            return redirect(url_for('paper'))
        # 检查是否已经有通讯作者，并且该通讯作者不是当前要修改的老师
        if ca:
            existing_ca = TeacherPaper.query.filter_by(PaID=pid, TPaCA=True).first()
            if existing_ca is not None and existing_ca.TID != tid:
                flash("Error: The paper already has a corresponding author.")
                return redirect(url_for('paper'))
        # 检查是否已经有相同的作者排名，并且该排名不是当前要求改的老师的原有的排名
        existing_ranking = TeacherPaper.query.filter_by(PaID=pid, TPaRanking=ranking).first()
        if existing_ranking is not None and existing_ranking.TID != tid:
            flash("Error: The author ranking is already taken.")
            return redirect(url_for('paper'))
        # 如果所有检查都通过，修改关系并保存到数据库
        existing_relation.TPaRanking = ranking
        existing_relation.TPaCA = ca
        db.session.commit()
        flash("Success: The teacher-paper relation has been updated successfully.")
        return redirect(url_for('paper'))


# 根据teacher ID查询paper
@app.route('/search_paper_by_tid', methods=['POST'])
def search_paper_by_tid():
    if request.method == 'POST':
        tid = request.form['tid']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid:
            return jsonify({'error': 'Please enter all the fields.'})
        # 如果对应的老师不存在，则返回错误信息
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            return jsonify({'error': 'The teacher does not exist.'})
        # 如果该老师没有论文记录，则返回错误信息
        existing_teacher_paper = TeacherPaper.query.filter_by(TID=tid).first()
        if existing_teacher_paper is None:
            return jsonify({'error': 'The teacher does not have any paper.'})
        # 如果所有检查都通过，查询该老师的所有论文
        # 首先，在 TeacherPaper 表中查询该老师的所有论文的 paper ID
        paper_ids = TeacherPaper.query.filter_by(TID=tid).with_entities(TeacherPaper.PaID).all()
        paper_ids = [id[0] for id in paper_ids]
        # 然后，在 Paper 表中查询所有论文的信息
        papers = Paper.query.filter(Paper.PaID.in_(paper_ids)).all()
        # 再在 TeacherPaper 表中根据tid和pid查询对应的排名和是否为通讯作者，返回所有结果
        paper_data = [{
            'PaID': paper.PaID,
            'PaName': paper.PaName,
            'PaSource': paper.PaSource,
            'PaDate': paper.PaDate,
            'PaType': paper.PaType,
            'PaLevel': paper.PaLevel,
            'TPaRanking': TeacherPaper.query.filter_by(TID=tid, PaID=paper.PaID).first().TPaRanking,
            'TPaCA': TeacherPaper.query.filter_by(TID=tid, PaID=paper.PaID).first().TPaCA
        } for paper in papers]

        return jsonify(paper_data)


# 添加teacher和project的关系
@app.route('/add_relation_TPj', methods=['POST'])
def add_relation_TPj():
    if request.method == 'POST':
        tid = request.form['tid']
        pid = request.form['pid']
        ranking = request.form['ranking']
        budget = request.form['budget']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid or not pid or not ranking or not budget:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('project'))
        ranking = int(request.form['ranking'])
        budget = float(request.form['budget'])
        # 检查教师和项目是否存在
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            flash("Error: The teacher does not exist.")
            return redirect(url_for('project'))
        existing_project = Project.query.get(pid)
        if existing_project is None:
            flash("Error: The project does not exist.")
            return redirect(url_for('project'))
        # 检查是否已经存在相同的教师和项目关系
        existing_relation = TeacherProject.query.filter_by(TID=tid, ProID=pid).first()
        if existing_relation is not None:
            flash("Error: The teacher-project relation already exists.")
            return redirect(url_for('project'))
        # 检查是否已经有相同的项目排名
        existing_ranking = TeacherProject.query.filter_by(ProID=pid, TProRanking=ranking).first()
        if existing_ranking is not None:
            flash("Error: The project ranking is already taken.")
            return redirect(url_for('project'))
        # 如果所有检查都通过，创建新的关系并保存到数据库
        new_relation = TeacherProject(
            TID=tid,
            ProID=pid,
            TProRanking=ranking,
            TProBudget=budget
        )
        db.session.add(new_relation)
        db.session.commit()
        flash("Success: The teacher-project relation has been added successfully.")
        return redirect(url_for('project'))


# 删除老师和项目的关系
@app.route('/delete_relation_TPj', methods=['POST'])
def delete_relation_TPj():
    if request.method == 'POST':
        tid = request.form['tid']
        pid = request.form['pid']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid or not pid:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('project'))
        # 检查教师和项目是否存在
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            flash("Error: The teacher does not exist.")
            return redirect(url_for('project'))
        existing_project = Project.query.get(pid)
        if existing_project is None:
            flash("Error: The project does not exist.")
            return redirect(url_for('project'))
        # 检查是否存在相同的教师和项目关系
        existing_relation = TeacherProject.query.filter_by(TID=tid, ProID=pid).first()
        if existing_relation is None:
            flash("Error: The teacher-project relation does not exist.")
            return redirect(url_for('project'))
        # 如果所有检查都通过，删除关系并保存到数据库
        db.session.delete(existing_relation)
        db.session.commit()
        flash("Success: The teacher-project relation has been deleted successfully.")
        return redirect(url_for('project'))


# 修改老师和项目的关系
@app.route('/update_relation_TPj', methods=['POST'])
def update_relation_TPj():
    if request.method == 'POST':
        tid = request.form['tid']
        pid = request.form['pid']
        ranking = request.form['ranking']
        budget = request.form['budget']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid or not pid or not ranking or not budget:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('project'))
        ranking = int(request.form['ranking'])
        budget = float(request.form['budget'])
        # 检查教师和项目是否存在
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            flash("Error: The teacher does not exist.")
            return redirect(url_for('project'))
        existing_project = Project.query.get(pid)
        if existing_project is None:
            flash("Error: The project does not exist.")
            return redirect(url_for('project'))
        # 检查是否存在教师和项目关系
        existing_relation = TeacherProject.query.filter_by(TID=tid, ProID=pid).first()
        if existing_relation is None:
            flash("Error: The teacher-project relation does not exist.")
            return redirect(url_for('project'))
        # 检查是否发生更改
        if existing_relation.TProRanking == ranking and existing_relation.TProBudget == budget:
            flash("Error: Nothing changed.")
            return redirect(url_for('project'))
        # 检查是否已经有相同的项目排名，并且该排名不是当前要求改的老师的原有的排名
        existing_ranking = TeacherProject.query.filter_by(ProID=pid, TProRanking=ranking).first()
        if existing_ranking is not None and existing_ranking.TID != tid:
            flash("Error: The project ranking is already taken.")
            return redirect(url_for('project'))
        # 如果所有检查都通过，修改关系并保存到数据库
        existing_relation.TProRanking = ranking
        existing_relation.TProBudget = budget
        db.session.commit()
        flash("Success: The teacher-project relation has been updated successfully.")
        return redirect(url_for('project'))


# 根据teacher ID查询project
@app.route('/search_project_by_tid', methods=['POST'])
def search_project_by_tid():
    if request.method == 'POST':
        tid = request.form['tid']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid:
            return jsonify({'error': 'Please enter all the fields.'})
        # 如果对应的老师不存在，则返回错误信息
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            return jsonify({'error': 'The teacher does not exist.'})
        # 如果该老师没有项目记录，则返回错误信息
        existing_teacher_project = TeacherProject.query.filter_by(TID=tid).first()
        if existing_teacher_project is None:
            return jsonify({'error': 'The teacher does not have any project.'})
        # 如果所有检查都通过，查询该老师的所有项目
        # 首先，在 TeacherProject 表中查询该老师的所有项目的 project ID
        project_ids = TeacherProject.query.filter_by(TID=tid).with_entities(TeacherProject.ProID).all()
        project_ids = [id[0] for id in project_ids]
        # 然后，在 Project 表中查询所有项目的信息
        projects = Project.query.filter(Project.ProID.in_(project_ids)).all()
        # 再在 TeacherProject 表中根据tid和pid查询对应的排名和预算，返回所有结果
        project_data = [{
            'ProID': project.ProID,
            'ProName': project.ProName,
            'ProSource': project.ProSource,
            'ProType': project.ProType,
            'ProBudget': project.ProBudget,
            'ProStart': project.ProStart,
            'ProEnd': project.ProEnd,
            'TProRanking': TeacherProject.query.filter_by(TID=tid, ProID=project.ProID).first().TProRanking,
            'TProBudget': TeacherProject.query.filter_by(TID=tid, ProID=project.ProID).first().TProBudget
        } for project in projects]

        return jsonify(project_data)


# 添加老师和课程的关系
@app.route('/add_relation_TC', methods=['POST'])
def add_relation_TC():
    if request.method == 'POST':
        tid = request.form['tid']
        cid = request.form['cid']
        date = request.form['date']
        term = request.form['term']
        hour = request.form['hour']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid or not cid or not date or not term or not hour:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('course'))
        date = int(request.form['date'])
        term = int(request.form['term'])
        hour = int(request.form['hour'])
        # 检查教师和课程是否存在
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            flash("Error: The teacher does not exist.")
            return redirect(url_for('course'))
        existing_course = Course.query.get(cid)
        if existing_course is None:
            flash("Error: The course does not exist.")
            return redirect(url_for('course'))
        # 检查该老师该学年该学期是否已经上了这门课
        existing_relation = TeacherCourse.query.filter_by(TID=tid, CID=cid, TCDate=date, TCTerm=term).first()
        if existing_relation is not None:
            flash("Error: The teacher has already taught this course in this term.")
            return redirect(url_for('course'))
        # 如果所有检查都通过，创建新的关系并保存到数据库
        new_relation = TeacherCourse(
            TID=tid,
            CID=cid,
            TCDate=date,
            TCTerm=term,
            TCHour=hour
        )
        db.session.add(new_relation)
        db.session.commit()
        flash("Success: The teacher-course relation has been added successfully.")
        return redirect(url_for('course'))


# 删除老师和课程的关系
@app.route('/delete_relation_TC', methods=['POST'])
def delete_relation_TC():
    if request.method == 'POST':
        tid = request.form['tid']
        cid = request.form['cid']
        date = request.form['date']
        term = request.form['term']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid or not cid or not date or not term:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('course'))
        date = int(request.form['date'])
        term = int(request.form['term'])
        # 检查教师和课程是否存在
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            flash("Error: The teacher does not exist.")
            return redirect(url_for('course'))
        existing_course = Course.query.get(cid)
        if existing_course is None:
            flash("Error: The course does not exist.")
            return redirect(url_for('course'))
        # 检查是否存在相同的教师和课程关系
        existing_relation = TeacherCourse.query.filter_by(TID=tid, CID=cid, TCDate=date, TCTerm=term).first()
        if existing_relation is None:
            flash("Error: The teacher-course relation does not exist.")
            return redirect(url_for('course'))
        # 如果所有检查都通过，删除关系并保存到数据库
        db.session.delete(existing_relation)
        db.session.commit()
        flash("Success: The teacher-course relation has been deleted successfully.")
        return redirect(url_for('course'))


# 修改老师和课程的关系，这里只会修改课时数目 Hour
@app.route('/update_relation_TC', methods=['POST'])
def update_relation_TC():
    if request.method == 'POST':
        tid = request.form['tid']
        cid = request.form['cid']
        date = request.form['date']
        term = request.form['term']
        hour = request.form['hour']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid or not cid or not date or not term or not hour:
            flash("Error: Please enter all the fields.")
            return redirect(url_for('course'))
        date = int(request.form['date'])
        term = int(request.form['term'])
        hour = int(request.form['hour'])
        # 检查教师和课程是否存在
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            flash("Error: The teacher does not exist.")
            return redirect(url_for('course'))
        existing_course = Course.query.get(cid)
        if existing_course is None:
            flash("Error: The course does not exist.")
            return redirect(url_for('course'))
        # 检查是否存在该教师和课程关系
        existing_relation = TeacherCourse.query.filter_by(TID=tid, CID=cid, TCDate=date, TCTerm=term).first()
        if existing_relation is None:
            flash("Error: The teacher-course relation does not exist.")
            return redirect(url_for('course'))
        # 检查是否发生更改
        if existing_relation.TCHour == hour:
            flash("Error: Nothing changed.")
            return redirect(url_for('course'))
        # 如果所有检查都通过，修改关系并保存到数据库
        existing_relation.TCDate = date
        existing_relation.TCTerm = term
        existing_relation.TCHour = hour
        db.session.commit()
        flash("Success: The teacher-course relation has been updated successfully.")
        return redirect(url_for('course'))


# 根据teacher ID查询course
@app.route('/search_course_by_tid', methods=['POST'])
def search_course_by_tid():
    if request.method == 'POST':
        tid = request.form['tid']
        # 如果传过来的信息不完整，则返回错误信息
        if not tid:
            return jsonify({'error': 'Please enter all the fields.'})
        # 如果对应的老师不存在，则返回错误信息
        existing_teacher = Teacher.query.get(tid)
        if existing_teacher is None:
            return jsonify({'error': 'The teacher does not exist.'})
        # 如果该老师没有课程记录，则返回错误信息
        existing_teacher_course = TeacherCourse.query.filter_by(TID=tid).first()
        if existing_teacher_course is None:
            return jsonify({'error': 'The teacher does not have any course.'})
        # 如果所有检查都通过，查询该老师的所有课程
        # 首先，在 TeacherCourse 表中查询该老师的所有课程的 course ID
        course_ids = TeacherCourse.query.filter_by(TID=tid).with_entities(TeacherCourse.CID).all()
        course_ids = [id[0] for id in course_ids]
        # 然后，在 Course 表中查询所有课程的信息
        courses = Course.query.filter(Course.CID.in_(course_ids)).all()
        # 再在 TeacherCourse 表中根据tid和cid查询对应的课时数目，返回所有结果
        course_data = [{
            'CID': course.CID,
            'CName': course.CName,
            'CHours': course.CHours,
            'CType': course.CType,
            'TCDate': TeacherCourse.query.filter_by(TID=tid, CID=course.CID).first().TCDate,
            'TCTerm': TeacherCourse.query.filter_by(TID=tid, CID=course.CID).first().TCTerm,
            'TCHour': TeacherCourse.query.filter_by(TID=tid, CID=course.CID).first().TCHour
        } for course in courses]

        return jsonify(course_data)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
