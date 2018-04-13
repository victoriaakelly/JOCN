#### JOCN task- part 1 ####

#timings:
# decision 5s
# waiting 4-6s
# outcome 2s

#trials 10 (5 low-rate, 5 high-rate)

#import modules
from psychopy import os, visual, core, event, gui, data, sound, logging
import csv
import datetime
import random

# path to working directory, keep images here for now, link to image folder l8r
directory = os.getcwd()

#parameters
useFullScreen = False
DEBUG = False

frame_rate=2
decision_dur=2
instruct_dur=5
outcome_dur=2

responseKeys=('1', '2', '3', '4', '5', '6', '7')

runs = 10

#exit task
#w1 = visual.Window()
#w1.close()

#get subjID
subjDlg=gui.Dlg(title="JOCN paper- rate items")
subjDlg.addField('Enter Subject ID: ')
subjDlg.show()


if gui.OK:
    subj_id=subjDlg.data[0]
else:
    sys.exit()

run_data = {
            'Participant ID' : subj_id,
            'Date': str(datetime.datetime.now()),
            'Description': 'JOCN paper- rate items'
            }

#window setup
win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=False,
    allowGUI=False)

#define stimulus
fixation = visual.TextStim(win, text="+", height=2)
ready_screen = visual.TextStim(win, text="Ready...", height=1.5)
waiting = visual.TextStim(win, text="Waiting...", height=1.5)

# instruction screen #
instruct_screen = visual.TextStim(win, text=
    'Rate how much you prefer the items \n- from 1 (little to no preference) \n- to 7 (very high preference).',
    pos = (0,1), wrapWidth=20, height = 1.2)

#decision screen
pictureStim =  visual.ImageStim(win, pos=(0,1.5))
ratingScale = visual.RatingScale(win, choices=['1', '2', '3', '4', '5', '6', '7'])
while ratingScale.noResponse:
    pictureStim.draw()
    ratingScale.draw()
    win.flip()
rating = ratingScale.getRating()
decisionTime = ratingScale.getRT()
choiceHistory = ratingScale.getHistory()

#image list
images = []
for file in os.listdir(directory):
    #Here  I'm converting the filenames to lower case and checking if they have a .jpg or .png extension
    if file.lower().endswith(".jpg")  or file.lower().endswith(".png") :
        #If the file is a jpg or png, add it to our list of images
        images.append(file)
# Randomize order of images
random.shuffle(images)

# testing##############
#highrating1 = visual.ImageStim(win, image='high_rating_1.jpg', flipHoriz=True, pos=(0, 4.50), units='deg')

# outcome screen
outcome_stim = visual.TextStim(win, text='Time is up.')

outcome_map = {
    1-7: 'Thank you for choosing.',
    None: 'Remember to choose quickly.'
    }

'''
outcome_subj_keep = visual.TextStim(win, text='Thank you for choosing.')
outcome_no_resp = visual.TextStim(win, text='Remember to choose quickly.')
'''

#logging
#log_file = logging.LogFile("logs/%s.log" % (subj_id), level=logging.DATA, filemode='w')
log_file = 'logs/{}_run_{}.csv'

globalClock = core.Clock()
logging.setDefaultClock(globalClock)

timer = core.Clock()

#trial hanlder
trial_data = [r for r in csv.DictReader(open('JOCNdesign1.csv','rU'))]

# condition to stim mapping - testing  - edit -
stim_map = {
  '1': '1',
  '2': '2',
  '3': '3',
  '4': '4',
  '5': '5',
  '6': '6',
  '7': '7'
  }


trials = data.TrialHandler(trial_data[:5], 1, extraInfo=run_data,
    dataTypes=['stim_onset', 'resp_onset', 'rt', 'resp'], method='sequential')

#parsing out file data
runs=[]
run_data = []
for t in range(1,10):
    #sample = random.sample(range(1,10),1)[0]
    run_data.append(trial_data.pop(0))
runs.append(run_data)

# main task loop
def do_run(trial_data, run_num):

    trials = data.TrialHandler(trial_data, 1, method="sequential")

    for trial in trials:

        # add trial logic
        # i.e. show stimuli
        # get resp
        # add data to 'trial'

        instruct_screen.draw()

        condition_label = stim_map[trial['Condition']]
        #image = "C:\Users\tuj67828\Desktop\JOCNdesign\images" % condition_label
        highrating1.draw()
        pictureStim.setImage(highrating1)

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


        trials.addData('resp', resp_val)
        trials.addData('rt', resp_onset)

        #reset rating number color
        resp_text_keep.setColor([1,1,1])
        resp_text_share.setColor([1,1,1])

        #ISI
        logging.log(level=logging.DATA, msg='ISI') #send fixation log event
        timer.reset()
        isi_for_trial = float(trial['ISI'])
        while timer.getTime() < isi_for_trial:
            waiting.draw()
            win.flip()

        #outcome phase
        if resp_val == 1-7:
            partner_resp=random.randint(0,1)
            outcome_txt = outcome_map[2][partner_resp].format(condition_label)
            #trials.addData('outcome', partner_resp)
        else:
            print('please respond faster')

    trials.saveAsText(fileName=log_file.format(subj_id, run_num)) #, dataOut='all_raw', encoding='utf-8')

runs = range(1,11)

#for r, myrun in enumerate(runs):
#    #print "got to checkpoint %d" % r
#    do_run(myrun[:3], r+1)
#    #print run_data
#

for ridx, run_trials in enumerate(runs):
    #do_run(run_trials[:3], ridx+1)
    do_run(run_trials, ridx+1)
