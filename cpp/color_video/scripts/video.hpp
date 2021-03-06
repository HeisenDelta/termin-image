#include "../../color_image/scripts/optimized_image.hpp"
#include <iostream>
#include <thread>
#include <chrono>
#include "keypress.h"

#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

using namespace std::this_thread;
using namespace std::chrono;
using namespace std::chrono_literals;

namespace cvvid {
    static int render_video(VideoCapture cap, const int frame_rate, float B) {   
        // Frame rate only corresponds to the delay between frames 
        // B stands for the brightness

        Mat frame;
        if (!cap.isOpened()) {
            cerr << "Video not found\n";
            return 0;
        }

        while (true) {

            cap >> frame;
            if (frame.empty()) break;

            // imshow("Frame", frame);
            // cvimg::render_image(frame, true);
            cv_opt::render_image_opt(frame, true, 0, B);
            cout << "\x1B[3J\x1B[H";                                     // "\x1B[2J\x1B[H" doesn't work that well

            // Frame rate is only used for delay between frames
            this_thread::sleep_for(milliseconds(1000 / frame_rate));

        }

        cap.release();
        // destroyAllWindows();
        return 0;

    }
}
