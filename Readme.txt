simplifyDeleteTracesStand5
->creates the simplified log and deletes traces where two the same events have the same timestamp

PatternMFS
->creates MFS based on pyfpgrowth.find_frequent_patterns using (event,time)

mvsBoxplot
->creates mvs based on the quartiles

TrajectoryDataAnonymizer
->based on mvs,mfs changes the simplified log

createEventLog
->the changed simplified log is used to change the original log

PatternMFSEvent
-> will be creating the mfs based on just the events

Algorithm
->everything that is running combined in one script

testscript
->used for testing the modules while writing them

