import os
import pickle


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
        treeFilePath = input("Masukkan path dari file tree yang akan digunakan: ")
        tree = loadTreeFromPickle(treeFilePath)

    if tree is not None:
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

            # Tanya apakah pakar pengguna menyetujui kesimpulan yang diberikan
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

        # Tanya apakah ingin menyimpan tree yang sudah digunakan
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
                print("File akan disimpan pada current directory")
                newTreeFilename = input("Masukkan nama file tree tanpa extension: ")
                newTreeFilePath = newTreeFilename + ".pkl"
            else:
                newTreeFilePath = treeFilePath
            with open(newTreeFilePath, "wb") as f:
                pickle.dump(tree, f)
            print("File " + newTreeFilePath + " telah berhasil disimpan")
