# Obstacle avoidance challenge

Proposal as a Technical Challenge for RoboCup 2020 SPL Championship. Version from 6. Dec 2019.

## Goal

Teams at RoboCup 2019 self-reported working on/having finished improvements of their obstacle avoidance. Replacing the most simple obstacle avoidance implementation (don't walk forward if you don't see field color in front of you) should be encouraged by the league. This challenge gives teams to display their improvements in obstacle avoidance. It might aid in lowering the amount of pushing during games.

## Setup

![](figs/obstacle_challenge_2020.png)

A ball is placed at kickoff point. The challenged robot in placed in front of the center circle facing the target goal.  Between ball and target goal three obstacles are placed.

- One robot as an obstacle, facing down the long dimension of the field, centered on the imaginary line between kickoff point and center of the target goal.
- One robot as an obstacle, facing down the long dimension of the field, offset to the left or right so its outermost shoulder point is a balls radius away from the imaginary line between kickoff point and center of the target goal.
- Two robots  as an obstacles, facing down the long dimension of the field, positioned offset to the sides so dribbling a ball in between them is the fastest route to the target goal. The space in between them the sum of the robots shoulder-to-shoulder width and a balls diameter.

The order of the obstacles are set up in is randomized by dice throw at the competition before the first team is challenged. Thus no team is aware of the exact setup beforehand and all teams face the same challenge.

Obstacle robots may wear any jersey. Which jerseys are not specified beforehand so teams can't prepare for specific jerseys.

The team currently challenged and the two upcoming teams are present at the field and may set up their robots for the challenge. Teams are informed of their order of participation in the challenge by the judges. Thus avoiding the whole league joining a single fields wireless AP.

## Scoring

The challenged robot is tasked to dribble the ball into the target goal. Teams are scored by the time it took to move the ball into the goal (rounded to full seconds). Lower durations are better.

Touching an obstacle with the ball increases the scored duration by 5 seconds. Touching an obstacle with the challenged robot increases the scored duration by 10 seconds. 

A robot has at most 90 seconds to complete the challenge.

## Miscellaneous comments

My first intuition says: obstacle robots should be standing upright. If that is not reliable they can also be in a sitting position.

 The challenge could be made harder by having one obstacle move.

We can modify the challenge to allow kicks (after being close enough to the goal?). 