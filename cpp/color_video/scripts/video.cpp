#include "video.hpp"

int main( void ) {

    string path;
    cout << "[Path to your video]: ";
    cin >> path;
    if (path == "default") path = "/home/heisendelta/Videos/aot.mp4";

    VideoCapture cap(path);
    cvvid::render_video(cap, 60);

}
