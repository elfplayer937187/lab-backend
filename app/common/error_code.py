# 业务上的错误码
class Code:
    SUCCESS = 200  # 成功
    PARAM_ERROR = 400  # 参数错误
    UNAUTHORIZED = 401  # 未认证
    ACCESS_FORBIDDEN = 403  # 无权限
    SYSTEM_ERROR = 500  # 系统错误

    # Token
    TOKEN_INVALID = 201  # Token 无效
    TOKEN_ACCESS_FORBIDDEN = 202  # Token 访问被拒绝
    ACCESS_UNAUTHORIZED = 203  # 访问未授权

    # 用户/账户
    ACCOUNT_SAME = 230  # 账户已存在
    USER_NOT_EXIST = 231  # 用户不存在
    USER_DISABLED = 232  # 用户被禁用
    UNKNOWN_ERROR = 240  # 未知错误

    # 菜单
    MENU_NOT_EXIST = 241
    MENU_NOT_EMPTY = 242
    # 实验室
    LAB_NOT_EXIST = 250  # 实验室不存在
    LAB_EXIST = 251  # 实验室已存在
    LAB_BOOK_CONFLICT = 261

    # 角色
    ROLE_NOT_EXIST = 252  # 角色不存在
    ROLE_EXIST = 253
    LAB_BOOK_NOT_EXIST = 254  # 角色已存在

# 业务码 → HTTP 状态码的兜底映射。
#
# 只在抛 BusinessError 时没显式传 http_status 才用得上。同一个业务码在不同接口
# 的 HTTP 语义可能不同 —— 比如 USER_NOT_EXIST:登录失败应该回 401,查用户详情
# 应该回 404。这种时候在抛的地方显式传 http_status 覆盖本表。
#
# 表里没有的业务码一律按 400 处理(见 BusinessError.__init__)。
HTTP_STATUS: dict[int, int] = {
    Code.SUCCESS: 200,
    Code.PARAM_ERROR: 400,
    Code.UNAUTHORIZED: 401,
    Code.ACCESS_FORBIDDEN: 403,
    Code.SYSTEM_ERROR: 500,
    # Token
    Code.TOKEN_INVALID: 401,
    Code.TOKEN_ACCESS_FORBIDDEN: 403,
    Code.ACCESS_UNAUTHORIZED: 401,
    # 用户/账户
    Code.ACCOUNT_SAME: 409,
    Code.USER_NOT_EXIST: 404,
    Code.USER_DISABLED: 403,
    Code.UNKNOWN_ERROR: 500,
    # 实验室
    Code.LAB_NOT_EXIST: 450,
    Code.LAB_EXIST: 451,
    Code.LAB_BOOK_CONFLICT: 452,
    # 角色
    Code.ROLE_NOT_EXIST: 404,
    Code.ROLE_EXIST: 409,
}
