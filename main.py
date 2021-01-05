from sites.gimbab import doGimBab
from sites.seoulvinyl import doSeoulVinyl
from sites.dope import doBeatitMusic
from sites.naverBase import doNaver
from sites.soundlook import doSoundLook
from sites.soundsgood import doSoundsGood
from sites.welcomerecords import doWelcomeRecords
from sites.rm360 import dorm360

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

# sixshop base(api) : welcome, soundsgood, seoulvinyl

