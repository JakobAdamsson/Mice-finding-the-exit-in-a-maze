#include <stdio.h>
#include <stdlib.h>
#include <math.h>

float euclidianDistance(int x0, int y0, int x1, int y1)
{
    return (float)(sqrt( pow(x1-x0, 2) + pow(y1-y0, 2) ));
}
