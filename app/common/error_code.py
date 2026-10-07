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
