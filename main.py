from sites.gimbab import doGimBab
from sites.seoulvinyl import doSeoulVinyl
from sites.dope import doBeatitMusic
from sites.naverBase import doNaver

if __name__ == "__main__":
    print("Keyword you want to Search : ", end="")
    keyword = input()

    print("=========== GimBabRecords ===========")
    doGimBab(keyword)
    print("=========== ============= ===========")

    print("===========  SeoulVinyl   ===========")
    doSeoulVinyl(keyword)
    print("=========== ============= ===========")

    print("===========  DopeRecords  ===========")
    doBeatitMusic(keyword)
    print("=========== ============= ===========")

    print("===========   NaverBase   ===========")
    doNaver(keyword)
    print("=========== ============= ===========")
