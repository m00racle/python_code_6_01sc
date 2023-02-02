import state_machine as sm
import feedback_sm as fb
import cascade as cd

def main():
    # fadd = fb.FeedbackAdd(cd.Cascade(sm.Wire(), sm.Delay(0)), sm.Delay(0))
    fadd = fb.FeedbackAdd(sm.Wire(), sm.Wire())
    print(fadd.transduce(range(10)))

if __name__ == "__main__":
    main()