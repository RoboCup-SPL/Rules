# Obstacle avoidance challenge

Technical Challenge for RoboCup 2021 SPL Championship. Version from 29. Nov 2020.

## Goal

Teams at RoboCup 2019 self-reported working on/having finished improvements of their obstacle avoidance. Replacing simple obstacle avoidance implementations (don't walk forward if you don't see field color in front of you) should be encouraged by the league. This challenge gives teams to display their improvements in obstacle avoidance. It might aid in lowering the amount of pushing during games.

## Setup

![](figs/obstacle_challenge_2021.jpeg)

A ball is placed in the center of the center circle. The challenged robot is placed in front of the center circle on the opposite side of the of the target goal (equivalent to manual placement of attacking robots during kickoff in SPL games). Between ball and target goal three obstacles are placed.

- One moving robot as an obstacle. This robot is continuously moving back and forth along an imaginary line oriented along the short axis of the field, facing the direction of travel as it moves. The distance travelled by the robot is approximately the width of the penalty area (see dimension H of section "Field Construction" of the SPL rules).
- One stationary robot as an obstacle, facing down the long dimension of the field, offset to the left or right so its outermost shoulder point is a balls radius away from the imaginary line between kick-off point and center of the target goal. The stationary robot is standing upright.
- Two stationary robots as an obstacle, facing down the long dimension of the field, positioned offset to the sides so dribbling a ball in between them is the fastest route to the target goal. The space in between them is twice the robots' shoulder-to-shoulder width.  Both stationary robots are standing upright.

Regarding to the position of the obstacles along the long axis of the field:

- One obstacle is placed on the goalbox line (see line F of section "Field Construction" of the SPL rules).
- One obstacle is placed just outside the penalty box so it does not touch the line (see distance  G).
- One obstacle is placed is placed away from the center line towards the target goal. The distance to the center line is the radius of the center circle (half of distance J).

The order of the obstacles are set up in (i.e. which kind of obstacle stands in which position, and the offset side of the one stationary robot) is randomized by dice throw (or similar randomization tool) at the competition before the first team is challenged. Thus, no team is aware of the exact setup beforehand and all teams face the same challenge. Due to this randomization teams might be challenged with one of these setups:

<img src="/home/mu/vcs/git/robocup_tc/Rules/figs/obstacle_challenge_2021_a.jpeg" style="zoom:12%;" /><img src="/home/mu/vcs/git/robocup_tc/Rules/figs/obstacle_challenge_2021_b.jpeg" style="zoom:12%;" />

<img src="/home/mu/vcs/git/robocup_tc/Rules/figs/obstacle_challenge_2021_c.jpeg" style="zoom:12%;" /><img src="/home/mu/vcs/git/robocup_tc/Rules/figs/obstacle_challenge_2021_d.jpeg" style="zoom:12%;" />

<img src="/home/mu/vcs/git/robocup_tc/Rules/figs/obstacle_challenge_2021_e.jpeg" style="zoom:12%;" /><img src="/home/mu/vcs/git/robocup_tc/Rules/figs/obstacle_challenge_2021_f.jpeg" style="zoom:12%;" />

Obstacle robots may wear any jersey legal in RoboCup SPL competition or no jersey at all. Which jerseys are not specified beforehand so teams cannot prepare for specific jerseys.

## Challenge management and planning

The date, time and field used for the challenge will be announced at RoboCup 2021. In the 30 minutes leading up to the challenge all participating teams must deliver their participating robot and place it along the outside of the field with the robots turned off.

The order of the obstacles is randomized by dice throw (or similar randomization tool) while all participating robots are turned off.

The team currently challenged and the two upcoming teams may turn on and set up their robots for the challenge. Teams must be able to set up robots for participating within 120 seconds of being asked.  Teams are informed of their order of participation in the challenge by the judges. Teams that have completed the challenge must disconnect from the fields wireless network. Thus, avoiding the whole league joining a single fields wireless AP.

Teams hand over their robots to the judges to be placed on the field. The challenge is started by a judge pressing the chest button of the robot once.

## Scoring

The challenged robot is tasked to advance with the ball into the target goal. Both dribbling and kicks are permitted to move the ball. The maximum distance for goal shots is restricted for this challenge. Shots that do not score a goal are unrestricted.

Shots into the goal are only allowed with the center of the ball being within 1.3 meter from the end field line. This threshold is at the same height as the penalty cross (see dimension I of section "Field Construction" of the SPL rules).

Goals shot from a larger distance do not complete the challenge. In this case, the challenged robot is required to walk into the goal, move the ball outside of the goal and score another goal according to the rules of the challenge.

Teams are scored by the time it took to move the ball into the goal (rounded up to full seconds). Lower durations are better. In case of a draw, tied teams are required to repeat the challenge.

If the ball is moved out of the field a judge takes the ball and places it on the kick-off point.

Touching an obstacle with the ball increases the scored duration by 5 seconds. Touching an obstacle with the challenged robot increases the scored duration by 10 seconds.

A robot has at most 3 minutes (penalties excluded) to complete the challenge.

## Considerations for virtual RoboCup

This challenge may be simplified due to possible limits on the presence of teams at the RoboCup competition site. The SPL TC will monitor the ongoing situation and inform the teams about changes to avoid the necessity for teams to travel.

The following changes are in consideration to allow a remote participation in this challenge:

- Allowing the use of scaled down fields. Adapting the challenge for teams with only half a field in their local venue.
- Lowering the number of obstacles.
- Removing the need for a moving obstacle. Allowing the stationary robots to sit down and power off.
- Adapting the scoring and judgment to allow participation via live streams.
