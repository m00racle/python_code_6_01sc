import state_machine as sm
import feedback_sm as fb
import cascade as cd
import plants_controller as pc
from datetime import datetime

def pc_run():
    """  
    test run the pc class
    """
    k_value = [-0.5, -1.0, -1.5, -2.0, -2.5]
    for k in k_value:
        robot = fb.Feedback(cd.Cascade(pc.WallController(k, 1.0), pc.WallWorld(0.1, 5)))
        print(f'\nk = {k}, run = {robot.run(30)}\n')

def main():
    # fadd = fb.FeedbackAdd(cd.Cascade(sm.Wire(), sm.Delay(0)), sm.Delay(0))
    # fadd = fb.FeedbackAdd(cd.Cascade(sm.Increment(2), sm.Delay(0)), sm.Wire())
    # print(fadd.transduce(range(10)))
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f'run on: {now}\n')
    pc_run()
    

if __name__ == "__main__":
    main()