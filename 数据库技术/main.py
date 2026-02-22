# -*- coding: utf-8 -*-
import re
import sys
import pymssql
import os
import time  # 导入time模块,用于在部分位置实现延时,增强用户操作体验
import pandas  # 使用pandas模块将数据库中的数据以数据框的形式显示出来,增强数据显示效果
# keyboard 仅非 macOS 下按需导入，避免 macOS 上 __CFDataValidateRange 断言崩溃

# 本程序具有多重异常处理,让管理员有更精确而多样的反馈,从而更快地知道问题出在哪里,理论上每种异常都应该有其对应的提示

# 确保终端与 pandas 使用 UTF-8，使中文正常显示
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 改变界面颜色（仅 Windows 支持 color 命令）
if sys.platform == "win32":
    os.system("color F0")


def pause():
    """跨平台：按回车继续（Windows 用 pause，其它用 input）"""
    if sys.platform == "win32":
        pause()
    else:
        input("按回车继续...")


def cls_scr():
    """跨平台清屏（Windows 用 cls，其它用 clear）"""
    os.system("cls" if sys.platform == "win32" else "clear")


pandas.set_option('display.max_columns', None,
                  'display.max_rows', None,
                  'display.width', 200,
                  'display.max_colwidth', 200,
                  'display.unicode.ambiguous_as_wide', True,
                  'display.unicode.east_asian_width', True,
                  'display.encoding', 'utf-8')  # 设置pandas显示格式，中文正常显示


def Display():  # 输出函数,用于将数据库中的数据以数据框的形式显示出来
    data = pandas.DataFrame(cursor.fetchall(), columns=[x[0] for x in cursor.description])
    if data.empty:  # 判断数据框是否为空,为空则输出"无数据"
        print("\n无数据\n")
    else:
        rows_per_page = 30  # 设置每页显示的行数
        num_rows = data.shape[0]  # 获取数据框的总行数
        num_pages = num_rows // rows_per_page  # 计算显示完所有数据框所需要的总页数
        if num_rows % rows_per_page > 0:
            num_pages += 1  # 如果最后一页不满30行,则总页数加1,以保证显示完所有数据
        if num_pages == 1:
            print("\n", data, "\n")  # 如果只有一页,则直接输出数据框,不需要分页
        else:  # 如果有多页,则需要分页显示
            page = 0  # 设置倍率,以控制起始页数
            page_num = 1  # 设置初始页码为1

            def DisplayPage():
                start_row = page * rows_per_page  # 每一次显示的起始行数(序数)
                end_row = start_row + rows_per_page  # 每一次显示的结束行数(序数)
                cls_scr()  # 清屏
                print(f"第{page_num}/{num_pages}页 ({start_row + 1}-{end_row}):")
                print("\n", data.iloc[start_row:end_row], "\n")  # 输出数据框,换行更好看
            DisplayPage()  # 调用显示函数,先显示第一页(第1到第30个数据)
            # macOS 上不使用 keyboard，避免 __CFDataValidateRange 断言崩溃，改用回车/输入翻页
            if sys.platform == "darwin":
                print("\n有多页数据,将分页循环显示!"
                      "\n输入 回车=下一页, n+回车=上一页, q+回车=退出:")
                while True:
                    s = input().strip().lower()
                    if s == "q" or s == "quit":
                        break
                    if s == "n":
                        page -= 1
                        page_num -= 1
                        if page < 0:
                            page = num_pages - 1
                            page_num = num_pages
                        DisplayPage()
                    else:
                        page += 1
                        page_num += 1
                        if page > num_pages - 1:
                            page = 0
                            page_num = 1
                        DisplayPage()
                    print("回车=下一页, n+回车=上一页, q+回车=退出:")
            else:
                print("\n有多页数据,将分页循环显示!"
                      "\n请按'='键或'-'键换页"
                      "\n按'ctrl'加鼠标滑轮可缩放页面"
                      "\n按其他任意键退出此显示功能:\n")
                import keyboard  # 非 macOS 下按需导入
                while True:
                    time.sleep(0.5)
                    key = keyboard.read_key()
                    if key == "=":
                        page += 1
                        page_num += 1
                        if page > num_pages - 1:
                            page = 0
                            page_num = 1
                        DisplayPage()
                    elif key == "-":
                        page -= 1
                        page_num -= 1
                        if page < 0:
                            page = num_pages - 1
                            page_num = num_pages
                        DisplayPage()
                    elif key == "ctrl":
                        pass
                    else:
                        break


def convert_reader_id(reader_id):  # 判断有无该读者,存在唯一一位读者具有该编号,则pass,否则raise ValueError
    if reader_id == "":
        raise ValueError("读者编号不能为空!")
    elif len(reader_id) not in (6, 10) or not reader_id.isdecimal() or int(reader_id) <= 0:
        # 判断读者编号是否为6位或10位数字,且大于0,否则raise ValueError
        raise ValueError("读者编号必须为6位(教师或研究生)或10位(本科生或其他)的正整数!")
    try:
        reader_id = int(reader_id)
        cursor.execute("SELECT * FROM 读者信息 WHERE 读者编号 = '{}'".format(reader_id))  # reader_id为读者编号,python中为int型
    except:
        raise ValueError("SQL语句执行错误!")  # 正常情况下不会报这种错误,除非SQL语句写错
    else:
        if len(cursor.fetchall()) == 1:  # 由于主键约束,若存在该读者,则查询结果只会有一条
            pass  # 完成了判断有无该读者的功能并完成了数据类型转换
        else:
            raise ValueError("该读者不存在!")
            # 若不存在该读者,raise ValueError,若存在,则实现了str到int型的转换且程序能够继续进行下去


def convert_ISBN(ISBN):
    if ISBN == "":
        raise ValueError("ISBN不能为空!")
    elif len(ISBN) not in (10, 13) or not ISBN.isdecimal() or int(ISBN) <= 0:
        raise ValueError("ISBN必须为10位或13位的正整数!")
    try:
        ISBN = int(ISBN)
        cursor.execute("SELECT * FROM 图书信息 WHERE ISBN = '{}'".format(ISBN))
    except:
        raise ValueError("SQL语句执行错误!")
    else:
        if len(cursor.fetchall()) != 0:
            pass
        else:
            raise ValueError("该ISBN不对应馆内任何一本图书!")
            # 若不存在该图书,raise ValueError,若存在,则实现了对ISBN从str到int型的转换且程序能够继续进行下去

def convert_book_id(book_id):
    if book_id == "":
        raise ValueError("图书编号不能为空!")
    elif not book_id.isdecimal() or int(book_id) <= 0:
        raise ValueError("图书编号必须为正整数!")
    try:
        book_id = int(book_id)
        cursor.execute("SELECT * FROM 图书信息 WHERE 图书编号 = '{}'".format(book_id))
    except:
        raise ValueError("SQL语句执行错误!")
    else:
        if len(cursor.fetchall()) == 1:
            pass
        else:
            raise ValueError("该图书编号不对应馆内任何一本图书!")
            # 若不存在该图书,raise ValueError,若存在,则实现了对图书编号从str到int型的转换且程序能够继续进行下去


def _sql_escape(s):
    """转义单引号，用于拼入 SQL 字符串字面量"""
    return str(s).replace("'", "''")


def convert_to_float(str):  # 这个函数用来判断str是否为正的浮点数,若是,则返回float型,否则raise ValueError
    try:
        str = float(str)
    except:
        raise ValueError("输入内容非数值类型,无法转为浮点数!")
    else:
        if str <= 0:
            raise ValueError("请输入正整数或带小数点的正小数!")
        else:
            return str

def HomePage_1():  # 主页
    cls_scr()
    try:
        global db_host, db_user, db_password, conn, cursor  # 申明为全局变量,以方便后续连接和管理
        print("=====欢迎使用图书管理系统=====")
        print("\n请输入主机地址、账号、密码以连接数据库:")
        db_host = input("\n请输入主机地址: ") or "localhost"
        db_user = input("请输入账号: ") or "sa"
        db_password = input("请输入密码: ") or "Lxy@2026sql"
        conn = pymssql.connect(db_host, db_user, db_password, charset='utf8')  # 连接数据库，utf8 以正确读写中文
        conn.autocommit(True)  # 开启自动提交
        cursor = conn.cursor(as_dict=True)  # 创建游标,以字典形式返回数据
        cursor.execute('USE BOOKS')  # 选择数据库
    except:
        print("\n数据库连接失败!请重新输入！")
        time.sleep(1)  # 延时1秒,以保证用户能够看到错误信息
        HomePage_1()
    else:
        print("\n数据库连接成功！")
        time.sleep(1)
        ChooseCharacter_2()


def ChooseCharacter_2():  # 选择身份
    cls_scr()
    print("=====身份选择页面=====")
    print("\n请选择您的身份：")
    print("\n1.管理员")
    print("2.读者")
    print("0.退出系统")
    choose = input("\n请输入您的选择：")
    if choose == '1':
        ManagerLogin_3()
    elif choose == '2':
        ReaderLogin_3()
    elif choose == '0':
        print("\n感谢您的使用!")
        conn.cursor(as_dict=False)  # 关闭默认的字典输出
        conn.autocommit(False)  # 关闭自动提交
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库连接
        print("数据库连接已关闭,即将退出系统!")
        try:
            pause()  # 按回车继续，若 stdin 已关闭则直接退出
        except (EOFError, OSError):
            pass
        sys.exit(0)  # 退出系统（避免使用 exit(0) 以便顶层统一捕获 SystemExit）
    else:
        print("\n身份选择有误，请重新选择！")
        time.sleep(1)
        ChooseCharacter_2()


def ManagerLogin_3():  # 管理员登录
    cls_scr()  # 清屏
    print("=====管理员登录=====")
    global adm_name, adm_password  # 申明为全局变量,以方便后续使用
    adm_name = input("\n请输入管理员账号：") or "admin"
    adm_password = input("请输入管理员密码：") or "admin"
    cursor.execute(
        "SELECT * FROM 管理员信息 WHERE 管理员账号 = '{}' AND 管理员密码 = '{}'".format(adm_name, adm_password))
    if len(cursor.fetchall()) == 1:  # 如果长度为1,则账号密码正确,登录成功
        print("\n管理员账户登录成功!")
        time.sleep(1)
        ManagerBase_4()
    else:
        print("\n管理员账户登录失败!请检查账号密码后重新输入！")
        choice = input("是否重新输入？     [Y(y)/其他:选择身份]\n")  # 判断是否重新输入,Y(y)表示"是",其他表示"否",下同
        if choice == "Y" or choice == "y":
            ManagerLogin_3()
        else:
            ChooseCharacter_2()


def ReaderLogin_3():  # 读者登录
    cls_scr()
    print("=====读者登录=====")
    global user_id, user_password  # 申明为全局变量,以方便后续使用
    try:
        user_id = input("\n请输入读者编号：") or '111111'  # 输入的读者编号需要转换为整数,有报错风险,所以用try,except
        user_password = input("请输入读者密码：") or 'zhangyu123'
        user_id = int(user_id)
        cursor.execute(
            "SELECT * FROM 读者信息 WHERE 读者编号 = '{}' AND 密码 = '{}'".format(int(user_id), user_password))
        if len(cursor.fetchall()) == 1:
            print("\n读者账户登录成功!")
            time.sleep(1)
            ReaderBase_4()  # 登录成功,进入读者基本操作界面
        else:
            print("\n读者账户登录失败!请检查账号密码后重新输入！")  # 格式正确,但是长度不为1,即为0,则账号密码错误
            choice = input("是否重新输入？     [Y(y)/其他:选择身份]\n")
            if choice == "Y" or choice == "y":
                ReaderLogin_3()
            else:
                ChooseCharacter_2()
    except (EOFError, OSError):
        # stdin 关闭（如 Ctrl+D）时 input 会抛错，直接返回身份选择
        print("\n输入已关闭，返回身份选择页面。")
        time.sleep(1)
        ChooseCharacter_2()
    except Exception:
        print("\n输入读者编号时格式有误,请检查后重新输入!\n")
        try:
            choice = input("是否重新输入？     [Y(y)/其他]\n")
        except (EOFError, OSError):
            print("\n输入已关闭，返回身份选择页面。")
            time.sleep(1)
            ChooseCharacter_2()
            return
        if choice == "Y" or choice == "y":
            ReaderLogin_3()
        else:
            print("\n已取消登录,即将返回身份选择页面！")
            time.sleep(1)
            ChooseCharacter_2()


def ManagerBase_4():  # 管理员功能界面首页
    cls_scr()
    print("=====管理员功能=====")  # 管理员功能主界面
    print("\n1.图书管理")
    print("2.读者管理")
    print("3.借阅管理")
    print("4.管理员管理")
    print("5.备份数据库")
    print("6.恢复数据库")
    print("0.退出登录")  # 除了以上选择外,其他均为非法输入,下同
    choice = input("\n请输入您的选择：")
    if choice == '1':
        BM_BookManage_5()
    elif choice == '2':
        RM_ReaderManage_5()
    elif choice == '3':
        BrM_BorrowManage_5()
    elif choice == '4':
        AM_AdminManage_5()
    elif choice == '5':
        Backup()
    elif choice == '6':
        Restore()
    elif choice == '0':
        ChooseCharacter_2()
    else:
        print("\n管理员功能选择有误，请重新选择！")
        time.sleep(1)
        ManagerBase_4()


def ReaderBase_4():  # 读者功能界面首页
    cls_scr()
    print("=====读者功能=====")  # 读者功能主界面
    print("\n1.浏览个人信息")
    print("2.图书信息查询")
    print("3.借阅信息查询")
    print("4.借阅历史查询")
    print("5.充值扣款记录查询")
    print("6.修改登录密码")
    print("0.退出登录")  # 除了以上选择外,其他均为非法输入,下同
    choose = input("\n请输入您的选择：")
    if choose == '1':
        R_ReaderInfo_5r()
    elif choose == '2':
        R_ReaderBookSearch_5r()
    elif choose == '3':
        R_BorrowInfoNow_5r()
    elif choose == '4':
        R_BorrowInfoHistory_5r()
    elif choose == '5':
        R_RechargeInfo_5r()
    elif choose == '6':
        R_ReaderPassword_5r()
    elif choose == '0':
        ChooseCharacter_2()
    else:
        print("\n读者功能选择有误，请重新选择！")
        time.sleep(1)
        ReaderBase_4()


def BM_BookManage_5():  # 图书管理
    cls_scr()
    print("=====图书管理=====")
    print("\n1.添加图书")
    print("2.删除图书")
    print("3.修改图书信息")
    print("4.浏览图书")
    print("0.返回管理员主菜单")
    choice = input("\n请选择操作：")
    if choice == '1':
        BM_BookIn()
    elif choice == '2':
        BM_BookDel()
    elif choice == '3':
        BM_BookInfoChange()
    elif choice == '4':
        BM_BookBrowse()
    elif choice == '0':
        ManagerBase_4()
    else:
        print("\n图书管理功能选择有误，请重新选择！")
        time.sleep(1)
        BM_BookManage_5()


def BM_BookIn():  # 图书上架 (添加图书)
    cls_scr()
    try:
        print("请输入待上架的图书信息:")   #上架图书当然都是完好的,所以状态默认为'在馆'
        ISBN = input("\n(13位)ISBN：")   #可以添加已存在的图书(具有相同的ISBN),但是只会导致图书数量增加,不能修改信息
        if len(ISBN) not in (10, 13) or not ISBN.isdecimal() or int(ISBN) <= 0:
            raise ValueError("ISBN不为10或13位正整数！")
        ISBN = int(ISBN)
        cursor.execute("SELECT * FROM 图书信息 WHERE ISBN= '{}'".format(ISBN))
        # 依据相关法律法规,ISBN是唯一的,版本不同的图书也会有不同的ISBN
        if len(cursor.fetchall()) != 0:
            print("\n该图书当前馆内已存在,您可以增加它的册数！")
            time.sleep(1)
            NUM = input("\n增加数量：")
            if not NUM.isdecimal() or int(NUM) <= 0:
                raise ValueError("增加数量必须为正整数！")
            else:
                NUM = int(NUM)
                while NUM > 0:  # 复制性上架,会将该图书再复制多份,数量为NUM
                    cursor.execute(
                        "INSERT INTO 图书信息(分类编码, ISBN, 书名, 作者, 出版社, 出版日期, 单价, 简介, 状态) "
                        "SELECT TOP 1 分类编码, ISBN, 书名, 作者, 出版社, 出版日期, 单价, 简介, '在馆' "
                        "FROM 图书信息 "
                        "WHERE ISBN= '{}'".format(ISBN))    # 任意取一份信息,然后复制图书信息,设置状态为'在馆'
                    NUM -= 1  # 每次循环都会添加一本图书,直到数量为0
        else:
            print("\n该图书当前馆内不存在,请输入该全新图书的信息！")
            time.sleep(1)
            CAT = input("分类编码(单字母A-Z,须先在图书分类表中存在)：").strip().upper()
            if len(CAT) != 1 or not CAT.isalpha():
                raise ValueError("分类编码须为单字母A-Z！")
            cursor.execute(
                "SELECT 1 AS ok FROM 图书分类 WHERE 分类编码 = N'{}'".format(_sql_escape(CAT))
            )
            if len(cursor.fetchall()) == 0:
                raise ValueError("该分类编码不存在，请先在图书分类中维护！")
            NAME = input("\n书名(非空,50字以内)：")
            if len(NAME) == 0 or len(NAME) > 50:
                raise ValueError("书名不可为空且不应超过50字！")
            AUT = input("作者(非空,20字以内)：")
            if len(AUT) == 0 or len(AUT) > 20:
                raise ValueError("作者不可为空且不应超过20字！")
            PUB = input("出版社(非空,20字以内): ")
            if len(PUB) == 0 or len(PUB) > 20:
                raise ValueError("出版社不可为空且不应超过20字！")
            DAT = input("出版日期 (格式：yyyy-mm-dd,默认为1900-01-01)：").strip()
            if DAT == "":
                DAT = "1900-01-01"
            if not re.match(r"\d{4}-\d{2}-\d{2}", DAT):
                raise ValueError("日期格式错误,注意月和日可能需要补0(如2022-01-01)！")
            PRI = input("单价(非空,两位小数,超出则四舍五入)：")
            PRI = convert_to_float(PRI)
            INS = input("简介(可空)：")
            NUM = input("上架数量：")
            if len(NUM) == 0 or not NUM.isdecimal() or int(NUM) <= 0:
                raise ValueError("上架数量必须为正整数！")
            NUM = int(NUM)
            sql1 = (
                "EXEC 图书上架存储过程 N'{}',{},N'{}',N'{}',N'{}',N'{}',{},N'{}',{}"
                .format(
                    _sql_escape(CAT), ISBN,
                    _sql_escape(NAME), _sql_escape(AUT), _sql_escape(PUB),
                    _sql_escape(DAT), float(PRI), _sql_escape(INS), NUM
                )
            )
            cursor.execute(sql1)
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BM_BookIn()
        else:
            BM_BookManage_5()
    except Exception as e:
        print("\n上架失败:", str(e))
        choice = input("是否重试？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BM_BookIn()
        else:
            BM_BookManage_5()
    else:
        cursor.execute(
            "EXEC 管理员浏览图书信息存储过程 N'{}'".format(_sql_escape(str(ISBN)))
        )
        print("\n图书上架(添加)成功!请查看该ISBN对应的全部图书:")
        Display()
        time.sleep(3)
        choice = input("是否继续上架(添加)图书？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BM_BookIn()  # 递归调用
        else:
            BM_BookManage_5()  # 返回图书管理页面


def BM_BookDel():  # 图书下架 (删除图书)
    cls_scr()
    try:
        print("=====图书下架=====")
        # 由于图书编号为借阅历史表的外键(在init.py中用了级联删除),
        # 所以删除图书时会自动删除与该图书相关的除借阅信息外的所有信息
        # 由于借阅信息里的书都是还没还的,所以不应该删除借阅信息表里的信息(会造成读者无法还书或图书馆的经济损失)
        ISBN_ID = input("\n请输入待删除的图书的图书编号或ISBN：")
        # 使用str类型以便在SQL语句中使用len()函数,或者也可采用int类型,在SQL语句中使用cast()函数
        # 在SQL中通过len()函数判断是否为ISBN(10或13位)
        if not ISBN_ID.isdecimal() or int(ISBN_ID) <= 0:  # 判断是否为非负整数
            raise ValueError("图书编号或ISBN必须为正整数！")
        cursor.execute("EXEC 管理员浏览图书信息存储过程 %s", (str(ISBN_ID),))
        Display()
        print("警告:\n    此操作将会删除包括 以上各图书(不包括状态为'借出'的图书)的图书信息、与之相关的历史借阅信息 在内的所有信息！")
        choice = input("\n是否确认删除？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            cursor.execute("EXEC 图书下架存储过程 '{}' ".format(ISBN_ID))
        else:
            raise InterruptedError("取消删除！")
    except InterruptedError as e:
        print("中断原因:", e)
        print("是否继续删除其它图书？     [Y(y)/其他]\n")
        choice = input()
        if choice == "Y" or choice == "y":
            BM_BookDel()
        else:
            BM_BookManage_5()
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BM_BookDel()
        else:
            BM_BookManage_5()
    except:
        choice = input("\n\n未找到该图书或该图书(全)为'借出'状态,无法删除!是否重新删除其他图书?     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BM_BookDel()
        else:
            BM_BookManage_5()
    else:
        print("\n图书下架(删除)成功(若输入的是ISBN则不包括状态为'借出'的图书)!")
        time.sleep(1)
        choice = input("\n是否继续下架(删除)？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BM_BookDel()
        else:
            BM_BookManage_5()


def BM_BookInfoChange():  # 修改图书信息
    cls_scr()
    try:
        print("=====修改图书信息=====")
        ISBN_ID = input("\n请输入待修改图书的图书编号或ISBN (修改前后不发生变化) ：")
        if not ISBN_ID.isdecimal() or int(ISBN_ID) <= 0:  # 判断是否为非负整数
            raise ValueError("图书编号或ISBN必须为正整数！")
        # 图书编号和ISBN作为一本书或一簇书的唯一标识,不可修改,在此依据此确定待修改的图书
        cursor.execute(
            "EXEC 管理员浏览图书信息存储过程 N'{}'".format(_sql_escape(ISBN_ID))
        )
        Display()   #存在则显示图书信息
        print("请输入修改后的信息：")
        CAT = input("分类编码(单字母A-Z,须在图书分类表中存在)：").strip().upper()
        if len(CAT) != 1 or not CAT.isalpha():
            raise ValueError("分类编码须为单字母A-Z！")
        cursor.execute(
            "SELECT 1 AS ok FROM 图书分类 WHERE 分类编码 = N'{}'".format(_sql_escape(CAT))
        )
        if len(cursor.fetchall()) == 0:
            raise ValueError("该分类编码不存在，请先在图书分类中维护！")
        NAM = input("书名(非空,50字以内)：")
        if len(NAM) == 0 or len(NAM) > 50:
            raise ValueError("书名不可为空且不应超过50字！")
        AUT = input("作者(非空,20字以内)：")
        if len(AUT) == 0 or len(AUT) > 20:
            raise ValueError("作者不可为空且不应超过20字！")
        PUB = input("出版社(非空,20字以内): ")
        if len(PUB) == 0 or len(PUB) > 20:
            raise ValueError("出版社不可为空且不应超过20字！")
        DAT = input("出版日期 (格式：yyyy-mm-dd,空则1900-01-01)：").strip()
        if DAT == "":
            DAT = "1900-01-01"
        if not re.match(r"\d{4}-\d{2}-\d{2}", DAT):
            raise ValueError("日期格式错误,注意月和日可能需要补0(如2022-01-01)！")
        PRI = input("单价(两位小数,实行四舍五入)：")
        PRI = convert_to_float(PRI)
        INS = input("简介(可空,100字以内)：")
        if len(INS) > 100:
            raise ValueError("简介不应超过100字！")
        STA = input("状态(请填写'在馆'、'借出'、'丢失'、'损坏'四者之一): ")
        if STA != "在馆" and STA != "借出" and STA != "丢失" and STA != "损坏":
            raise ValueError("状态输入错误！")
        sql3 = (
            "EXEC 管理员修改图书信息存储过程 N'{}',N'{}',N'{}',N'{}',N'{}',N'{}',{},N'{}',N'{}'"
            .format(
                _sql_escape(ISBN_ID), _sql_escape(CAT),
                _sql_escape(NAM), _sql_escape(AUT), _sql_escape(PUB),
                _sql_escape(DAT), float(PRI), _sql_escape(INS), _sql_escape(STA)
            )
        )
        cursor.execute(sql3)
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BM_BookInfoChange()
        else:
            BM_BookManage_5()
    except Exception as e:
        err = str(e)
        if "图书编号或ISBN不存在" in err or "不存在" in err:
            choice = input("\n\n没有以该数字为图书编号或ISBN的图书,是否重试？     [Y(y)/其他]\n")
        else:
            print("\n修改失败:", err)
            choice = input("是否重试？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BM_BookInfoChange()
        else:
            BM_BookManage_5()
    else:
        cursor.execute(
            "EXEC 管理员浏览图书信息存储过程 N'{}'".format(_sql_escape(ISBN_ID))
        )
        print("\n修改成功!该图书编号(或ISBN)所对应的新信息如下:")
        Display()
        time.sleep(1)
        choice = input("\n是否继续修改？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BM_BookInfoChange()
        else:
            BM_BookManage_5()


def BM_BookBrowse():  # 浏览图书信息
    cls_scr()
    try:
        print("=====浏览图书信息=====")
        print("\n温馨提示:全屏浏览体验更佳!")  # 全屏有利于显示更多的信息,展现完整的数据框
        ID_ISBN = input("\n请输入想要浏览的图书的编号或ISBN (若空置,则浏览所有图书) :")
        if len(ID_ISBN) == 0:
            pass
        elif not ID_ISBN.isdecimal() or int(ID_ISBN) <= 0:
            raise ValueError("图书编号或ISBN必须为正整数！")
        if ID_ISBN == "":  # 若输入为空,则浏览所有图书
            SQL4 = "EXEC 管理员浏览图书信息存储过程"
        else:  # 若输入不为空,则浏览指定图书
            ID_ISBN = int(ID_ISBN)
            SQL4 = "EXEC 管理员浏览图书信息存储过程 '{}'".format(ID_ISBN)
        cursor.execute(SQL4)
        if cursor.rowcount == 0:
            raise ValueError("该图书编号不存在！")
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BM_BookBrowse()
        else:
            BM_BookManage_5()
    except:
        choice = input("\n\n不存在以该正整数为图书编号或ISBN的图书,是否重试？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BM_BookBrowse()
        else:
            BM_BookManage_5()
    else:
        Display()
        time.sleep(1)
        print("\n浏览成功,按任意键返回图书管理页面!")
        pause()
        BM_BookManage_5()


def RM_ReaderManage_5():  # 读者管理
    cls_scr()
    print("=====读者功能=====")
    print("\n1.添加读者")
    print("2.删除读者")
    print("3.修改读者信息")
    print("4.查询读者信息")
    print("5.重置读者密码")
    print("6.记录重要操作")
    print("7.查询重要操作记录")
    print("0.返回管理员主菜单")
    ch = input("\n请选择操作：")
    if ch == '1':
        RM_ReaderIn()
    elif ch == '2':
        RM_ReaderDel()
    elif ch == '3':
        RM_ReaderInfoChange()
    elif ch == '4':
        RM_ReaderSeek()
    elif ch == '5':
        RM_ReaderReset()
    elif ch == '6':
        RM_RecordOperations()
    elif ch == '7':
        RM_RecordSeek()
    elif ch == '0':
        ManagerBase_4()
    else:
        print("\n读者管理功能选择有误，请重新选择！")
        time.sleep(1)
        RM_ReaderManage_5()


def RM_ReaderIn():  # 添加读者
    cls_scr()
    try:
        print("=====添加读者=====")
        print("\n请输入读者信息")
        time.sleep(1)
        ID = input("\n读者编号 [6位(教师或研究生)或10位(本科生或其他)整数]：")
        if len(ID) not in (6, 10) or not ID.isdecimal() or int(ID) <= 0:
            raise ValueError("读者编号必须为6位或10位正整数！")
        ID = int(ID)
        cursor.execute("SELECT * FROM 读者信息 WHERE 读者编号 = '{}' ".format(ID))
        if len(cursor.fetchall()) != 0:
            raise ValueError("该读者编号已存在！")
        name = input("\n姓名(非空,20个字以内)：")
        if len(name) == 0 or len(name) > 20:
            raise ValueError("姓名不能为空且不能超过20个字！")
        sex = input("性别(非空,'男','女')：")
        if sex not in ("男", "女"):
            raise ValueError("性别只能为'男'或'女'！")
        category = input("类型 (非空,'教师','研究生','本科生','其他') ：")
        if len(str(ID)) == 6:
            if category not in ("教师", "研究生"):
                raise ValueError("读者类型错误,读者编号长度为6位的只能为'教师'或'研究生'！")
        if len(str(ID)) == 10:
            if category not in ("本科生", "其他"):
                raise ValueError("读者类型错误,读者编号长度为10位的只能为'本科生'或'其他'！")
        contact = input("联系方式(非空,20字以内)：").strip()
        if len(contact) == 0 or len(contact) > 20:
            raise ValueError("联系方式不能为空且不能超过20字！")
        balance = input("初始余额(非空,不少于20元):")
        balance = convert_to_float(balance)
        if balance < 20 or balance > 99999999.99:
            raise ValueError("初始余额必须在[20,99999999.99]范围内！")
        password = input("密码(非空,8到20位的英文+数字)：")
        if len(password) < 8 or len(password) > 20 or not password.isalnum():
            raise ValueError("密码必须为8到20位英文或数字！")
        SQL = "EXEC 管理员添加读者存储过程 '{}','{}','{}','{}','{}','{}','{}','{}' "\
            .format(ID, name, sex, category, contact, balance, adm_name, password)
        cursor.execute(SQL)
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderIn()
        else:
            RM_ReaderManage_5()
    except:
        choice = input("\n未知错误,是否重试？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderIn()
        else:
            RM_ReaderManage_5()
    else:
        cursor.execute("EXEC 管理员查询读者信息存储过程 '{}' ".format(ID))
        print("\n读者添加成功!:")
        Display()
        cursor.execute(
            "SELECT TOP 1 * FROM 管理员重要操作记录 "
            "WHERE 受影响的读者编号 = '{}' "
            "ORDER BY 操作时间 DESC".format(ID))
        print("\n此项操作已被记录完成:")
        Display()
        time.sleep(1)
        choice = input("\n是否继续添加？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderIn()
        else:
            RM_ReaderManage_5()


def RM_ReaderDel():  # 删除读者
    cls_scr()
    try:
        print("=====删除读者=====")
        ID = input("\n请输入读者编号(6位或10位整数)：")
        convert_reader_id(ID)
        cursor.execute("EXEC 管理员查询读者信息存储过程 '{}'".format(ID))
        # 查询读者信息,由于存储过程中参数格式为str(为了既可以通过读者编号查,也可以通过姓名查),所以此处不用int
        Display()
        cursor.execute("SELECT 当前借阅数量 FROM 所有读者当前借阅图书数量视图 WHERE 读者编号 = '{}'".format(ID))
           # 查询读者当前借阅数量,如果不为0,即还有没还的书籍,则不允许删除
        if cursor.fetchone() != None:
            raise ValueError("当前借阅数量不为0,不允许删除,请先归还所有图书！")
        reason = input("\n请输入删除该读者的原因,其将被记录进'管理员重要操作记录表'(100字以内,默认为'毕业'): ") or "毕业"
        if len(reason) > 100:
            raise ValueError("删除原因的长度不能超过100个字符！")
        cursor.execute("SELECT * FROM 历史借阅信息 WHERE 读者编号 = '{}'".format(ID))
        print("\n该读者的历史借阅信息表: ")
        Display()
        cursor.execute("SELECT * FROM 充值扣款记录 WHERE 读者编号 = '{}'".format(ID))
        print("\n该读者的充值扣款记录: ")
        Display()
        time.sleep(1)
        choice = input("警告:\n    除读者信息外,以上各条历史借阅信息、充值扣款记录也均会被彻底删除!"
                           "\n    但与该读者相关的'管理员重要操作记录'不会被删除\n\n是否确认删除该读者？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            SQL = "EXEC 管理员删除读者存储过程 '{}','{}','{}' ".format(adm_name, int(ID), reason)
            cursor.execute(SQL)
        else:
            raise InterruptedError("已取消删除该读者")
    except ValueError as e:
        # 多重异常处理,让管理员有更精确多样的反馈,从而更快地知道问题出在哪里,理论上每种异常都应该有自己的处理方式
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderDel()
        else:
            RM_ReaderManage_5()
    except InterruptedError as e:
        cls_scr()
        print("\n中断原因：", e)
        time.sleep(1)
        choice = input("是否继续删除其他读者？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderDel()
        else:
            RM_ReaderManage_5()

    else:
        cls_scr()
        cursor.execute(
            "SELECT TOP 1 * FROM 管理员重要操作记录 WHERE 受影响的读者编号 = '{}' ORDER BY 操作时间 DESC".format(ID))
        print("\n删除成功!(本次操作已被记录)")
        Display()
        time.sleep(1)
        choice = input("是否继续删除其他读者信息？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderDel()
        else:
            RM_ReaderManage_5()


def RM_ReaderInfoChange():  # 修改读者信息
    cls_scr()
    try:
        print("=====修改读者信息=====")
        ID = input("\n请输入读者编号 [(6或10位整数)  为保障相关记录的安全性,其不允许被修改]：")
        # 由于管理员重要操作记录里读者编号不是外键.倘若修改读者编号,将会造成记录混乱,因此不允许修改合情合理
        convert_reader_id(ID)  # 检查读者是否存在,不存在则抛出异常,避免浪费时间;若存在则将其转换为int类型
        cursor.execute("EXEC 管理员查询读者信息存储过程 '{}'".format(ID))
        Display()
        print("\n请输入修改后的读者信息: ")
        name = input("\n姓名(非空,20个字以内)：")
        if name == "" or len(name) > 20:
            raise ValueError("姓名不能为空且不能超过20个字")
        sex = input("性别: ")
        if sex not in ("男", "女"):
            raise ValueError("性别只能为'男'或'女'")
        category = input("类型('教师','研究生','本科生','其他'四者之一)：")
        # 由于读者类型与读者编号长度相匹配,故只能'教师'、研究生之间互相改,剩余两种类型之间可互相改
        if len(str(ID)) == 6:
            if category not in ("教师", "研究生"):
                raise ValueError("读者类型错误,读者编号长度为6位的只能为'教师'或'研究生'！")
        elif len(str(ID)) == 10:
            if category not in ("本科生", "其他"):
                raise ValueError("读者类型错误,读者编号长度为6位的只能为'本科生'或'其他'！")
        contact = input("联系方式(非空,20字以内)：").strip()
        if len(contact) == 0 or len(contact) > 20:
            raise ValueError("联系方式不能为空且不能超过20字！")
        balance = input("余额(保留两位小数,对此项的修改将被记录进'充值扣款记录'表中：")
        balance = convert_to_float(balance)
        if balance < 0 or balance > 99999999.99:
            raise ValueError("初始余额必须在[0,99999999.99]范围内！")
        # 对余额的修改将被记录进'充值扣款记录'表中
        reason = input("\n请输入修改读者信息的原因(将被记录进'管理员重要操作记录'表中): ")
        if reason == "" or len(reason) > 100:
            raise ValueError("原因不能为空且不能超过100个字")
        cursor.execute("EXEC 管理员修改读者信息存储过程 '{}','{}','{}','{}','{}','{}','{}','{}' ".format(adm_name, ID, name, sex, category, contact, balance, reason))
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        time.sleep(1)
        choice = input("是否重新修改？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderInfoChange()
        else:
            RM_ReaderManage_5()
    except:
        choice = input("\n未知错误,是否重试？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderInfoChange()
        else:
            RM_ReaderManage_5()
    else:
        print("\n修改成功!")
        cursor.execute("EXEC 管理员查询读者信息存储过程 '{}'".format(ID))
        print("\n读者信息已更新:")
        Display()
        cursor.execute(
            "SELECT TOP 1 * FROM 管理员重要操作记录 "
            "WHERE 受影响的读者编号 = '{}' ORDER BY 记录编号 DESC".format(ID))
        print("\n本次操作已被记录:")
        Display()  # 显示最新的一条记录

        cursor.execute("SELECT TOP 1 * FROM 充值扣款记录 "
                       "WHERE 读者编号 = '{}' ORDER BY 记录编号 DESC".format(ID))
        print("\n本次余额变动已被记录:")
        Display()  # 显示最新的一条记录
        time.sleep(1)
        choice = input("\n是否继续修改其他读者的信息？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderInfoChange()
        else:
            RM_ReaderManage_5()

def RM_ReaderSeek():  # 查询读者信息
    cls_scr()
    try:
        print("=====查询读者信息=====")
        ID_NAME = input("\n请输入需查找的读者编号(6或10位整数)或姓名\n\n"
                        "(若为空,则查看所有读者信息):")
        if ID_NAME == "":
            try:
                cursor.execute("EXEC 管理员查询读者信息存储过程")
                print("\n所有读者信息如下:")    # 在else里Display()显示所有信息
            except:
                print("\n查询失败!")
        else:
            try:
                ID = int(ID_NAME)
                # 尝试将输入内容当作编号转换为整数,如果成功!则按编号查找,否则按姓名查找
                SQL = "EXEC 管理员查询读者信息存储过程 '{}'".format(ID)
                cursor.execute(SQL)
                print("\n该姓名对应读者的信息如下:")
            except:
                SQL = "EXEC 管理员查询读者信息存储过程 '{}'".format(ID_NAME)
                cursor.execute(SQL)
                print("\n该姓名对应读者的信息如下:")
    except:
        print("\n查询失败!没有与输入信息相对应的读者\n")
        choice = input("\n是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderSeek()
        else:
            RM_ReaderManage_5()
    else:
        Display()
        time.sleep(1)
        choice = input("\n是否继续查询？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderSeek()
        else:
            RM_ReaderManage_5()


def RM_ReaderReset():  # 管理员重置读者密码
    cls_scr()
    try:
        print("=====重置读者密码=====")
        ID = input("\n请输入读者编号：")
        convert_reader_id(ID)
        # 检查读者是否存在,只要读者编号不存在(包括输入格式错误或者查不到对应读者),则抛出异常,跳转到except,以节省时间
        cursor.execute("EXEC 管理员查询读者信息存储过程 '{}'".format(ID))  # 显示读者信息
        Display()
        newpassword = input("请输入新密码(8到20位)：")
        if len(newpassword) < 8 or len(newpassword) > 20 or not newpassword.isalnum():
            raise ValueError("密码必须为8到20位英文或数字！")
        choice = input(
            "\n警告:"
            "\n    此项操作极其敏感"
            "\n    产生的记录将永久地被保存且不可被删改"
            "\n    您只应在读者当面出示有效身份证件并要求重置的情况下才可执行此项操作"
            "\n    若在读者不知情的情况下进行操作,您可能将承担相应法律责任"
            "\n"
            "\n您是否仍确认要重置此读者的密码？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            cursor.execute("EXEC 管理员重置读者密码存储过程 '{}','{}','{}' ".format(adm_name, ID, newpassword))
        else:
            raise InterruptedError("您已取消重置密码操作")
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("\n是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderReset()
        else:
            RM_ReaderManage_5()
    except InterruptedError as e:
        cls_scr()
        print("\n中断原因: ", e, "\n")
        choice = input("\n是否继续重置密码？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderReset()
        else:
            RM_ReaderManage_5()
    except:
        choice = input("\n未知错误!是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_ReaderReset()
        else:
            RM_ReaderManage_5()
    else:
        cursor.execute(
            "SELECT TOP 1 * FROM 管理员重要操作记录 "
            "WHERE 受影响的读者编号 = '{}' ORDER BY 记录编号 DESC".format(ID))
        print("\n重置成功!本次操作已被记录")
        Display()
        print("\n请按任意键返回读者管理页面")
        pause()
        RM_ReaderManage_5()


def RM_RecordOperations():
    cls_scr()
    try:
        print("=====记录重要操作=====")
        print("\n请输入操作过程的相关信息:")
        time.sleep(1)
        choice = input("\n请输入受影响的对象的类型: "
                       "\n\n"
                       "1.读者 2.管理员 3.其他"
                       "\n\n")  # 其他类型供管理员自由记录
        if choice == "1":
            ID = input("\n请输入受影响的读者编号(须当前存在): ")
            convert_reader_id(ID)
            # 只能记录当前存在的读者,可以一定程度上防止管理员错误记录
            # 如果没有相应读者,则抛出异常,跳转到except,以节省时间,若读者存在,转换为int型
        elif choice == '2':
            inf_admchar = input("\n请输入受影响的管理员账号: ")  # 二者均可空
            cursor.execute("SELECT * FROM 管理员信息 WHERE 管理员账号 = '{}'".format(inf_admchar))
            if len(cursor.fetchall()) == 0:
                raise ValueError("管理员账号不存在")
        elif choice == '3':
            print("")
            # 其他类型的操作记录不需要受影响的对象,直接记录即可
        else:
            raise ValueError("受影响的对象的类型选择错误")
        print("\n请输入操作过程的相关信息:\n")
        alteration = input("\n操作内容(不可为空,50个字以内)：")
        if len(alteration) == 0 or len(alteration) > 50:
            raise ValueError("操作内容不可为空且不能超过50个字")
        reason = input("\n操作原因(不可为空,100个字以内)：")
        if len(reason) == 0 or len(reason) > 100:
            raise ValueError("操作原因不可为空且不能超过100个字")
        # 这里的操作原因是指管理员操作的原因
        if choice == "1":
            cursor.execute(
                "EXEC 创建管理员重要操作存储过程 '{}','{}',NULL,'{}','{}'"
                .format(adm_name, ID, alteration, reason))  # 受影响者为读者时
        elif choice == "2":  # 均记录了当前操作者的账号
            cursor.execute(
                "EXEC 创建管理员重要操作存储过程 '{}',NULL,'{}','{}','{}'"
                .format(adm_name, inf_admchar, alteration, reason)) # 受影响者为管理员时
        elif choice == "3":
            cursor.execute(
                "EXEC 创建管理员重要操作存储过程 '{}',NULL,NULL,'{}','{}'"
                .format(adm_name, alteration, reason))  # 受影响者为其他时
    except ValueError as e:
        # 多重except,让找问题更加简便
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_RecordOperations()
        else:
            RM_ReaderManage_5()
    except:  # 记录时自动记录当前时间
        choice = input("\n未知错误!是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_RecordOperations()
        else:
            RM_ReaderManage_5()
    else:
        cursor.execute("SELECT TOP 1 * FROM 管理员重要操作记录 ORDER BY 记录编号 DESC")
        print("\n成功记录!")
        Display()
        choice = input("是否继续记录？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_RecordOperations()
        else:
            RM_ReaderManage_5()


def RM_RecordSeek():
    cls_scr()
    try:
        print("=====查看重要操作记录=====")
        print(
            "\n请输入管理员账号和受影响的读者编号或受影响的管理员账号,以查询相应的重要操作记录"
            "\n根据填入信息对该项进行筛选,不填则不筛选"
            "\n'受影响的读者'和'受影响的管理员'不可同时为非空")
        time.sleep(1)
        opadm_name = input("\n执行操作的管理员账号(可空)：")  # 也不一定非得是当前存在的管理员,可以是已经被删除的管理员
        # 不输入则默认为空(查询所有管理员对下列对象的操作),为了方便读者问询,应允许查看其他管理员重要操作记录
        if len(opadm_name) == 0:
            pass
        elif not opadm_name.isalnum():
            raise ValueError("管理员账号只能由字母和数字组成")
        RID = input("\n请输入受影响的读者编号(可空)：")  # 填了也不一定非得是当前存在的读者,因此不调用convert_reader_id()函数
        # 不输入则默认为空(查询所有读者),这里不设置convert_reader_id()是因为可能有读者被删除
        if len(RID) == 0:
            pass
        elif not RID.isdecimal() or len(RID) not in (6, 10) or int(RID) <= 0:
            raise ValueError("读者编号只能为6或10位正整数")
        MID = input("\n请输入受影响的管理员账号(可空)：")  # 填了也不一定非得是当前存在的管理员
        if len(MID) == 0:
            pass
        elif not MID.isalnum():
            raise ValueError("管理员账号只能由字母和数字组成")
        # 受影响的读者和受影响的管理员二者均可空,也可以同时为空,但不能同时为非空
        if RID != "" and MID != "":
            raise ValueError("受影响的读者编号和管理员账号不能同时为非空!")  # 如果两个都不为空,则抛出异常
        else:
            if opadm_name == "":  # 都可以为空,但是受影响的读者编号和管理员账号不能同时为非空
                if RID == "" and MID == "":
                    print("\n管理员重要操作记录表全部数据如下:")
                    cursor.execute("EXEC 管理员查看重要操作记录存储过程 NULL,NULL,NULL ")
                elif RID == "" and MID != "":
                    print("\n管理员重要操作记录表中受影响的管理员账号为'{}'的数据如下:".format(MID))
                    cursor.execute("EXEC 管理员查看重要操作记录存储过程 NULL,NULL,'{}' ".format(MID))
                elif RID != "" and MID == "":
                    RID = int(RID)
                    print("\n管理员重要操作记录表中受影响的读者编号为'{}'的数据如下:".format(RID))
                    cursor.execute("EXEC 管理员查看重要操作记录存储过程 NULL,'{}',NULL ".format(RID))
            else:
                if RID == "" and MID == "":
                    print("\n管理员重要操作记录表中执行操作的管理员账号为'{}'的数据如下:".format(opadm_name))
                    cursor.execute("EXEC 管理员查看重要操作记录存储过程 '{}',NULL,NULL ".format(opadm_name))
                elif RID == "" and MID != "":
                    print("\n管理员重要操作记录表中执行操作的管理员账号为'{}',且受影响的管理员账号为'{}'的数据如下:".format(
                            opadm_name, MID))
                    cursor.execute("EXEC 管理员查看重要操作记录存储过程 '{}',NULL,'{}' ".format(opadm_name, MID))
                elif RID != "" and MID == "":
                    RID = int(RID)
                    print("\n管理员重要操作记录表中执行操作的管理员账号为'{}',且受影响的读者编号为'{}'的数据如下:".format(
                            opadm_name, RID))
                    cursor.execute("EXEC 管理员查看重要操作记录存储过程 '{}','{}',NULL ".format(opadm_name, RID))
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_RecordSeek()
        else:
            RM_ReaderManage_5()
    except:
        choice = input("\n未知错误!是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_RecordSeek()
        else:
            RM_ReaderManage_5()
    else:
        print("\n查询成功!")
        Display()
        time.sleep(1)
        choice = input("是否继续查询？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            RM_RecordSeek()
        else:
            RM_ReaderManage_5()


def BrM_BorrowManage_5():  # 借阅管理
    cls_scr()
    print("===读者管理===")
    print("\n1、借阅图书")
    print("2、归还图书")  # 逾期扣款功能作为触发器在读者还书时实现
    print("3、读者充值")
    print("4、浏览所有读者当前借阅图书数量")
    print("5、浏览被借阅前10位的图书")
    print("0、返回管理员主菜单")
    A = input("\n请输入操作序号：")
    if A == '1':
        BrM_BorrowBook()
    elif A == '2':
        BrM_ReturnBook()
    elif A == '3':
        BrM_ReaderRechargeByAD()
    elif A == '4':
        BrM_AllBorrowNow()
    elif A == '5':
        BrM_Top10()
    elif A == '0':
        ManagerBase_4()
    else:
        print("\n借阅管理功能选择有误，请重新选择！")
        time.sleep(1)
        BrM_BorrowManage_5()


def BrM_BorrowBook():  # 借阅图书
    cls_scr()
    try:
        print("=====借阅图书=====")
        ID = input("\n请输入想要借书的读者的读者编号：")
        convert_reader_id(ID)  # 检查输入是否合法且读者是否存在,以避免浪费时间,避免后面输入了一大堆东西结果才发现读者不存在,若存在则将读者编号转换为整型
        cls_scr()
        cursor.execute("SELECT 读者信息.读者编号, 读者信息.数目限制, 当前借阅数量 FROM 读者信息,所有读者当前借阅图书数量视图 "
                       "WHERE 读者信息.读者编号 = 所有读者当前借阅图书数量视图.读者编号 "
                       "GROUP BY 读者信息.读者编号, 读者信息.数目限制, 当前借阅数量 "
                       "HAVING 读者信息.读者编号= '{}'".format(ID))
        print("\n#该读者当前借阅图书的数目情况如下：")  # 保护读者隐私,不宜公开显示读者姓名和借阅图书清单,显示借阅数目即可
        Display()
        pause()
        cls_scr()
        print("\n#当前馆内所有可供该读者借阅的图书的清单\n     (已去除当前已被该读者借阅的图书):")  # 便于管理员输入可借阅的ISBN
        cursor.execute("SELECT DISTINCT ISBN, 书名, 作者, 出版社 FROM 图书信息 "
                       "WHERE 状态 = '在馆' AND "
                       "ISBN NOT IN (SELECT ISBN FROM 借阅信息 WHERE 读者编号 = '{}' )".format(ID))
        Display()
        ISBN = input("请输入想要借阅的图书的ISBN号：")  # 从而得到该ISBN对应的'在馆'图书的清单,以便管理员选择图书编号
        convert_ISBN(ISBN)  # 检查输入是否合法且图书是否存在,以避免浪费时间,输入后面一大堆东西结果才发现图书不存在,若存在则将ISBN转换为整型
        cls_scr()  # 未排除不按照引导借阅的情况
        cursor.execute("SELECT * FROM 图书信息 WHERE ISBN = '{}' AND 状态 = '在馆'".format(ISBN))
        Display()
        BookID = input("\n请输入想要借阅的图书的编号：")  # 管理员任意选择一个'在馆'图书的编号
        convert_book_id(BookID)  # 检查输入是否合法且图书是否存在,若存在则将图书编号转换为整型(未排除不按照引导借阅的情况)
        cls_scr()
        cursor.execute("SELECT * FROM 图书信息 WHERE 图书编号 = '{}'".format(BookID))
        print("\n请确认图书信息：")  # 确认图书信息,防止借错了
        Display()
        choice = input("是否借阅？     [Y(y)/其他]")
        if choice == "Y" or choice == "y":
            cursor.execute("EXEC 图书借阅存储过程 '{}','{}'".format(ID, BookID))
        else:
            raise InterruptedError("借阅已取消！")

    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BrM_BorrowBook()
        else:
            BrM_BorrowManage_5()

    except InterruptedError as e:  # 如果读者取消借阅,则抛出异常
        cls_scr()
        print("\n中断原因：", e)
        time.sleep(1)
        choice = input("是否重新借阅？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BrM_BorrowBook()
        else:
            BrM_BorrowManage_5()
    except: #为执行SQL语句时的错误
        print("\n借阅失败! 可能的原因(未按上述引导借书):"
              "\n   1.没有该图书"
              "\n   2.该图书被全部借出"
              "\n   3.当前该读者已借阅该书,不可再次借阅同样的书"
              "\n   4.该读者借阅图书数量已达上限,请先归还部分图书")
        cursor.execute("SELECT * FROM 借阅信息 WHERE ISBN = '{}'".format(ISBN))
        print("\n该读者当前借阅该书(同ISBN图书)的情况:")
        Display()
        cursor.execute("SELECT 读者信息.读者编号, 读者信息.数目限制, 当前借阅数量 "
                       "FROM 读者信息,所有读者当前借阅图书数量视图 "
                       "WHERE 读者信息.读者编号 = 所有读者当前借阅图书数量视图.读者编号 "
                       "GROUP BY 读者信息.读者编号, 读者信息.数目限制, 当前借阅数量 "
                       "HAVING 读者信息.读者编号= '{}'".format(ID)) #由于在此不需要显示读者姓名且需要显示数目限制
        print("\n该读者当前借阅数目情况如下：")  # 保护读者隐私,不宜公开显示读者姓名和其他借阅图书清单
        Display()
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BrM_BorrowBook()
        else:
            BrM_BorrowManage_5()
    else:
        print("\n借阅成功!")
        time.sleep(1)
        choice = input("是否继续借阅？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BrM_BorrowBook()
        else:
            BrM_BorrowManage_5()


def BrM_ReturnBook():  # 归还图书
    cls_scr()
    try:
        print("=====归还图书=====")
        SQL = "SELECT 读者编号, 当前借阅数量 FROM 所有读者当前借阅图书数量视图"
        # 保护读者隐私,不宜公开显示读者姓名和借阅图书清单
        cursor.execute(SQL)
        print("\n所有读者当前借阅图书数量: ")
        Display()
        READERID = input("\n请输入想要归还图书的读者的读者编号：")
        convert_reader_id(READERID)  # 检查读者是否存在,不存在则抛出异常,以避免浪费时间,若存在则返回整型的读者编号
        cls_scr()
        cursor.execute("SELECT 图书编号, ISBN, 借阅日期, 应还日期 "
                       "FROM 借阅信息 WHERE 读者编号 = '{}'".format(READERID))
        # 查看该读者借阅图书清单,为保护隐私,未显示书名等信息
        print("\n该读者当前借阅情况如下：")
        Display()
        BOOKID = input("请输入图书编号进行归还(若空置则归还该读者当前借阅的所有图书)：")
        if BOOKID == "":
            pass
        else:
            convert_book_id(BOOKID)
        DATE = input("请输入归还日期(格式：YYYY-MM-DD,若空置则取当前时间)：")
        if BOOKID == "":
            if DATE == "":
                SQL = "EXEC 图书归还存储过程 '{}','{}',NULL,NULL "\
                    .format(adm_name, READERID)  # 按当前时间归还所借的所有书
            else:
                SQL = "EXEC 图书归还存储过程 '{}','{}',NULL,'{}' "\
                    .format(adm_name, READERID, DATE)  # 按指定时间归还所借的所有书
        else:
            convert_book_id(BOOKID)  # 检查图书是否存在,不存在则抛出异常,存在则则转换为整型
            if DATE == "":
                SQL = "EXEC 图书归还存储过程 '{}','{}','{}',NULL "\
                    .format(adm_name, READERID, BOOKID)  # 按当前时间归还指定书
            else:
                SQL = "EXEC 图书归还存储过程 '{}','{}','{}','{}' "\
                    .format(adm_name, READERID, BOOKID,DATE)  # 按指定时间归还指定书
        cursor.execute(SQL)  # 同时逾期多本图书可能会导致归还失败
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        print("\n是否重新输入？     [Y(y)/其他]\n")
        choice = input()
        if choice == "Y" or choice == "y":
            BrM_ReturnBook()
        else:
            BrM_BorrowManage_5()
    except:
        print(
            "\n归还失败!可能的原因:"
            "\n   1.该读者当前未借该图书(见上表)"
            "\n   2.该读者当前未借任何图书(见上表)"
            "\n   3.不可同时逾期多本图书"
            "\n   4.该读者当前余额不足以缴纳图书逾期罚款(见下表),请及时充值")
        cursor.execute("SELECT 读者编号, 余额 FROM 读者信息 "
                       "WHERE 读者编号 = '{}'".format(READERID))
        print("\n该读者当前余额信息: ")
        Display()  # 显示该读者当前余额,已确认有无余额变动
        time.sleep(3)
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BrM_ReturnBook()
        else:
            BrM_BorrowManage_5()
    else:
        print("\n归还成功!若管理员更改图书归还日期,则该操作已被记录!")
        time.sleep(1)
        cls_scr()
        cursor.execute("SELECT 图书编号, ISBN, 借阅日期, 应还日期 FROM 借阅信息 "
                       "WHERE 读者编号 = '{}'".format(READERID))
        # 查看该读者借阅图书清单,为保护隐私,未显示书名等信息
        print("\n该读者最新当前借阅情况如下：")
        Display()  # 展示还书的结果: 该读者当前借阅情况
        cursor.execute("SELECT 图书编号, ISBN, 借阅日期, 应还日期, 实还日期 FROM 历史借阅信息 "
                       "WHERE 读者编号 = '{}'".format(READERID))
        # 查看该读者借阅图书清单,为保护隐私,未显示书名等信息
        print("\n该读者最新历史借阅信息如下：")
        Display()  # 展示还书的结果: 该读者历史借阅情况
        pause()
        cls_scr()
        cursor.execute("SELECT TOP 1 变动金额, 变动日期, 管理员账号, 变动原因 "
                       "FROM 充值扣款记录 WHERE 读者编号 = '{}' "
                       "ORDER BY 记录编号 DESC".format(READERID))
        print("\n该读者最新一条充值扣款记录：")
        Display()  # 展示还书的结果: 该读者充值扣款记录,如果没有逾期,则无变动
        cursor.execute("SELECT TOP 1 管理员账号, 操作时间, 操作内容, 操作原因 FROM 管理员重要操作记录 "
                       "WHERE 受影响的读者编号 = '{}' "
                       "ORDER BY 记录编号 DESC".format(READERID))
        print("\n与该读者相关且为最新一条的管理员重要操作记录: ")
        Display()
        choice = input("是否继续归还？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BrM_ReturnBook()
        else:
            BrM_BorrowManage_5()


def BrM_ReaderRechargeByAD():  # 读者充值
    cls_scr()
    try:
        print("=====读者充值=====")
        ID = input("\n请输入读者编号：")
        convert_reader_id(ID)
        # 检查读者是否存在,任何情况下(输入格式错误,编号格式正确但是没有该读者都算)只要查不到读者信息就抛出异常,节省时间
        cursor.execute("EXEC 管理员查询读者信息存储过程 '{}'".format(ID))
        print("\n该读者当前信息如下：")
        Display()
        MONEY = input("请输入充值金额：")
        MONEY = convert_to_float(MONEY) # 检查输入金额是否为正整数或正小数
        if MONEY % 50 != 0:
            raise ValueError("充值金额必须为50的整数倍！")
        SQL = "EXEC 读者充值存储过程 '{}','{}','{}' ".format(adm_name, ID, MONEY)
        cursor.execute(SQL)
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        print("是否重新输入？     [Y(y)/其他]")
        choice = input()
        if choice == "Y" or choice == "y":
            BrM_ReaderRechargeByAD()
        else:
            BrM_BorrowManage_5()
    except:
        print("\n充值失败!未知错误!")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BrM_ReaderRechargeByAD()
        else:
            BrM_BorrowManage_5()
    else:
        print("\n充值成功!")
        cursor.execute("EXEC 管理员查询读者信息存储过程 '{}'".format(ID))
        print("\n该读者最新信息如下：")
        Display()
        time.sleep(1)
        choice = input("是否继续充值？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BrM_ReaderRechargeByAD()
        else:
            BrM_BorrowManage_5()


def BrM_AllBorrowNow():  # 浏览所有读者当前借阅图书数量
    cls_scr()
    try:
        print("=====浏览所有读者当前借阅图书数量=====")
        SQL = "SELECT * FROM 所有读者当前借阅图书数量视图"
        cursor.execute(SQL)
    except:
        print("\n查询失败!")
        choice = input("是否重新查询？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BrM_AllBorrowNow()
        else:
            BrM_BorrowManage_5()
    else:
        print("\n所有读者当前借阅图书数量如下：")
        Display()
        time.sleep(1)
        choice = input("是否回到上一级菜单？     [Y(y)/其他(返回管理员主菜单)]\n")
        if choice == "Y" or choice == "y":
            BrM_BorrowManage_5()
        else:
            ManagerBase_4()


def BrM_Top10():  # 浏览被借阅前10位的图书
    cls_scr()
    try:
        print("=====浏览被借阅前10位的图书=====")
        cursor.execute("SELECT * FROM 总借阅量TOP10视图")
    except:
        print("\n查询失败!")
        choice = input("是否重新查询？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            BrM_Top10()
        else:
            BrM_BorrowManage_5()
    else:
        print("\n被借阅前10位的图书如下：")
        Display()
        time.sleep(1)
        choice = input("是否回到上一级菜单？     [Y(y)/其他(返回管理员主菜单)]\n")
        if choice == "Y" or choice == "y":
            BrM_BorrowManage_5()
        else:
            ManagerBase_4()


def AM_AdminManage_5():
    cls_scr()
    print("===管理员管理===")
    print("\n1、管理员信息浏览")
    print("2、管理员修改登录密码")
    print("3、添加新管理员")
    print("4、删除管理员")
    print("0、返回管理员主菜单")
    A = input("请输入操作序号：")
    if A == '1':
        AM_AdInfo()
    elif A == '2':
        AM_AdChangePassword()
    elif A == '3':
        AM_AddAdmin()
    elif A == '4':
        AM_DeleteAdmin()
    elif A == '0':
        ManagerBase_4()
    else:
        print("\n管理员管理功能选择有误，请重新选择！")
        time.sleep(1)
        AM_AdminManage_5()

def Backup():   # 备份数据库（路径需根据本机修改，或改为运行时输入）
    try:
        # 备份路径：其他环境请修改为实际路径
        backup_path = r'C:\Users\LiXiuyin\Desktop\Restore\BackUp.bak'
        cursor.execute("BACKUP DATABASE BOOKS TO DISK = '{}'".format(backup_path.replace("'", "''")))
        print("\n数据库备份成功!")
    except pymssql.Error as e:
        print(f"备份失败: {str(e)}")
    finally:
        time.sleep(1)
        ManagerBase_4()

def Restore():  # 恢复数据库（路径需与 Backup 一致，其他环境请修改）
    try:
        restore_path = r'C:\Users\LiXiuyin\Desktop\Restore\BackUp.bak'
        cursor.execute("USE master")
        cursor.execute("RESTORE DATABASE BOOKS FROM DISK = '{}' WITH REPLACE".format(restore_path.replace("'", "''")))
        print("\n数据库恢复成功!")
        cursor.execute("USE BOOKS")
    except pymssql.Error as e:
        print(f"恢复失败: {str(e)}")
    finally:
        time.sleep(1)
        ManagerBase_4()

def AM_AdInfo():  # 管理员信息浏览
    cls_scr()
    try:
        print("=====管理员信息浏览=====")
        SQL = "EXEC 管理员信息浏览存储过程 '{}','{}' "\
            .format(adm_name, adm_password)  # 调用存储过程,验证当前账号密码
        cursor.execute(SQL)
    except:
        cls_scr()
        print("查询失败!")
        choice = input("是否重新查询？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            AM_AdInfo()
        else:
            AM_AdminManage_5()
    else:
        cls_scr()
        print("\n查询成功!")
        Display()
        choice = input("是否回到上一级菜单？     [Y(y)/其他(返回管理员主菜单)]\n")
        if choice == "Y" or choice == "y":
            AM_AdminManage_5()
        else:
            ManagerBase_4()


def AM_AdChangePassword():  # 管理员修改登录密码
    cls_scr()
    try:
        print("=====管理员修改登录密码=====")
        now_password = input("\n请输入当前密码：")  # 先校验当前密码，确认身份后再允许修改
        if not now_password.isalnum() or len(now_password) < 5 or len(now_password) > 20:
            raise ValueError("\n密码应由字母或数字组成,长度应在[5,20]内！")
        cursor.execute(
            "SELECT 1 AS ok FROM 管理员信息 WHERE 管理员账号 = N'{}' AND 管理员密码 = N'{}'"
            .format(_sql_escape(adm_name), _sql_escape(now_password))
        )
        if len(cursor.fetchall()) == 0:
            raise ValueError("当前密码错误！")
        new_password = input("\n请输入管理员新密码(5到20位):")
        if not new_password.isalnum() or len(new_password) < 5 or len(new_password) > 20:
            raise ValueError("\n密码应由字母或数字组成,长度应在[5,20]内！")
        if new_password == now_password:
            raise ValueError("新密码不能与当前密码相同！")
        sql = (
            "EXEC 管理员修改自己密码存储过程 N'{}',N'{}',N'{}'"
            .format(_sql_escape(adm_name), _sql_escape(now_password), _sql_escape(new_password))
        )
        cursor.execute(sql)
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            AM_AdChangePassword()
        else:
            AM_AdminManage_5()
    except Exception as e:
        cls_scr()
        print("\n修改失败:", str(e))
        choice = input("是否重新修改？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            AM_AdChangePassword()
        else:
            AM_AdminManage_5()
    else:
        cls_scr()
        print("\n管理员", adm_name, "的密码修改成功!")
        time.sleep(1)
        print("\n您当前登录已失效,请按任意键重新登录\n")
        pause()
        ManagerLogin_3()


def AM_AddAdmin():  # 添加新管理员
    cls_scr()
    try:
        print("=====添加新管理员=====")
        # 仅主管理员(是否为主管理员=1)可添加，由存储过程校验
        newadm_name = input("\n请输入新管理员账号:")
        if not newadm_name.isalnum() or len(newadm_name) > 20 or len(newadm_name) < 5:
            raise ValueError("\n账号应由字母或数字组成,长度应在[5,20]内！")
        cursor.execute("SELECT * FROM 管理员信息 WHERE 管理员账号 = '{}'".format(newadm_name))
        if len(cursor.fetchall()) != 0:
            raise ValueError("\n该账号已存在！")
        newadm_password = input("\n请输入新管理员密码(5到20位数字与字母):")
        if not newadm_password.isalnum() or len(newadm_password) < 5 or len(newadm_password) > 20:
            raise ValueError("\n密码应由字母或数字组成,长度应在[5,20]内！")
        is_primary = input("是否设为主管理员？(主管理员可添加/删除其他管理员) [Y(y)/其他:普通管理员]: ")
        is_primary_bit = 1 if (is_primary == "Y" or is_primary == "y") else 0
        SQL = "EXEC 添加管理员存储过程 '{}','{}',{},'{}' ".format(adm_name, newadm_name, is_primary_bit, newadm_password)
        cursor.execute(SQL)
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            AM_AddAdmin()
        else:
            AM_AdminManage_5()
    except:
        cls_scr()
        print("\n添加失败!未知错误!")
        choice = input("是否重新添加？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            AM_AddAdmin()
        else:
            AM_AdminManage_5()
    else:
        cls_scr()
        cursor.execute("SELECT TOP 1 * FROM 管理员重要操作记录 ORDER BY 记录编号 DESC")
        print("\n添加成功!本次操作已被记录如下: ")
        Display()
        choice = input("是否回到上一级菜单？     [Y(y)/其他(返回管理员主菜单)]\n")
        if choice == "Y" or choice == "y":
            AM_AdminManage_5()
        else:
            ManagerBase_4()


def AM_DeleteAdmin():  # 删除管理员,用于某管理员辞职后让其他管理员删除自己的账户(但重要操作记录是永久保存的)
    cls_scr()
    try:
        print("=====删除管理员=====")
        # 仅主管理员(是否为主管理员=1)可删除其他管理员，由存储过程校验
        deladm_name = input("\n请输入要删除的管理员账号:")
        if deladm_name == adm_name:
            raise ValueError("\n不能删除当前登录的管理员账号!")
        if not deladm_name.isalnum() or len(deladm_name) > 20 or len(deladm_name) < 5:
            raise ValueError("\n账号应由字母或数字组成,长度应在[5,20]内！")
        cursor.execute("SELECT * FROM 管理员信息 WHERE 管理员账号 = '{}'".format(deladm_name))
        if len(cursor.fetchall()) != 1:
            raise ValueError("\n该管理员不存在!")
        deladm_pass = input("请输入要删除的管理员账号的密码:")
        if not deladm_pass.isalnum() or len(deladm_pass) < 5 or len(deladm_pass) > 20:
            raise ValueError("\n密码应由字母或数字组成,长度应在[5,20]内！")
        reason = input("请输入删除原因:")  # 删除管理员时需要输入删除原因,以便记录,不可空
        if reason == "" or len(reason) > 100:
            raise ValueError("\n删除原因不能为空且不能超过100字!")
        SQL = "EXEC 删除管理员存储过程 '{}','{}','{}','{}' ".format(adm_name, deladm_name, deladm_pass, reason)
        cursor.execute(SQL)
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新输入？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            AM_DeleteAdmin()
        else:
            AM_AdminManage_5()
    except:
        cls_scr()
        print("\n删除失败!账户密码验证失败!")
        choice = input("\n是否重新删除？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            AM_DeleteAdmin()
        else:
            AM_AdminManage_5()
    else:
        cls_scr()
        cursor.execute("SELECT TOP 1 * FROM 管理员重要操作记录 ORDER BY 记录编号 DESC")
        print("\n删除成功!本次操作已被记录如下: ")
        Display()
        choice = input("是否回到上一级菜单？     [Y(y)/其他(返回管理员主菜单)]\n")
        if choice == "Y" or choice == "y":
            AM_AdminManage_5()
        else:
            ManagerBase_4()


def R_ReaderInfo_5r():
    try:
        print("=====读者信息浏览=====")
        SQL = "EXEC 读者查询个人信息存储过程 '{}','{}'"\
            .format(user_id, user_password)
        cursor.execute(SQL)
    except:
        cls_scr()
        print("\n查询失败!")
        choice = input("是否重新查询？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            R_ReaderInfo_5r()
        else:
            ReaderBase_4()
    else:
        cls_scr()
        print("\n您的个人信息:")
        Display()
        print("\n请按任意键返回读者主菜单\n")
        pause()
        ReaderBase_4()


def R_ReaderBookSearch_5r():
    cls_scr()
    print("=====读者图书查询=====")
    print("\n输入图书名、作者或出版社以浏览对应的图书列表")
    try:
        time.sleep(1)
        allinone = input("\n请输入：")
        print("\n为避免查询误差,请选择输入的类型:")  # 有可能书名为人名
        print("\n1、图书名")
        print("2、作者")
        print("3、出版社")
        A = input("\n请输入操作序号：")
        print("\n查询结果:")
        if A == '1':
            SQL = "EXEC 读者查询图书信息存储过程 '{}', NULL, NULL".format(allinone)
            cls_scr()
            print("\n图书名为", allinone, "的图书列表:")
        elif A == '2':
            SQL = "EXEC 读者查询图书信息存储过程 NULL, '{}', NULL".format(allinone)
            cls_scr()
            print("\n作者为", allinone, "的图书列表:")
        elif A == '3':
            SQL = "EXEC 读者查询图书信息存储过程 NULL, NULL, '{}'".format(allinone)
            cls_scr()
            print("\n出版社为", allinone, "的图书列表:")
        else:
            raise InterruptedError("输入类型选择错误!")
        cursor.execute(SQL)
    except InterruptedError as e:
        print("\n中断原因：", e)
        choice = input("是否重新查询？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            R_ReaderBookSearch_5r()
        else:
            ReaderBase_4()
    except:
        cls_scr()
        print("\n查询失败!在该条件下未找到任何图书!")
        choice = input("是否重新查询？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            R_ReaderBookSearch_5r()
        else:
            ReaderBase_4()
    else:
        Display()
        time.sleep(1)
        print("\n请按任意键返回读者主菜单\n")
        pause()
        ReaderBase_4()


def R_BorrowInfoNow_5r():  # 读者当前借阅信息浏览
    cls_scr()
    try:
        print("=====读者当前借阅信息浏览=====")
        SQL = "EXEC 读者查询当前借阅信息存储过程 '{}','{}'".format(user_id, user_password)
        cursor.execute(SQL)
    except:
        cls_scr()
        print("\n查询失败!")
        choice = input("是否重新查询？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            R_BorrowInfoNow_5r()
        else:
            ReaderBase_4()
    else:
        cls_scr()
        print("\n您当前的借阅信息:")
        Display()
        time.sleep(1)
        print("\n请按任意键返回读者主菜单\n")
        pause()
        ReaderBase_4()


def R_BorrowInfoHistory_5r():  # 读者查询历史借阅信息
    cls_scr()
    try:
        print("=====读者历史借阅信息浏览=====")
        SQL = "EXEC 读者查询历史借阅信息存储过程 '{}','{}'".format(user_id, user_password)
        cursor.execute(SQL)
    except:
        cls_scr()
        print("\n查询失败!")
        choice = input("是否重新查询？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            R_BorrowInfoHistory_5r()
        else:
            ReaderBase_4()
    else:
        cls_scr()
        print("\n您的历史借阅信息:")
        Display()
        time.sleep(1)
        print("\n请按任意键返回读者主菜单\n")
        pause()
        ReaderBase_4()


def R_RechargeInfo_5r():  # 读者充值信息浏览
    cls_scr()
    try:
        print("=====读者充值扣款信息浏览=====")
        SQL = "EXEC 读者查询充值扣款信息存储过程 '{}','{}'".format(user_id, user_password)
        cursor.execute(SQL)
    except:
        cls_scr()
        print("\n查询失败!")
        choice = input("是否重新查询？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            R_RechargeInfo_5r()
        else:
            ReaderBase_4()
    else:
        cls_scr()
        print("\n您的充值扣款信息:")
        Display()
        time.sleep(1)
        print("\n请按任意键返回读者主菜单\n")
        pause()
        ReaderBase_4()


def R_ReaderPassword_5r():  # 读者修改登录密码
    cls_scr()
    print("===读者修改登录密码===")
    try:
        old_password = input("\n请输入您的旧密码:")
        cursor.execute(
            "SELECT 1 AS ok FROM 读者信息 WHERE 读者编号 = {} AND 密码 = N'{}'"
            .format(user_id, _sql_escape(old_password))
        )
        if len(cursor.fetchall()) == 0:
            raise ValueError("旧密码错误!")
        new_password = input("\n请输入您将要修改的新密码:")
        if new_password == user_password:
            raise ValueError("新密码与旧密码相同!")
        if len(new_password) < 8 or len(new_password) > 20 or not new_password.isalnum():
            raise ValueError("新密码应由英文与数字组成,长度在[8,20]内!")
        sql = (
            "EXEC 读者修改登录密码存储过程 N'{}',N'{}',N'{}'"
            .format(_sql_escape(str(user_id)), _sql_escape(old_password), _sql_escape(new_password))
        )
        cursor.execute(sql)
    except ValueError as e:
        print("\n错误原因: ", e, "\n")
        choice = input("是否重新修改？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            R_ReaderPassword_5r()
        else:
            ReaderBase_4()
    except Exception as e:
        cls_scr()
        print("\n修改失败:", str(e))
        choice = input("是否重新修改？     [Y(y)/其他]\n")
        if choice == "Y" or choice == "y":
            R_ReaderPassword_5r()
        else:
            ReaderBase_4()
    else:
        cls_scr()
        print("\n读者", user_id, "的密码修改成功!")
        time.sleep(1)
        print("\n您当前登录已失效,请按任意键重新登录\n")
        pause()
        ReaderLogin_3()

if __name__ == '__main__':
    try:
        HomePage_1()
    except SystemExit as e:
        # 用户选择 0 退出时调用 exit(0)，让其正常退出
        sys.exit(e.code if e.code is not None else 0)
    except KeyboardInterrupt:
        print("\n\n已中断，退出程序。")
        sys.exit(130)
    except Exception as e:
        # 避免未捕获异常时打印整条 "During handling of the above exception" 调用链
        print("\n程序异常退出:", e)
        sys.exit(1)
