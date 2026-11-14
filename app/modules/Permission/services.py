from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.junction.database import RolePermission
from app.modules.Permission.database import Permission
from app.modules.Permission.schemas import MenuTreeResponse


def get_tree_menu(db: Session, role_id: int | None = None):
    stmt = select(Permission)
    # 原始orm的menu平铺列表
    menus = db.scalars(stmt).all()

    # 传了 role_id 就注入角色已拥有的权限:命中 check=1,其余 check=0。
    # 不传时保持默认 0,不影响 /menu/tree 这种纯菜单查询。
    checked_ids: set[int] = set()
    if role_id is not None:
        checked_ids = set(
            db.scalars(
                select(RolePermission.permission_id).where(
                    RolePermission.role_id == role_id
                )
            ).all()
        )

    # pydantic id:menu 的映射。先全部实例化,保证同一个节点只有一个对象,
    # 否则父节点被实例化多次,挂上去的 children 和最终返回的不是同一个。
    dict_nodes = {menu.id: MenuTreeResponse.model_validate(menu) for menu in menus}
    for menu_id, node in dict_nodes.items():
        node.check = 1 if menu_id in checked_ids else 0

    # 构建菜单树
    tree: list[MenuTreeResponse] = []
    for menu in menus:
        node = dict_nodes[menu.id]
        parent = dict_nodes.get(menu.pid or -1)
        if parent is None:
            # 父节点不在结果里(顶级菜单,或父节点被禁用而没查出来) -> 当根节点
            tree.append(node)
        else:
            parent.children.append(node)

    return tree
