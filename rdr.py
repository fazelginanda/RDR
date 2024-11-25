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
        print(str(self.condition) + " -> " + self.conclusion +
              " | Kasus Kunci: " + str(self.case))


class Tree:
    def __init__(self, root):
        self.root = root
        self.left = None
        self.right = None

    def deriveConclusion(self, data, conclusion):
        if self.root:
            if self.root.isSatisfied(data):
                conclusion = self.root.conclusion
                if self.right:
                    return self.right.deriveConclusion(data, conclusion)
            else:
                if self.left:
                    return self.left.deriveConclusion(data, conclusion)
        return conclusion

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


if __name__ == "__main__":
    # Ripple Down Rule

    # TODO: Tanya pakar apakah ingin membuat RDR baru atau menggunakan RDR yang sudah disimpan

    # Buat tree dengan menginisialisasi root yang berisi kesimpulan default
    defaultConclusion = input("Masukkan kesimpulan default: ")
    defaultCondition = True
    defaultRule = Rule(defaultCondition, defaultConclusion, [])
    tree = Tree(defaultRule)

    # Print Tree RDR
    print("Tree RDR")
    tree.printPreorder()

    # Tanya pakar apakah ingin memasukkan data baru
    print()
    while True:
        print("Apakah Anda ingin memasukkan data baru?")
        print("1. Ya")
        print("2. Tidak")
        inputNewData = input("Jawaban: ")
        inputNewData = int(inputNewData)
        if (inputNewData == 1 or inputNewData == 2):
            break
        else:
            print("Jawaban tidak valid. Masukkan 1 atau 2")

    # Jika pakar ingin memasukkan data baru, maka baca data dan lakukan inferensi
    while inputNewData == 1:
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
            feedback = int(feedback)
            if (feedback == 1 or feedback == 2):
                break
            else:
                print("Jawaban tidak valid. Masukkan 1 atau 2")

        # Jika pengguna pakar tidak setuju, maka buat rule baru
        # Cari rule terakhir yang dipenuhi pada jalur inferensi yang menghasilkan klasifikasi yang salah
        if feedback == 2:
            print()
            print("Manipulasi pohon RDR")
            print("Data saat ini: " + str(data))
            print("Kasus kunci yang terakhir dipenuhi: " +
                  str(foundTree.root.case))

            # Cari kondisi yang ada pada data saat ini dan tidak ada pada kasus kunci terakhir
            difference = [
                condition for condition in data if condition not in foundTree.root.case]
            print(
                "Selisih antara data saat ini dengan kasus kunci terakhir: " + str(difference))

            # Tanya pakar apa kondisi yang dipilih untuk rule baru
            print()
            print("Pilih kondisi untuk rule baru. Kondisi harus merupakan bagian dari selisih yang ditampilkan sebelumnya.")
            while True:
                newCondition = input("Masukkan kondisi untuk rule baru: ")
                listOfNewCondition = [condition.strip()
                                      for condition in newCondition.split(",")]
                if set(listOfNewCondition).issubset(set(difference)):
                    break
                else:
                    print("Pilihan kondisi tidak valid. Ulangi masukan")

            # Tanya pakar apa kesimpulan untuk rule baru
            print()
            newConclusion = input("Masukkan kesimpulan baru: ")

            # Buat rule baru
            newRule = Rule(listOfNewCondition, newConclusion, data)
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
            print("Apakah Anda ingin memasukkan data baru?")
            print("1. Ya")
            print("2. Tidak")
            inputNewData = input("Jawaban: ")
            inputNewData = int(inputNewData)
            if (inputNewData == 1 or inputNewData == 2):
                break
            else:
                print("Jawaban tidak valid. Masukkan 1 atau 2")

    # TODO: Tanya apakah ingin menyimpan tree yang sudah dimodifikasi
