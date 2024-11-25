from rdr import Rule, Tree


# Fungsi untuk mencari kesimpulan dari data berdasarkan tree
def deriveConclusion(tree, data, conclusion):
    if tree.root:
        if tree.root.isSatisfied(data):
            conclusion = tree.root.conclusion
            if tree.right:
                return deriveConclusion(tree.right, data, conclusion)
        else:
            if tree.left:
                return deriveConclusion(tree.left, data, conclusion)
    return conclusion


# Tes fungsi Rule dan Tree
def testRuleAndTree():
    rule = Rule("A", "X", ["P", "Q"])
    tree = Tree(rule)

    rule1 = Rule("B", "Y", ["R"])
    tree1 = Tree(rule1)

    rule2 = Rule("C", "Z", ["S"])
    tree2 = Tree(rule2)

    rule3 = Rule(["A", "C"], "Y", ["T"])
    tree3 = Tree(rule3)

    tree.left = tree1
    tree.right = tree2

    tree1.left = tree3

    tree.printPreorder()


# Tes inferensi
def testInference():
    print("Tree RDR")
    rule = Rule(True, "Sehat", [])
    tree = Tree(rule)

    rule1 = Rule(["A", "B"], "X", ["A", "B", "C"])
    tree1 = Tree(rule1)
    tree.right = tree1

    rule2 = Rule(["D"], "Y", ["A", "B", "D"])
    tree2 = Tree(rule2)
    tree1.right = tree2

    rule3 = Rule(["E"], "Z", ["A", "B", "E"])
    tree3 = Tree(rule3)
    tree2.left = tree3

    rule4 = Rule(["C"], "P", ["C", "F"])
    tree4 = Tree(rule4)
    tree1.left = tree4

    rule5 = Rule(True, "dX", ["A", "B", "C"])
    tree5 = Tree(rule5)
    tree3.left = tree5

    tree.printPreorder()

    data1 = ["A", "B", "C"]
    print()
    print("Data: " + str(data1))
    print("Kesimpulan: " + str(deriveConclusion(tree, data1, "")))

    data2 = ["A", "B", "D"]
    print()
    print("Data: " + str(data2))
    print("Kesimpulan: " + str(deriveConclusion(tree, data2, "")))

    data3 = ["A", "B", "E"]
    print()
    print("Data: " + str(data3))
    print("Kesimpulan: " + str(deriveConclusion(tree, data3, "")))

    data4 = ["C", "F"]
    print()
    print("Data: " + str(data4))
    print("Kesimpulan: " + str(deriveConclusion(tree, data4, "")))

    data5 = ["A", "B", "I"]
    print()
    print("Data: " + str(data5))
    print("Kesimpulan: " + str(deriveConclusion(tree, data5, "")))


if __name__ == "__main__":
    testRuleAndTree()
    print()
    print("--------------")
    print()
    testInference()
