import os
import pickle
from graphviz import Digraph


class Rule:
    def __init__(self, condition, conclusion, case):
        self.condition = condition
        self.conclusion = conclusion
        self.case = case

    def isSatisfied(self, data):
        if isinstance(self.condition, bool):
            return self.condition
        elif isinstance(self.condition, list):
            return set(self.condition).issubset(set(data))
        else:
            return False

    def print(self):
        print(
            str(self.condition)
            + " -> "
            + self.conclusion
            + " | Kasus Kunci: "
            + str(self.case)
        )


class Tree:
    def __init__(self, root):
        self.root = root
        self.left = None
        self.right = None

    def search(self, data, tree):
        if self.root:
            if self.root.isSatisfied(data):
                tree = self
                if self.right:
                    return self.right.search(data, tree)
            else:
                if self.left:
                    return self.left.search(data, tree)
        return tree

    def insertRule(self, rule):
        if self.root:
            if not self.right:
                self.right = Tree(rule)
            else:
                currentTree = self.right
                while currentTree.left:
                    currentTree = currentTree.left
                currentTree.left = Tree(rule)
        return self

    def printPreorder(self):
        self.root.print()
        if self.left:
            self.left.printPreorder()
        if self.right:
            self.right.printPreorder()


# Fungsi untuk load file Pickle
def loadTreeFromPickle(file_path):
    try:
        # Periksa apakah ada file yang ingin dicari
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' tidak ditemukan.")

        # Buka dan load file pickle
        with open(file_path, "rb") as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


# Fungsi untuk mengubah RDR tree menjadi graph menggunakan library Digraph agar dapat divisualisasikan
def addNodesAndEdges(tree, graph, parent_id=None, position=""):
    if tree is None:
        return

    # Buat identifier unik untuk sebuah simpul
    nodeId = id(tree)

    # Buat label untuk kondisi dari sebuah rule
    if isinstance(tree.root.condition, bool) and tree.root.condition is True:
        conditionText = "Kondisi: True"
    else:
        conditionText = f"Kondisi: {', '.join(tree.root.condition)}"

    # Buat label untuk kesimpulan dari sebuah rule
    conclusionText = f"Kesimpulan: {tree.root.conclusion}"

    # Buat label untuk kasus kunci pada sebuah rule
    if not tree.root.case:
        caseText = "Kasus Kunci: []"
    else:
        caseText = f"Kasus Kunci: {', '.join(tree.root.case)}"

    ruleLabel = f"{conditionText}\n{conclusionText}\n{caseText}"

    # Tambahkan node yang baru dibuat ke dalam graph
    graph.node(str(nodeId), ruleLabel)

    # Jika ada parent, maka tambahkan edge
    if parent_id is not None:
        if position == "left":
            graph.edge(str(parent_id), str(nodeId), xlabel="Left")
        elif position == "right":
            graph.edge(str(parent_id), str(nodeId), xlabel="Right")

    # Panggil fungsi secara rekursif untuk anak kiri dan anak kanan
    addNodesAndEdges(tree.left, graph, nodeId, position="left")
    addNodesAndEdges(tree.right, graph, nodeId, position="right")


# Fungsi to memvisualisasikan Ripple Down Rule (RDR) tree
def visualizeRdrTree(RdrTree, treeImageFilePath):
    dot = Digraph(comment="Ripple Down Rule Tree")
    dot.attr(rankdir="TB", nodesep="0.5", ranksep="0.5")
    addNodesAndEdges(RdrTree, dot)
    dot.render(treeImageFilePath, format="png", cleanup=True)


if __name__ == "__main__":
    # Ripple Down Rule

    # Tanya pakar apakah ingin membuat RDR baru atau menggunakan RDR yang sudah disimpan
    while True:
        print("Pilih cara penggunaan RDR")
        print("1. Membuat tree RDR baru")
        print("2. Menggunakan RDR yang sudah disimpan")
        inputRDR = input("Jawaban: ")
        if inputRDR == "1" or inputRDR == "2":
            break
        else:
            print("Jawaban tidak valid. Masukkan 1 atau 2")

    # Inisialisasi tree dengan nilai kosong None
    tree = None

    # Mendapatkan current path
    current_directory = os.getcwd()

    tree_folder = "Tree Pickles"
    visualization_folder = "Tree Visualizations"

    # Cek eksistensi folder, jika tidak ada, buat folder
    tree_folder_path = os.path.join(current_directory, tree_folder)
    visualization_folder_path = os.path.join(current_directory, visualization_folder)

    if not os.path.exists(tree_folder_path):
        os.makedirs(tree_folder_path)

    if not os.path.exists(visualization_folder_path):
        os.makedirs(visualization_folder_path)

    # Path akhir pickles dan visualisasi
    folderPath = tree_folder_path
    visualizationPath = visualization_folder_path

    # Membuat tree RDR baru
    if inputRDR == "1":
        # Buat tree dengan menginisialisasi root yang berisi kesimpulan default
        print()
        print("Buat Tree RDR Baru")
        defaultConclusion = input("Masukkan kesimpulan default: ")
        defaultCondition = True
        defaultRule = Rule(defaultCondition, defaultConclusion, [])
        tree = Tree(defaultRule)

    # Menggunakan RDR yang sudah disimpan
    elif inputRDR == "2":
        # Cari dan hitung banyak file tree yang tersimpan pada folder yang telah ditentukan
        listOfTreeFileName = [
            file for file in os.listdir(folderPath) if file.endswith(".pkl")
        ]
        numOfTreeFile = len(listOfTreeFileName)

        # Jika tidak ada file tree yang disimpan, maka program berhenti
        if numOfTreeFile == 0:
            print("Tidak ada file tree yang disimpan")
        # Jika ada file tree yang disimpan, maka tampilkan daftar nama file tree dan minta pengguna untuk memilih file tree yang ingin digunakan
        else:
            print()
            print("Daftar nama file tree yang disimpan:")
            for i in range(len(listOfTreeFileName)):
                print(str(i + 1) + ". " + listOfTreeFileName[i])

            # Tanya pengguna file tree mana yang ingin digunakan
            print()
            while True:
                inputTreeFileNumber = input(
                    "Masukkan nomor file tree yang ingin digunakan: "
                )
                if inputTreeFileNumber.isdigit() and not inputTreeFileNumber.startswith(
                    "0"
                ):
                    inputTreeFileNumberInt = int(inputTreeFileNumber)
                    if inputTreeFileNumberInt >= 1 and inputTreeFileNumberInt <= (
                        len(listOfTreeFileName) + 1
                    ):
                        break
                    else:
                        print(
                            "Nomor file tree tidak valid. Nomor file tree yang dimasukkan harus sesuai dengan pilihan pada daftar yang ditampilkan."
                        )
                else:
                    print(
                        "Nomor file tree tidak valid. Nomor file tree yang dimasukkan harus sesuai dengan pilihan pada daftar yang ditampilkan."
                    )
            inputTreeFileName = listOfTreeFileName[inputTreeFileNumberInt - 1]
            treeFilePath = folderPath + "/" + inputTreeFileName
            tree = loadTreeFromPickle(treeFilePath)

    if tree is None:
        print("Tree gagal dibuat atau gagal diload dari file")
    else:
        # Print Tree RDR yang digunakan
        print("Tree RDR")
        tree.printPreorder()
        # Tanya pakar apakah ingin memasukkan data baru
        print()
        while True:
            print("Apakah Anda ingin memasukkan data?")
            print("1. Ya")
            print("2. Tidak")
            inputNewData = input("Jawaban: ")
            if inputNewData == "1" or inputNewData == "2":
                break
            else:
                print("Jawaban tidak valid. Masukkan 1 atau 2")

        # Jika pakar ingin memasukkan data baru, maka baca data dan lakukan inferensi
        while inputNewData == "1":
            # Baca data baru dari masukan pengguna
            print()
            data = input("Masukkan data: ")
            data = [item.strip() for item in data.split(",")]

            # Cari kesimpulan berdasarkan data masukan
            foundTree = tree.search(data, None)
            print("Kesimpulan: " + foundTree.root.conclusion)

            # Tanya apakah pengguna pakar menyetujui kesimpulan yang diberikan
            while True:
                print("Apakah Anda setuju dengan kesimpulan yang diberikan?")
                print("1. Setuju")
                print("2. Tidak Setuju")
                feedback = input("Jawaban: ")
                if feedback == "1" or feedback == "2":
                    break
                else:
                    print("Jawaban tidak valid. Masukkan 1 atau 2")

            # Jika pengguna pakar tidak setuju, maka buat rule baru
            # Cari rule terakhir yang dipenuhi pada jalur inferensi yang menghasilkan klasifikasi yang salah
            if feedback == "2":
                print()
                print("Manipulasi pohon RDR")
                print("Data saat ini: " + str(data))
                print("Kasus kunci yang terakhir dipenuhi: " + str(foundTree.root.case))

                # Cari kondisi yang ada pada data saat ini dan tidak ada pada kasus kunci terakhir
                difference = [
                    condition
                    for condition in data
                    if condition not in foundTree.root.case
                ]
                print(
                    "Selisih antara data saat ini dengan kasus kunci terakhir: "
                    + str(difference)
                )

                # Jika selisih tidak kosong, maka tanya pakar apa kondisi yang dipilih untuk rule baru
                if difference:
                    print()
                    print(
                        "Pilih kondisi untuk rule baru. Kondisi harus merupakan bagian dari selisih yang ditampilkan sebelumnya."
                    )
                    while True:
                        newCondition = input("Masukkan kondisi untuk rule baru: ")
                        newCondition = [
                            condition.strip() for condition in newCondition.split(",")
                        ]
                        if set(newCondition).issubset(set(difference)):
                            break
                        else:
                            print("Pilihan kondisi tidak valid. Ulangi masukan")
                # Jika selisih kosong, maka kondisi adalah True. Pakar ingin merevisi keputusan yang telah dibuat sebelumnya
                else:
                    print(
                        "Kondisi rule baru adalah True. Anda merevisi keputusan yang telah Anda buat sebelumnya."
                    )
                    newCondition = True

                # Tanya pakar apa kesimpulan untuk rule baru
                print()
                newConclusion = input("Masukkan kesimpulan baru: ")

                # Buat rule baru
                newRule = Rule(newCondition, newConclusion, data)
                print("Rule baru: ", end="")
                newRule.print()

                # Tambahkan rule baru pada lokasi yang tepat
                modifiedTree = foundTree.insertRule(newRule)

                # Print Tree RDR setelah dimanipulasi
                print()
                print("Tree RDR setelah dimanipulasi")
                tree.printPreorder()

            # Tanya pakar apakah ingin memasukkan data baru kembali
            print()
            while True:
                print("Apakah Anda ingin memasukkan data?")
                print("1. Ya")
                print("2. Tidak")
                inputNewData = input("Jawaban: ")
                if inputNewData == "1" or inputNewData == "2":
                    break
                else:
                    print("Jawaban tidak valid. Masukkan 1 atau 2")

        # Tanya pengguna apakah ingin menyimpan tree yang sudah digunakan
        print()
        while True:
            print("Apakah Anda ingin menyimpan tree yang sudah digunakan?")
            print("1. Ya")
            print("2. Tidak")
            inputSave = input("Jawaban: ")
            if inputSave == "1" or inputSave == "2":
                break
            else:
                print("Jawaban tidak valid. Masukkan 1 atau 2")

        # Jika pengguna ingin menyimpan tree, simpan tree sebagai file Pickle
        if inputSave == "1":
            print()
            if inputRDR == "1":
                print("File akan disimpan pada direktori " + folderPath)
                newTreeFilename = input("Masukkan nama file tree tanpa extension: ")
                newTreeFilePath = folderPath + "/" + newTreeFilename + ".pkl"
            else:
                newTreeFilePath = treeFilePath
            with open(newTreeFilePath, "wb") as f:
                pickle.dump(tree, f)
            print("File tree telah berhasil disimpan")

        # Tanya pengguna apakah ingin menyimpan hasil visualisasi tree
        print()
        while True:
            print("Apakah Anda ingin menyimpan visualisasi tree yang sudah digunakan?")
            print("1. Ya")
            print("2. Tidak")
            inputImageSave = input("Jawaban: ")
            if inputImageSave == "1" or inputImageSave == "2":
                break
            else:
                print("Jawaban tidak valid. Masukkan 1 atau 2")

        # Jika pengguna ingin menyimpan visualisasi tree, simpan visualisasi tree sebagai file png
        if inputImageSave == "1":
            print()
            print("File visualisasi akan disimpan pada direktori " + visualizationPath)
            treeImageFilename = input(
                "Masukkan nama file visualisasi tree tanpa extension: "
            )
            treeImageFilePath = visualizationPath + "/" + treeImageFilename
            visualizeRdrTree(tree, treeImageFilePath)
            print("File visualisasi telah berhasil disimpan")
