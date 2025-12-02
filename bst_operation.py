class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    """Пункт 1: бинарное дерево поиска(BST)"""
    def __init__(self):
        self.root = None

    # Вставка
    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert_recursive(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_recursive(node.right, key)
    # Поиск
    def search(self, key):
        return self._search_recursive(self.root, key) is not None

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    # Минимум и максимум
    def find_min(self):
        if not self.root:
            return None
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur.key

    def find_max(self):
        if not self.root:
            return None
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur.key

    # Удаление
    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _delete_recur(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete_recur(node.left, key)
        elif key > node.key:
            node.right = self._delete_recur(node.right, key)
        else:
            # узел найден
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # два ребёнка
            min_node = node.right
            while min_node.left:
                min_node = min_node.left
            node.key = min_node.key
            node.right = self._delete_recur(node.right, min_node.key)
        return node

    # Обходы
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.key)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.key)

    def bfs(self):
        if not self.root:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    # Высота дерева
    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if not node:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))


# -----------------------------------------------------
# Пункт 2: AVL-дерево
# -----------------------------------------------------
class AVLNode(Node):
    def __init__(self, key):
        super().__init__(key)
        self.height = 1


class AVL(BST):
    """AVL-дерево"""
    def __init__(self):
        super().__init__()

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node

        node.height = 1 + max(self._get_h(node.left), self._get_h(node.right))

        balance = self._get_balance(node)

        # LL
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)
        # RR
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)
        # LR
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        # RL
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            min_node = node.right
            while min_node.left:
                min_node = min_node.left
            node.key = min_node.key
            node.right = self._delete(node.right, min_node.key)

        node.height = 1 + max(self._get_h(node.left), self._get_h(node.right))
        balance = self._get_balance(node)

        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # вспомогательные методы
    def _get_h(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_h(node.left) - self._get_h(node.right)

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_h(z.left), self._get_h(z.right))
        y.height = 1 + max(self._get_h(y.left), self._get_h(y.right))
        return y

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_h(z.left), self._get_h(z.right))
        y.height = 1 + max(self._get_h(y.left), self._get_h(y.right))
        return y


# --------------------------------------------------------
# Пункт 3: Красно-чёрное дерево — тоже через наследование
# --------------------------------------------------------
class RBNode(Node):
    def __init__(self, key):
        super().__init__(key)
        self.color = 'RED'
        self.parent = None


class RedBlackTree(BST):
    """Красно-чёрное дерево"""
    def __init__(self):
        super().__init__()

    def insert(self, key):
        if not self.root:
            self.root = RBNode(key)
            self.root.color = 'BLACK'
            return

        parent = None
        cur = self.root
        while cur:
            parent = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return  # дубликат

        node = RBNode(key)
        node.parent = parent
        if key < parent.key:
            parent.left = node
        else:
            parent.right = node

        self._fix_insert(node)

    def _fix_insert(self, z):
        while z != self.root and z.parent.color == 'RED':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # дядя
                if y and y.color == 'RED':
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    self._right_rotate(z.parent.parent)
            else:  # симметрично
                y = z.parent.parent.left
                if y and y.color == 'RED':
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    self._left_rotate(z.parent.parent)
        self.root.color = 'BLACK'

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right:
            x.right.parent = y
        x.parent = y.parent
        if not y.parent:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x


if __name__ == "__main__":
    print("1) BST")
    bst = BST()
    for x in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(x)
    print("Порядок:", bst.inorder())
    print("Высота BST:", bst.height())

    print("\n2) AVL-дерево")
    avl = AVL()
    for x in [50, 30, 70, 20, 40, 60, 80, 10]:
        avl.insert(x)
    print("Порядок:", avl.inorder())
    print("Высота AVL:", avl.height())

    print("\n3) Красно-чёрное дерево")
    rb = RedBlackTree()
    for x in [50, 30, 70, 20, 40, 60, 80, 10, 15]:
        rb.insert(x)
    print("Порядок:", rb.inorder())
    print("Высота RB:", rb.height())
