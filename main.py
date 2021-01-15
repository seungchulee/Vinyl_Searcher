from sites.gimbab import doGimBab, doGimBab2
from sites.seoulvinyl import doSeoulVinyl
from sites.dope import doBeatitMusic
from sites.naverBase import doNaver, showNewNaver
from sites.soundlook import doSoundLook
from sites.soundsgood import doSoundsGood
from sites.welcomerecords import doWelcomeRecords
from sites.rm360 import dorm360
from sites.bigPortal import printBigPortal


def search():
    print("Keyword you want to Search : ", end="")
    keyword = input()

    print("=========== GimBabRecords ===========")
    doGimBab(keyword)
    print("=========== ============= ===========")

    print("=========== GimBabRecord2 ===========")
    doGimBab2(keyword)
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

    print("===========   SoundLook   ===========")
    doSoundLook(keyword)
    print("=========== ============= ===========")

    print("===========  SoundsGood   ===========")
    doSoundsGood(keyword)
    print("=========== ============= ===========")

    print("========== WelcomeRecords ===========")
    doWelcomeRecords(keyword)
    print("=========== ============= ===========")

    print("==========      rm360     ===========")
    dorm360(keyword)
    print("=========== ============= ===========")

    print("그 외 참고하면 좋을 사이트")
    printBigPortal(keyword)

    # sixshop base(api) : welcome, soundsgood, seoulvinyl


def show_new():
    showNewNaver()


if __name__ == "__main__":
    while True:
        print("1. Search (검색)")
        print("2. New (신상품)")
        print("3. Quit")
        print("What do you want to do? : ", end="")
        menu = input()

        if menu == "1":
            search()
        elif menu == "2":
            show_new()
        elif menu == "3":
            break
        else:
            print("wrong menu")

