from gimbab import doGimBab
from seoulvinyl import doSeoulVinyl

if __name__ == "__main__":
    print("Keyword you want to Search : ", end="")
    keyword = input()

    print("=========== GimBabRecords ===========")
    doGimBab(keyword)
    print("=========== ============= ===========")

    print("===========  SeoulVinyl   ===========")
    doSeoulVinyl(keyword)
    print("=========== ============= ===========")
