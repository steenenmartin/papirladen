

def prettify(element, indent='  '):
    queue = [(0, element)]  # (level, element)
    while queue:
        level, element = queue.pop(0)
        children = [(level + 1, child) for child in list(element)]
        if children:
            # for child open
            element.text = '\n' + indent * (level + 1)

        if queue:
            # for sibling open
            element.tail = '\n' + indent * queue[0][0]
        else:
            # for parent close
            element.tail = '\n' + indent * (level - 1)

        # prepend so children come before siblings
        queue[0:0] = children
