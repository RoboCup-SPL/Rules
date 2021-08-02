#ifndef PICKUP_H
#define PICKUP_H

static const int PICKUP_UDP_PORT = 9000; // arbitrary - each team will communicate on different ports, to be assigned the day of competition

struct PickUpSoccerBroadcastInfo {
    char header[4];    // "PkUp"
    int playerNum;     // 1-5
    int team;          // 0 is red 1 is blue

    // position of robot
    // coordinates in centimetres
    // 0,0 is in centre of field
    // +ve x-axis points towards the goal we are atempting to score on
    // +ve y-axis is 90 degrees counterclockwise from the +ve x-axis
    // angles in radians, 0 along the +x axis, increasing counterclockwise

    float pos[3];      // x,y,theta

    // main diagonal of covariance matrix of position of robot
    // i.e. variance in x, y and theta without any correlation information

    float posVar[3];

    // Ball information
    float ballAge;        // seconds since this robot last saw the ball. -1 if we haven't seen it

    // position of ball (same coordinate system as above, without heading)

    float ball[2];

    // main diagonal of covariance of position of ball

    float ballVar[2];

    // velocity of the ball (same coordinate system as above, without heading)

    float ballVel[2];

    // seconds the robot has been penalized. -1 if not penalized

    float penalized;

    // seconds the robot has been fallen.  -1 if not fallen

    float fallen;

};

#endif // PICKUP_H
