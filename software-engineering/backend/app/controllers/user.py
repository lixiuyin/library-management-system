from app.models.models import User
from app import CustomException, db

def add_user(name, gender, type_, contact, password, num_limit=0, time_limit=0, balance=0, commit_now=True):
    # 添加用户
    # name: 用户名
    # gender: 性别
    # type_: 用户类型
    # contact: 联系方式
    # balance: 余额
    # password: 密码
    # num_limit: 借阅数量限制
    # time_limit: 借阅时间限制
    # commit_now: 是否立即提交
    IDformat = {'教师': ('T',6), '研究生': ('G',6), '本科生': ('B',10), '其他': ('O',10)}
    if type_ not in IDformat:
        raise CustomException('未知用户类型')
    ID_char, ID_length = IDformat[type_]
    # user_id = ID_char+str(User.query.filter(User.user_id.like(ID_char + '%')).count() + 1).zfill(ID_length)
    
    last_user_id = User.query.order_by(User.user_id.desc()).filter(User.user_id.like(ID_char+'%')).first()
    user_id = int(last_user_id.user_id[1:])+1 if last_user_id else 1
    user_id = ID_char + str(user_id).zfill(ID_length-1)
    
    user = User(user_id=user_id, 
                name=name, 
                gender=gender, 
                type_=type_,
                num_limit=num_limit if num_limit else 0, 
                time_limit=time_limit if time_limit else 0, 
                contact=contact,
                balance=balance if balance else 0, 
                password=password 
                )
    try:
        db.session.add(user)
        if commit_now:
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return user.user_id

def get_user(user_id):
    # 获取用户信息
    # user_id: 用户编号
    return User.query.filter_by(user_id=user_id).first()

def update_user(user_id, name=None, gender=None, type_=None, contact=None, password=None, num_limit=None, time_limit=None, balance=None, commit_now=True):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise CustomException('用户不存在')
    if name is not None:
        user.name = name
    if gender is not None:
        user.gender = gender
    if type_ is not None:
        user.type_ = type_
    if contact is not None:
        user.contact = contact
    if password is not None:
        user.password = password
    if num_limit is not None:
        user.num_limit = num_limit
    if time_limit is not None:
        user.time_limit = time_limit
    if balance is not None:
        user.balance = balance
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def get_user_by_keyword(keyword='', page=1, per_page=10):
    users = User.query.filter(      User.user_id.like('%' + keyword + '%') |
                                    User.name.like('%' + keyword + '%')|
                                    User.type_.like('%' + keyword + '%')|
                                    User.contact.like('%' + keyword + '%')
                                ).paginate(page=page, per_page=per_page)
    return users

def delete_user(user_id, commit_now=True):
    # 删除用户
    # user_id: 用户编号
    # 检查用户是否存在使用记录
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        raise CustomException('用户不存在')
    try:
        db.session.query(User).filter(User.user_id == user_id).delete()
        if commit_now:
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return None