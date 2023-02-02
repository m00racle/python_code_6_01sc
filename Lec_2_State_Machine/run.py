import state_machine as sm
import feedback_sm as fb

def main():
    fadd = fb.FeedbackAdd(sm.Delay(0), sm.Wire())
    print(fadd.transduce(range(10)))

if __name__ == "__main__":
    main()