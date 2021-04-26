#include "video.hpp"

int main( void ) {

    VideoCapture cap("/home/heisendelta/Videos/dont_judge_me.mp4");
    cvvid::render_video(cap, 60);

}
