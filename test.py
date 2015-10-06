import time
import sys

def draw_progress_bar(percent, start, barLen=20):
	sys.stdout.write("\r")
	progress = ""
	for i in range(barLen):
		if i < int(barLen * percent):
			progress += "="
		else:
			progress += " "
	
	elapsedTime = time.time() - start;
	estimatedRemaining = int(elapsedTime * (1.0/percent) - elapsedTime)
	
	if (percent == 1.0):
		sys.stdout.write("[ %s ] %.1f%% Elapsed: %im %02is ETA: Done!\n" % (progress, percent * 100, int(elapsedTime)/60, int(elapsedTime)%60))
		sys.stdout.flush()
		return
	else:
		sys.stdout.write("[ %s ] %.1f%% Elapsed: %im %02is ETA: %im%02is " % (progress, percent * 100, int(elapsedTime)/60, int(elapsedTime)%60,estimatedRemaining/60, estimatedRemaining%60))
		sys.stdout.flush()
		return

percent = 50.0
start = time.time()
draw_progress_bar(percent, start)


