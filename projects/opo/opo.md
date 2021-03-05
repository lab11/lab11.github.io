Opo.
====
Sensing face to face interactions.
-------------------

Face to face interactions and the distances they occur at are thought to be 
important in a number of fields, such as epidemiology, psychology, and 
robot usability. However, past smartphone and smart badge technologies are unable 
to provide the right combination of high resolution data and usability.

Smart badges have offered the highest quality data so far. However, the difficulty in 
synchronizing unpredictable mobile node has resulted in either bulky, high powered
nodes or infrastructure heavy systems. To overcome this challenge, Opo uses a 
novel ultra low power ultrasonic wake up circuit to synchronize nodes, bypassing 
the time synchronization / scheduling challenges faced by traditional RF synchronization.

Opo is able to provide 2 s time resolution and 5 cm spatial resolution, while running 
for 4 days on a battery the size of a dime. Opo tags are around 3 cm in diameter and 
weigh 8 grams, making them easily wearable using a lanyard, lapel pin, or magnetic clips.

[HOMEPAGE_BREAK]

The cornerstone of Opo is an ultrasonic wakeup circuit that draws 19 &mu;A
when no neighbors are present, enabling us to solve the mobile node
coordination problem via <i>broadcast synchronization</i>. Broadcast
synchronization allows nodes to remain asleep most of the time and be
asynchronously awoken when a neighbor appears. This allows Opo to run
without any infrastructure nodes or high powered RF neighbor discovery protocols.
