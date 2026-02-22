USE BOOKS
--ALTER DATABASE BOOKS SET SINGLE_USER WITH ROLLBACK IMMEDIATE
USE MASTER
DROP DATABASE IF EXISTS BOOKS   --如果数据库存在,则删除;否则建立数据库
GO

-- 下方路径适用于 Docker 容器（docker.sh 使用命名卷 sqledge-data 挂载为容器内 /var/opt/mssql，含 data/log）。
-- 使用支持中文的排序规则，确保中文正常存储与显示。
CREATE DATABASE BOOKS
    ON PRIMARY
    (   NAME = 'BOOKS',
        FILENAME = '/var/opt/mssql/data/BOOK.mdf',
        SIZE = 10MB,
        MAXSIZE = 1TB,
        FILEGROWTH = 5%
        )
    LOG ON
    (   NAME = 'BOOKS_log',
        FILENAME = '/var/opt/mssql/log/BOOK_log.ldf',
        SIZE = 10MB,
        MAXSIZE = 1TB,
        FILEGROWTH = 5%
        )
    COLLATE Chinese_PRC_CI_AS
GO

USE BOOKS
DROP TABLE IF EXISTS 备份恢复记录,管理员重要操作记录,充值扣款记录,管理员信息,历史借阅信息,借阅信息,读者信息,图书信息,图书分类

CREATE TABLE 图书分类
(
    分类编码 nvarchar(10) NOT NULL,
    分类名称 nvarchar(100) NOT NULL,
    CONSTRAINT PK_分类编码 PRIMARY KEY CLUSTERED (分类编码),    --显式地创建主键聚集索引
    CONSTRAINT CK_分类编码 CHECK (分类编码 LIKE '[A-Z]'),
    CONSTRAINT CK_分类名称 CHECK (LEN(分类名称) > 0)
)
GO
CREATE TABLE 图书信息
(
    图书编号 int IDENTITY(1,1), --图书编号int类型容量完全足够,自增(不打开开关则不允许修改),从1开始,步长为1,不允许为空
    分类编码 nvarchar(10) NOT NULL,
    ISBN bigint NOT NULL,
    书名 nvarchar(50) NOT NULL,   --部分书名比较长,所以设置为nvarchar(50)
    作者 nvarchar(20) NOT NULL,   --部分书的作者可能有几位,所以设置为nvarchar(20),容纳20个中英文字符
    出版社 nvarchar(20) NULL,
    出版日期 date NULL,     --出版日期可以为空(即表示1900-01-01)
    单价 decimal(10,2) NOT NULL,  --decimal(10,2)表示10位数字,其中2位小数,保证精度
    简介 nvarchar(100) NULL,  --关于图书的简介,100字以内,也可以为空
    状态 nvarchar(2) NOT NULL DEFAULT '在馆',       --默认值为'在馆'
    CONSTRAINT PK_ISBN PRIMARY KEY CLUSTERED (图书编号),     --显式地创建主键聚集索引(非空,唯一,不重复)
    CONSTRAINT FK_分类编码 FOREIGN KEY (分类编码) REFERENCES 图书分类(分类编码) ON DELETE CASCADE,
    CONSTRAINT CK_ISBN CHECK (LEN(ISBN) IN (10,13)),   --ISBN长度为10(未加978)或13(978开头)
    CONSTRAINT CK_单价 CHECK (单价 >= 0),
    CONSTRAINT CK_状态 CHECK (状态 IN ('在馆','借出','丢失','损坏'))
    --状态只能为'在馆','借出','丢失','损坏'(只有状态为'在馆'的图书才能借出)
)

CREATE TABLE 读者信息
(
    读者编号 bigint NOT NULL,
    姓名 nvarchar(20) NOT NULL,   --部分外国人或国内少数民族同胞的姓名会很长,所以设置为nvarchar(20)
    性别 nvarchar(1) NOT NULL,
    类型 nvarchar(3) NOT NULL,    --类型不能为空,否则无法激发'借阅权限生成触发器'
    数目限制 smallint NULL,     --数目限制暂时可为空,以实现在插入读者信息后由触发器自动赋值,以免无法插入读者信息
    时间限制 smallint NULL,     --时间限制暂时可为空,以实现在插入读者信息后由触发器自动赋值,以免无法插入读者信息
    联系方式 nvarchar(20) NOT NULL,
    余额 decimal(10,2) NOT NULL,      --最多为十位数字,其中两位为小数,保证精度(money小数位数太多,不合适)
    密码 nvarchar(20) NULL,
    CONSTRAINT PK_读者编号 PRIMARY KEY CLUSTERED (读者编号),    --显式地创建主键聚集索引
    CONSTRAINT CK_读者编号 CHECK (LEN(读者编号) IN (6,10)),    --读者编号长度为6(研究生或教师)或10(本科生或其他)
    CONSTRAINT CK_性别 CHECK (性别 IN ('男','女')),
    CONSTRAINT CK_类型 CHECK (类型 IN ('教师','研究生','本科生','其他')),
    CONSTRAINT CK_余额 CHECK (余额 >= 0),
    CONSTRAINT CK_密码长度限制 CHECK (LEN(密码) >= 8 AND LEN(密码) <= 20), --密码长度限制为8-20,保证密码安全
    CONSTRAINT CK_类型与编号限制 CHECK(类型 = '教师' AND LEN(读者编号) = 6
        OR 类型 = '研究生' AND LEN(读者编号) = 6
        OR 类型 = '本科生' AND LEN(读者编号) = 10
        OR 类型 = '其他' AND LEN(读者编号) = 10)    --类型要与读者编号长度限制相对应,教师和研究生为6位,本科生和其他为10位
    --这样也限制了在修改读者信息时读者类型只能在'本科生'和'其他'之间,'研究生'和'教师'之间互相改
)

CREATE TABLE 借阅信息
(
    借阅编号 int IDENTITY(1,1) NOT NULL,
    图书编号 int NOT NULL,
    ISBN bigint NOT NULL,
    读者编号 bigint NOT NULL,
    借阅日期 date NOT NULL,   --这里参考了山大图书馆,借阅时间没必要精确到某一秒.借阅日期不能为空,永远为当前日期(在借阅图书时由GETDATE()实现)
    应还日期 date NULL, --应还日期为借阅日期+时间限制,时间限制为读者信息表中的时间限制,此处暂时为NULL,其后由'应还日期填充触发器'自动计算并填充
    CONSTRAINT PK_借阅编号 PRIMARY KEY (借阅编号),  --隐式地创建主键聚集索引(因为没有其他的聚集索引而又没硬性规定为非聚集索引)
    CONSTRAINT FK_图书编号 FOREIGN KEY (图书编号) REFERENCES 图书信息(图书编号),
    CONSTRAINT FK_读者编号 FOREIGN KEY (读者编号) REFERENCES 读者信息(读者编号)
    --不用ON DELETE CASCADE,因为不应该删除借阅信息,会造成图书馆财产损失
)

CREATE TABLE 历史借阅信息
(
    历史借阅编号 int IDENTITY(1,1) NOT NULL,
    图书编号 int NOT NULL,
    ISBN bigint NOT NULL,
    读者编号 bigint NOT NULL,
    借阅日期 date NOT NULL,
    应还日期 date NOT NULL,
    实还日期 date NOT NULL,
    CONSTRAINT PK_借阅编号_历史 PRIMARY KEY (历史借阅编号),
    CONSTRAINT FK_图书编号_历史 FOREIGN KEY (图书编号) REFERENCES 图书信息(图书编号)  ON DELETE CASCADE,
    --删除图书信息时,删除其对应的历史借阅信息
    CONSTRAINT FK_读者编号_历史 FOREIGN KEY (读者编号) REFERENCES 读者信息(读者编号) ON DELETE CASCADE,
    --级联删除,删除读者信息时,其历史借阅信息也会被自动删除(按照题目要求)
    CONSTRAINT CK_实还日期 CHECK (实还日期>=借阅日期)   --实还日期必须大于等于借阅日期
)

CREATE TABLE 管理员信息
(
    管理员编号 int IDENTITY(1,1) NOT NULL,
    是否为主管理员 bit NOT NULL DEFAULT 0,   --默认为0,即不是主管理员
    管理员账号 nvarchar(20) NOT NULL,
    管理员密码 nvarchar(20) NOT NULL,
    CONSTRAINT PK_管理员编号 PRIMARY KEY (管理员编号),
    CONSTRAINT UQ_管理员账号 UNIQUE (管理员账号),   --管理员账号唯一,作为登录账号
    CONSTRAINT CK_管理员密码长度限制 CHECK (LEN(管理员密码) >= 5 AND LEN(管理员密码) <= 20)  --管理员密码限制为长度为5-20的字符串
)

CREATE TABLE 充值扣款记录
(
    记录编号 int IDENTITY(1,1) NOT NULL,
    读者编号 bigint NOT NULL,
    变动金额 decimal(10,2) NOT NULL,
    变动日期 date NOT NULL DEFAULT SYSDATETIME(),
    管理员账号 nvarchar(20) NOT NULL,
    变动原因 nvarchar(100) NOT NULL, --必须记录变动原因,以便于后期追溯时管理员进行回忆和解释
    CONSTRAINT PK_记录编号_余额 PRIMARY KEY (记录编号),
    CONSTRAINT PK_读者编号_余额 FOREIGN KEY (读者编号) REFERENCES 读者信息(读者编号) ON DELETE CASCADE
    --级联删除,删除读者信息时,其充值扣款记录也会被删除(按照题目要求)
)

CREATE TABLE 管理员重要操作记录
    --需要永久保存以方便追溯而不应该随着读者信息和管理员信息等内容的删除而删除,因此不需要设置外键
    --牺牲了一定的完整性,但是不影响主要功能,换来了较高独立性和安全性(重要操作记录永久可追溯追责)
(
    记录编号 int IDENTITY(1,1) NOT NULL,
    管理员账号 nvarchar(20) NOT NULL,
    受影响的读者编号 bigint NULL,   --不设读者编号外键.因为管理员可以删除读者信息,但是管理员不应该删除这项操作的记录,以免造成追溯不便
    受影响的管理员账号 nvarchar(20) NULL,   --不设管理员账号外键.因为admin管理员可以删除管理员信息,但是管理员不应该删除这项操作的记录,以免造成追溯不便
    操作时间 datetime NOT NULL,     --操作时间和时间,相比图书借阅时的date格式,这个更加精确
    操作内容 nvarchar(50) NOT NULL, --对读者造成较大影响的操作的内容,比如删除读者信息,更改读者信息,自定读者归还图书的时间等
    操作原因 nvarchar(100) NOT NULL, --必须记录操作内容和操作原因,以便于后期追溯
    CONSTRAINT CK_操作内容不为空 CHECK (LEN(操作内容) > 0),
    CONSTRAINT CK_操作原因不为空 CHECK (LEN(操作原因) > 0),
    CONSTRAINT PK_记录编号_管理员重要操作记录 PRIMARY KEY (记录编号)
)
GO

CREATE TABLE 备份恢复记录
(
    备份编号 int IDENTITY(1,1) NOT NULL,
    备份时间 datetime NULL,
    备份路径 nvarchar(100) NULL,
    恢复时间 datetime NULL,
    恢复路径 nvarchar(100) NULL,
    CONSTRAINT PK_备份编号 PRIMARY KEY (备份编号),
    CONSTRAINT CK_备份还原记录有效性 CHECK
        (
            (备份时间 IS NOT NULL AND 备份路径 IS NOT NULL AND 恢复时间 IS NULL AND 恢复路径 IS NULL)
            OR
            (备份时间 IS NULL AND 备份路径 IS NULL AND 恢复时间 IS NOT NULL AND 恢复路径 IS NOT NULL)
        )
)

CREATE NONCLUSTERED INDEX IX_图书信息_ISBN ON 图书信息 (ISBN)
CREATE NONCLUSTERED INDEX IX_借阅信息_读者借阅 ON  借阅信息(读者编号,图书编号,ISBN)
CREATE NONCLUSTERED INDEX IX_历史借阅信息_读者借阅 ON 历史借阅信息(读者编号,图书编号,ISBN)
CREATE NONCLUSTERED INDEX IX_充值扣款信息_读者充值 ON 充值扣款记录(读者编号)
GO

CREATE TRIGGER 借阅权限生成触发器 ON 读者信息        --根据身份类型生成借阅权限,更新读者信息表中的数目限制与时间限制
    FOR INSERT,UPDATE
    AS
BEGIN
    -- 仅更新本次插入或修改的行,按类型设置数目限制与时间限制
    UPDATE r SET
        r.数目限制 = CASE i.类型 WHEN N'教师' THEN 15 WHEN N'研究生' THEN 10 WHEN N'本科生' THEN 5 ELSE 5 END,
        r.时间限制 = CASE i.类型 WHEN N'教师' THEN 180 WHEN N'研究生' THEN 180 WHEN N'本科生' THEN 60 ELSE 30 END
    FROM 读者信息 r INNER JOIN INSERTED i ON r.读者编号 = i.读者编号
END
GO

CREATE TRIGGER 数目超限警告触发器 ON 借阅信息
    FOR INSERT
    AS
BEGIN
    DECLARE @在借图书数量 smallint;
    DECLARE @数目限制 smallint;
    DECLARE @读者编号 int;

    -- 从插入的记录中获取读者编号
    SELECT @读者编号 = 读者编号 FROM INSERTED;

    -- 获取在借图书数量和数目限制
    SELECT @在借图书数量 = COUNT(借阅编号), @数目限制 = 数目限制
    FROM 借阅信息
             INNER JOIN 读者信息 ON 借阅信息.读者编号 = 读者信息.读者编号
    WHERE 借阅信息.读者编号 = @读者编号
    GROUP BY 数目限制;

    -- 检查是否超过限制
    IF @在借图书数量 > @数目限制
        BEGIN
            RAISERROR('在借图书数量超过限制 (%d 本), 请先归还部分书籍再借阅!', 16, 1, @数目限制)
            ROLLBACK;  -- 回滚事务
        END
END;
GO


CREATE TRIGGER 应还日期填充触发器 ON 借阅信息 --借阅图书时,自动填充应还日期(仅针对本次插入或修改的行)
    FOR INSERT,UPDATE
    AS
BEGIN
    UPDATE b SET b.应还日期 = DATEADD(day, r.时间限制, b.借阅日期)
    FROM 借阅信息 b INNER JOIN INSERTED i ON b.借阅编号 = i.借阅编号
    INNER JOIN 读者信息 r ON r.读者编号 = b.读者编号
END
GO

CREATE TRIGGER 逾期扣款触发器 ON 历史借阅信息
    FOR INSERT
    AS
BEGIN
    -- 支持一次插入多条历史借阅：对所有逾期记录按读者汇总罚款，校验余额后统一扣款并写入充值扣款记录
    IF NOT EXISTS(SELECT * FROM INSERTED WHERE 实还日期 > 应还日期)
        RETURN;
    DECLARE @OverdueTable TABLE (读者编号 bigint, 逾期天数 int, 罚款金额 decimal(10,2))
    INSERT INTO @OverdueTable (读者编号, 逾期天数, 罚款金额)
    SELECT 读者编号, DATEDIFF(DAY, 应还日期, 实还日期), 0.1 * DATEDIFF(DAY, 应还日期, 实还日期)
    FROM INSERTED WHERE 实还日期 > 应还日期
    -- 检查每位读者余额是否足够支付其所有逾期罚款
    IF EXISTS (
        SELECT 1 FROM (
            SELECT 读者编号, SUM(罚款金额) AS 总罚款 FROM @OverdueTable GROUP BY 读者编号
        ) o INNER JOIN 读者信息 r ON r.读者编号 = o.读者编号 WHERE r.余额 < o.总罚款
    )
    BEGIN
        ROLLBACK TRANSACTION
        RAISERROR('余额不足,请充值!',16,1)
        RETURN
    END
    BEGIN TRANSACTION
    BEGIN TRY
        UPDATE r SET r.余额 = r.余额 - o.总罚款
        FROM 读者信息 r
        INNER JOIN (SELECT 读者编号, SUM(罚款金额) AS 总罚款 FROM @OverdueTable GROUP BY 读者编号) o ON r.读者编号 = o.读者编号
        INSERT INTO 充值扣款记录(读者编号,变动金额,变动日期,管理员账号,变动原因)
        SELECT 读者编号, -罚款金额, GETDATE(), 'admin', '逾期罚款' FROM @OverdueTable
        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION
        RAISERROR('逾期扣款失败!',16,1)
    END CATCH
END
GO

CREATE TRIGGER 禁止修改历史借阅信息触发器 ON 历史借阅信息      --借阅历史只能添加、删除不能修改
    INSTEAD OF UPDATE
    AS
BEGIN
    RAISERROR('禁止修改历史借阅信息!',16,1)
    ROLLBACK TRANSACTION
END
GO

CREATE TRIGGER 禁止更新删除管理员重要操作记录触发器 ON 管理员重要操作记录
    --管理员对读者密码的重置和对读者余额的修改等事关读者切身利益的操作都将被记录在管理员重要操作记录表中(管理员也可以主动记录其他重要事件)
    --出于对读者权益的保护和对管理员行为的规范,禁止任何人修改或者删除这类记录,以防止管理员违规操作,损害读者权益
    INSTEAD OF UPDATE,DELETE    --此触发器内部内容代替通常的触发动作,即只报错,而不执行UPDATE与DELETE命令,从而禁止修改和删除
    AS
BEGIN
    RAISERROR('禁止任何人对管理员重要操作记录进行任何改动或删除!',16,1)
    ROLLBACK TRANSACTION
END
GO

CREATE TRIGGER 禁止更新充值扣款记录触发器 ON 充值扣款记录
    --禁止任何人修改或者删除充值扣款记录,以防止管理员瞎搞,损害读者权益
    INSTEAD OF UPDATE
    AS
BEGIN
    RAISERROR('禁止对充值扣款记录进行更新!',16,1)
    ROLLBACK TRANSACTION
END
GO

-- 与 init.py 一致：先删视图与存储过程，便于重复执行
DROP VIEW IF EXISTS 所有读者当前借阅图书数量视图
DROP VIEW IF EXISTS 总借阅量TOP10视图
DROP PROCEDURE IF EXISTS 图书上架存储过程
DROP PROCEDURE IF EXISTS 图书下架存储过程
DROP PROCEDURE IF EXISTS 创建管理员重要操作存储过程
DROP PROCEDURE IF EXISTS 管理员修改图书信息存储过程
DROP PROCEDURE IF EXISTS 管理员浏览图书信息存储过程
DROP PROCEDURE IF EXISTS 管理员添加读者存储过程
DROP PROCEDURE IF EXISTS 管理员删除读者存储过程
DROP PROCEDURE IF EXISTS 管理员修改读者信息存储过程
DROP PROCEDURE IF EXISTS 管理员查询读者信息存储过程
DROP PROCEDURE IF EXISTS 管理员重置读者密码存储过程
DROP PROCEDURE IF EXISTS 管理员查看重要操作记录存储过程
DROP PROCEDURE IF EXISTS 图书借阅存储过程
DROP PROCEDURE IF EXISTS 图书归还存储过程
DROP PROCEDURE IF EXISTS 读者充值存储过程
DROP PROCEDURE IF EXISTS 管理员信息浏览存储过程
DROP PROCEDURE IF EXISTS 添加管理员存储过程
DROP PROCEDURE IF EXISTS 删除管理员存储过程
DROP PROCEDURE IF EXISTS 管理员修改自己密码存储过程
DROP PROCEDURE IF EXISTS 读者查询个人信息存储过程
DROP PROCEDURE IF EXISTS 读者修改登录密码存储过程
DROP PROCEDURE IF EXISTS 读者查询当前借阅信息存储过程
DROP PROCEDURE IF EXISTS 读者查询历史借阅信息存储过程
DROP PROCEDURE IF EXISTS 读者查询充值扣款信息存储过程
DROP PROCEDURE IF EXISTS 备份数据库存储过程
DROP PROCEDURE IF EXISTS 恢复数据库存储过程
DROP PROCEDURE IF EXISTS 读者查询图书信息存储过程
GO

CREATE VIEW 所有读者当前借阅图书数量视图
AS
SELECT 读者信息.读者编号,读者信息.姓名,读者信息.性别,读者信息.类型,
       COUNT(借阅信息.借阅编号) AS 当前借阅数量
FROM 读者信息,借阅信息
WHERE 读者信息.读者编号=借阅信息.读者编号
GROUP BY 读者信息.读者编号,读者信息.姓名,读者信息.性别,读者信息.类型
GO

CREATE VIEW 总借阅量TOP10视图
AS
SELECT TOP 10 图书信息.ISBN,图书信息.书名,图书信息.作者,图书信息.出版社,
              COUNT(DISTINCT 借阅信息.借阅编号) AS 当前借阅量,
              COUNT(DISTINCT 历史借阅信息.历史借阅编号) AS 历史借阅量,
              COUNT(DISTINCT 借阅信息.借阅编号)+COUNT(DISTINCT 历史借阅信息.历史借阅编号) AS 总借阅量
FROM 图书信息 LEFT JOIN 借阅信息 ON 图书信息.ISBN=借阅信息.ISBN,历史借阅信息
WHERE 图书信息.ISBN=历史借阅信息.ISBN
GROUP BY 图书信息.ISBN,图书信息.书名,图书信息.作者,图书信息.出版社
ORDER BY 总借阅量 DESC
GO

CREATE PROCEDURE 图书上架存储过程
(
    @分类编码 nvarchar(10),
    @ISBN bigint,
    @书名 nvarchar(50),
    @作者 nvarchar(20),
    @出版社 nvarchar(20),
    @出版日期 date,
    @单价 float,
    @简介 nvarchar(100),
    @上架数量 smallint
)
AS
BEGIN
    IF @上架数量 <= 0
        BEGIN
            RAISERROR('上架数量不能小于等于0!', 16, 1)
            RETURN
        END
    DECLARE @转换后单价 decimal(10,2) = CAST(@单价 AS decimal(10,2))
    BEGIN TRANSACTION
        BEGIN TRY
            WHILE @上架数量 > 0
                BEGIN
                    INSERT INTO 图书信息(分类编码, ISBN, 书名, 作者, 出版社, 出版日期, 单价, 简介)
                    VALUES(@分类编码, @ISBN, @书名, @作者, @出版社, @出版日期, @转换后单价, @简介)
                    SET @上架数量 = @上架数量 - 1
                END
            COMMIT TRANSACTION
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION
            RAISERROR('上架过程中出现错误!', 16, 1)
        END CATCH
END
GO



CREATE PROCEDURE 图书下架存储过程
(
    @图书编号或ISBN nvarchar(13)
)
AS
BEGIN
    DECLARE @转换后 bigint = TRY_CAST(@图书编号或ISBN AS bigint)
    IF @转换后 IS NULL
        BEGIN
            RAISERROR('输入无效，请重新输入!', 16, 1)
            RETURN
        END
    ELSE IF LEN(@图书编号或ISBN) IN (10, 13)  -- 判断输入的是否为ISBN
        BEGIN
            IF EXISTS(SELECT * FROM 图书信息 WHERE ISBN = @转换后 AND 状态 = '借出')
                RAISERROR ('该ISBN存在未归还图书，请归还后再删除!', 16, 1)
            ELSE
                DELETE FROM 图书信息 WHERE ISBN = @转换后 AND 状态 != '借出'
        END
    ELSE
        BEGIN
            IF EXISTS(SELECT * FROM 图书信息 WHERE 图书编号 = @转换后 AND 状态 != '借出')
                BEGIN
                    DELETE FROM 借阅信息 WHERE 图书编号 = @转换后
                    DELETE FROM 图书信息 WHERE 图书编号 = @转换后
                END
            ELSE
                BEGIN
                    RAISERROR('该图书已被借出，请归还后再删除!', 16, 1)
                END
        END
END
GO


CREATE PROCEDURE 创建管理员重要操作存储过程
(
    @管理员账号 nvarchar(20),
    @受影响的读者编号 bigint,   --添加读者、删除读者或修改读者信息等过程中受影响的读者编号
    @受影响的管理员账号 nvarchar(20),    --添加管理员、删除管理员等过程中受影响的管理员编号
    @操作内容 nvarchar(50), --操作内容,如添加读者、删除读者、修改读者信息、添加管理员、删除管理员等
    @操作原因 nvarchar(100)     --操作原因,除默认的操作原因外,还可以自定义操作原因
)
AS
BEGIN
    INSERT INTO 管理员重要操作记录(管理员账号,受影响的读者编号,受影响的管理员账号,操作时间,操作内容,操作原因)
    VALUES(@管理员账号,@受影响的读者编号,@受影响的管理员账号,SYSDATETIME(),@操作内容,@操作原因)
END
GO

CREATE PROCEDURE 管理员修改图书信息存储过程 --输入图书编号或者ISBN以修改某一书籍的特定单本或各本
(
    @图书编号或ISBN nvarchar(13), --输入字符串类型,以便实现一次输入即可通过图书编号和ISBN两种方式修改图书
    @分类编码 nvarchar(10) ,
    @书名 nvarchar(50) ,
    @作者 nvarchar(20) ,
    @出版社 nvarchar(20) ,
    @出版日期 date ,
    @单价 float ,     --设置单价为float类型,以便main.py中实现与读者的简单交互
    @简介 nvarchar(100) ,
    @状态 nvarchar(2)  --主要用于修改状态为丢失或损坏
)
AS
BEGIN
    --将float类型单价转换为decimal(10,2)类型以对应数据库中的单价字段,从而避免精度丢失
    SELECT @单价 = CAST(@单价 AS decimal(10,2))
    DECLARE @转换后 bigint = TRY_CAST(@图书编号或ISBN AS bigint)
    IF LEN(@图书编号或ISBN) IN (10,13) AND EXISTS(SELECT * FROM 图书信息 WHERE ISBN = @转换后)
        --判断输入的是否为ISBN且该ISBN是否存在(因为图书编号是唯一的,一个小图书馆不太可能出现上亿本图书,所以这样做比较合理),以下同理
        BEGIN   --如果输入的是ISBN,则修改所有该书籍的所有本
            UPDATE 图书信息 SET 分类编码 = @分类编码, 书名 = @书名,作者 = @作者,出版社 = @出版社,出版日期 = @出版日期,单价 = @单价,简介 = @简介,状态 = @状态
            WHERE ISBN = @转换后
        END
    ELSE IF EXISTS(SELECT * FROM 图书信息 WHERE 图书编号 = @转换后)
        BEGIN   --如果输入的是图书编号,则修改该书籍的单本
            UPDATE 图书信息 SET 分类编码 = @分类编码, 书名 = @书名,作者 = @作者,出版社 = @出版社,出版日期 = @出版日期,单价 = @单价,简介 = @简介,状态 = @状态
            WHERE 图书编号 = @转换后
        END
    ELSE
        BEGIN
            RAISERROR('图书编号或ISBN不存在!',16,1)
        END
END
GO

CREATE PROCEDURE 管理员浏览图书信息存储过程   --输入图书编号或者ISBN以浏览某一书籍的单本或各本
(
    @图书编号或ISBN nvarchar(13) = NULL
    --设置字符类型为字符串类型以便采用len()函数判断输入的是否为ISBN
    --从而实现一次输入即可通过图书编号和ISBN两种方式浏览图书
    --对于任何一个图书馆而言图书都不会有那么多(图书编号也就不会有那么多),所以这样做是合理的
)
AS
BEGIN
    DECLARE @转换后 bigint = TRY_CAST(@图书编号或ISBN AS bigint)    --将输入的字符串转换为bigint类型以便与数据库中的ISBN或者图书编号进行对应
    IF @图书编号或ISBN IS NOT NULL
        IF LEN(@图书编号或ISBN) IN (10,13) AND EXISTS(SELECT * FROM 图书信息 WHERE ISBN = @转换后)
            BEGIN
                SELECT * FROM 图书信息 WHERE ISBN = @转换后
            END
        ELSE IF EXISTS(SELECT * FROM 图书信息 WHERE 图书编号 = @转换后)
            BEGIN
                SELECT * FROM 图书信息 WHERE 图书编号 = @转换后
            END
        ELSE
            BEGIN
                RAISERROR('图书编号或ISBN不存在!',16,1)
            END
    ELSE
        BEGIN
            SELECT * FROM 图书信息
        END
END
GO

CREATE PROCEDURE 管理员添加读者存储过程
(
    @读者编号 bigint ,
    @姓名 nvarchar(20),
    @性别 nvarchar(1),
    @类型 nvarchar(3),
    @联系方式 nvarchar(20),
    @初始余额 float,    --设置浮点数类型以便于在main.py中进行输入
    @执行添加操作的管理员账号 nvarchar(20), --当前管理员账号,以便在管理员重要操作记录表中记录这项重要操作
    @密码 nvarchar(20)
)
AS
BEGIN
    --将@初始余额转换为decimal(10,2)类型
    SET @初始余额 = CONVERT(decimal(10,2),@初始余额)
    IF NOT EXISTS(SELECT * FROM 读者信息 WHERE 读者编号 = @读者编号)
        BEGIN
            INSERT INTO 读者信息(读者编号,姓名,性别,类型,联系方式,余额,密码) VALUES
                (@读者编号,@姓名,@性别,@类型,@联系方式,@初始余额,@密码)
            INSERT INTO 充值扣款记录(读者编号,变动金额,变动日期,管理员账号,变动原因)
            VALUES(@读者编号,@初始余额,SYSDATETIME(),@执行添加操作的管理员账号,'添加读者')
            EXEC 创建管理员重要操作存储过程 @执行添加操作的管理员账号,@读者编号,NULL,
                 '添加读者','添加读者'
            --添加读者须充值金额,因此变动原因为'添加读者',
            --变动金额为初始余额,并记录添加读者的管理员账号
        END
    ELSE
        BEGIN
            RAISERROR('该读者编号已存在!',16,1)
        END
END
GO

CREATE PROCEDURE 管理员删除读者存储过程  --输入读者编号以删除该读者(该读者必须先归还所有书籍,否则无法删除,会报错--外键约束,这也是为了保护借阅信息在未还书的情况下被删除)
--在删除该读者的读者信息的同时,删除该读者的历史借阅记录和充值扣款记录(因为题目要求和外键约束)
(
    @管理员账号 nvarchar(20),     --在main.py中获取当前管理员账号(adm_name为全局变量,在管理员登录时即获得赋值)
    @读者编号 bigint,
    @删除原因 nvarchar(100)     --记入管理员重要操作记录表中
)
AS
BEGIN
    IF EXISTS(SELECT * FROM 借阅信息 WHERE 读者编号=@读者编号)
        BEGIN
            RAISERROR('该读者有未归还的图书，无法删除',16,1)
        END
    IF EXISTS(SELECT * FROM 读者信息 WHERE 读者编号=@读者编号)
        BEGIN
            DELETE FROM 读者信息 WHERE 读者编号=@读者编号
            EXEC 创建管理员重要操作存储过程 @管理员账号,@读者编号,NULL,'删除读者',@删除原因
        END
    ELSE
        BEGIN
            RAISERROR('读者编号不存在!',16,1)
        END
END
GO

CREATE PROCEDURE 管理员修改读者信息存储过程  --输入读者编号以修改该读者的信息(读者编号不可修改)
(
    @执行修改操作的管理员账号 nvarchar(20),     --只要修改了读者信息,就要记录这项重要操作
    @读者编号 bigint,
    @姓名 nvarchar(20),
    @性别 nvarchar(1),
    @类型 nvarchar(3),
    @联系方式 nvarchar(20),
    @余额 float,  --可用于扣除多充的钱,补上误扣的钱等
    @修改原因 nvarchar(100)
)
AS
BEGIN
    --将float类型单价转换为decimal(10,2)类型以对应数据库表中的单价字段,从而避免精度丢失
    SET @余额 = CONVERT(decimal(10,2),@余额)
    IF EXISTS(SELECT * FROM 读者信息 WHERE 读者编号 = @读者编号)
        BEGIN
            DECLARE @变动金额 decimal(10,2) = @余额 - (SELECT 余额 FROM 读者信息 WHERE 读者编号 = @读者编号)    --用于记入充值扣款记录表中
            UPDATE 读者信息 SET 姓名=@姓名,性别=@性别,类型=@类型,余额=@余额, 联系方式=@联系方式
                WHERE 读者编号 = @读者编号
            EXEC 创建管理员重要操作存储过程 @执行修改操作的管理员账号,@读者编号,
                 NULL,'管理员修改读者信息',@修改原因
            IF @变动金额 <> 0       --如果通过修改信息中余额的方式造成余额变动,则也需要记录执行这一操作的管理员账号,以免损害读者利益
                BEGIN
                    INSERT INTO 充值扣款记录(读者编号,变动金额,变动日期,管理员账号,变动原因)
                        VALUES(@读者编号,@变动金额,SYSDATETIME(),@执行修改操作的管理员账号,'修改读者余额')
                END
        END
    ELSE
        BEGIN
            RAISERROR('读者编号不存在!',16,1)
        END
END
GO

CREATE PROCEDURE 管理员查询读者信息存储过程  --直接输入读者编号或姓名以查询该读者的信息,若输入为空则查询所有读者信息
(
    @读者编号或者姓名 nvarchar(20) = NULL
)
AS
BEGIN
    IF @读者编号或者姓名 IS NULL
        BEGIN
            SELECT 读者编号, 姓名, 性别, 类型, 数目限制, 时间限制, 余额, 联系方式 FROM 读者信息
        END
    ELSE
        BEGIN
            IF EXISTS(SELECT * FROM 读者信息 WHERE 姓名 = @读者编号或者姓名)--若输入的是姓名(没有人会以数字命名),则查询该姓名的读者信息
                BEGIN
                    SELECT 读者编号, 姓名, 性别, 类型, 数目限制, 时间限制, 余额, 联系方式 FROM 读者信息 WHERE 姓名 = @读者编号或者姓名
                END
            ELSE
                BEGIN
                    SELECT @读者编号或者姓名 = CAST(@读者编号或者姓名 AS bigint)--若输入的是读者编号,则将其转换为bigint类型,再查询该读者信息
                    IF EXISTS(SELECT * FROM 读者信息 WHERE 读者编号 = @读者编号或者姓名)
                        BEGIN
                            SELECT 读者编号, 姓名, 性别, 类型, 数目限制, 时间限制, 余额, 联系方式 FROM 读者信息 WHERE 读者编号 = @读者编号或者姓名
                        END
                    ELSE
                        BEGIN
                            RAISERROR('不存在以输入内容作为姓名或编号的读者!',16,1)
                        END
                END
        END
END
GO

CREATE PROCEDURE 管理员重置读者密码存储过程
(
    @执行重置操作的管理员账号 nvarchar(20),    --敏感操作,需要管理员账号并记录操作者
    @读者编号 bigint,
    @新密码 nvarchar(20)
)
AS
BEGIN
    IF EXISTS(SELECT * FROM 读者信息 WHERE 读者编号 = @读者编号)
        BEGIN
            UPDATE 读者信息 SET 密码=@新密码 WHERE 读者编号 = @读者编号
            EXEC 创建管理员重要操作存储过程 @执行重置操作的管理员账号,@读者编号,
                 NULL,'重置读者密码','读者忘记密码,凭有效身份证件重置'
        END
    ELSE
        BEGIN
            RAISERROR('读者编号不存在!',16,1)
        END
END
GO

CREATE PROCEDURE 管理员查看重要操作记录存储过程
(
    @管理员账号 nvarchar(20) = NULL,    --管理员账号,若为空则查询所有管理员的操作记录
    @受影响的读者编号 bigint = NULL,        --受影响的读者编号,若为空则查询对所有读者的操作记录
    @受影响的管理员账号 nvarchar(20) = NULL      --受影响的管理员账号,若为空则查询对所有管理员的操作记录
)
AS
BEGIN
    IF @管理员账号 IS NULL
        BEGIN
            IF @受影响的读者编号 IS NULL AND @受影响的管理员账号 IS NOT NULL     --查询所有管理员对某个管理员的操作记录
                BEGIN
                    SELECT * FROM 管理员重要操作记录 WHERE 受影响的管理员账号 = @受影响的管理员账号
                END
            ELSE IF @受影响的读者编号 IS NOT NULL AND @受影响的管理员账号 IS NULL    --查询所有管理员对某个读者的操作记录
                BEGIN
                    SELECT * FROM 管理员重要操作记录 WHERE 受影响的读者编号 = @受影响的读者编号
                END
            ELSE IF @受影响的读者编号 IS NULL AND @受影响的管理员账号 IS NULL    --查询所有管理员的操作记录
                BEGIN
                    SELECT * FROM 管理员重要操作记录
                END
            ELSE
                BEGIN
                    RAISERROR ('参数输入错误,请重新输入!',16,1)    --参数输入错误(管理员一次只能操作一名对象,所以不存在两者都不为空的情况)
                END
        END
    ELSE
        BEGIN
            IF @受影响的读者编号 IS NULL AND @受影响的管理员账号 IS NOT NULL    --查询某个管理员对某个管理员的操作记录
                BEGIN
                    SELECT * FROM 管理员重要操作记录 WHERE 受影响的管理员账号 = @受影响的管理员账号 AND 管理员账号 = @管理员账号
                END
            ELSE IF @受影响的读者编号 IS NOT NULL AND @受影响的管理员账号 IS NULL    --查询某个管理员对某个读者的操作记录
                BEGIN
                    SELECT * FROM 管理员重要操作记录 WHERE 受影响的读者编号 = @受影响的读者编号 AND 管理员账号 = @管理员账号
                END
            ELSE IF @受影响的读者编号 IS NULL AND @受影响的管理员账号 IS NULL    --查询某个管理员的操作记录
                BEGIN
                    SELECT * FROM 管理员重要操作记录 WHERE 管理员账号 = @管理员账号
                END
            ELSE
                BEGIN
                    RAISERROR ('参数输入错误,请重新输入!',16,1)    --参数输入错误(管理员一次只能操作一名对象,所以不存在两者都不为空的情况)
                END
        END
END
GO

CREATE PROCEDURE 图书借阅存储过程
(
    @读者编号 bigint,
    @图书编号 int
)
AS
BEGIN
    DECLARE @ISBN bigint = (SELECT ISBN FROM 图书信息 WHERE 图书编号 = @图书编号) --获取图书的ISBN,用于接下来检查该读者有无借阅该图书
    IF EXISTS(SELECT * FROM 借阅信息 WHERE 读者编号 = @读者编号 AND ISBN = @ISBN)
        BEGIN
            RAISERROR('该读者已借阅该图书,不可在同期内借多本相同图书!',16,1)
            --依据大多数图书馆的规则,同一读者在同一期限内不可借多本相同图书,以避免造成图书资源的浪费
        END
    ELSE
        BEGIN
            IF (SELECT COUNT(*) FROM 图书信息 WHERE (图书编号 = @图书编号 AND 状态 = '在馆')) = 1 --要么为0要么为1,所以用1
                AND EXISTS(SELECT * FROM 读者信息 WHERE 读者编号 = @读者编号)
                BEGIN   --检查图书是否在馆,读者是否存在 --只有状态为'在馆'的图书才能被借阅
                    INSERT INTO 借阅信息(图书编号, ISBN, 读者编号, 借阅日期) VALUES (@图书编号, @ISBN, @读者编号, GETDATE())
                    UPDATE 图书信息 SET 状态 = '借出' WHERE 图书编号 = @图书编号        --有人有书,完成借阅
                END
            ELSE
                BEGIN
                    IF (SELECT COUNT(*) FROM 图书信息 WHERE (ISBN=@ISBN AND 状态 = '在馆')) = 0
                        AND EXISTS(SELECT * FROM 读者信息 WHERE 读者编号 = @读者编号)       --有人无书,借阅失败,提示图书已被借出
                        BEGIN
                            RAISERROR('该图书已被借出!',16,1)
                        END
                    ELSE
                        BEGIN
                            RAISERROR('读者编号不存在!',16,1)
                        END
                END
        END
END
GO

CREATE PROCEDURE 图书归还存储过程
(
    @管理员账号 varchar(20),     --管理员自定义图书归还时间属于敏感操作,需要在管理员重要操作记录中记录下来
    @读者编号 bigint,
    @图书编号 int = NULL,
    @实还日期 date = '9999-01-01'   --默认值为9999-01-01,表示管理员未手动输入实还日期,接下来替换掉它,然后以系统当前日期为实还日期
)
AS
BEGIN
    IF @图书编号 IS NOT NULL    --如果图书编号不为空,则根据图书编号进行归还
        BEGIN
            IF EXISTS(SELECT * FROM 借阅信息 WHERE 读者编号=@读者编号 AND 图书编号=@图书编号)
                BEGIN
                    IF @实还日期 NOT IN ('9999-01-01')      --如果管理员手动输入了实还日期,则以管理员输入的日期为准
                        BEGIN
                            INSERT INTO 历史借阅信息(图书编号, ISBN, 读者编号, 借阅日期, 应还日期, 实还日期)
                            SELECT 图书编号, ISBN, 读者编号, 借阅日期, 应还日期, @实还日期 FROM 借阅信息
                            WHERE 读者编号=@读者编号 AND 图书编号=@图书编号
                            EXEC 创建管理员重要操作存储过程 @管理员账号, @读者编号,NULL,'自定图书归还时间','测试逾期扣款功能'
                        END
                    ELSE        --如果管理员未手动输入实还日期,则以系统当前日期为实还日期
                        BEGIN
                            INSERT INTO 历史借阅信息(图书编号, ISBN, 读者编号, 借阅日期, 应还日期, 实还日期)
                            SELECT 图书编号, ISBN, 读者编号, 借阅日期, 应还日期,GETDATE() FROM 借阅信息
                            WHERE 读者编号=@读者编号 AND 图书编号=@图书编号
                        END
                    DELETE FROM 借阅信息 WHERE 读者编号=@读者编号 AND 图书编号=@图书编号
                    UPDATE 图书信息 SET 状态 = '在馆' WHERE 图书编号 = @图书编号
                END
            ELSE
                BEGIN
                    RAISERROR('该读者当前未借阅该图书',16,1)
                END
        END
    ELSE    --如果图书编号为空,则归还读者编号对应读者所借阅的所有图书
        BEGIN
            IF EXISTS(SELECT * FROM 借阅信息 WHERE 读者编号=@读者编号)
                BEGIN   --如果没有实还日期,则默认为当前日期,否则为实还日期
                    IF @实还日期 NOT IN ('9999-01-01')      --如果管理员手动输入了实还日期,则以管理员输入的日期为实还日期
                        BEGIN
                            INSERT INTO 历史借阅信息(图书编号, ISBN, 读者编号, 借阅日期, 应还日期, 实还日期)
                            SELECT 图书编号, ISBN, 读者编号, 借阅日期, 应还日期, @实还日期 FROM 借阅信息 WHERE 读者编号=@读者编号
                            EXEC 创建管理员重要操作存储过程 @管理员账号, @读者编号,NULL,'自定图书归还时间','测试逾期扣款功能'
                        END
                    ELSE        --如果管理员没有手动输入实还日期,则以系统当前日期为实还日期
                        BEGIN
                            INSERT INTO 历史借阅信息(图书编号, ISBN, 读者编号, 借阅日期, 应还日期, 实还日期)
                            SELECT 图书编号, ISBN, 读者编号, 借阅日期, 应还日期, GETDATE() FROM 借阅信息 WHERE 读者编号=@读者编号
                        END
                    UPDATE 图书信息 SET 状态 = '在馆' WHERE 图书编号 IN (SELECT 图书编号 FROM 借阅信息 WHERE 读者编号=@读者编号)
                    DELETE FROM 借阅信息 WHERE 读者编号=@读者编号
                END
            ELSE
                BEGIN
                    RAISERROR('该读者当前未借阅任何图书',16,1)
                END
        END
END
GO

CREATE PROCEDURE 读者充值存储过程
(
    @管理员账号 nvarchar(20),    --取执行该存储过程的管理员账号,用于记录进管理员重要操作表
    @读者编号 bigint,
    @充值金额 float
)
AS
BEGIN
    SET @充值金额 = CAST(@充值金额 AS DECIMAL(10,2))
    IF EXISTS(SELECT * FROM 读者信息 WHERE 读者编号=@读者编号) AND @充值金额>0      --判断读者编号是否存在,充值金额是否大于0
        BEGIN
            UPDATE 读者信息 SET 余额 = ((SELECT 余额 FROM 读者信息 WHERE 读者编号=@读者编号)+@充值金额) WHERE 读者编号=@读者编号        --更新读者余额
            INSERT INTO 充值扣款记录(读者编号,变动金额,变动日期,管理员账号,变动原因)
            VALUES (@读者编号,@充值金额,GETDATE(),@管理员账号,'读者充值')        --变动原因为读者充值,管理员账号为当前管理员账号(以避免账单对不上且无法追责)
        END
    ELSE
        BEGIN
            RAISERROR('读者编号不存在或充值金额不正确',16,1)
        END
END
GO

CREATE PROCEDURE 管理员信息浏览存储过程
(
    @管理员账号 nvarchar(20),
    @管理员密码 nvarchar(20)
)
AS
BEGIN
    IF EXISTS(SELECT * FROM 管理员信息 WHERE 管理员账号=@管理员账号 AND 管理员密码=@管理员密码)
        BEGIN
            SELECT 管理员账号 AS 您的管理账号, 管理员密码 AS 您的管理密码
            FROM 管理员信息 WHERE 管理员账号=@管理员账号 AND 管理员密码=@管理员密码
        END
    ELSE
        BEGIN
            RAISERROR('管理员账号或密码错误',16,1)
        END
END
GO

CREATE PROCEDURE 添加管理员存储过程
(
    @当前管理员账号 nvarchar(20),    --执行者，须为主管理员(是否为主管理员=1)
    @新加管理员账号 nvarchar(20),
    @新加管理员类型 bit,   --1表示主管理员，0表示普通管理员
    @新加密码 nvarchar(20)
)
AS
BEGIN
    IF EXISTS(SELECT * FROM 管理员信息 WHERE 管理员账号=@当前管理员账号 AND 是否为主管理员=1)
        BEGIN
            IF NOT EXISTS(SELECT * FROM 管理员信息 WHERE 管理员账号=@新加管理员账号)
                BEGIN
                    INSERT INTO 管理员信息(管理员账号,管理员密码,是否为主管理员)
                    VALUES(@新加管理员账号,@新加密码,@新加管理员类型)
                    EXEC 创建管理员重要操作存储过程 @当前管理员账号,NULL,@新加管理员账号,'添加新管理员','添加新管理员'
                END
            ELSE
                BEGIN
                    RAISERROR('该管理员账号已存在!',16,1)
                END
        END
    ELSE
        BEGIN
            RAISERROR('您不是主管理员，无法添加管理员!',16,1)
        END
END
GO

CREATE PROCEDURE 删除管理员存储过程
(
    @当前管理员账号 nvarchar(20),
    @被删除的管理员账号 nvarchar(20),
    @被删除的管理员密码 nvarchar(20),
    @删除原因 nvarchar(100)
)
AS
BEGIN
    IF EXISTS(SELECT * FROM 管理员信息 WHERE 管理员账号=@当前管理员账号 AND 是否为主管理员=1)
        BEGIN
            IF EXISTS(SELECT * FROM 管理员信息 WHERE 管理员账号=@被删除的管理员账号 AND 管理员密码=@被删除的管理员密码)
                BEGIN
                    DELETE FROM 管理员信息 WHERE 管理员账号=@被删除的管理员账号
                    EXEC 创建管理员重要操作存储过程 @当前管理员账号,NULL,@被删除的管理员账号,'删除管理员',@删除原因
                END
            ELSE
                IF EXISTS(SELECT * FROM 管理员信息 WHERE 管理员账号=@被删除的管理员账号)
                    BEGIN
                        RAISERROR('管理员密码错误!',16,1)
                    END
                ELSE
                    BEGIN
                        RAISERROR('该管理员账号不存在!',16,1)
                    END
        END
    ELSE
        BEGIN
            RAISERROR('您不是主管理员，无法删除管理员!',16,1)
        END
END
GO

CREATE PROCEDURE 管理员修改自己密码存储过程
(
    @管理员账号 nvarchar(20),
    @管理员密码 nvarchar(20),
    @管理员新密码 nvarchar(20)
)
AS
BEGIN
    -- 检查账号是否存在且旧密码是否正确
    IF NOT EXISTS (SELECT 1 FROM 管理员信息 WHERE 管理员账号 = @管理员账号 AND 管理员密码 = @管理员密码)
        BEGIN
            RAISERROR('当前密码错误!', 16, 1)
            RETURN
        END

    -- 检查新密码是否与旧密码相同
    IF @管理员新密码 = @管理员密码
        BEGIN
            RAISERROR('新密码不能与旧密码相同!', 16, 1)
            RETURN
        END

    -- 检查新密码长度
    IF LEN(@管理员新密码) < 5 OR LEN(@管理员新密码) > 20
        BEGIN
            RAISERROR('密码长度必须是5到20位!', 16, 1)
            RETURN
        END

    -- 更新密码
    BEGIN TRY
        UPDATE 管理员信息 SET 管理员密码 = @管理员新密码 WHERE 管理员账号 = @管理员账号
    END TRY
    BEGIN CATCH
        -- 捕获可能的更新异常
        RAISERROR('修改失败,未知错误!', 16, 1)
    END CATCH
END
GO


CREATE PROCEDURE 读者查询个人信息存储过程
(
    @读者编号 bigint,
    @密码 nvarchar(20)
)
AS
BEGIN
    IF EXISTS(SELECT * FROM 读者信息 WHERE 读者编号=@读者编号 AND 密码=@密码)    --如果有该读者且密码正确,就返回该读者的信息(由于是该读者自己看,所以返回全部信息)
        BEGIN
            SELECT * FROM 读者信息 WHERE 读者编号=@读者编号
        END
    ELSE
        BEGIN
            RAISERROR('读者编号或密码错误',16,1)
        END
END
GO

CREATE PROCEDURE 读者修改登录密码存储过程
(
    @读者编号 bigint,
    @旧密码 nvarchar(20),
    @新密码 nvarchar(20)
)
AS
BEGIN
    IF EXISTS(SELECT * FROM 读者信息 WHERE 读者编号=@读者编号 AND 密码=@旧密码) AND @旧密码<>@新密码     --要求新旧密码不能相同
        BEGIN
            UPDATE 读者信息 SET 密码 = @新密码 WHERE 读者编号=@读者编号
        END
    ELSE
        BEGIN
            RAISERROR('修改失败!',16,1)
        END
END
GO


CREATE PROCEDURE 读者查询当前借阅信息存储过程
(
    @读者编号 bigint,
    @密码 nvarchar(20)
)
AS
BEGIN
    IF EXISTS(SELECT 1 FROM 读者信息 WHERE 读者编号 = @读者编号 AND 密码 = @密码)
        BEGIN
            SELECT b.借阅编号, b.图书编号, i.书名, c.分类名称, i.作者, i.ISBN, b.借阅日期, b.应还日期
            FROM 借阅信息 b
                     INNER JOIN 图书信息 i ON b.图书编号 = i.图书编号
                     INNER JOIN 图书分类 c ON i.分类编码 = c.分类编码
            WHERE b.读者编号 = @读者编号
        END
    ELSE
        BEGIN
            RAISERROR('查询失败!', 16, 1)
        END
END
GO

CREATE PROCEDURE 读者查询历史借阅信息存储过程
(
    @读者编号 bigint,
    @密码 nvarchar(20)
)
AS
BEGIN
    IF EXISTS(SELECT 1 FROM 读者信息 WHERE 读者编号 = @读者编号 AND 密码 = @密码)
        BEGIN
            SELECT h.历史借阅编号, h.图书编号, i.书名, c.分类名称, i.作者, i.ISBN, h.借阅日期, h.应还日期, h.实还日期
            FROM 历史借阅信息 h
                     INNER JOIN 图书信息 i ON h.图书编号 = i.图书编号
                     INNER JOIN 图书分类 c ON i.分类编码 = c.分类编码
            WHERE h.读者编号 = @读者编号
        END
    ELSE
        BEGIN
            RAISERROR('查询失败!', 16, 1)
        END
END
GO

CREATE PROCEDURE 读者查询充值扣款信息存储过程
(
    @读者编号 bigint,
    @密码 nvarchar(20)
)
AS
BEGIN
    IF EXISTS(SELECT * FROM 读者信息 WHERE 读者编号=@读者编号 AND 密码=@密码)
        BEGIN
            SELECT * FROM 充值扣款记录 WHERE 读者编号=@读者编号
        END
    ELSE
        BEGIN
            RAISERROR('查询失败!',16,1)
        END
END
GO

CREATE PROCEDURE 备份数据库存储过程
(
    @备份路径 nvarchar(100)
)
AS
BEGIN
    BEGIN TRY
        BACKUP DATABASE BOOKS TO DISK = @备份路径
        INSERT INTO 备份恢复记录(备份时间, 备份路径) VALUES (SYSDATETIME(), @备份路径)
    END TRY
    BEGIN CATCH
        RAISERROR('备份失败!',16,1)
    END CATCH
END
GO

CREATE PROCEDURE 恢复数据库存储过程
(
    @恢复路径 nvarchar(100)
)
AS
BEGIN
    BEGIN TRY
        RESTORE DATABASE BOOKS FROM DISK = @恢复路径
        INSERT INTO 备份恢复记录(恢复时间, 恢复路径) VALUES (SYSDATETIME(), @恢复路径)
    END TRY
    BEGIN CATCH
        RAISERROR('恢复失败!',16,1)
    END CATCH
END
GO

CREATE PROCEDURE 读者查询图书信息存储过程
(
    @书名 nvarchar(50) = NULL,
    @作者 nvarchar(20) = NULL,
    @出版社 nvarchar(20) = NULL
)
AS
BEGIN
    SELECT 图书信息.图书编号, 图书信息.书名, 图书分类.分类名称, 图书信息.作者, 图书信息.出版社, 图书信息.出版日期, 图书信息.单价, 图书信息.简介, 图书信息.状态
    FROM 图书信息
             INNER JOIN 图书分类 ON 图书信息.分类编码 = 图书分类.分类编码
    WHERE 图书信息.书名 LIKE '%' + ISNULL(@书名, 图书信息.书名) + '%' AND 图书信息.作者 LIKE '%' + ISNULL(@作者, 图书信息.作者) + '%' AND 图书信息.出版社 LIKE '%' + ISNULL(@出版社, 图书信息.出版社) + '%'
    IF @@ROWCOUNT = 0
        RAISERROR('没有找到相关图书', 16, 1)
END
GO

-- 初始主管理员（是否为主管理员=1，可添加/删除其他管理员）
INSERT INTO 管理员信息(管理员账号,管理员密码,是否为主管理员) VALUES ('admin','admin',1)
SELECT * FROM 管理员信息 WHERE 管理员账号='admin'
INSERT INTO 图书分类 (分类编码, 分类名称)
VALUES
    ('A', '马列主义、毛泽东思想、邓小平理论'),
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
    ('Z', '综合性图书')
GO

EXEC 图书上架存储过程 'O', 9781111111111,'复变函数论','钟玉泉','高等教育出版社','2013-08-01',59,'复变函数教材',2
EXEC 图书上架存储过程 'T', 9782222222222,'Python语言程序设计基础','嵩天','高等教育出版社','2017-2-19',39,'零基础学习Python语言',5
EXEC 图书上架存储过程 'A', 9783333333333,'毛泽东选集','毛泽东','人民出版社','2018-1-12',99,'毛泽东思想的集中展现',5
EXEC 图书上架存储过程 'O', 9784444444444,'高等代数','姚慕生','复旦大学出版社','2019-12-1',29,'数学系基础课教材',5
EXEC 图书上架存储过程 'O', 9785555555555,'数学分析-下册','陈纪修','复旦大学出版社','2019-12-1',54,'数学系基础课教材',3
EXEC 图书上架存储过程 'O', 9786666666666,'数学分析-上册','陈纪修','复旦大学出版社','2019-12-1',34.6,'数学系基础课教材',4
EXEC 图书上架存储过程 'O', 9787777777777,'概率论基础','李贤平','高等教育出版社','2019-12-1',29.2,'概率论基础',5
EXEC 图书上架存储过程 'K', 9788888888888,'明朝那些事儿','当年明月','人民文学出版社','2019-12-1',39,'历史也可以很有趣',6
EXEC 图书上架存储过程 'I', 9789999999999,'平凡的世界','路遥','人民文学出版社','2019-12-1',69,'献给我生活的土地和岁月',3
EXEC 图书上架存储过程 'T', 9781234567890,'Python数据分析','Wes McKinney','人民邮电出版社','2020-8-1',108,'数据分析入门教材',5
EXEC 图书上架存储过程 'T', 9781234567891,'数据结构(C语言版)','严蔚敏','清华大学出版社','2021-12-01',49,'数据结构入门教材',5
EXEC 图书上架存储过程 'T', 9781234567892,'机器学习','周志华','清华大学出版社','2016-1-1',108,'机器学习入门教材',5
EXEC 图书上架存储过程 'T', 9781234567893,'计算机网络','谢希仁','清华大学出版社','2016-1-1',108,'计算机网络入门教材',4
EXEC 图书上架存储过程 'T', 9781234567894,'操作系统','王爽','清华大学出版社','2016-1-1',108,'操作系统入门教材',5
EXEC 图书上架存储过程 'T', 9781234567895,'数据库系统概念','王珊','高等教育出版社','2016-1-1',108,'数据库入门教材',5
EXEC 图书上架存储过程 'T', 9781234567896,'计算机组成原理','唐朔飞','高等教育出版社','2016-1-1',108,'计算机组成原理入门教材',5
EXEC 图书上架存储过程 'T', 9781234567897,'数据库必知必会','Ben Forta','人民邮电出版社','2020-8-1',108,'SQL领域教材',5
EXEC 图书上架存储过程 'T', 9781234567898,'统计学习方法','李航','清华大学出版社','2020-8-1',108,'机器学习入门教材',5
EXEC 图书上架存储过程 'T', 9781234567899,'数据科学入门','Joel Grus','人民邮电出版社','2020-8-1',108,'功能强大、简单易学',5
EXEC 管理员浏览图书信息存储过程
EXEC 管理员添加读者存储过程 111111,'张宇','男','教师','电话号码：19563122993', 200,'admin','zhangyu123'
EXEC 管理员添加读者存储过程 222222,'王康','女','研究生','QQ:1763571365',150,'admin','wangkang123'
EXEC 管理员添加读者存储过程 333333,'刘浸','男','研究生','QQ：2983909243',240,'admin','liujin123'
EXEC 管理员添加读者存储过程 444444,'赵灼','男','教师','QQ：2502196137',140,'admin','zhaozhuo123'
EXEC 管理员添加读者存储过程 2100820001,'钱文','男','本科生','住址：山东大学',350,'admin','qianwen123'
EXEC 管理员添加读者存储过程 2100000002,'孙强','男','其他','住址：汉东省公安厅',120,'admin','sunqiang123'
EXEC 管理员添加读者存储过程 2100000003,'吴宛','女','其他','住址：翻斗花园',120,'admin','wuwan123'
EXEC 管理员添加读者存储过程 2100820077,'钟遇','男','本科生','邮箱：1763571365@qq.com',160,'admin','zhongyu123'
EXEC 管理员查询读者信息存储过程
EXEC 图书借阅存储过程 111111,1
EXEC 图书借阅存储过程 111111,3
EXEC 图书借阅存储过程 111111,8
EXEC 图书借阅存储过程 111111,13
EXEC 图书借阅存储过程 111111,18
EXEC 图书借阅存储过程 111111,21
EXEC 图书借阅存储过程 111111,25
EXEC 图书借阅存储过程 111111,30
EXEC 图书借阅存储过程 111111,36
EXEC 图书借阅存储过程 111111,39
EXEC 图书借阅存储过程 222222,44
EXEC 图书借阅存储过程 222222,49
EXEC 图书借阅存储过程 222222,54
EXEC 图书借阅存储过程 222222,58
EXEC 图书借阅存储过程 333333,63
EXEC 图书借阅存储过程 333333,68
EXEC 图书借阅存储过程 333333,73
EXEC 图书借阅存储过程 444444,78
EXEC 图书借阅存储过程 444444,83
EXEC 图书借阅存储过程 444444,62
EXEC 图书借阅存储过程 2100820001,4
EXEC 图书借阅存储过程 2100820001,10
EXEC 图书借阅存储过程 2100000002,22
EXEC 图书借阅存储过程 2100000003,26
EXEC 图书借阅存储过程 2100820077,32
EXEC 图书借阅存储过程 2100820077,37
EXEC 图书借阅存储过程 2100820077,56
EXEC 图书借阅存储过程 2100820077,80
EXEC 图书借阅存储过程 111111,4
EXEC 图书借阅存储过程 2100820077,86
EXEC 图书借阅存储过程 2100820077,23
EXEC 图书归还存储过程 'admin',222222,54
EXEC 图书归还存储过程 'admin',2100820077,86,'2029-12-06'
EXEC 图书归还存储过程 'admin',333333
EXEC 图书归还存储过程 'admin',444444,1000
EXEC 图书归还存储过程 'admin',444444,78,'2029-09-01'
