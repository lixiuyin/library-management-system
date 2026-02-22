"""
种子数据初始化脚本：插入图书分类、超级管理员、测试管理员、测试用户、测试图书、
借阅记录、充值/扣款记录、管理员操作记录。
用法：uv run python seed.py          # 仅插入种子数据
      uv run python seed.py --test   # 插入种子数据后运行完整性约束测试
      可重复执行，已有数据会跳过。
"""
import sys
from datetime import date, datetime, timedelta

from sqlalchemy.exc import IntegrityError, DataError

from app import app, db
from app.models.models import (
    Book_category,
    Admin_info,
    User,
    Book_info,
    Borrow_info,
    Historical_borrowInfo,
    Recharge_deduction_record,
    Admin_operation_record,
)

# ---------------------------------------------------------------------------
# 图书分类（中图法简表）
# ---------------------------------------------------------------------------
CATEGORIES = [
    ('A', '马克思主义、列宁主义、毛泽东思想、邓小平理论'),
    ('B', '哲学、宗教'),
    ('C', '社会科学总论'),
    ('D', '政治、法律'),
    ('E', '军事'),
    ('F', '经济'),
    ('G', '文化、科学、教育、体育'),
    ('H', '语言、文字'),
    ('I', '文学'),
    ('J', '艺术'),
    ('K', '历史、地理'),
    ('N', '自然科学总论'),
    ('O', '数理科学和化学'),
    ('P', '天文学、地球科学'),
    ('Q', '生物科学'),
    ('R', '医药、卫生'),
    ('S', '农业科学'),
    ('T', '工业技术'),
    ('U', '交通运输'),
    ('V', '航空、航天'),
    ('X', '环境科学、安全科学'),
    ('Z', '综合性图书'),
    ('TP', '自动化技术、计算机技术'),
]

# ---------------------------------------------------------------------------
# 管理员：(admin_id, password)，密码 5–20 位
# ---------------------------------------------------------------------------
SUPER_ADMIN = ('S00001', 'admin12345')
ADMINS = [
    ('A00001', 'admin12345'),
    ('A00002', 'manager123'),
]

# ---------------------------------------------------------------------------
# 用户： (user_id, name, gender, type_, contact, password)
# user_id：教师/研究生 6 位（T/G+5 位），本科生/其他 10 位（B/O+9 位）
# ---------------------------------------------------------------------------
USERS = [
    ('T00001', '张三', '男', '教师', '13800000001', 'password01'),
    ('T00002', '李梅', '女', '教师', '13800000002', 'password02'),
    ('G00001', '王研', '男', '研究生', '13900000001', 'password03'),
    ('G00002', '刘芳', '女', '研究生', '13900000002', 'password04'),
    ('B000000001', '赵明', '男', '本科生', '13700000001', 'password05'),
    ('B000000002', '孙丽', '女', '本科生', '13700000002', 'password06'),
    ('B000000003', '周杰', '男', '本科生', '13700000003', 'password07'),
    ('O000000001', '钱七', '男', '其他', '13600000001', 'password08'),
    ('O000000002', '吴静', '女', '其他', '13600000002', 'password09'),
]

# ---------------------------------------------------------------------------
# 图书：(category_code, isbn, title, author, publisher, publish_date, price,
#       intro)。isbn 为 10 位或 13 位数字
# ---------------------------------------------------------------------------
BOOKS = [
    # 计算机类 TP
    ('TP', 9787111213826, '深入理解计算机系统', 'Randal E.Bryant', '机械工业出版社',
     date(2016, 11, 1), 139.00, '从程序员视角阐述计算机系统本质概念'),
    ('TP', 9787115546081, '算法导论', 'Thomas H.Cormen', '人民邮电出版社',
     date(2022, 12, 1), 128.00, '算法领域经典教材'),
    ('TP', 9787111641247, '计算机网络：自顶向下方法', 'James F.Kurose', '机械工业出版社',
     date(2021, 5, 1), 89.00, '自顶向下方法讲授计算机网络'),
    ('TP', 9787302423287, '数据库系统概论', '王珊', '高等教育出版社',
     date(2014, 9, 1), 39.20, '国内数据库经典教材'),
    ('TP', 9787115428028, 'Python编程：从入门到实践', 'Eric Matthes', '人民邮电出版社',
     date(2020, 10, 1), 89.00, 'Python 入门经典教程'),
    ('TP', 9780134685991, 'Effective Java 中文版', 'Joshua Bloch', '机械工业出版社',
     date(2018, 12, 1), 79.00, 'Java 编程最佳实践'),
    ('TP', 9787115459527, '流畅的Python', 'Luciano Ramalho', '人民邮电出版社',
     date(2017, 5, 1), 139.00, 'Python 进阶必读'),
    # 文学 I
    ('I', 9787020002078, '红楼梦', '曹雪芹', '人民文学出版社',
     date(2008, 7, 1), 59.70, '中国古典四大名著之一'),
    ('I', 9787544270878, '百年孤独', '加西亚·马尔克斯', '南海出版公司',
     date(2011, 6, 1), 39.50, '魔幻现实主义代表作'),
    ('I', 9787020042524, '围城', '钱钟书', '人民文学出版社',
     date(1991, 2, 1), 36.00, '中国现代长篇小说经典'),
    ('I', 9787532765793, '活着', '余华', '作家出版社',
     date(2012, 8, 1), 20.00, '当代文学经典'),
    # 数理 O（10 位 ISBN 示例）
    ('O', 7040396638, '高等数学（第七版）上册', '同济大学', '高等教育出版社',
     date(2014, 7, 1), 34.40, '理工科经典高数教材'),
    ('O', 9787040396638, '高等数学（第七版）下册', '同济大学', '高等教育出版社',
     date(2014, 7, 1), 32.90, '理工科经典高数教材'),
    # 经济 F
    ('F', 9787111267638, '经济学原理', 'N.格里高利·曼昆', '机械工业出版社',
     date(2020, 6, 1), 88.00, '经济学入门经典教科书'),
    ('F', 9787208061644, '穷查理宝典', '彼得·考夫曼', '上海人民出版社',
     date(2010, 10, 1), 88.00, '查理·芒格智慧箴言录'),
    # 语言 H
    ('H', 9787560013466, '大学英语综合教程1', '李荫华', '上海外语教育出版社',
     date(2015, 1, 1), 46.90, '大学英语核心教材'),
    ('H', 9787560026602, '新概念英语2', 'L.G.Alexander', '外语教学与研究',
     date(1997, 10, 1), 29.90, '经典英语学习教材'),
    # 其他
    ('D', 9787010049922, '毛泽东选集 第一卷', '毛泽东', '人民出版社',
     date(1991, 6, 1), 45.00, '毛泽东思想重要著作'),
    ('K', 9787101003048, '史记', '司马迁', '中华书局',
     date(2013, 8, 1), 128.00, '二十四史之首'),
    ('R', 9787117267222, '内科学（第9版）', '葛均波 徐永健', '人民卫生出版社',
     date(2018, 7, 1), 98.00, '临床医学本科教材'),
]


def _ensure_user(uid, name, gender, type_, contact, password, balance=100.00):
    """若用户不存在则插入。返回该用户。"""
    u = db.session.get(User, uid)
    if u:
        return u
    type_limits = {
        '教师': (5, 60), '研究生': (3, 30), '本科生': (3, 30), '其他': (3, 30),
    }
    num_limit, time_limit = type_limits.get(type_, (3, 30))
    u = User(
        user_id=uid,
        name=name,
        gender=gender,
        type_=type_,
        num_limit=num_limit,
        time_limit=time_limit,
        contact=contact,
        balance=balance,
        password=password,
    )
    db.session.add(u)
    db.session.commit()
    return u


def _ensure_book(cat, isbn, title, author, pub, pub_date, price, intro, status='在馆'):
    """若该书（按 isbn）不存在则插入。返回 (book, created)。"""
    existing = Book_info.query.filter_by(isbn=isbn).first()
    if existing:
        return existing, False
    book = Book_info(
        category_code=cat,
        isbn=isbn,
        title=title,
        author=author,
        publisher=pub,
        publish_date=pub_date,
        price=price,
        intro=intro,
        status=status,
    )
    db.session.add(book)
    db.session.commit()
    return book, True


def seed():
    with app.app_context():
        print('[seed] 开始插入种子数据...')

        # --- 图书分类 ---
        added = 0
        for code, name in CATEGORIES:
            if not db.session.get(Book_category, code):
                db.session.add(Book_category(code=code, name=name))
                added += 1
        db.session.commit()
        print(f'  图书分类：新增 {added} 条，共 {len(CATEGORIES)} 条')

        # --- 超级管理员 ---
        sid, spwd = SUPER_ADMIN
        if not db.session.get(Admin_info, sid):
            db.session.add(Admin_info(admin_id=sid, password=spwd))
            db.session.commit()
            print(f'  超级管理员：{sid}（密码 {spwd}）')
        else:
            print(f'  超级管理员：{sid} 已存在，跳过')

        # --- 普通管理员 ---
        for aid, apwd in ADMINS:
            if not db.session.get(Admin_info, aid):
                db.session.add(Admin_info(admin_id=aid, password=apwd))
                db.session.commit()
                print(f'  管理员：{aid}（密码 {apwd}）')
            else:
                print(f'  管理员：{aid} 已存在，跳过')

        # --- 用户（固定 user_id）---
        user_list = []
        for uid, name, gender, type_, contact, password in USERS:
            u = db.session.get(User, uid)
            if not u:
                _ensure_user(uid, name, gender, type_, contact, password)
                print(f'  用户：{uid} {name}（{type_}，密码 {password}）')
            else:
                print(f'  用户：{uid} 已存在，跳过')
            user_list.append(uid)

        # --- 图书 ---
        book_ids = []
        for cat, isbn, title, author, pub, pub_date, price, intro in BOOKS:
            book, created = _ensure_book(cat, isbn, title, author, pub, pub_date, price, intro)
            book_ids.append(book.book_id)
            if created:
                print(f'  图书：《{title}》（book_id={book.book_id}）')
            else:
                print(f'  图书：《{title}》已存在（book_id={book.book_id}），'
                      '跳过')

        today = date.today()

        # --- 当前借阅（多本书、多用户）---
        borrow_data = [
            (book_ids[0], user_list[0], today - timedelta(days=10), today + timedelta(days=20)),
            (book_ids[1], user_list[1], today - timedelta(days=5), today + timedelta(days=25)),
            (book_ids[2], user_list[2], today - timedelta(days=3), today + timedelta(days=27)),
            (book_ids[4], user_list[3], today - timedelta(days=1), today + timedelta(days=29)),
            (book_ids[7], user_list[4], today - timedelta(days=15), today + timedelta(days=15)),
        ]
        for bid, uid, borrow_dt, due_dt in borrow_data:
            if Borrow_info.query.filter_by(book_id=bid, user_id=uid).first():
                print(f'  借阅：book_id={bid} -> {uid} 已存在，跳过')
                continue
            book = db.session.get(Book_info, bid)
            if book and book.status == '在馆':
                book.status = '借出'
                db.session.add(Borrow_info(
                    book_id=bid, user_id=uid,
                    borrow_date=borrow_dt, due_date=due_dt,
                ))
                db.session.commit()
                print(f'  借阅：book_id={bid} -> {uid}（到期 {due_dt}）')
            else:
                print(f'  借阅：book_id={bid} 不在馆或已借出，跳过')

        # --- 历史借阅（多条）---
        historical_data = [
            (book_ids[3], user_list[5],
             today - timedelta(days=30), today - timedelta(days=5), today - timedelta(days=3)),
            (book_ids[5], user_list[6],
             today - timedelta(days=60), today - timedelta(days=40), today - timedelta(days=38)),
            (book_ids[8], user_list[7],
             today - timedelta(days=20), today - timedelta(days=2), today),
        ]
        for bid, uid, borrow_dt, due_dt, return_dt in historical_data:
            if Historical_borrowInfo.query.filter_by(book_id=bid, user_id=uid).first():
                print(f'  历史借阅：book_id={bid} -> {uid} 已存在，跳过')
                continue
            db.session.add(Historical_borrowInfo(
                book_id=bid, user_id=uid,
                borrow_date=borrow_dt, due_date=due_dt, return_date=return_dt,
            ))
            db.session.commit()
            print(f'  历史借阅：book_id={bid} -> {uid}（已归还 {return_dt}）')

        # --- 充值/扣款记录 ---
        recharge_data = [
            (user_list[0], 'A00001', 200.00, today - timedelta(days=5),
             '开学充值'),
            (user_list[1], 'A00001', 100.00, today - timedelta(days=3), '充值'),
            (user_list[4], 'A00002', -50.00, today - timedelta(days=2),
             '逾期扣款'),
            (user_list[2], 'A00001', 50.00, today - timedelta(days=1), '补缴'),
        ]
        for uid, admin_id, value, d, reason in recharge_data:
            existing = Recharge_deduction_record.query.filter_by(
                user_id=uid, admin_id=admin_id, date=d, value=value
            ).first()
            if not existing:
                db.session.add(Recharge_deduction_record(
                    user_id=uid, admin_id=admin_id, value=value, date=d,
                    reason=reason,
                ))
                db.session.commit()
                print(f'  充值/扣款：{uid} {value:+.2f}（{reason}）')
            else:
                print(f'  充值/扣款：{uid} {value:+.2f} 已存在，跳过')

        # --- 管理员操作记录 ---
        now = datetime.now()
        operation_data = [
            ('A00001', user_list[0], None, '借书',
             '读者借阅《深入理解计算机系统》'),
            ('A00001', user_list[4], None, '扣款', '逾期扣款 50 元'),
            ('S00001', None, 'A00002', '添加管理员', '新增普通管理员 A00002'),
        ]
        for admin_id, aff_uid, aff_aid, content, reason in operation_data:
            existing = Admin_operation_record.query.filter_by(
                admin_id=admin_id, content=content, reason=reason,
            ).first()
            if not existing:
                db.session.add(Admin_operation_record(
                    admin_id=admin_id,
                    affected_user_id=aff_uid,
                    affected_admin_id=aff_aid,
                    date_time=now,
                    content=content,
                    reason=reason,
                ))
                db.session.commit()
                print(f'  操作记录：{admin_id} - {content}')
            else:
                print(f'  操作记录：{content} 已存在，跳过')

        print('[seed] 种子数据插入完成！')
        print()
        print('=== 测试账号汇总 ===')
        print(f'  超级管理员：{SUPER_ADMIN[0]} / {SUPER_ADMIN[1]}')
        for aid, apwd in ADMINS:
            print(f'  管理员：    {aid} / {apwd}')
        for uid, name, _, type_, _, password in USERS:
            print(f'  {type_}：    {uid} / {password}  （{name}）')


# ---------------------------------------------------------------------------
# 完整性约束测试：期望违反约束时抛出 IntegrityError 或 DataError
# ---------------------------------------------------------------------------
def test_constraints():
    """测试数据库中各类完整性约束（CHECK、FK、唯一等）。"""
    with app.app_context():
        print('\n[test] 开始完整性约束测试...')
        passed = 0
        failed = 0
        today = date.today()
        user_list = [u.user_id for u in User.query.all()[:1]]
        book_ids = [b.book_id for b in Book_info.query.all()[:1]]

        def expect_fail(name, fn):
            nonlocal passed, failed
            try:
                fn()
                db.session.rollback()
                print(f'  [FAIL] {name}: 期望违反约束，但提交成功')
                failed += 1
            except (IntegrityError, DataError):
                db.session.rollback()
                print(f'  [OK]   {name}')
                passed += 1
            except Exception:
                db.session.rollback()
                print(f'  [OK]   {name}')
                passed += 1

        # ----- User -----
        def u(uid, g, t, c, p, b):  # noqa: E741
            return _commit_user(uid, '测', g, t, c, p, b)

        expect_fail('User: gender 非法', lambda: u('T00099', 'X', '教师',
                                                   '13800000099', 'password99', 0))
        expect_fail('User: type 非法', lambda: u('T00099', '男', '学生',
                                                 '13800000099', 'password99', 0))
        expect_fail('User: balance 负数', lambda: u('T00099', '男', '教师',
                                                     '13800000099', 'password99', -1))
        expect_fail('User: password 过短', lambda: u('T00099', '男', '教师',
                                                     '13800000099', 'short1', 0))
        expect_fail('User: password 过长', lambda: u('T00099', '男', '教师',
                                                     '13800000099', 'a' * 21, 0))
        expect_fail('User: user_id 长度非法', lambda: u('T1234', '男', '教师',
                                                        '13800000099', 'password99', 0))
        expect_fail('User: 教师应为 6 位 id', lambda: u('B000000099', '男', '教师',
                                                       '13800000099', 'password99', 0))
        expect_fail('User: 本科生应为 10 位 id', lambda: u('B000099', '男', '本科生',
                                                           '13800000099', 'password99', 0))

        # ----- Book_category -----
        expect_fail('Book_category: 主键重复',
                    lambda: _commit_category('A', '重复A'))

        # ----- Book_info -----
        def b(c, i, s='在馆'):
            return _commit_book(c, i, '测', '作', '出', None, 0, None, status=s)

        expect_fail('Book_info: category_code 外键不存在',
                    lambda: b('XX', 9780000000001))
        expect_fail('Book_info: ISBN 长度非法', lambda: b('A', 123456789))
        expect_fail('Book_info: price 负数',
                    lambda: _commit_book('A', 9780000000001, '测', '作', '出',
                                         None, -1, None))
        expect_fail('Book_info: status 非法', lambda: b('A', 9780000000001, '未知'))

        # ----- Borrow_info / Historical_borrowInfo：外键 -----
        if user_list and book_ids:
            expect_fail('Borrow_info: book_id 不存在',
                        lambda: _commit_borrow(999999, user_list[0], today,
                                                today + timedelta(days=30)))
            expect_fail('Borrow_info: user_id 不存在',
                        lambda: _commit_borrow(book_ids[0], 'X99999', today,
                                                today + timedelta(days=30)))
            expect_fail('Historical_borrowInfo: user_id 不存在',
                        lambda: _commit_historical(
                            book_ids[0], 'X99999',
                            today - timedelta(days=10), today, today))

        # ----- Admin_info -----
        expect_fail('Admin_info: password 过短',
                    lambda: _commit_admin('A99999', '1234'))
        expect_fail('Admin_info: password 过长',
                    lambda: _commit_admin('A99999', 'a' * 21))

        # ----- Admin_operation_record -----
        expect_fail('Admin_operation_record: content 为空',
                    lambda: _commit_operation('A00001', None, None, '',
                                              '原因说明'))
        expect_fail('Admin_operation_record: reason 为空',
                    lambda: _commit_operation('A00001', None, None, '操作',
                                              ''))
        expect_fail('Admin_operation_record: admin_id 外键不存在',
                    lambda: _commit_operation('X99999', None, None, '操作',
                                              '原因'))

        print(f'\n[test] 约束测试结束：通过 {passed}，失败 {failed}')
        if failed:
            sys.exit(1)


def _commit_user(uid, name, gender, type_, contact, password, balance):
    u = User(
        user_id=uid, name=name, gender=gender, type_=type_,
        contact=contact, balance=balance, password=password,
        num_limit=5, time_limit=60,
    )
    db.session.add(u)
    db.session.commit()


def _commit_category(code, name):
    db.session.add(Book_category(code=code, name=name))
    db.session.commit()


def _commit_book(cat, isbn, title, author, pub, pub_date, price, intro,
                 status='在馆'):
    b = Book_info(
        category_code=cat, isbn=isbn, title=title, author=author,
        publisher=pub, publish_date=pub_date, price=price,
        intro=intro, status=status,
    )
    db.session.add(b)
    db.session.commit()


def _commit_borrow(book_id, user_id, borrow_date, due_date):
    db.session.add(Borrow_info(
        book_id=book_id, user_id=user_id,
        borrow_date=borrow_date, due_date=due_date,
    ))
    db.session.commit()


def _commit_historical(book_id, user_id, borrow_date, due_date, return_date):
    db.session.add(Historical_borrowInfo(
        book_id=book_id, user_id=user_id,
        borrow_date=borrow_date, due_date=due_date, return_date=return_date,
    ))
    db.session.commit()


def _commit_admin(admin_id, password):
    db.session.add(Admin_info(admin_id=admin_id, password=password))
    db.session.commit()


def _commit_operation(admin_id, aff_uid, aff_aid, content, reason):
    db.session.add(Admin_operation_record(
        admin_id=admin_id,
        affected_user_id=aff_uid,
        affected_admin_id=aff_aid,
        date_time=datetime.now(),
        content=content,
        reason=reason,
    ))
    db.session.commit()


if __name__ == '__main__':
    seed()
    if '--test' in sys.argv:
        test_constraints()
