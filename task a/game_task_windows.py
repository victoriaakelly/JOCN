#### trust game task ####

#timings:
# decision 2s
# waiting 4-6s
# outcome 2s

#trials 72 (24 stranger, 24 computer, 24 friend)

#import modules

from psychopy import visual, core, event, gui, data, sound, logging
import csv
import datetime
import random

#parameters
useFullScreen = False
DEBUG = False

frame_rate=1
decision_dur=2
instruct_dur=8
outcome_dur=2

responseKeys=('1','2')

runs = 1

#get subjID
subjDlg=gui.Dlg(title="Trust Game Task")
subjDlg.addField('Enter Subject ID: ')
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
else:
    sys.exit()

run_data = {
    'Participant ID': subj_id,
    'Date': str(datetime.datetime.now()),
    'Description': 'SRNDNA Pilot - Trust Game Task'
    }

#window setup
win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False)

#define stimulus
fixation = visual.TextStim(win, text="+", height=2)
ready_screen = visual.TextStim(win, text="Ready...", height=1.5)
waiting = visual.TextStim(win, text="Waiting...", height=1.5)

#decision screen
pictureStim =  visual.ImageStim(win, pos=(0,1.5))
resp_text_keep = visual.TextStim(win,text="Keep $1.00", pos =(-7,-4.8), height=1, alignHoriz="center")
resp_text_share = visual.TextStim(win,text="Share $3.00", pos =(7,-4.8), height=1, alignHoriz="center")

# outcome screen
outcome_stim = visual.TextStim(win, text='')

outcome_map = {
    1: 'You have chose to keep the money',
    2: ['{} has chosen to keep the money','{} has chosen to share the money'],
    None: 'You have two seconds to choose'
    }

'''
outcome_subj_keep = visual.TextStim(win, text="You have chosen to keep the money")
outcome_partner_share = visual.TextStim(win, text="[Partner] has chosen to share the money")
outcome_partner_keep = visual.TextStim(win, text="[Partner] has chosen to keep the money")
outcome_no_resp = visual.TextStim(win, text="You have two seconds to choose")
'''

# instruction screen #
instruct_screen = visual.TextStim(win,
    text='Decide whether \n- to keep the money (press 1) \n- to share the money (press 2)',
    pos = (0,1), wrapWidth=20, height = 1.2)

#logging
#log_file = logging.LogFile("logs/%s.log" % (subj_id), level=logging.DATA, filemode='w')
log_file = 'logs/{}_run_{}.csv'

globalClock = core.Clock()
logging.setDefaultClock(globalClock)

timer = core.Clock()

#trial hanlder
trial_data = [r for r in csv.DictReader(open('design1.csv','rU'))]

#trials = data.TrialHandler(trial_data[:5], 1, extraInfo=run_data, dataTypes=['stim_onset', 'resp_onset', 'rt', 'resp'], method='sequential')

# condition to stim mapping
stim_map = {
  '1': 'Friend',
  '2': 'Stranger',
  '3': 'Computer',
  }

#parsing out file data
runs=[]
for run in range(6):
    run_data = []
    for t in range(12):
        sample = random.sample(range(len(trial_data)),1)[0]
        run_data.append(trial_data.pop(sample))
    runs.append(run_data)


# main task loop
def do_run(trial_data, run_num):

    trials = data.TrialHandler(trial_data, 1, method="sequential")

    for trial in trials:

        # add trial logic
        # i.e. show stimuli
        # get resp
        # add data to 'trial'

        condition_label = stim_map[trial['Condition']]
        image = "images\%s.png" % condition_label
        pictureStim.setImage(image)

        #decision phase
        timer.reset()

        event.clearEvents()

        resp_val=None
        resp_onset=None
        while timer.getTime() < decision_dur:
            pictureStim.draw()
            resp_text_keep.draw()
            resp_text_share.draw()
            win.flip()

            resp = event.getKeys(keyList = responseKeys)


            if len(resp)>0:
                resp_val = int(resp[0])
                resp_onset = globalClock.getTime()
                if resp_val == 1:
                    resp_text_keep.setColor('red')
                if resp_val == 2:
                    resp_text_share.setColor('red')


        trials.addData('resp', resp_val)
        trials.addData('rt', resp_onset)

        #reset rating number color
        resp_text_keep.setColor('#FFFFFF')
        resp_text_share.setColor('#FFFFFF')

        #ISI
        logging.log(level=logging.DATA, msg='ISI') #send fixation log event
        timer.reset()
        isi_for_trial = float(trial['ISI'])
        while timer.getTime() < isi_for_trial:
            waiting.draw()
            win.flip()

        #outcome phase
        if resp_val == 2:
            partner_resp=random.randint(0,1)
            outcome_txt = outcome_map[2][partner_resp].format(condition_label)
            #trials.addData('outcome', partner_resp)
        else:
            outcome_txt = outcome_map[resp_val]
        outcome_stim.setText(outcome_txt)
        outcome_stim.draw()
        trials.addData('outcome_txt', outcome_txt)
        win.flip()
        core.wait(2)

    trials.saveAsText(fileName=log_file.format(subj_id, run_num)) #, dataOut='all_raw', encoding='utf-8')


for ridx, run_trials in enumerate(runs):
    do_run(run_trials[:3], ridx+1)
